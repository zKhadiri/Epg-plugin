#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,ch,os,sys
from datetime import datetime,timedelta
from time import sleep,strftime
from requests.adapters import HTTPAdapter

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinema.txt','r')
time_zone = fil.read().strip()
fil.close()

headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

REDC =  '\033[31m'                                                              
ENDC = '\033[m'                                                                 
                                                                                
def cprint(text):                                                               
    print REDC+text+ENDC 

times=[]
titles=[]
des=[]
prog=[]
ends=[]
starts=[]
prog_end=[]
end_date=[]
with io.open("/etc/epgimport/elcinema.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in ch.elc_channels:
    with io.open("/etc/epgimport/elcinema.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x.replace("_",' ')+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))

now = datetime.today().strftime('%Y %m %d')
today = datetime.now().strftime('%Y')
nb_channel=['1138','1145','1310','1314','1334','1356','1342','1241','1261','1174','1173','1169','1137','1223','1176','1199','1156','1262','1227','1198','1177','1193','1158',
            '1170','1159','1226','1292','1203','1101','1134','1283','1188','1260','1290','1204','1269','1280',
            '1300','1298','1297','1301','1299','1296','1304','1317','1302','1321','1338','1339','1350','1355','1148','1217',
            '1147','1149','1358']
def elci():
    for nb in nb_channel:
        with requests.Session() as s:
            s.mount('http://', HTTPAdapter(max_retries=10))
            url = s.get('http://elcinema.com/en/tvguide/'+nb+'/',headers=headers)
            time = re.findall(r'\d{2}:\d{2}\s+\w\w',url.text)
            dates=re.findall(r'class=" dates">(\s+.*\s+)<\/div>',url.text)
            channel_name=re.findall(r'<li>(.*?)<\/li>\s+<li\sclass=\"localization\">',url.text)
            end_time=re.findall(r'\[\d+\sminutes]',url.text)
            times[:]=[]
            titles[:]=[]
            des[:]=[]
            prog[:]=[]
            ends[:]=[]
            starts[:]=[]
            prog_end[:]=[]
            end_date[:]=[]
            for ti,en in zip(time,end_time):
                start=datetime.strptime(ti,'%I:%M %p')
                end = int(en.replace('[','').replace(' minutes]',''))
                times.append(start.strftime('%H:%M'))
                ends.append(end)
            
            toda = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
            last_hr = 0
            for d in times:
                h, m = map(int, d.split(":"))
                if last_hr > h:
                    toda = toda + timedelta(days=1)
                last_hr = h
                starts.append(toda + timedelta(hours=h, minutes=m))
                
            url_ar = s.get('http://elcinema.com/ar/tvguide/'+nb+'/',headers=headers)
            first=re.findall(r'<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>',url_ar.text)
            last=re.findall(r"<span class='hide'>[^\n]+",url_ar.text)
            for f,l in zip(first,last):
                des.append(f+l.replace("<span class='hide'>",'').replace('</span></li>',''))
                
            title_l = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li',url_ar.text)

            mt2 = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>',url_ar.text)
            for m in mt2:
                if m[0]=='' and m[1]=='':
                    titles.append('Unknown program')
                elif m[0]=='':
                    titles.append(m[1])
                else:
                    titles.append(m[0])
            error = False
            try:
                for index, element in enumerate(titles):
                    if element not in title_l:
                        des.insert(index,"No description Found for this program")

                b = datetime.strptime(str(today)+' '+dates[0].strip()+' '+times[0],'%Y %A %d %B %H:%M').strftime('%Y %A %d %B %H:%M')
                a = datetime.strptime(b,'%Y %A %d %B %H:%M')

                for r in ends:
                    x=a+timedelta(minutes=r)
                    a += timedelta(minutes=r)
                    prog_end.append(x)
                    
                for elem,next_elem in zip(starts,prog_end):
                    chnm = re.sub(' +', '', ''.join(channel_name)).replace(u'\xa0 Channel', '').replace('Channel', '')
                    startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    prog.append(2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+chnm.strip()+'">\n')
                    date_end =datetime.strptime(str(prog_end[-1]),'%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
                    day = datetime.strptime(date_end,'%Y/%m/%d')
                    date_now = datetime.strptime(now,'%Y %m %d')
                    nb_days = day - date_now
                    end_date.append(nb_days.days) 
                    
            except IndexError:
                cprint('No epg found or missing data for : '+''.join(channel_name))
                sys.stdout.flush()
                error = True
                pass
                
            for p,tt,d in zip(prog,titles,des):
                space=re.sub(' +', ' ', d).replace('\r','').replace('\n','').replace('&amp;','and').replace('(','').replace(')','').replace('&#39;',"'").replace('&quot;','"')
                ch='' 
                ch+=p
                ch+='     <title lang="ar">'+tt.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and')+'</title>\n'
                ch+='     <desc lang="ar">'+space+'</desc>\n  </programme>\r'
                with io.open("/etc/epgimport/elcinema.xml","a",encoding='UTF-8')as f:
                    f.write(ch)
            
            chan='\n'.join(channel_name).strip()
            if error:
                pass
            else:
                print chan+' epg downloaded for : '+str(end_date[-1])+' Days'
                sys.stdout.flush()
                
                
    with io.open("/etc/epgimport/elcinema.xml", "a",encoding="utf-8") as f:
        f.write(('</tv>').decode('utf-8'))          
    
if __name__=='__main__':
    import time
    Hour = time.strftime("%H:%M")
    start='00:00'
    end='02:00'
    if Hour>=start and Hour<end:
        print 'Please come back at 2am to download the epg'
    else:
        elci()

        
    
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