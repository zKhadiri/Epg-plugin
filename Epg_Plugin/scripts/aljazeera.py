#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter

now = (datetime.today()+timedelta(hours=3)).strftime('%Y-%m-%d')

with io.open("/etc/epgimport/aljazeera.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
    f.write(("\n"+'  <channel id="aljazeera">'+"\n"+'    <display-name lang="en">aljazeera</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))
    
with requests.Session() as s:
    s.mount('https://', HTTPAdapter(max_retries=50))
    url = s.get('https://www.aljazeera.net/schedule')

times = re.findall(r'<div class="schedule__row__timeslot">(.*?)</div>',url.text)
title = re.findall(r'<div class="schedule__row__showname">(.*?)</div>',url.text)
des = re.findall(r'<div class="schedule__row__description">(.*?)</div>',url.text)

if len(times)>0:
    for elem, next_elem,tit,de in zip(times, times[1:] + [times[0]],title,des):
        ch=''
        if times[-1]==elem and times[0]==next_elem:
            start = datetime.strptime(now+' '+elem,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
            extend_prog = (datetime.strptime(start,'%Y%m%d%H%M%S')+timedelta(hours=1)).strftime('%Y%m%d%H%M%S')
            end = extend_prog
        else:
            start = datetime.strptime(now+' '+elem,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
            end = datetime.strptime(now+' '+next_elem,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
        ch+= 2 * ' ' +'<programme start="' + start + ' +0300" stop="' + end+ ' +0300" channel="aljazeera">\n'
        ch+=4*' '+'<title lang="ar">'+tit.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','و'.decode('utf-8')).replace('<div class="schedule__row__nowshowing">','')+'</title>\n'
        ch+=4*' '+'<desc lang="ar">'+de.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','و'.decode('utf-8')).strip()+'</desc>\n  </programme>\r'
        with io.open("/etc/epgimport/aljazeera.xml", "a",encoding="utf-8") as f:
            f.write(ch)
    print 'aljazeera epg download finished'
        
else:
    'No data found for aljazeera'
    
with io.open("/etc/epgimport/aljazeera.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
import json
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"]=="aljazeera":
        channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
    json.dump(data, f)
