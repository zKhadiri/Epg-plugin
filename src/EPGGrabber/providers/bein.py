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
from datetime import datetime, timedelta

urls = []
print('**************BEIN SPORTS EPG******************')
sys.stdout.flush()


def bein():
    for i in range(0, 3):
        week = (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')
        with requests.Session() as s:
            url = 'https://www.bein.com/ar/epg-ajax-template/?action=epg_fetch&offset=%2B2&category=sports&serviceidentity=bein.net&mins=00&cdate={}&language=AR&postid=25344&loadindex='.format(str(week)) + str(i)
            link = s.get(url)
            time = re.findall(r'<p\sclass=time>(.*?)<\/p>', link.text)
            times = [t.replace('&nbsp;-&nbsp;', '-').split('-') for t in time]
            title = re.findall(r'<p\sclass=title>(.*?)<\/p>', link.text)
            formt = re.findall(r'<p\sclass=format>(.*?)<\/p>', link.text)
            channels = re.findall(r"https:\/\/assets\.bein\.com\/mena\/sites\/\d+\/\d+\/\d+\/(.*?)\.png\'\sdata", link.text)

            desc = []
            titles = []
            title_chan = []
            prog = []
            for tit in title:
                title_chan.append(tit.replace('   ', ' ').split('- ')[0])
                spl = re.search(r'-\s(.*)', tit)
                if spl != None:
                    desc.append(4 * ' ' + '<desc lang="ar">' + spl.group().replace('- ', '').replace('&', 'and') + '</desc>\n  </programme>\r')
                else:
                    desc.append(4 * ' ' + '<desc lang="ar">' + tit.replace('&', 'and') + '</desc>\n  </programme>\r')

            for title_, form_ in zip(title_chan, formt):
                titles.append(4 * ' ' + '<title lang="en">' + title_.replace('&', 'and').strip() + ' - ' + form_.replace('2014', '2021') + '</title>' + '\n')
            try:
                for time_, chann_, chc, chch in zip(times, channels, channels, channels[1:] + [channels[0]]):
                    date = re.search(r'\d{4}-\d{2}-\d{2}', url)
                    end = '05:59'
                    start = '18:00'
                    if time_[0] >= start and time_[1] <= end and chc == chch:
                        fix = (datetime.strptime(date.group(), '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                        starttime = datetime.strptime(fix + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        prog.append(2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + chann_.replace('_Digital_Mono', '').replace('_DIGITAL_Mono', '') + '">' + '\n')

                    elif chc != chch and time_[1] >= '00:00':
                        fix = (datetime.strptime(date.group(), '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                        starttime = datetime.strptime(date.group() + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(fix + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        prog.append(2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + chann_.replace('_Digital_Mono', '').replace('_DIGITAL_Mono', '') + '">' + '\n')
                    else:
                        starttime = datetime.strptime(date.group() + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        prog.append(2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + chann_.replace('_Digital_Mono', '').replace('_DIGITAL_Mono', '') + '">' + '\n')
            except:
                break
            if len(title) != 0:
                for tt, d, p in zip(titles, desc, prog):
                    with io.open(EPG_ROOT + "/bein.xml", "a", encoding='UTF-8')as fil:
                        fil.write(p + tt + d)
                dat = re.search(r'\d{4}-\d{2}-\d{2}', url)
                print('Date' + ' : ' + dat.group())
                sys.stdout.flush()
            else:
                print('No data found')
                break


def main():
    with open(API_PATH + '/bouquets.json', 'r') as f:
        jsData = json.load(f)
        for channel in jsData['bouquets']:
            if channel["name"] == "Bein sports":
                xml_header(EPG_ROOT + '/bein.xml', channel['channels'])

    bein()

    from datetime import datetime
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for bouquet in data['bouquets']:
        if bouquet["bouquet"] == "bein":
            bouquet['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    close_xml(EPG_ROOT + '/bein.xml')

    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream os image found\nSorting data please wait.....')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/bein.xml')
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_ROOT + '/bein.xml', xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    main()

print("**************FINISHED******************")
