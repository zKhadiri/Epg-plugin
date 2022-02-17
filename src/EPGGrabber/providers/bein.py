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

print('**************BEIN SPORTS EPG******************')
sys.stdout.flush()

def bein():

    channels_found = []
    for i in range(0, 3):
        week = (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')
        with requests.Session() as s:
            for idx in range(0,4):
                url = 'https://www.bein.com/ar/epg-ajax-template/?action=epg_fetch&category=sports&serviceidentity=bein.net&mins=00&cdate={}&language=AR&postid=25344&loadindex={}'.format(week , idx)
                data = s.get(url).text
                time = re.findall(r'<p\sclass=time>(.*?)<\/p>', data)
                times = [t.replace('&nbsp;-&nbsp;', '-').split('-') for t in time]
                title = re.findall(r'<p\sclass=title>(.*?)<\/p>', data)
                formt = re.findall(r'<p\sclass=format>(.*?)<\/p>', data)
                channels = re.findall(r"data-img.*?sites\/\d+\/\d+\/\d+\/(.*?)\.png", data)
                channels_found += channels

                desc = []
                title_chan = []
                for tit in title:
                    title_chan.append(tit.replace('   ', ' ').split('- ')[0])
                    spl = re.search(r'-\s(.*)', tit)
                    if spl != None:
                        desc.append(spl.group().replace('- ', '').replace('&', 'and'))
                    else:
                        desc.append(tit.replace('&', 'and'))
                try:
                    for title_, form_, time_, ch, des in zip(title_chan, formt, times, channels, desc):
                        date = re.search(r'\d{4}-\d{2}-\d{2}', url)
                        starttime = datetime.strptime(date.group() + ' ' + time_[0], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                        epg = ''
                        epg += 2 * ' ' + '<programme start="' + starttime + ' +0000" stop="' + endtime + ' +0000" channel="' + ch.replace('_Digital_Mono', '').replace('_DIGITAL_Mono', '').replace('-1','') + '">' + '\n'
                        epg += 4 * ' ' + '<title lang="en">' + title_.replace('&', 'and').strip() + ' - ' + form_.replace('2014', '2021') + '</title>' + '\n'
                        epg += 4 * ' ' + '<desc lang="ar">' + des.replace('- ', '').replace('&', 'and') + '</desc>\n  </programme>\r'
                        with io.open(EPG_ROOT + '/bein.xml', "a", encoding='UTF-8')as f:
                            f.write(epg)
                except:
                    break
                
                if len(title) != 0:
                    dat = re.search(r'\d{4}-\d{2}-\d{2}', url)
                    print('Date' + ' : ' + dat.group()+' & Index : '+str(idx))
                    sys.stdout.flush()
                else:
                    print('No data found')
                    break

    if len(channels_found) > 0:
        channels_found = sorted([ch.replace('_Digital_Mono', '').replace('_DIGITAL_Mono', '').replace('-1','') for ch in list(dict.fromkeys(channels_found))])
        update_channels("Bein sports",channels_found)

def main():

    provider = __file__.rpartition('/')[-1].replace('.py', '')
    channels = get_channels("Bein sports")
    xml_header(EPG_ROOT + '/bein.xml', channels)

    bein()

    close_xml(EPG_ROOT + '/bein.xml')
    update_status(provider)

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

    print("**************FINISHED******************")

if __name__ == '__main__':
    main()

