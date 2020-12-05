#!/usr/bin/python
# -*- coding: utf-8 -*-

# python3
from __future__ import print_function

from time import sleep
import os,io,re,sys,requests

path = '/etc/epgimport/ziko_epg/dstv.xml'

print("Downloading SuperSport epg guide\nPlease wait....")
sys.stdout.flush()

url = requests.get('http://github.com/ziko-ZR1/XML/blob/master/dstv.xml?raw=true')
with io.open(path,'w',encoding="utf-8") as f:
    f.write(url.text)
 
print("dstv.xml donwloaded with success")

from datetime import datetime
import json
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"]=="dstvback":
        channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
    json.dump(data, f)

if os.path.exists('/var/lib/dpkg/status'):
    print('Dream os image found\nSorting data please wait.....')
    sys.stdout.flush()
    import xml.etree.ElementTree as ET
    tree = ET.parse('/etc/epgimport/ziko_epg/dstv.xml')
    data = tree.getroot()
    els = data.findall("*[@channel]")
    new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
    data[:] = new_els
    tree.write('/etc/epgimport/ziko_epg/dstv.xml', xml_declaration=True, encoding='utf-8')
