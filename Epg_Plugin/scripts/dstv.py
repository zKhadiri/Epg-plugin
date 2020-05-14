#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,re,ch,os,sys
from datetime import datetime

urls=[]

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()

for i in range(0,5):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('https://www.dstv.co.za/webmethods/no-cache/GetChannelAllDate.ashx?d='+str(week)+'')

with io.open("/etc/epgimport/dstv.xml","w",encoding='UTF-8')as f:
    f.write(('<tv generator-info-name="By ZR1">').decode('utf-8'))
for cc in ch.ZA:
    with io.open("/etc/epgimport/dstv.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+cc+'">'+"\n"+'    <display-name lang="en">'+cc+'</display-name>'+"\n"+'  </channel>'+"\r").decode('utf-8'))

def dstv():
    for url in urls:
        link = requests.get(url,headers=headers)
        data=json.loads(link.text)
        for d in data['Channels']:
            for prog in d['Programmes']:
                ch=''
                startime= datetime.datetime.strptime(prog['StartTime'].replace('T',' ').replace('Z',''),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                endtime= datetime.datetime.strptime(prog['EndTime'].replace('T',' ').replace('Z',''),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                ch+=2*' '+'<programme start="'+startime+' '+time_zone+'" stop="'+endtime+' '+time_zone+'" channel="'+d['Name'].replace(' ','').replace('&','and')+'">\n'
                ch+=4*' '+'<title lang="en">'+prog['Title'].replace('&','and')+'</title>\n'
                ch+=4*' '+'<desc lang="en">No description Found for this programme</desc>\n  </programme>\r'
                with io.open("/etc/epgimport/dstv.xml","a",encoding='UTF-8')as f:
                    f.write(ch)
        dat = re.search(r'\d{4}-\d{2}-\d{2}',url)
        print('Date'+' : '+dat.group())    
        sys.stdout.flush()
if __name__=='__main__':
    dstv()
    from datetime import datetime
    with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt") as f:
        lines = f.readlines()
    lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt", "w") as f:
        f.writelines(lines)


with io.open("/etc/epgimport/dstv.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
if os.path.exists('/var/lib/dpkg/status'):
    print 'Dream os image found\nSorting data please wait.....'
    sys.stdout.flush()
    import xml.etree.ElementTree as ET
    tree = ET.parse('/etc/epgimport/dstv.xml')
    data = tree.getroot()
    els = data.findall("*[@channel]")
    new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
    data[:] = new_els
    tree.write('/etc/epgimport/dstv.xml', xml_declaration=True, encoding='utf-8')
    
    
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