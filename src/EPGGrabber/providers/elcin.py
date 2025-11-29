#!/usr/bin/python
# -*- coding: utf-8 -*-
# modified by iet5
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
from time import sleep, strftime
from requests.adapters import HTTPAdapter
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Define the output directory
output_dir = "/etc/epgimport/ziko_epg"

headers = {
    'Host': 'elcinema.com',
    "Connection": "keep-alive",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
}
# Function to fetch available channels from Elcinema
def fetch_channels():
    url = "https://elcinema.com/en/tvguide/"
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        channels = set(re.findall(r'<a title="(.*?)" href="/en/tvguide/(\d+)/">', response.text))
        # Fixed sorting using lower() for Python 2.7 compatibility
        sorted_channels = sorted(["{}-{}".format(channel_id, channel_name) for channel_name, channel_id in channels], 
                               key=lambda x: x.split("-", 1)[1].lower())
        return sorted_channels
    except requests.RequestException as e:
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

class Elcinema:
    def __init__(self, channel):
        self.getData(channel)
        self.prog_start = []
        self.prog_end = []
        self.description = []
        self.titles = []
        self.now = datetime.today().strftime('%Y %m %d')
        self.Toxml(channel)

    # Fetch data for a specific channel
    def getData(self, ch):
        with requests.Session() as s:
            ssl._create_default_https_context = ssl._create_unverified_context
            s.mount('https://', HTTPAdapter(max_retries=100))
            url = s.get('https://elcinema.com/tvguide/' +
                        ch.split('-')[0] + '/', headers=headers, verify=False)
            self.data = url.text

    def Starttime(self):
        hours = []
        for time in re.findall(r'(\d\d\:\d\d.*)', self.data):
            if PY3:
                if 'مساءً' in time or 'صباحًا' in time:
                    start = datetime.strptime(time.replace(
                        '</li>', '').replace('مساءً', 'PM').replace('صباحًا', 'AM'),'%I:%M %p')
                    hours.append(start.strftime('%H:%M'))
            else:
                if 'مساءً'.decode('utf-8') in time or 'صباحًا'.decode('utf-8') in time:
                    start = datetime.strptime(time.replace('</li>', '').replace('مساءً'.decode(
                        'utf-8'), 'PM').replace('صباحًا'.decode('utf-8'), 'AM'), '%I:%M %p')
                    hours.append(start.strftime('%H:%M'))
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
        minutes = []
        for end in re.findall(r'\"subheader\">\[(\d+)', self.data):
            minutes.append(int(end))
        start = datetime.strptime(datetime.strptime(str(self.Starttime(
        )[0]), '%Y-%m-%d %H:%M:%S').strftime('%Y %m %d %H:%M'), '%Y %m %d %H:%M')
        for m in minutes:
            x = start + timedelta(minutes=m)
            start += timedelta(minutes=m)
            self.prog_end.append(x)

        return self.prog_end

    def GetDes(self):
        for f, l in zip(re.findall(r'<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>', self.data), re.findall(r"<span class='hide'>[^\n]+", self.data)):
            self.description.append(
                f + l.replace("<span class='hide'>", '').replace('</span></li>', ''))
        return self.description

    def Gettitle(self):
        self.title = re.findall(
            r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li', self.data)
        mt = re.findall(
            r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>', self.data)
        for m in mt:
            if m[0] == '' and m[1] == '':
                if PY3:
                    self.titles.append("Unable to retrieve program information")
                else:
                    self.titles.append(
                        "Unable to retrieve program information".decode('utf-8'))
            elif m[0] == '':
                self.titles.append(m[1])
            else:
                self.titles.append(m[0])
        for index, element in enumerate(self.titles):
            if element not in self.title:
                if PY3:
                    self.GetDes().insert(index, "Unable to retrieve program information")
                else:
                    self.GetDes().insert(index, "Unable to retrieve program information".decode('utf-8'))

        return self.titles

    def Toxml(self, channel):

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Create the directory if it doesn't exist

        for elem, next_elem, title, des in zip(self.Starttime(), self.Endtime(), self.Gettitle(), self.GetDes()):
            ch = ''
            startime = datetime.strptime(
                str(elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            endtime = datetime.strptime(
                str(next_elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            ch += 2 * ' ' + '<programme start="' + startime + ' ' + time_zone + '" stop="' + \
                endtime + ' ' + time_zone + '" channel="' + \
                '-'.join(channel.split('-')[1:]) + '">\n'
            ch += 4 * ' ' + '<title lang="ar">' + \
                title.replace('&#39;', "'").replace(
                    '&quot;', '"').replace('&amp;', 'and') + '</title>\n'
            ch += 4 * ' ' + '<desc lang="ar">' + des.replace('&#39;', "'").replace('&quot;', '"').replace(
                '&amp;', 'and').replace('(', '').replace(')', '').strip() + '</desc>\n  </programme>\r'
            with io.open(os.path.join(output_dir, "elcinema.xml"), "a", encoding='UTF-8') as f:
                f.write(ch)
        print('-'.join(channel.split('-')[1:]) +
              ' epg ends at : ' + str(self.Endtime()[-1]))
        sys.stdout.flush()

# Main function to generate EPG data
def main():
    from datetime import datetime
    import json
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "elcin":
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    print('**************ELCINEMA EPG******************')
    sys.stdout.flush()

    print("============================================")
    print("Time_zone is set to {}".format(time_zone))
    print("============================================")

    print("=================================================")
    print("There are {} channels available for EPG data.".format(len(nb_channel)))
    print("=================================================")
    channels = [ch.split('-')[1] for ch in nb_channel]
    xml_header(os.path.join("/etc/epgimport/ziko_epg", "elcinema.xml"), channels)
    
    # Direct processing without time check
    for nb in nb_channel:
        try:
            Elcinema(nb)
        except IndexError:
            cprint('No epg found or missing data for: ' + nb.split('-')[1])
            sys.stdout.flush()
            continue
# Entry point for the script
if __name__ == '__main__':
    main()
    close_xml(os.path.join(output_dir, "elcinema.xml"))

print('**************FINISHED******************')
sys.stdout.flush()