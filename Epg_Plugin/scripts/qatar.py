#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,os
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter


fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/qatar.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()

print('**************QATAR******************')

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

with io.open("/etc/epgimport/qatar.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
    
with io.open("/etc/epgimport/qatar.xml","a",encoding='UTF-8')as f:
    f.write(("\n"+'  <channel id="QATAR.TV">\n    <display-name lang="en">QATAR.TV</display-name>\n  </channel>\r').decode('utf-8'))

times=[]
prog_start=[]
epg=[]
with requests.Session() as s:
    s.mount('http://', HTTPAdapter(max_retries=50))
    url = s.get('http://www.qmcdemo.site/TransmissionScheduled',headers=headers)
    for day in re.findall(r"nav-(\d)' aria-selected='true'>",url.text):
        pass
for time in re.findall(r"<span>(.*?)</span>\s+<\/div>\s+<div class='col-md",url.text):
    times.append(datetime.strptime(time,'%I:%M %p').strftime('%H:%M'))

titles=re.findall(r'<h3>(.*?)</h3>',url.text)
des= re.findall(r'h3>\s+<p>(.*?)</p>',url.text)
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=int(day))
last_hr = 0
for d in times:
    h, m = map(int, d.split(":"))
    if last_hr > h:
        today += + timedelta(days=1)
    last_hr = h
    prog_start.append(today + timedelta(hours=h, minutes=m))
    
for elem,next_elem,title,descr in zip(prog_start,prog_start[1:] + [prog_start[0]],titles,des):
    ch=''
    startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
    endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
    ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="QATAR.TV">\n'
    ch+=4*' '+'<title lang="ar">'+title.replace('&#39;',"'").replace('&quot;','"')+'</title>\n'
    if title==descr:
        ch+=4*' '+'<desc lang="ar">يتعذر الحصول على معلومات هذا البرنامج</desc>\n  </programme>\r'.decode('utf-8')
    else:
        ch+=4*' '+'<desc lang="ar">'+descr.replace('&#39;',"'").replace('&quot;','"').strip()+'</desc>\n  </programme>\r'
    epg.append(ch)

print 'Qatar epg ends at : '+str(prog_start[-1])

epg.pop(-1)
for prog in epg:
    with io.open("/etc/epgimport/qatar.xml","a",encoding='UTF-8')as f:
        f.write(prog)

with io.open("/etc/epgimport/qatar.xml", "a",encoding="utf-8") as f:
    f.write(('\n'+'</tv>').decode('utf-8'))
    
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/qatar.txt") as f:
    lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/qatar.txt", "w") as f:
    f.writelines(lines)
    
    
if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    print('Downloading custom.channels config')
    custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.channels.xml?raw=true')
    with io.open('/etc/epgimport/custom.channels.xml','w',encoding="utf-8") as f:
        f.write(custom_channels.text)
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    custom_source=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.sources.xml?raw=true')
    with io.open('/etc/epgimport/custom.sources.xml','w',encoding="utf-8") as f:
        f.write(custom_source.text)

if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    elcinema_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/elcinema.channels.xml','w',encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/dstv.channels.xml'):
    print('Downloading dstv channels config')
    dstv_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/dstv.channels.xml?raw=true')
    with io.open('/etc/epgimport/dstv.channels.xml','w',encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/eliftv.channels.xml'):
    print('Downloading eliftv channels config')
    elif_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/eliftv.channels.xml?raw=true')
    with io.open('/etc/epgimport/eliftv.channels.xml','w',encoding="utf-8") as f:
        f.write(elif_channels.text)
    
print('**************FINISHED******************')