#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __init__ import *

import requests
import re
import io
import os
import sys
import json
from time import sleep, strftime
from requests.adapters import HTTPAdapter

print('**************BEIN ENTERTAINMENT EPG******************')
sys.stdout.flush()
urls = []
for i in range(0, 5):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('https://www.bein.com/en/wp-admin/admin-ajax.php?action=epg_fetch&offset=%2B1&category=entertainment&serviceidentity=bein.net&mins=00&cdate=' + str(week) + '&language=EN&postid=25356')

desc = []
title_chan = []
titles = []
prog = []


def beinen():
    for url in urls:
        from datetime import datetime, timedelta
        desc[:] = []
        title_chan[:] = []
        titles[:] = []
        prog[:] = []
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=10))
            link = s.get(url)
            title = re.findall(r'<p\sclass=title>(.*?)<\/p>', link.text)
            time = re.findall(r'<p\sclass=time>(.*?)<\/p>', link.text)
            formt = re.findall(r'<p\sclass=format>(.*?)<\/p>', link.text)
            times = [t.replace('&nbsp;-&nbsp;', '-').split('-') for t in time]
            channels = re.findall(r"<li\s+id='slider_.*_item\d+'.*img='.*/(.*).*.png", link.text)
            for tt_ in title:
                titles.append(4 * ' ' + '<title lang="en">' + tt_.replace('&', 'and') + '</title>' + '\n')
                #desc.append(4*' '+'<category lang="en">No data found</category>'+'\n')
            format_ = [4 * ' ' + '<desc lang="en">' + f + '</desc>' + "\n" + '  </programme>' + '\n' for f in formt]
            try:
                for time_, chann_, chc, chch in zip(times, channels, channels, channels[1:] + [channels[0]]):
                    end = '05:59'
                    start = '18:00'
                    date = re.search(r'\d{4}-\d{2}-\d{2}', url)
                    channel_b = chann_.replace('-logo-2018-1', '').replace('-Yellow-1', '').replace('-1', '').replace('-2', '')
                    if time_[0] >= start and time_[1] <= end and chc == chch:
                        fix = (datetime.strptime(date.group(), '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                        starttime = datetime.strptime(fix + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        prog.append(2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + channel_b + '">' + '\n')
                    elif chc != chch and time_[1] >= '00:00':
                        fix = (datetime.strptime(date.group(), '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                        starttime = datetime.strptime(date.group() + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(fix + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        prog.append(2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + channel_b + '">' + '\n')
                    else:
                        starttime = datetime.strptime(date.group() + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        prog.append(2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + channel_b + '">' + '\n')
            except:
                break
            if len(title) != 0:
                for ttt, f, p in zip(titles, format_, prog):
                    with io.open(EPG_ROOT + '/beinent.xml', "a", encoding='UTF-8')as fil:
                        fil.write(p + ttt + f)
                dat = re.search(r'\d{4}-\d{2}-\d{2}', url)
                print('Date' + ' : ' + dat.group())
                sys.stdout.flush()
                update([channel.replace('-logo-2018-1', '').replace('-Yellow-1', '').replace('-1', '').replace('-2', '') for channel in channels])
            else:
                print('No data found')
                break


def update(chan):
    with open(BOUQUETS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["name"] == "bein entertainment.net":
            channel['channels'] = sorted([ch for ch in list(dict.fromkeys(chan))])
    with open(BOUQUETS_ROOT, 'w') as f:
        json.dump(data, f)


def main():
    with open(BOUQUETS_ROOT, 'r') as f:
        jsData = json.load(f)
    for channel in jsData['bouquets']:
        if channel["name"] == "bein entertainment.net":
            xml_header(EPG_ROOT + '/beinent.xml', channel['channels'])

    beinen()

    close_xml(EPG_ROOT + '/beinent.xml')

    from datetime import datetime

    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for bouquet in data['bouquets']:
        if bouquet["bouquet"] == "beinent":
            bouquet['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream os image found\nSorting data please wait.....')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/beinent.xml')
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_ROOT + '/beinent.xml', xml_declaration=True, encoding='utf-8')

    print("**************FINISHED******************")


if __name__ == '__main__':
    main()
