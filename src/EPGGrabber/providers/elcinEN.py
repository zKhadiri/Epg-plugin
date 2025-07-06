#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
try:
    from __init__ import *
except:
    from .__init__ import *

from elcin import Elcinema, nb_channel, headers, cprint
import ssl
import requests
import sys
import re
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta

# Define headers for HTTP requests
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
# Define timezone (assuming tz() is defined elsewhere)
time_zone = tz()

# ElcinEn class to handle EPG data for a specific channel
class ElcinEn(Elcinema, object):

    def __init__(self, channel):
        super(ElcinEn, self).__init__(channel)

    # Fetch data for a specific channel
    def getData(self, ch):
        with requests.Session() as s:
            ssl._create_default_https_context = ssl._create_unverified_context
            s.mount('https://', HTTPAdapter(max_retries=100))
            url = s.get('https://elcinema.com/en/tvguide/' + ch.split('-')[0] + '/', headers=headers, verify=False)
            self.data = url.text

    # Extract program titles from the fetched data
    def Gettitle(self):
        self.title = re.findall(r'<a\shref=\"\/en\/work\/\d+\/\">(.*?)<\/a><\/li', self.data)
        mt = re.findall(r'<a\shref=\"\/en\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>', self.data)
        for m in mt:
            if m[0] == '' and m[1] == '':
                self.titles.append("No data found")
            elif m[0] == '':
                self.titles.append(m[1])
            else:
                self.titles.append(m[0])
        for index, element in enumerate(self.titles):
            if element not in self.title:
                self.GetDes().insert(index, "No data found")
        return self.titles

    # Extract program start times from the fetched data
    def Starttime(self):
        hours = []
        for time in re.findall(r'(\d\d\:\d\d.*)', self.data):
            if 'AM' in time or 'PM' in time:
                start = datetime.strptime(time.replace('</li>', ''), '%I:%M %p')
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

# Main function to generate EPG data
def main():
    channels = [nb.split('-')[1] for nb in nb_channel]

    print('**************ELCINEMA ENGLISH EPG******************')
    sys.stdout.flush()
    print("=================================================")
    print("There are {} channels available for EPG data.".format(len(nb_channel)))
    print("=================================================")
    channels = [ch.split('-')[1] for ch in nb_channel]
    xml_header(EPG_ROOT + "/elcinema.xml", channels)
    import time
    Hour = time.strftime("%H:%M")
    start = '00:00'
    end = '02:00'
    if start <= Hour < end:
        print('Please come back at 2am to download the EPG')
        sys.stdout.flush()
    else:
        for nb in nb_channel:
            try:
                ElcinEn(nb)
            except IndexError:
                cprint('No EPG found or missing data for: ' + nb.split('-')[1])
                sys.stdout.flush()
                continue
        provider = __file__.rpartition('/')[-1].replace('.py', '')
        update_status(provider)
        close_xml(EPG_ROOT + '/elcinema.xml')

# Entry point for the script
if __name__ == '__main__':
    main()
    print('**************FINISHED******************')
    sys.stdout.flush()