#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,re,os,sys
from datetime import datetime
from requests.adapters import HTTPAdapter

urls=[]

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}


print('**************DSTV EPG******************')
for i in range(0,5):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('https://www.dstv.co.za/webmethods/no-cache/GetChannelAllDate.ashx?d='+str(week)+'')

with io.open("/etc/epgimport/dstv.xml","w",encoding='UTF-8')as f:
    f.write(('<tv generator-info-name="By ZR1">').decode('utf-8'))
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/bouquets.json', 'r') as f:
    jsData = json.load(f)
for channel in jsData['bouquets']:
    if channel["name"]=="DSTV":  
        for nt in channel['channels']:
            with io.open("/etc/epgimport/dstv.xml","a",encoding='UTF-8')as f:
                f.write(("\n"+'  <channel id="'+nt+'">'+"\n"+'    <display-name lang="en">'+nt.replace("_"," ")+'</display-name>'+"\n"+'  </channel>'+"\r").decode('utf-8'))

def dstv():
    for url in urls:
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=100))
            link = s.get(url,headers=headers)
            data=json.loads(link.text)
            for d in data['Channels']:
                for prog in d['Programmes']:
                    ch=''
                    startime= datetime.datetime.strptime(prog['StartTime'].replace('T',' ').replace('Z',''),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    endtime= datetime.datetime.strptime(prog['EndTime'].replace('T',' ').replace('Z',''),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    ch+=2*' '+'<programme start="'+startime+' +0200" stop="'+endtime+' +0200" channel="'+d['Name'].replace(' ','').replace('&','and')+'">\n'
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
    import json
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
        data = json.load(f)
    for bouquet in data['bouquets']:
        if bouquet["bouquet"]=="dstv":
            bouquet['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
        json.dump(data, f)


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
    
    

print('**************FINISHED******************')
