#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,os,re,sys
from datetime import datetime
from requests.adapters import HTTPAdapter
from time import strftime

reload(sys)
sys.setdefaultencoding('utf-8')

urls=[]

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

def get_tz():
    try:
        url_timezone = 'http://worldtimeapi.org/api/ip'
        requests_url = requests.get(url_timezone)
        ip_data = requests_url.json()
        return ip_data['utc_offset'].replace(':', '')
    except:
        return strftime("%z")
    
time_zone = get_tz()


today = int(datetime.strptime('' + str(datetime.now().strftime('%Y-%m-%d')) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000

channels=['mbc1','mbc-drama','mbc-maser','mbc-maser2','mbc4','mbc2','mbc-action','mbc-bollywood'
          ,'mbc-drama-plus','mbc-max','mbc-iraq','mbc5','Wanasa']
import datetime, time
from datetime import timedelta
week = datetime.date.today() + timedelta(days=7)
milli = int(datetime.datetime.strptime('' + str(week) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000
for c in channels:
    urls.append('https://www.mbc.net/.rest/api/channel/grids?channel='+c+'&from='+str(today)+'&to='+str(milli)+'')
    
with io.open("/etc/epgimport/mbc.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
   
ch=['MBC1','MBCDrama','MBCEgypt','MBCEgypt2','MBC4','MBC2','MBCAction','MBCBollywood',
    'MBC+Drama','MBCMovieMax','MBCIraq','MBCCinq','Wanasah','QATAR.TV','noordubai']

for x in ch:
    with io.open("/etc/epgimport/mbc.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))  

programme=[]
times=[]
end=[]
titles=[]
des=[]
sub=[]
channel=[]

print('**************MBC EPG******************')

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
            print 'No data found for : '+''.join(nf)
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
                with io.open("/etc/epgimport/mbc.xml","a",encoding='UTF-8')as f:
                    f.write(prog+title+descri)
                    
        print nm+' epg donwloaded For : '+str(nb_days.days)+' Days'
        sys.stdout.flush()
        
def qatar():
    times=[]
    prog_start=[]
    epg=[]
    from datetime import datetime
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
        with io.open("/etc/epgimport/mbc.xml","a",encoding='UTF-8')as f:
            f.write(prog)        

def noor():
    times=[]
    data=[]
    from datetime import datetime
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
            ch+=4*' '+'<desc lang="ar">·إذاعة نور دبي : افتتحت في 09/05/2006 تحت شعار اجتماعية برؤية إسلامية، وهي الإذاعة الأولى التي تصغي إلى الهموم اليومية والحياتية للمقيمين في دولة الإمارات العربية المتحدة، وتطل من خلال قناة نور دبي التلفزيونية التي انطلق بثها في 01/09/2008، لتركز على الرياضة والاقتصاد والتربية والصحة، وذلك في إطار اجتماعي وبرؤية إسلامية معتدلة.</desc>\n  </programme>\r'.decode('utf-8')
        else:
            ch+=4*' '+'<desc lang="ar">'+descri.strip()+'</desc>\n  </programme>\r'
        data.append(ch)
        
    data.pop(-1)

    for epg in data:
        with io.open("/etc/epgimport/mbc.xml", "a",encoding="utf-8") as f:
            f.write((epg).decode('utf-8'))
        
    
if __name__ == "__main__":
    mbc()
    #qatar()
    noor()
    
    from datetime import datetime
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"]=="mbc":
            channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
        json.dump(data, f)
    
    with io.open("/etc/epgimport/mbc.xml", "a",encoding="utf-8") as f:
        f.write(('</tv>').decode('utf-8'))    


print('**************FINISHED******************')
