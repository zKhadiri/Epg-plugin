#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,sys
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/noor.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()

print('**************NOOR DUBAI EPG******************')

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

with io.open("/etc/epgimport/noor.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
    
with io.open("/etc/epgimport/noor.xml","a",encoding='UTF-8')as f:
    f.write(("\n"+'  <channel id="noordubai">'+"\n"+'    <display-name lang="en">noordubai</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))


times=[]
data=[]
with requests.Session() as s:
    s.mount('http://', HTTPAdapter(max_retries=50))
    url = s.get('http://www.noordubai.com/content/noordubai/ar-ae/schedule/2.html',headers=headers)
    time= re.findall(r'GMT:\s+(\d{2}:\d{2})',url.content)
    des = re.findall(r"class=\"post-title mt-0 mb-5\"><a href='#'>(.*?)</a></h5>\s+<h6><i",url.content)
    title = re.findall(r"<h4 class=\"post-title mt-0 mb-5\"><a href='#'>(.*?)</a>",url.content)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
last_hr = 0
for d in time:
    h, m = map(int, d.split(":"))
    if last_hr > h:
        today += + timedelta(days=1)
    last_hr = h
    times.append(today + timedelta(hours=h, minutes=m))
    
print 'Noor Dubai epg ends at {}'.format(times[-1])
for elem,next_elem,tit,descri in zip(times, times[1:] + [times[0]],title,des):
    ch=''
    startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
    endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
    ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="noordubai">\n'
    ch+=4*' '+'<title lang="ar">'+tit+'</title>\n'
    if descri=='':
        #ch+=4*' '+'<desc lang="ar">يتعذر الحصول على معلومات هذا البرنامج</desc>\n  </programme>\r'
        ch+=4*' '+'<desc lang="ar">·إذاعة نور دبي : افتتحت في 09/05/2006 تحت شعار اجتماعية برؤية إسلامية، وهي الإذاعة الأولى التي تصغي إلى الهموم اليومية والحياتية للمقيمين في دولة الإمارات العربية المتحدة، وتطل من خلال قناة نور دبي التلفزيونية التي انطلق بثها في 01/09/2008، لتركز على الرياضة والاقتصاد والتربية والصحة، وذلك في إطار اجتماعي وبرؤية إسلامية معتدلة.</desc>\n  </programme>\r'
    else:
        ch+=4*' '+'<desc lang="ar">'+descri.strip()+'</desc>\n  </programme>\r'
    data.append(ch)
    
data.pop(-1)

for epg in data:
    with io.open("/etc/epgimport/noor.xml", "a",encoding="utf-8") as f:
        f.write((epg).decode('utf-8'))
    
with io.open("/etc/epgimport/noor.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/noor.txt") as f:
    lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/noor.txt", "w") as f:
    f.writelines(lines)
    
print('**************FINISHED******************')