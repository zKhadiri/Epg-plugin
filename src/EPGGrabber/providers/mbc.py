#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import io
import os
import re
import sys
from datetime import datetime
from requests.adapters import HTTPAdapter
from time import strftime
from __init__ import *

if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

urls=[]

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

time_zone = tz()


today = int(datetime.strptime('' + str(datetime.now().strftime('%Y-%m-%d')) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000

channels=['mbc1','mbc-drama','mbc-maser','mbc-maser2','mbc4','mbc2','mbc-action','mbc-bollywood','mbc-drama-plus','mbc-max','mbc-iraq','mbc5','Wanasa']
import datetime
import time
from datetime import timedelta
week = datetime.date.today() + timedelta(days=7)
milli = int(datetime.datetime.strptime('' + str(week) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000
for c in channels:
    urls.append('https://www.mbc.net/.rest/api/channel/grids?channel='+c+'&from='+str(today)+'&to='+str(milli)+'')
    

ch=['MBC1','MBCDrama','MBCEgypt','MBCEgypt2','MBC4','MBC2','MBCAction','MBCBollywood',
    'MBC+Drama','MBCMovieMax','MBCIraq','MBCCinq','Wanasah','QATAR.TV','noordubai']

programme=[]
times=[]
end=[]
titles=[]
des=[]
sub=[]
channel=[]



now = datetime.datetime.now().strftime('%Y/%m/%d')
def mbc():
    for url in urls:
        programme[:]=[]
        times[:]=[]
        end[:]=[]
        titles[:]=[]
        des[:]=[]
        sub[:]=[]
        channel[:]=[]
        link = requests.get(url)
        data = json.loads(link.text)
        if data ==[]:
            nf = re.findall(r'channel=(.*?)&',str(url))
            print('No data found for : '+''.join(nf))
            sys.stdout.flush()
        else:
            for d in data:
                times.append(d['startTime'])
                end.append(d['endTime'])
                channel.append(d['channelLabel'])
                titles.append('     <title lang="ar">'+d['showPageTitle'].replace('&','-')+'</title>\n')
                if d['showPageGenreInArabic']==None or d['showPageAboutInArabic']==None:
                    des.append('     <desc lang="ar">No description for this programme</desc>\n  </programme>\r')
                    #sub.append('     <sub-title lang="ar">No data</sub-title>\n  </programme>\r')
                else:
                    des.append('     <desc lang="ar">'+d['showPageAboutInArabic'].replace('&','-')+'</desc>\n  </programme>\r')
                    #sub.append('     <sub-title lang="ar">'+d['showPageGenreInArabic'].replace('&','-')+'</sub-title>\n  </programme>\r')
            from datetime import datetime
            for elem, next_elem,en,nm in zip(times, times[1:] + [times[0]],end,channel):
                if times[-1]==elem and times[0]==next_elem:
                    prog_start=datetime.fromtimestamp(int(elem)// 1000).strftime('%Y%m%d%H%M%S')
                    prog_end=datetime.fromtimestamp(int(en)// 1000).strftime('%Y%m%d%H%M%S')
                    date_end =datetime.fromtimestamp(int(en)// 1000).strftime('%Y/%m/%d')
                    day = datetime.strptime(date_end,'%Y/%m/%d')
                    date_now = datetime.strptime(now,'%Y/%m/%d')
                    nb_days = day - date_now 
                else:
                    prog_start=datetime.fromtimestamp(int(elem)// 1000).strftime('%Y%m%d%H%M%S')
                    prog_end=datetime.fromtimestamp(int(next_elem)// 1000).strftime('%Y%m%d%H%M%S')
                programme.append(2 * ' ' + '<programme start="' + prog_start + ' '+time_zone+'" stop="' + prog_end + ' '+time_zone+'" channel="'+nm.replace(' ','').replace('-','')+'">\n')
            for prog,title,descri in zip(programme,titles,des):
                with io.open(EPG_ROOT+'/mbc.xml',"a",encoding='UTF-8')as f:
                    f.write(prog+title+descri)
                    
        print(nm+' epg donwloaded For : '+str(nb_days.days)+' Days')
        sys.stdout.flush()
               

def noor():
    times=[]
    data=[]
    from datetime import datetime
    with requests.Session() as s:
        s.mount('http://', HTTPAdapter(max_retries=50))
        url = s.get('http://www.noordubai.com/content/noordubai/ar-ae/schedule/2.html',headers=headers)
        time= re.findall(r'GMT:\s+(\d{2}:\d{2})',url.text)
        des = re.findall(r"class=\"post-title mt-0 mb-5\"><a href='#'>(.*?)</a></h5>\s+<h6><i",url.text)
        title = re.findall(r"<h4 class=\"post-title mt-0 mb-5\"><a href='#'>(.*?)</a>",url.text)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
    last_hr = 0
    for d in time:
        h, m = map(int, d.split(":"))
        if last_hr > h:
            today += + timedelta(days=1)
        last_hr = h
        times.append(today + timedelta(hours=h, minutes=m))
        
    print('Noor Dubai epg ends at {}'.format(times[-1]))
    for elem,next_elem,tit,descri in zip(times, times[1:] + [times[0]],title,des):
        ch=''
        startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="noordubai">\n'
        ch+=4*' '+'<title lang="ar">'+tit+'</title>\n'
        if descri=='':
            #ch+=4*' '+'<desc lang="ar">يتعذر الحصول على معلومات هذا البرنامج</desc>\n  </programme>\r'
            if not PY3:
                ch+=4*' '+'<desc lang="ar">·إذاعة نور دبي : افتتحت في 09/05/2006 تحت شعار اجتماعية برؤية إسلامية، وهي الإذاعة الأولى التي تصغي إلى الهموم اليومية والحياتية للمقيمين في دولة الإمارات العربية المتحدة، وتطل من خلال قناة نور دبي التلفزيونية التي انطلق بثها في 01/09/2008، لتركز على الرياضة والاقتصاد والتربية والصحة، وذلك في إطار اجتماعي وبرؤية إسلامية معتدلة.</desc>\n  </programme>\r'.decode('utf-8')
            else:
                ch+=4*' '+'<desc lang="ar">·إذاعة نور دبي : افتتحت في 09/05/2006 تحت شعار اجتماعية برؤية إسلامية، وهي الإذاعة الأولى التي تصغي إلى الهموم اليومية والحياتية للمقيمين في دولة الإمارات العربية المتحدة، وتطل من خلال قناة نور دبي التلفزيونية التي انطلق بثها في 01/09/2008، لتركز على الرياضة والاقتصاد والتربية والصحة، وذلك في إطار اجتماعي وبرؤية إسلامية معتدلة.</desc>\n  </programme>\r'
        else:
            ch+=4*' '+'<desc lang="ar">'+descri.strip()+'</desc>\n  </programme>\r'
        data.append(ch)
        
    data.pop(-1)

    for epg in data:
        with io.open(EPG_ROOT+'/mbc.xml', "a",encoding="utf-8") as f:
            if not PY3:
                f.write((epg).decode('utf-8'))
            else:
                f.write(epg)
                
        
def main():
    print('**************MBC EPG******************')
    sys.stdout.flush()
    
    xml_header(EPG_ROOT+'/mbc.xml',ch)
    
    mbc()
    noor()
    
    from datetime import datetime
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"]=="mbc":
            channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)
        
    close_xml(EPG_ROOT+'/mbc.xml')
    
    print('**************FINISHED******************')
    sys.stdout.flush()
   
if __name__ == "__main__":
    main()
    
       



