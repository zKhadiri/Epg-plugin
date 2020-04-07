#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,json,io,threading,os,sys,ch
from datetime import datetime
from time import sleep, strftime
from requests.adapters import HTTPAdapter

time_zone = strftime('%z')

import time
os.environ['TZ'] = 'UTC'


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

for i in range(0,3):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour+timedelta(days=i)
    channels=['BO1','OCM','OFM','OMX','OM1','AHD','OPR','STM','PAR','OMK','OYH','OYA','OYC','OFH','OBG','OCO','OMZ','OLH','ONS','KDZ','CCE','STW','ETV','B4A','SER','SE4','YAW','SAF','CM1','CM2','DSC','SCI','DCX','CAI','HIS','HI2','NGO','NHD','NAH','TLC','VH1','DIS','DXD','MTL','DJR','NIC','NJR','NKT','BAB','BTV','VIV','FAN','NOW']
    for c in channels:
        pyl.append({"newDate": week.strftime("%m/%d/%Y"), "selectedCountry": "SA", "channelCode": c, "isMobile": "false", "hoursForMobile": "24"})
            

now = datetime.datetime.today().strftime('%Y-%m-%d')
pll=[]
def oss(url):
    global days,nam
    with requests.Session() as s:
        s.mount('http://', HTTPAdapter(max_retries=10))
        ur= s.post('http://www.osn.com/CMSPages/TVScheduleWebService.asmx/GetTVChannelsProgramTimeTable',data=url,headers=headers)
        pg = ur.text.replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">','').replace('</string>','')
        data = json.loads(pg)
        sleep(0.5)
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
                    nm=data[0][u'ChannelNameEnglish'].replace(' ','_').replace('Crime_&_Investigation_Network','Crime_And_Investigation_Network')
                    nam=data[0][u'ChannelNameEnglish']
                    days=datetime.datetime.fromtimestamp(int(data[0][u'StartDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime("%Y-%d-%m")
                    days_end=datetime.datetime.fromtimestamp(int(data[0][u'EndDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime("%Y-%d-%m")
                    strt=datetime.datetime.fromtimestamp(int(data[0][u'StartDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime("%H:%M")
                    endd = datetime.datetime.fromtimestamp(int(data[0][u'EndDateTime'].replace("/Date(",'').replace(")/",'')) // 1000).strftime("%H:%M")
                    starttime = datetime.datetime.strptime(days+" "+strt, '%Y-%d-%m %H:%M').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.datetime.strptime(days_end+" "+endd, '%Y-%d-%m %H:%M').strftime('%Y%m%d%H%M%S')
                    ch+= 2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+nm+'">'+'\n'
                    ch+='     <title lang="en">'+data[0][u'Title'].replace('&','and')+'</title>'+"\n"
                    ch+='     <desc lang="ar">'+data[0][u'Arab_Synopsis']+'</desc>'+"\n"
                    ch+='     <sub-title lang="ar">'+data[0][u'GenreArabicName']+'</sub-title>'+"\n"+'  </programme>'+"\n"
                    with io.open("/etc/epgimport/osn.xml","a",encoding='UTF-8')as f:
                        f.write(ch)
        for _ in progressbar((pll*120),nam+" "+days+" : ", 15):pass
        sleep(0.005)
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

def main():
    threads = [threading.Thread(target=oss, args=(url,)) for url in pyl]
    for thread in threads:
        thread.start()
        sleep(1)
    for thread in threads:
        thread.join()
        
if __name__=='__main__':
    main()
    
with io.open("/etc/epgimport/osn.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))

if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    print('Downloading custom.channels config')
    ur = requests.get('http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/custom.channels.xml',headers=headers)
    if ur.status_code ==200:
        with io.open('/etc/epgimport/custom.channels.xml','w') as f:
            f.write(ur.text)
        print('Done')
    else:
        print('Cannot establish connection to the server')
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    uri = requests.get('http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/custom.sources.xml',headers=headers)
    if uri.status_code==200:
        with io.open('/etc/epgimport/custom.sources.xml','w') as f:
            f.write(uri.text)
        print('Done')
    else:
        print('Cannot establish connection to the server')

if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    uri = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/elcinema.channels.xml',headers=headers)
    if uri.status_code ==200:
        with io.open('/etc/epgimport/elcinema.channels.xml','w') as f:
            f.write(uri.text)
        print('Done')
    else:
        print('Cannot establish connection to the server')

    
