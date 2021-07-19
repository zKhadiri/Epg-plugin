#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __init__ import *

import requests
import re
import io
import sys
import random
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from core.proxies import proxy

print('************Al jazeera arabic EPG **************')
sys.stdout.flush() 

def random_prox():
    p = random.choice(list(proxy()))
    return {'http':'http://'+p,'https':'https://'+p}


def to_xml(data):             
    times = re.findall(r'<div class="schedule__row__timeslot">(.*?)</div>',data)
    title = re.findall(r'<div class="schedule__row__showname">(.*?)</div>',data)
    des = re.findall(r'<div class="schedule__row__description">(.*?)</div>',data)

    if len(times)>0:
        now = (datetime.today()+timedelta(hours=3)).strftime('%Y-%m-%d')
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
            if PY3:
                ch+=4*' '+'<title lang="ar">'+tit.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','و').replace('<div class="schedule__row__nowshowing">','')+'</title>\n'
                ch+=4*' '+'<desc lang="ar">'+de.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','و').strip()+'</desc>\n  </programme>\r'
            else:
                ch+=4*' '+'<title lang="ar">'+tit.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','و'.decode('utf-8')).replace('<div class="schedule__row__nowshowing">','')+'</title>\n'
                ch+=4*' '+'<desc lang="ar">'+de.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','و'.decode('utf-8')).strip()+'</desc>\n  </programme>\r'
            
            with io.open(EPG_ROOT+"/aljazeera.xml", "a",encoding="utf-8") as f:
                f.write(ch)
                
        print('aljazeera epg download finished')
        sys.stdout.flush()   
    else:
        print('No data found for aljazeera')
        sys.stdout.flush()

def jscNews():
    with requests.Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            url = s.get('https://www.aljazeera.net/schedule',timeout=5)
            to_xml(url.text)
        except ConnectionError:
        
            print("Ip blocked , using proxy....\nPlease wait this might take a while.")
            sys.stdout.flush()
            
            tries = 10
            while tries >0:
                
                try:
                    url = s.get('https://www.aljazeera.net/schedule',proxies = random_prox(),timeout=3)
                    if '<!doctype html>' in url.text:
                        to_xml(url.text)
                        break
                except Exception:
                    tries -=1
                    print('Error occured Retry!!',tries)
                    
def main():
    xml_header(EPG_ROOT+'/aljazeera.xml',['aljazeera'])
    
    jscNews()
    
    close_xml(EPG_ROOT+'/aljazeera.xml')
        
    import json
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"]=="aljazeera":
            channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    print("**************FINISHED******************")
    sys.stdout.flush()
    
if __name__ == "__main__":
    main()
