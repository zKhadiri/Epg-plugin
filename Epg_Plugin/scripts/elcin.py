#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,io,ch,os,threading,sys
from datetime import datetime
from time import sleep,strftime

time_zone = strftime('%z')

import time
os.environ['TZ'] = 'UTC'


headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

REDC =  '\033[31m'                                                              
ENDC = '\033[m'                                                                 
                                                                                
def cprint(text):                                                               
    print REDC+text+ENDC 

days=[]
times=[]
titles=[]
des=[]
cat=[]
prog=[]

with io.open("/etc/epgimport/elcinema.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in ch.elc_channels:
    with io.open("/etc/epgimport/elcinema.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x.replace("_",' ')+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))

now = datetime.today().year
nb_channel=['1186','1261','1174','1173','1169','1137','1223','1176','1199','1156','1262','1227','1198','1177','1193','1158',
            '1170','1159','1226','1292','1203','1101','1134','1283','1188','1260','1290','1204','1269','1280',
            '1300','1298','1297','1301','1299','1296','1304','1317','1302','1312','1321','1338','1339','1353','1350','1355']
def elci(nb):
    url = requests.get('http://elcinema.com/en/tvguide/'+nb+'/',headers=headers)
    time_d = re.findall(r'\d{2}:\d{2}\s+\w\w|<div\sclass=\" dates\">\s+(.*)',url.text)
    time = re.findall(r'\d{2}:\d{2}\s+\w\w',url.text)
    channel_name=re.findall(r'<li>(.*?)<\/li>\s+<li\sclass=\"localization\">',url.text)
    print('\n'.join(channel_name))
    days[:]=[]
    times[:]=[]
    titles[:]=[]
    des[:]=[]
    cat[:]=[]
    prog[:]=[]
    for ti in time:
        times.append(datetime.strptime(ti, '%I:%M %p').strftime('%H:%M'))

    for i, val in enumerate(time_d):
        if not val:
            time_d[i] = time_d[i-1]
            days.append(time_d[i])      
            
    url_ar = requests.get('http://elcinema.com/ar/tvguide/'+nb+'/',headers=headers)
    first=re.findall(r'<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>',url_ar.text)
    last=re.findall(r"<span class='hide'>[^\n]+",url_ar.text)
    desc=re.findall(r'<\/a><\/li>\s+<li>\s+\s+(.*\s+.*?)\s+<\/li>\s+<li>',url_ar.text)
    descc = [re.sub(' +',' ',d).replace('\n','') for d in desc]
    for f,l in zip(first,last):
        des.append(f+l.replace("<span class='hide'>",'').replace('</span></li>',''))
        
    for dess in descc:
        cat.append(dess)  
        
    title_l = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li',url_ar.text)

    mt2 = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>',url_ar.text)
    for m in mt2:
        if m[0]=='':
            titles.append(m[1])
        else:
            titles.append(m[0])

    error = False
    try:
        for index, element in enumerate(titles):
            if element not in title_l:
                des.insert(index,titles[index])
                cat.insert(index,titles[index])
        for elem,next_elem,td1,td2 in zip(times, times[1:]+[times[0]],days,days[1:]+[days[0]]):
            chnm = re.sub(' +', '', ''.join(channel_name)).replace(u'\xa0 Channel', '').replace('Channel', '')
            if elem.startswith('23') or next_elem.startswith('23'):
                fixed = int(datetime.strptime(str(td2),'%A %d %B').strftime('%d')) - 1
                fixed_l = datetime.strptime(str(td1), '%A %d %B').strftime('%d')
                month = datetime.strptime(str(td2),'%A %d %B').strftime('%m')
                startime = datetime.strptime(str(now) + ' ' + str(month)+' '+str(fixed)+ ' ' + elem,'%Y %m %d %H:%M').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(str(now) + ' ' + str(month)+' '+str(fixed_l)+ ' ' + next_elem,'%Y %m %d %H:%M').strftime('%Y%m%d%H%M%S')
                prog.append(2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+chnm.strip()+'">\n')
            else:
                startime=datetime.strptime(str(now)+' '+str(td1)+' '+elem,'%Y %A %d %B %H:%M').strftime('%Y%m%d%H%M%S')
                endtime=datetime.strptime(str(now)+' '+str(td2)+' '+next_elem,'%Y %A %d %B %H:%M').strftime('%Y%m%d%H%M%S')
                prog.append(2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+chnm.strip()+'">\n')
            
    except IndexError:
        cprint('No epg found or missing data for : '+''.join(channel_name))
        error = True
        pass
        
    
    
    for p,tt,d,c in zip(prog,titles,des,cat):
        space=re.sub(' +', ' ', d).replace('\r','').replace('\n','').replace('&amp;','and').replace('(','').replace(')','').replace('&#39;',"'").replace('&quot;','"')
        ch='' 
        ch+=p
        ch+='     <title lang="ar">'+tt.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and')+'</title>\n'
        ch+='     <desc lang="ar">'+space+'</desc>\n'
        ch+='     <category lang="ar">'+c+'</category>\n'+'  </programme>\n'
        with io.open("/etc/epgimport/elcinema.xml","a",encoding='UTF-8')as f:
            f.write(ch)
    
    chan='\n'.join(channel_name)
    if error:
        pass
    else:
        for _ in progressbar((nb_channel*120),chan, 15):pass
    sleep(3)
    
  
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
    threads = [threading.Thread(target=elci, args=(nb,)) for nb in nb_channel]
    for thread in threads:
        thread.start()
        sleep(1)
    for thread in threads:
        thread.join()

        
        
with io.open("/etc/epgimport/elcinema.xml", "a",encoding="utf-8") as f:
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