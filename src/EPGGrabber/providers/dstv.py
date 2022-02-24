#!/usr/bin/python
# -*- coding: utf-8 -*-


try:
	from .__init__ import *
except:
	from __init__ import *

import requests
import json
import io
import re
import os
import sys
from datetime import datetime
from requests.adapters import HTTPAdapter

urls = []

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}

for i in range(0, 5):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('https://www.dstv.co.za/webmethods/no-cache/GetChannelAllDate.ashx?d=' + str(week) + '')


channels = []


def dstv():
    for url in urls:
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=100))
            link = s.get(url, headers=headers)
            data = json.loads(link.text)
            for d in data['Channels']:
                for prog in d['Programmes']:
                    ch = ''
                    startime = datetime.datetime.strptime(prog['StartTime'].replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.datetime.strptime(prog['EndTime'].replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    ch += 2 * ' ' + '<programme start="' + startime + ' +0200" stop="' + endtime + ' +0200" channel="' + d['Name'].replace(' ', '').replace('&', 'and') + '">\n'
                    ch += 4 * ' ' + '<title lang="en">' + prog['Title'].replace('&', 'and') + '</title>\n'
                    ch += 4 * ' ' + '<desc lang="en">No description Found for this programme</desc>\n  </programme>\r'
                    with io.open(EPG_ROOT + '/dstv.xml', "a", encoding='UTF-8')as f:
                        f.write(ch)
                channels.append(d['Name'].replace(' ', '').replace('&', 'and'))
            dat = re.search(r'\d{4}-\d{2}-\d{2}', url)
            print('Date' + ' : ' + dat.group())
            sys.stdout.flush()
    update_channels("DSTV", channels)


def main():
    print('**************DSTV EPG******************')
    sys.stdout.flush()

    with open(BOUQUETS_ROOT, 'r') as f:
        jsData = json.load(f)

    for channel in jsData['bouquets']:
        if channel["name"] == "DSTV":
            xml_header(EPG_ROOT + '/dstv.xml', channel['channels'])

    dstv()

    close_xml(EPG_ROOT + '/dstv.xml')

    from datetime import datetime

    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for bouquet in data['bouquets']:
        if bouquet["bouquet"] == "dstv":
            bouquet['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream os image found\nSorting data please wait.....')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/dstv.xml')
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_ROOT + '/dstv.xml', xml_declaration=True, encoding='utf-8')

    print('**************FINISHED******************')


if __name__ == '__main__':
    main()
