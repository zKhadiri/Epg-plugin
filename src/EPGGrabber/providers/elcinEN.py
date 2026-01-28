#!/usr/bin/python
# -*- coding: utf-8 -*-
# modified by iet5  (27_01_2026) - EN
from __future__ import print_function
try:
    from .__init__ import *
except:
    from __init__ import *

import requests
import re
import io
import sys
import os
import ssl
import time
from datetime import datetime, timedelta
from time import sleep
from requests.adapters import HTTPAdapter
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# ---------------- TUNING (speed/stability) ----------------
REQUEST_TIMEOUT = 20          # prevent long hangs
MAX_RETRIES = 5               # avoid excessive retries
SLEEP_BETWEEN_CHANNELS = 0.2  # set 0.0 if you want no delay
# ----------------------------------------------------------
# Define the output directory
output_dir = "/etc/epgimport/ziko_epg"
xml_file = os.path.join(output_dir, "elcinema.xml")

# Define headers for HTTP requests
headers = {
    'Host': 'elcinema.com',
    "Connection": "keep-alive",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
}

# --------- ONE SHARED SESSION (SPEEDUP) --------------
SESSION = requests.Session()
SESSION.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
ssl._create_default_https_context = ssl._create_unverified_context
# -----------------------------------------------------

# --------- REGEX (compiled once for speed + accuracy) ---------
RE_CHANNELS = re.compile(r'<a title="(.*?)" href="/en/tvguide/(\d+)/">')
RE_DUR = re.compile(r'\"subheader\">\[(\d+)')
RE_DES_A = re.compile(r"<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>")
RE_DES_B = re.compile(r"<span class='hide'>[^\n]+")
RE_TITLE_LIST = re.compile(r'<a\shref=\"\/en\/work\/\d+\/\">(.*?)<\/a><\/li')
RE_TITLE_MIX = re.compile(
    r'<a\shref=\"\/en\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>'
)
# robust time capture: 1-2 digit hour + minutes + optional space + AM/PM (any case)
RE_TIME = re.compile(r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))')
# -------------------------------------------------------------

def fetch_channels():
    url = "https://elcinema.com/en/tvguide/"
    try:
        response = SESSION.get(url, headers=headers, verify=False, timeout=REQUEST_TIMEOUT)
        txt = getattr(response, "text", "") or ""
        response.raise_for_status()
        channels = set(RE_CHANNELS.findall(txt))

        # python2 safe sorting
        sorted_channels = sorted(
            ["{}-{}".format(channel_id, channel_name) for channel_name, channel_id in channels],
            key=lambda x: x.split("-", 1)[1].lower()
        )
        return sorted_channels

    except Exception as e:
        print("Error fetching channels:", e)
        return []

# Fetch channels and exit if no channels are found
nb_channel = fetch_channels()
if not nb_channel:
    print("No channels found, cannot proceed.")
    sys.exit(1)

# Function to get current UTC offset from receiver's local time
def get_local_offset():
    is_dst = time.localtime().tm_isdst
    utc_offset_sec = - (time.altzone if is_dst else time.timezone)
    hours = utc_offset_sec // 3600
    minutes = (utc_offset_sec % 3600) // 60
    return "{0:+03d}{1:02d}".format(hours, minutes)

time_zone = get_local_offset()

REDC = '\033[31m'
ENDC = '\033[m'

def cprint(text):
    print(REDC + text + ENDC)

class ElcinEn(object):
    def __init__(self, channel):
        # Guards to prevent repeated appends
        self._start_done = False
        self._end_done = False
        self._des_done = False
        self._title_done = False

        self.prog_start = []
        self.prog_end = []
        self.description = []
        self.titles = []
        self.getData(channel)
        self.Toxml(channel)

    # Fetch data for a specific channel
    def getData(self, ch):
        url = 'https://elcinema.com/en/tvguide/' + ch.split('-', 1)[0] + '/'
        resp = SESSION.get(url, headers=headers, verify=False, timeout=REQUEST_TIMEOUT)
        self.data = getattr(resp, "text", "") or ""

    # Extract program start times from the fetched data
    def Starttime(self):
        if self._start_done:
            return self.prog_start
        self._start_done = True
        hours = []
        times = RE_TIME.findall(self.data)

        for t in times:
            t = t.strip().replace('</li>', '').strip()
            t_up = t.upper()
            # ensure space before AM/PM: "10:00PM" -> "10:00 PM"
            if t_up.endswith('AM') and not t_up.endswith(' AM'):
                t_up = t_up[:-2] + ' ' + t_up[-2:]
            if t_up.endswith('PM') and not t_up.endswith(' PM'):
                t_up = t_up[:-2] + ' ' + t_up[-2:]
            try:
                start = datetime.strptime(t_up, '%I:%M %p')
                hours.append(start.strftime('%H:%M'))
            except:
                # ignore malformed time fragments
                pass

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_hr = 0
        for d in hours:
            h, m = list(map(int, d.split(":")))
            if last_hr > h:
                today += timedelta(days=1)
            last_hr = h
            self.prog_start.append(today + timedelta(hours=h, minutes=m))

        return self.prog_start

    def Endtime(self):
        if self._end_done:
            return self.prog_end
        self._end_done = True

        minutes = [int(x) for x in RE_DUR.findall(self.data)]
        starts = self.Starttime()
        if not starts:
            raise IndexError("No start times")

        start = datetime.strptime(
            datetime.strptime(str(starts[0]), '%Y-%m-%d %H:%M:%S').strftime('%Y %m %d %H:%M'),
            '%Y %m %d %H:%M'
        )

        for m in minutes:
            x = start + timedelta(minutes=m)
            start += timedelta(minutes=m)
            self.prog_end.append(x)

        return self.prog_end

    def GetDes(self):
        if self._des_done:
            return self.description
        self._des_done = True

        a = RE_DES_A.findall(self.data)
        b = RE_DES_B.findall(self.data)

        # make it safer if lengths differ
        n = min(len(a), len(b))
        for i in range(n):
            f = a[i]
            l = b[i]
            self.description.append(
                f + l.replace("<span class='hide'>", '').replace('</span></li>', '')
            )

        return self.description

    # Extract program titles from the fetched data
    def Gettitle(self):
        if self._title_done:
            return self.titles
        self._title_done = True

        base_titles = RE_TITLE_LIST.findall(self.data)
        mt = RE_TITLE_MIX.findall(self.data)

        for m in mt:
            if m[0] == '' and m[1] == '':
                # IMPORTANT: add ONE fallback only (avoid double append)
                self.titles.append("Unable to retrieve program information")
            elif m[0] == '':
                self.titles.append(m[1])
            else:
                self.titles.append(m[0])

        # align descriptions without re-calling GetDes() multiple times
        descs = self.GetDes()
        for index, element in enumerate(self.titles):
            if element not in base_titles:
                if PY3:
                    descs.insert(index, "Unable to retrieve program information")
                else:
                    descs.insert(index, "Unable to retrieve program information".decode('utf-8'))

        return self.titles

    def Toxml(self, channel):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        starts = self.Starttime()
        ends = self.Endtime()
        titles = self.Gettitle()
        descs = self.GetDes()

        for elem, next_elem, title, des in zip(starts, ends, titles, descs):
            startime = datetime.strptime(str(elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            endtime = datetime.strptime(str(next_elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')

            chxml = ''
            chxml += 2 * ' ' + '<programme start="' + startime + ' ' + time_zone + '" stop="' + endtime + ' ' + time_zone + '" channel="' + '-'.join(channel.split('-', 1)[1:]) + '">\n'
            # IMPORTANT: EN language tags
            chxml += 4 * ' ' + '<title lang="en">' + title.replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', 'and') + '</title>\n'
            chxml += 4 * ' ' + '<desc lang="en">' + des.replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', 'and').replace('(', '').replace(')', '').strip() + '</desc>\n  </programme>\r'

            with io.open(xml_file, "a", encoding='UTF-8') as f:
                f.write(chxml)

        # keep original print output for compatibility
        print('-'.join(channel.split('-', 1)[1:]) + ' epg ends at : ' + str(ends[-1]))
        sys.stdout.flush()

# Main function to generate EPG data
def main():
    # Keep original PROVIDERS_ROOT update logic (as plugin expects)
    try:
        from datetime import datetime
        import json
        with open(PROVIDERS_ROOT, 'r') as f:
            data = json.load(f)
        for channel in data.get('bouquets', []):
            if channel.get("bouquet") == "elcin":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        with open(PROVIDERS_ROOT, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

    print('**************ELCINEMA ENGLISH EPG******************')
    sys.stdout.flush()

    print("============================================")
    print("Time_zone is set to {}".format(time_zone))
    print("============================================")

    print("=================================================")
    print("There are {} channels available for EPG data.".format(len(nb_channel)))
    print("=================================================")

    channels = [ch.split('-', 1)[1] for ch in nb_channel]
    xml_header(xml_file, channels)

    # Direct processing without time check
    for nb in nb_channel:
        try:
            ElcinEn(nb)
        except IndexError:
            cprint('No epg found or missing data for: ' + nb.split('-', 1)[1])
            sys.stdout.flush()
        except requests.RequestException as e:
            cprint('Network error for: ' + nb.split('-', 1)[1] + ' -> ' + str(e))
            sys.stdout.flush()

        if SLEEP_BETWEEN_CHANNELS:
            sleep(SLEEP_BETWEEN_CHANNELS)

# Entry point for the script
if __name__ == '__main__':
    main()
    close_xml(xml_file)

print('**************FINISHED******************')
sys.stdout.flush()