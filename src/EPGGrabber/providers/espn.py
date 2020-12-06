#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __init__ import *

import requests,re,sys,io,json
from datetime import datetime,timedelta


def espn(channel):
    for i in range(0,7):
        days =  (datetime.today()+timedelta(days=i)).strftime('%Y%m%d')
        
        url = requests.get('http://www.guiaespn.com/dinamicas/grilladiaria/index.php?coca=695&fecha='+days+'&idMedio='+channel.split('-')[1]+'&formato=desktop')

        titles = re.findall(r'<span class=\"main-title\">(.*?)<\/span>',url.content)
        descriptions = re.findall(r'<div class=\"reviews-info\">(.*?)<\/div>',url.content)

        for time,end,title,des in zip(re.findall(r'<div class=\"item_hour\">(\d{2}:\d{2})',url.content),re.findall(r'duration\">.*\((\d+)',url.content),titles,descriptions):
            start = datetime.strptime(days+' '+time,'%Y%m%d %H:%M').strftime('%Y%m%d%H%M%S')
            end = datetime.strptime(days+' '+(datetime.strptime(time,"%H:%M")+timedelta(minutes=int(end))).strftime('%H:%M'),'%Y%m%d %H:%M').strftime('%Y%m%d%H%M%S')
            epg=''
            epg+=2 * ' ' + '<programme start="' + start + ' -0300" stop="' + end + ' -0300" channel="'+channel.split('-')[0]+'">\n'
            if PY3:
                epg+=4*' '+'<title lang="en">'+title.replace('&','and')+'</title>\n'
                epg+=4*' '+'<desc lang="en">'+des.replace('&','and')+'</desc>\n  </programme>\r'
            else:
                epg+=4*' '+'<title lang="en">'+title.decode('latin1').replace('&','and')+'</title>\n'
                epg+=4*' '+'<desc lang="en">'+des.decode('latin1').replace('&','and')+'</desc>\n  </programme>\r'
                
            with io.open(EPG_ROOT+'/espn.xml',"a",encoding='UTF-8')as f:
                f.write(epg)
                
    ends = datetime.strptime(end,'%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')
    print(channel.split('-')[0]+' EPG ends at : '+ends)
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
    
    xml_header(EPG_ROOT+'/espn.xml',['Espn 901','Espn 902'])
    
    for channel in ['Espn 901-1418','Espn 902-1107']:
        espn(channel)
    
    
    close_xml(EPG_ROOT+'/espn.xml')
    
    print("**************FINISHED******************")
    sys.stdout.flush()
    
if __name__=='__main__':
    main()