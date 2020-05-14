#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,sys,ch,os
from datetime import datetime,timedelta
from time import sleep,strftime
from requests.adapters import HTTPAdapter

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/entc.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()

headers={
    'Host': 'elcinema.com',
    'Referer': 'https://elcinema.com/tvguide/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}
nb_channel=['1322-BEINMOVIESPREMIERE','1323-BEINMOVIESACTION','1324-BEINMOVIESDRAMA','1325-BEINMOVIESFAMILY','1326-BeInBoxOffice','1327-BeInSeriesHD1'
            ,'1328-BeInSeriesHD2','1309-beINDrama','1330-FOXACTIONMOVIES','1331-FOXFAMILYMOVIESHD']

REDC =  '\033[31m'                                                              
ENDC = '\033[m'                                                                 
                                                                                
def cprint(text):                                                               
    print REDC+text+ENDC
    
with io.open("/etc/epgimport/beinentCin.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in ch.ent:
    with io.open("/etc/epgimport/beinentCin.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x.replace("_",' ')+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))

class elcin():
    def __init__(self):
        self.now=datetime.today().strftime('%Y %m %d')
        self.time=[]
        self.end=[]
        self.des=[]
        self.titles=[]
        self.prog_start=[]
        self.prog_end=[]
        self.title=[]
        self.error = False
        self.channel_name=''
        self.url=''
    def main(self):
        for nb in nb_channel:
            self.nb=nb
            self.time[:]=[]
            self.end[:]=[]
            self.des[:]=[]
            self.titles[:]=[]
            self.prog_start[:]=[]
            self.prog_end[:]=[]
            self.title[:]=[]
            with requests.Session() as s:
                s.mount('http://', HTTPAdapter(max_retries=10))
                self.url = s.get('http://elcinema.com/tvguide/'+self.nb.split('-')[0]+'/',headers=headers)
                for time,end in zip (re.findall(r'(\d\d\:\d\d.*)',self.url.text),re.findall(r'\"subheader\">\[(\d+)',self.url.text)):
                    start=datetime.strptime(time.replace('</li>','').replace('مساءً'.decode('utf-8'),'PM').replace('صباحًا'.decode('utf-8'),'AM'),'%I:%M %p')
                    self.time.append(start.strftime('%H:%M'))
                    self.end.append(int(end))
                    
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
                last_hr = 0
                for d in self.time:
                    h, m = map(int, d.split(":"))
                    if last_hr > h:
                        today += + timedelta(days=1)
                    last_hr = h
                    self.prog_start.append(today + timedelta(hours=h, minutes=m))
                    
                for f,l in zip(re.findall(r'<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>',self.url.text),re.findall(r"<span class='hide'>[^\n]+",self.url.text)):
                    self.des.append(f+l.replace("<span class='hide'>",'').replace('</span></li>',''))
                    
                self.title = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li',self.url.text)
                mt2 = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>',self.url.text)
                for m in mt2:
                    if m[0]=='' and m[1]=='':
                        self.titles.append('Unknown program')
                    elif m[0]=='':
                        self.titles.append(m[1])
                    else:
                        self.titles.append(m[0])
                try:
                    for index, element in enumerate(self.titles):
                        if element not in self.title:
                            self.des.insert(index,"No description Found for this program")
                    b = datetime.strptime(self.now+' '+self.time[0],'%Y %m %d %H:%M').strftime('%Y %m %d %H:%M')
                    a = datetime.strptime(b,'%Y %m %d %H:%M')
                    for r in self.end:
                        x=a+timedelta(minutes=r)
                        a += timedelta(minutes=r)
                        self.prog_end.append(x)
                except IndexError:
                    self.error = True
                    cprint('No epg found or missing data for : '+self.nb.split('-')[1])
                    sys.stdout.flush()
                    pass
                for elem,next_elem,title,des in zip(self.prog_start,self.prog_end,self.titles,self.des):
                    ch=''
                    startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+self.nb.split('-')[1]+'">\n'
                    ch+=4*' '+'<title lang="ar">'+title.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and')+'</title>\n'
                    ch+=4*' '+'<desc lang="ar">'+des.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and').replace('(','').replace(')','').strip()+'</desc>\n  </programme>\r'
                    with io.open("/etc/epgimport/beinentCin.xml","a",encoding='UTF-8')as f:
                        f.write(ch)
                        
            if self.error:
                self.error = False
                pass
            else:
                print self.nb.split('-')[1]+' epg ends at : '+str(self.prog_end[-1])
                sys.stdout.flush()
        
if __name__=='__main__':
    import time
    Hour = time.strftime("%H:%M")
    start='00:00'
    end='02:00'
    if Hour>=start and Hour<end:
        print 'Please come back at 2am to download the epg'
    else:
        elcin().main()
        from datetime import datetime
        with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/entc.txt") as f:
            lines = f.readlines()
        lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/entc.txt", "w") as f:
            f.writelines(lines)
    
    
with io.open("/etc/epgimport/beinentCin.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
    
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