#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,os,ch,sys
from time import sleep,strftime
from requests.adapters import HTTPAdapter

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt','r')
time_zone = fil.read().strip()
fil.close()



headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'epg.beinsports.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

urls=[]
print('**************STARTING******************')
for i in range(0,3):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('http://epg.beinsports.com/utctime_ar.php?cdate='+str(week))

now = str(datetime.datetime.now().year)+' '+str(datetime.datetime.now().month)

with io.open("/etc/epgimport/bein.xml","w",encoding='UTF-8')as f:
    f.write(('<tv generator-info-name="By ZR1">').decode('utf-8'))
for cc in ch.chann:
    with io.open("/etc/epgimport/bein.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+cc.replace(" ","_")+'">'+"\n"+'    <display-name lang="en">'+cc.replace("_"," ")+'</display-name>'+"\n"+'    <icon src="http://epg.beinsports.com/mena_sports/'+cc.replace('BS_NBA','BS NBA')+'.svg"/>'+"\n"+'    <url>http://www.bein.net/ar</url>'+"\n"+'  </channel>\r').decode('utf-8'))
alls=[]
def bein():
    for url in urls:
        alls[:]=[]
        from datetime import datetime
        with requests.Session() as s:
            s.mount('http://', HTTPAdapter(max_retries=10))
            link = s.get(url,headers=headers)
            time = re.findall(r'<p\sclass=time>(.*?)<\/p>',link.text)
            times = [t.replace('&nbsp;-&nbsp;','-').split('-') for t in time ]
            channels = re.findall(r"data-img='mena_sports\/(.*?)\.svg",link.text)
            title = re.findall(r'<p\sclass=title>(.*?)<\/p>',link.text)
            formt = re.findall(r'<p\sclass=format>(.*?)<\/p>',link.text)
            #format_=[4*' '+'<category lang="ar">'+f.replace('2014','2020')+'</category>'+'\n'+'  </programme>'+'\n' for f in formt]
            desc=[]
            title_chan=[]
            titles=[]
            prog=[]
            for tit in title:
                title_chan.append(tit.replace('   ',' ').split('- ')[0])
                spl = re.search(r'-\s(.*)',tit)
                if spl !=None:
                    desc.append(4*' '+'<desc lang="ar">'+spl.group().replace('- ','').replace('&','and')+'</desc>\n  </programme>\r')
                else:
                    desc.append(4*' '+'<desc lang="ar">'+tit.replace('&','and')+'</desc>\n  </programme>\r')

            for title_,form_ in zip(title_chan,formt):
                titles.append(4*' '+'<title lang="en">'+title_.replace('&','and')+' - '+form_.replace('2014','2020')+'</title>'+'\n')

            for time_,chann_ in zip(times,channels):
                from datetime import timedelta
                date = re.search(r'\d{4}-\d{2}-\d{2}',url)
                end ='05:59'
                start='18:00'
                if time_[0]>=start and time_[1]<=end:
                    fix = (datetime.strptime(date.group(),'%Y-%m-%d')-timedelta(days=1)).strftime('%Y-%m-%d')
                    starttime = datetime.strptime(fix+' '+time_[0],'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.strptime(date.group()+' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    prog.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+chann_.replace('BS NBA','BS_NBA')+'">'+'\n')
                else:
                    starttime = datetime.strptime(date.group()+' '+time_[0],'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    prog.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+chann_.replace('BS NBA','BS_NBA')+'">'+'\n')
    
            if len(title) !=0:
                for tt,d,p in zip(titles,desc,prog):
                    alls.append(p+tt+d)
                dat = re.search(r'\d{4}-\d{2}-\d{2}',url)
                print('Date'+' : '+dat.group())
                sys.stdout.flush()
                for pr,chc,chch in zip(alls,channels,channels[1:]+[channels[0]]):
                    if chc == chch: 
                        with io.open("/etc/epgimport/bein.xml","a",encoding='UTF-8')as fil:
                            fil.write(pr)
            else:
                print('No data found')
                break

if __name__=='__main__':
    bein()

     
with io.open("/etc/epgimport/bein.xml", "a",encoding="utf-8") as f:
    f.write(('\n'+'</tv>').decode('utf-8'))

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

print("**************FINISHED******************")