#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __init__ import *

import requests
import io
import sys
import os
import re
import json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from time import sleep, strftime

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

def espn():
    for i in range(0,7):
        week = (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=10))
            url = s.get('https://www.tvpassport.com/tv-listings/stations/espn/594/{}'.format(week),headers=headers,timeout=10)

        date_start = re.findall(r'data-st=\"(.*?)\"',url.text)
        duration = re.findall(r'data-duration=\"(.*?)\"',url.text)
        title = re.findall(r'data-showName=\"(.*?)\"',url.text)
        description = re.findall(r'data-description=\"(.*?)\"',url.text)
        team1 = re.findall(r'data-team1=\"(.*?)\"',url.text)
        team2 = re.findall(r'data-team2=\"(.*?)\"',url.text)

        for dt,m,t,d,t1,t2 in zip(date_start,duration,title,description,team1,team2):
            ch=''
            start = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            end = (datetime.strptime(start,'%Y%m%d%H%M%S') + timedelta(minutes=int(m))).strftime('%Y%m%d%H%M%S')
            ch+=2 * ' ' + '<programme start="' + str(start) + ' +0000" stop="' + str(end) + ' +0000" channel="ESPN">\n'
            if t1 != "" and t2 != "":
                ch+=4*' '+'<title lang="en">'+t.replace('&','and')+' : '+t1+' vs '+t2+'</title>\n'
            else:
                ch+=4*' '+'<title lang="en">'+t.replace('&','and')+'</title>\n'
            ch+=4*' '+'<desc lang="en">'+d.replace('&','and')+'</desc>\n  </programme>\r'
            with io.open(EPG_ROOT+'/espn.xml',"a",encoding='UTF-8')as f:
                f.write(ch)
        print(week)
        sys.stdout.flush()

def main():
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for bouquet in data['bouquets']:
        if bouquet["bouquet"]=="espn":
            bouquet['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f) 
    
    print('**************Espn EPG******************')
    sys.stdout.flush()
    
    xml_header(EPG_ROOT+'/espn.xml',['ESPN'])
    
    espn()
    
    
    close_xml(EPG_ROOT+'/espn.xml')
    
    print("**************FINISHED******************")
    sys.stdout.flush()
    
if __name__=='__main__':
    main()
