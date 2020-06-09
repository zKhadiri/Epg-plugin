 
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,os,sys,warnings,ssl
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

def get_tz():
    url_timezone = 'http://worldtimeapi.org/api/ip'
    requests_url = requests.get(url_timezone)
    ip_data = requests_url.json()

    try:
        return ip_data['utc_offset'].replace(':', '')
    except:
        return ('+0000')
    
    
time_zone=get_tz()
time=[]
epg=[]
channels_code=['74-CBC DRAMA','88-CBC','103-NILE DRAMA','90-AL MIHWAR','255-ON E','259-ON DRAMA','131-AL NAHAR','86-AL NAHAR DRAMA'
               ,'76-SADA ALBALAD','129-SADA ALBALAD DRAMA','81-AL HAYAT','233-al kahira wa nass','234-al kahira wa nass +2',
               '257-DMC','258-DMC DRAMA']

with io.open("/etc/epgimport/filfan.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in channels_code:
    with io.open("/etc/epgimport/filfan.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x.split('-')[1]+'">'+"\n"+'    <display-name lang="en">'+x.split('-')[1]+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8')) 

for channel in channels_code:
    with requests.Session() as s:
        s.mount('http://', HTTPAdapter(max_retries=50))
        ssl._create_default_https_context = ssl._create_unverified_context
        url = s.get('https://www.filfan.com/channel/details/'+channel.split('-')[0],headers=headers,verify=False)
        titles=re.findall(r'showtype=\d+\">(.*?)</a>\s</td>',url.text)
        times=re.findall(r'(\d{2}:\d{2})</td>',url.text)
        descrip = re.findall(r'tvrepeat\">(.*?)</td>',url.text)

    time[:]=[]
    epg[:]=[]
    if len(times)>0:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
        last_hr = 0
        for d in times:
            h, m = map(int, d.split(":"))
            if last_hr > h:
                today += + timedelta(days=1)
            last_hr = h
            time.append(today + timedelta(hours=h, minutes=m))
            
        for elem,next_elem,title,des in zip(time, time[1:] + [time[0]],titles,descrip):
            ch=''
            startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+channel.split('-')[1]+'">\n'
            ch+=4*' '+'<title lang="ar">'+title+'</title>\n'
            ch+=4*' '+'<desc lang="ar">'+des.strip()+'</desc>\n  </programme>\r'
            epg.append(ch)
    
        print channel.split('-')[1]+' epg ends at '+str(time[-1])
        sys.stdout.flush()
        epg.pop(-1)
        for ep in epg:
            with io.open("/etc/epgimport/filfan.xml","a",encoding='UTF-8')as f:
                f.write((ep))
    
    else:
        print 'no data found for '+channel.split('-')[1]
        sys.stdout.flush()
        
with io.open("/etc/epgimport/filfan.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
    
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/filfan.txt") as f:
    lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/filfan.txt", "w") as f:
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
        
        
if not os.path.exists('/etc/epgimport/jawwy.channels.xml'):
    print('Downloading jawwy channels config')
    jaw_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/jawwy.channels.xml?raw=true')
    with io.open('/etc/epgimport/jawwy.channels.xml','w',encoding="utf-8") as f:
        f.write(jaw_channels.text)
   
if not os.path.exists('/etc/epgimport/freesat.channels.xml'):
    print('Downloading freesat channels config')
    free_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/freesat.channels.xml?raw=true')
    with io.open('/etc/epgimport/freesat.channels.xml','w',encoding="utf-8") as f:
        f.write(free_channels.text)