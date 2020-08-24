#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,sys,io,json
from datetime import timedelta

import datetime
week = datetime.date.today() + timedelta(days=7)
from datetime import datetime
milli = (datetime.strptime('' + str(week) + ' 23:59:59', "%Y-%m-%d %H:%M:%S").strftime("%s"))+'.999'
today = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d'))+' 00:00:00',"%Y-%m-%d %H:%M:%S").strftime('%s')

ch_code =['81-MoviesHD1','82-MoviesHD2','83-MoviesHD3','90-MoviesHD4','112-SeriesHD1','175-SeriesHD2'
          ,'174-DramaHD1','170-gourmet','91-beJUNIOR','100-Jeem','99-Baraem']

with io.open("/etc/epgimport/beinent.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for code in ch_code:
    with io.open("/etc/epgimport/beinent.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+code.split('-')[1]+'">'+"\n"+'    <display-name lang="en">'+code.split('-')[1]+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8')) 
print('**************BEIN ENTERTAINMENT EPG******************')
sys.stdout.flush()
for code in ch_code: 
    query ={
        "languageId": "ara",
        "filter": '{"$and":[{"id_channel":{"$in":['+code.split('-')[0]+']}},{"endutc":{"$ge":'+today+'}},{"startutc":{"$le":'+milli+'}}]}'
    }
    url = requests.get('https://proxies-beinmena.portail.alphanetworks.be/cms/epg/filtered',params=query).json()
    for data in url['result']['epg']['chan_'+code.split('-')[0]]:
        start= datetime.fromtimestamp(int(data['startutc'])).strftime('%Y%m%d%H%M%S') 
        end = datetime.fromtimestamp(int(data['endutc'])).strftime('%Y%m%d%H%M%S')
        ch = ''
        ch+=2*' '+'<programme start="'+start+' +0000" stop="'+end+' +0000" channel="'+code.split('-')[1]+'">\n'
        ch+=4*' '+'<title lang="en">'+data['title'].replace('&','and').strip()+'</title>\n'
        ch+=4*' '+'<desc lang="en">'+data['synopsis'].strip().replace('&','and')+'</desc>\n  </programme>\r'
        with io.open('/etc/epgimport/beinent.xml','a',encoding="utf-8") as f:
            f.write(ch)
            
    endtime = datetime.strptime(start,'%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')
    print code.split('-')[1]+' epg ends at '+endtime
    sys.stdout.flush()

with io.open("/etc/epgimport/beinent.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
   

with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
    data = json.load(f)
for bouquet in data['bouquets']:
    if bouquet["bouquet"]=="beinent":
        bouquet['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
    json.dump(data, f)   
 
print("**************FINISHED******************")
sys.stdout.flush()