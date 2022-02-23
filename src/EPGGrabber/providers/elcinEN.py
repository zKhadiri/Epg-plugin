#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __init__ import *

from elcin import Elcinema, nb_channel, headers, cprint
import ssl
import requests
import sys
import re
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta

time_zone = tz()


class ElcinEn(Elcinema, object):

    def __init__(self, channel):
        super(ElcinEn, self).__init__(channel)

    def getData(self, ch):
        with requests.Session() as s:
            ssl._create_default_https_context = ssl._create_unverified_context
            s.mount('https://', HTTPAdapter(max_retries=100))
            url = s.get('https://elcinema.com/en/tvguide/' + ch.split('-')[0] + '/', headers=headers, verify=False)
            
            self.data = url.text
            
    def Gettitle(self):
        self.title = re.findall(r'<a\shref=\"\/en/work\/\d+\/\">(.*?)<\/a><\/li', self.data)
        mt = re.findall(r'<a\shref=\"\/en/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>', self.data)
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

    def Starttime(self):
        hours = []
        for time in re.findall(r'(\d\d\:\d\d.*)', self.data):
            if 'AM' in time or 'PM' in time:
                start = datetime.strptime(time.replace('</li>', ''), '%I:%M %p')
                hours.append(start.strftime('%H:%M'))

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_hr = 0
        for d in hours:
            h, m = map(int, d.split(":"))
            if last_hr > h:
                today += + timedelta(days=1)
            last_hr = h
            self.prog_start.append(today + timedelta(hours=h, minutes=m))

        return self.prog_start


def main():
    channels = [nb.split('-')[1] for nb in nb_channel]


    print('**************ELCINEMA ENGLISH EPG******************')
    sys.stdout.flush()
    import time
    Hour = time.strftime("%H:%M")
    start = '00:00'
    end = '02:00'
    if Hour >= start and Hour < end:
        print('Please come back at 2am to download the epg')
        sys.stdout.flush()
    else:
        xml_header(EPG_ROOT + '/elcinema.xml', channels)
        for nb in nb_channel:
            try:
                ElcinEn(nb)
            except IndexError:
                cprint('No epg found or missing data for : ' + nb.split('-')[1])
                sys.stdout.flush()
                continue
        provider = __file__.rpartition('/')[-1].replace('.py', '')
        update_status(provider)
        close_xml(EPG_ROOT + '/elcinema.xml')
        
    print('**************FINISHED******************')
    sys.stdout.flush()

if __name__ == '__main__':
    main()


