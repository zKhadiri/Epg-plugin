#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from time import sleep
import os,io,re,sys,requests,json

path = '/etc/epgimport/jawwytv.xml'

print "Downloading Jawwy epg guide\nPlease wait...."  
sys.stdout.flush()
url=requests.get('https://raw.githubusercontent.com/ziko-ZR1/XML/jawwy/jawwytv.xml')
with io.open(path,'w',encoding="utf-8") as f:
    f.write(url.text)
    
print "jawwytv.xml donwloaded with succes"
    
from datetime import datetime
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"]=="jawwy":
        channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
    json.dump(data, f)