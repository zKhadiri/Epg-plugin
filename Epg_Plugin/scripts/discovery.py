#!/usr/bin/python
# -*- coding: utf-8 -*-

# python3
from __future__ import print_function


import requests,re,sys,io
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter

reload(sys)
sys.setdefaultencoding('UTF8')

next_update = (datetime.today()+timedelta(days=20)).strftime('%Y-%m-%d 02:00:00')

channels = ['Discovery Central Europe|DCENENG-UTC','Animal Planet Europe|APEUENG-UTC','Discovery Showcase HD|HDEUENG-UTC'
            ,'Discovery Science Europe|SCEUENG-UTC','ID|IDDEENG-UTC','DTX|TUTUROM-UTC','Discovery World|CVEUENG-UTC',
            'Discovery Channel France|DFRAFRE-UTC','Discovery Science France|SCFRFRE-UTC',
            'Discovery Family France|DFFRFRE-UTC','Investigation Discovery France|IDFRFRE-UTC']

print('**************Discovery EPG******************')
sys.stdout.flush()

with io.open("/etc/epgimport/discovery.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in channels:
    with io.open("/etc/epgimport/discovery.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x.split('|')[0]+'">'+"\n"+'    <display-name lang="en">'+x.split('|')[0]+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))
        
french=['DFRAFRE-UTC','SCFRFRE-UTC','DFFRFRE-UTC','IDFRFRE-UTC']
def discovery():
    with requests.Session() as s:
        s.mount('http://', HTTPAdapter(max_retries=10))
        for ch in channels:
            url = s.get('https://exports.pawa.tv/discovery/europe/'+ch.split('|')[1]+'.xml')

            titles = re.findall(r'<BROADCAST_TITLE>(.*?)</BROADCAST_TITLE>',url.text)
            date_start = re.findall(r'<BROADCAST_START_DATETIME>(.*?)</BROADCAST_START_DATETIME>',url.text)
            date_end = re.findall(r'<BROADCAST_END_TIME>(.*?)</BROADCAST_END_TIME>',url.text)
            description = re.findall(r'<TEXT_TEXT>(.*?)</TEXT_TEXT>',url.text)
            dtx_titles = re.findall(r'<PROGRAMME_TITLE_ORIGINAL>(.*?)</PROGRAMME_TITLE_ORIGINAL>',url.text)
            dtx_des = re.findall(r'<PROGRAMME_SUBTITLE_ORIGINAL>(.*?)</PROGRAMME_SUBTITLE_ORIGINAL>',url.text)
            episode = re.findall(r'<EPISODE_NUMBER>(.*?)</EPISODE_NUMBER>',url.text)
            programme_year = re.findall(r'<PROGRAMME_YEAR>(.*?)</PROGRAMME_YEAR>',url.text)
            season = re.findall(r'<SERIES_NUMBER>(.*?)</SERIES_NUMBER>',url.text)
            for title,start,end,des,ep,py,dtx_t,dxt_d,se in zip(titles,date_start,date_end,description,episode,programme_year,dtx_titles,dtx_des,season):
                if end <=next_update:
                    last_date = end
                    prog_start = datetime.strptime(start,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    prog_end = datetime.strptime(end,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    epg=''
                    if ch.split('|')[0]=="DTX":
                        epg+=2 * ' ' + '<programme start="' + prog_start + ' +0000" stop="' + prog_end + ' +0000" channel="'+ch.split('|')[0]+'">\n'
                        epg+=4*' '+'<title lang="en">'+dtx_t.replace('&amp;','and')+'</title>\n'
                        epg+=4*' '+'<desc lang="en">'+py+' (S'+se+' Ep '+ep+') : '+dxt_d.replace('&amp;','and').strip()+'</desc>\n  </programme>\r'
                    elif ch.split('|')[1] in french:
                        epg+=2 * ' ' + '<programme start="' + prog_start + ' +0000" stop="' + prog_end + ' +0000" channel="'+ch.split('|')[0]+'">\n'
                        epg+=4*' '+'<title lang="en">'+title.replace('&amp;','and')+'</title>\n'
                        epg+=4*' '+'<desc lang="en">'+py+' (S'+se+' Ep '+ep+') : '+des.replace('&amp;','and').strip()+'</desc>\n  </programme>\r'
                    else:
                        epg+=2 * ' ' + '<programme start="' + prog_start + ' +0000" stop="' + prog_end + ' +0000" channel="'+ch.split('|')[0]+'">\n'
                        epg+=4*' '+'<title lang="en">'+title.replace('&amp;','and')+'</title>\n'
                        epg+=4*' '+'<desc lang="en">'+py+' (S'+se+' Ep '+ep+') : '+des.replace('&amp;','and').strip()+'</desc>\n  </programme>\r'
                    with io.open("/etc/epgimport/discovery.xml","a",encoding='UTF-8')as f:
                        f.write(epg)
                    
            print(ch.split('|')[0]+' epg ends at '+last_date)
            sys.stdout.flush()
            
if __name__ =='__main__':
    discovery()
    with io.open("/etc/epgimport/discovery.xml", "a",encoding="utf-8") as f:
        f.write(('</tv>').decode('utf-8'))
    import json
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
        data = json.load(f)
    for bouquet in data['bouquets']:
        if bouquet["bouquet"]=="discovery":
            bouquet['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
        json.dump(data, f)
        
    print('**************FINISHED******************')
    sys.stdout.flush()
