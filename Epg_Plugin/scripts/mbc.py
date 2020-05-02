#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,os,re,sys
from datetime import datetime

urls=[]


fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/mbc.txt','r')
time_zone = fil.read().strip()
fil.close()


today = int(datetime.strptime('' + str(datetime.now().strftime('%Y-%m-%d')) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000

channels=['mbc1','mbc-drama','mbc-maser2','mbc4','mbc2','mbc-action','mbc-bollywood','mbc-drama-plus','mbc-max','mbc-iraq','mbc5','Wanasa']
import datetime, time
from datetime import timedelta
week = datetime.date.today() + timedelta(days=7)
milli = int(datetime.datetime.strptime('' + str(week) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000
for c in channels:
    urls.append('https://www.mbc.net/.rest/api/channel/grids?channel='+c+'&from='+str(today)+'&to='+str(milli)+'')
    
with io.open("/etc/epgimport/mbc.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
   
ch=['MBC1','MBCDrama','MBCEgypt2','MBC4','MBC2','MBCAction','MBCBollywood','MBC+Drama','MBCMovieMax','MBCIraq','MBCCinq','Wanasah'] 
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
            for elem, next_elem,en,nm in zip(times, times[1:] + [times[0]],end,channel):
                if times[-1]==elem and times[0]==next_elem:
                    prog_start=datetime.datetime.fromtimestamp(int(elem)// 1000).strftime('%Y%m%d%H%M%S')
                    prog_end=datetime.datetime.fromtimestamp(int(en)// 1000).strftime('%Y%m%d%H%M%S')
                    date_end =datetime.datetime.fromtimestamp(int(en)// 1000).strftime('%Y/%m/%d')
                    day = datetime.datetime.strptime(date_end,'%Y/%m/%d')
                    date_now = datetime.datetime.strptime(now,'%Y/%m/%d')
                    nb_days = day - date_now 
                else:
                    prog_start=datetime.datetime.fromtimestamp(int(elem)// 1000).strftime('%Y%m%d%H%M%S')
                    prog_end=datetime.datetime.fromtimestamp(int(next_elem)// 1000).strftime('%Y%m%d%H%M%S')
                programme.append(2 * ' ' + '<programme start="' + prog_start + ' '+time_zone+'" stop="' + prog_end + ' '+time_zone+'" channel="'+nm.replace(' ','').replace('-','')+'">\n')
            for prog,title,descri in zip(programme,titles,des):
                with io.open("/etc/epgimport/mbc.xml","a",encoding='UTF-8')as f:
                    f.write(prog+title+descri)
                    
        print nm+' epg donwloaded For : '+str(nb_days.days)+' Days'
        sys.stdout.flush()
    
if __name__ == "__main__":
    mbc()
    
with io.open("/etc/epgimport/mbc.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    print('Downloading custom.channels config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.channels.xml?raw=true -O /etc/epgimport/custom.channels.xml')
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.sources.xml?raw=true -O /etc/epgimport/custom.sources.xml')


if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/elcinema.channels.xml?raw=true -O /etc/epgimport/elcinema.channels.xml')

if not os.path.exists('/etc/epgimport/dstv.channels.xml'):
    print('Downloading dstv channels config')
    os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/dstv.channels.xml?raw=true -O /etc/epgimport/dstv.channels.xml')