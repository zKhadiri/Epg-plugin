#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,json,io,os
from datetime import datetime
from time import strftime

time_zone = strftime('%z')

import time
os.environ['TZ'] = 'UTC'


headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip,deflate',
    'contenttype':'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}


def ond():
    with io.open("/etc/epgimport/osnd.xml","w",encoding='UTF-8')as f:
        f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">'+"\n"+'  <channel id="OSN_on_Demand">'+"\n"+'    <display-name lang="en">OSN on Demand</display-name>'+"\n"+'  </channel>'+"\n").decode('utf-8'))
    url = requests.get('http://www.osn.com/ar-sa/explore/channels/vhd/osn-on-demand-hd',headers=headers)
    time = re.findall(r'<li class="timeSpanNumber(.*)" data-schedule="(.*?)">',url.text)
    now = re.search(r"todaysDate = '(.*?)';",url.text)
    for t in time:
        ch=''
        hour = datetime.strptime(t[1], "%H:%M").strftime("%I:%M %p")
        data={"queryName":"customtable.OSNSchedules.GetProgramDetailsBySelectedTimeAndChannel","whereFilter":"ChannelCode = 'vhd' AND EndDateTime>'"+now.group().replace("todaysDate = '",'').replace("';",'')+" "+hour+"'","topItems":"1","countryCode":"SA"}
        url = requests.post('http://www.osn.com/CMSPages/TVScheduleWebService.asmx/GetCurrentProgramDetailsForChannel',headers=headers,data=data)
        js=json.loads(url.text.replace('<string xmlns="http://tempuri.org/">','').replace('<?xml version="1.0" encoding="utf-8"?>','').replace('</string>','').replace('\n',''))
        starttime=datetime.strptime(now.group().replace("todaysDate = '",'').replace("';",'')+' '+js[0]['StartTime'],'%m/%d/%Y %H:%M').strftime('%Y%m%d%H%M%S')
        endtime = datetime.strptime(now.group().replace("todaysDate = '",'').replace("';",'') + ' ' + js[0]['EndTime'], '%m/%d/%Y %H:%M').strftime('%Y%m%d%H%M%S')
        ch+=2*' '+'<programme start="'+starttime+' '+time_zone+'" stop="'+endtime+' '+time_zone+'" channel="'+js[0]['EnglishName'].replace(' ','_')+'">'+'\n'
        ch+=4*' '+'<title lang="en">'+js[0]['title'].replace('&','and')+'</title>'+'\n'
        ch+=4*' '+'<desc lang="ar">'+js[0]['Arab_Synopsis'].replace('.\r\n','')+'</desc>'+'\n'
        ch+=4*' '+'<category lang="en">'+'Duration : '+js[0]['DurationTime']+'</category>'+'\n'+'  </programme>'
        print(ch)
        with io.open("/etc/epgimport/osnd.xml","a",encoding='UTF-8')as f:
            f.write(ch)
    with io.open("/etc/epgimport/osnd.xml", "a", encoding='UTF-8')as f:
            f.write(('</tv>').decode('utf-8'))
    
if __name__=='__main__':
    ond()

if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    print('Downloading custom.channels config')
    ur = requests.get('http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/custom.channels.xml',headers=headers)
    if ur.status_code ==200:
        with io.open('/etc/epgimport/custom.channels.xml','w') as f:
            f.write(ur.text)
        print('Done')
    else:
        print('Cannot establish connection to the server')
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    uri = requests.get('http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/custom.sources.xml',headers=headers)
    if uri.status_code==200:
        with io.open('/etc/epgimport/custom.sources.xml','w') as f:
            f.write(uri.text)
        print('Done')
    else:
        print('Cannot establish connection to the server')

if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    uri = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/elcinema.channels.xml',headers=headers)
    if uri.status_code ==200:
        with io.open('/etc/epgimport/elcinema.channels.xml','w') as f:
            f.write(uri.text)
        print('Done')
    else:
        print('Cannot establish connection to the server')

