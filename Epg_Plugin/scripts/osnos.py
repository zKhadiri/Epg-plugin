#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,threading,os,sys,ch
from datetime import datetime
from time import sleep,strftime
from requests.adapters import HTTPAdapter

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()


pyl=[]



headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip,deflate',
    'contenttype':'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}


with io.open("/etc/epgimport/osn.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in ch.xm:
    with io.open("/etc/epgimport/osn.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x.replace("_",' ')+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))  

for i in range(0,7):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour+timedelta(days=i)
    channels=['VHD','OYH','OYA']
    for c in channels:
        pyl.append({"newDate": week.strftime("%m/%d/%Y"), "selectedCountry": "SA", "channelCode": c, "isMobile": "false", "hoursForMobile": "24"})
            
pyl.sort()
pll=[]
now = datetime.datetime.today().strftime('%Y-%m-%d')

def oss():
    for url in pyl:
        global aff,days,nam
        with requests.Session() as s:
            s.mount('http://', HTTPAdapter(max_retries=10))
            ur= s.post('http://www.osn.com/CMSPages/TVScheduleWebService.asmx/GetTVChannelsProgramTimeTable',data=url,headers=headers)
            pg = ur.text.replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">','').replace('</string>','')
            data = json.loads(pg)
            #sleep(0.05)
            for d in data:
                day=datetime.datetime.fromtimestamp(int(d['StartDateTime'].replace('/Date(','').replace(')/','')) // 1000).strftime('%Y-%m-%d')
                if now == day or day > now:
                    payload = {"prgmEPGUNIQID": d['EPGUNIQID'], "countryCode": "SA"}
                    pll.append(d['EPGUNIQID'])
                    ch=''
                    with requests.Session() as session:
                        session.mount('http://', HTTPAdapter(max_retries=10))
                        uri= session.post('http://www.osn.com/CMSPages/TVScheduleWebService.asmx/GetProgramDetails',data=payload,headers=headers)
                        pag = uri.text.replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">','').replace('</string>','')
                        data= json.loads(pag)
                        nm=data[0][u'ChannelNameEnglish'].replace(' ','_')
                        nam=data[0][u'ChannelNameEnglish']
                        days=datetime.datetime.fromtimestamp(int(data[0][u'StartDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime('%Y%m%d%H%M%S')
                        days_end=datetime.datetime.fromtimestamp(int(data[0][u'EndDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime('%Y%m%d%H%M%S')
                        aff =datetime.datetime.fromtimestamp(int(data[0][u'EndDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime('%Y-%m-%d')
                        ch+= 2 * ' ' + '<programme start="' + days + ' '+time_zone+'" stop="' + days_end + ' '+time_zone+'" channel="'+nm+'">'+'\n'
                        if url['channelCode'] =='SER' or url['channelCode'] =='YAW' or url['channelCode'] =='SAF' or url['channelCode'] =='CM1' or url['channelCode'] =='CM2' or url['channelCode'] =='FAN' or url['channelCode'] =='OYH' or url['channelCode'] =='OYA' or url['channelCode'] =='OYC':
                            ch+='     <title lang="en">'+data[0][u'Arab_Title']+'</title>'+"\n"
                        else:
                            ch+='     <title lang="en">'+data[0][u'Title'].replace('&','and')+'</title>'+"\n"
                        if data[0][u'Arab_Synopsis']==u'\r\n':
                            ch+='     <desc lang="ar">'+data[0][u'GenreArabicName']+'</desc>\n  </programme>\r'
                        else:
                            ch+='     <desc lang="ar">'+data[0][u'Arab_Synopsis']+'</desc>\n  </programme>\r' 
                        #ch+='     <sub-title lang="ar">'+data[0][u'GenreArabicName']+'</sub-title>'+"\n"+'  </programme>'+"\n"
                        with io.open("/etc/epgimport/osn.xml","a",encoding='UTF-8')as f:
                            f.write(ch)
            for _ in progressbar((pll*120),nam+" "+aff+" : ", 15):pass
            #sleep(0.005)
    with io.open("/etc/epgimport/osn.xml", "a",encoding="utf-8") as f:
        f.write(('</tv>').decode('utf-8'))
        
def progressbar(it, prefix="", size=20, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), (size*j/count)*6.7, 100))
        file.flush()        
    #show(0)
    for v, item in enumerate(it):
        yield item
    show(v+1)
    file.write("\n")
    file.flush()

  
if __name__=='__main__':
    oss()
    from datetime import datetime
    with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt") as f:
        lines = f.readlines()
    lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt", "w") as f:
        f.writelines(lines)
    


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