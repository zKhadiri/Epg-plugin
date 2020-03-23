import requests,re,threading,io,os,ch
from datetime import *
from time import sleep
from shutil import copyfile


headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}
print('**************STARTING******************')
urls=[]
for i in range(0,3):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('http://epg.beinsports.com/utctime.php?cdate='+str(week)+'&serviceidentity=beinsports.com&category=entertainment')

desc=[]
title_chan=[]
titles=[]
prog=[]
f=open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt",'r')
time_offset=f.read().replace('\n','')
f.close()

with io.open("/etc/epgimport/beinent.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
for nt in ch.net:
    with io.open("/etc/epgimport/beinent.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+nt+'">'+"\n"+'    <display-name lang="en">'+nt.replace("_"," ")+'</display-name>'+"\n"+'  </channel>'+"\n").decode('utf-8'))

def beinen():
    for url in urls:
        import _strptime
        desc[:]=[]
        title_chan[:]=[]
        titles[:]=[]
        prog[:]=[]
        link = requests.get(url,headers=headers)
        title = re.findall(r'<p\sclass=title>(.*?)<\/p>',link.text)
        time = re.findall(r'<p\sclass=time>(.*?)<\/p>',link.text)
        formt = re.findall(r'<p\sclass=format>(.*?)<\/p>',link.text)
        times = [t.replace('&nbsp;-&nbsp;','-').split('-') for t in time ]
        channels = re.findall(r"data-img='mena_entertaintment\/(.*?)\.",link.text)
        for tt_ in title:
            titles.append(4*' '+'<title lang="en">'+tt_.replace('&','and')+'</title>'+'\n')
            desc.append(4*' '+'<category lang="en">'+tt_.replace('&','and')+'</category>'+'\n')
        format_=[4*' '+'<desc lang="en">'+f+'</desc>'+"\n"+'  </programme>'+'\n' for f in formt]
        for time_,chann_ in zip(times,channels):
            date = re.search(r'\d{4}-\d{2}-\d{2}',url)
            starttime = datetime.datetime.strptime(date.group()+' '+time_[0],'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
            endtime = datetime.datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
            prog.append(2 * ' ' + '<programme start="' + starttime + ' '+time_offset+'" stop="' + endtime + ' '+time_offset+'" channel="'+chann_.replace('Star_World_HD','Star_World_B').replace('Star_Movies_HD','Star_Movies_B').replace('Bloomberg','Bloomberg_B')+'">'+'\n')
        
        for ttt,d,f,p in zip(titles,desc,format_,prog):
            with io.open("/etc/epgimport/beinent.xml","a",encoding='UTF-8')as fil:
                fil.write(p+ttt+d+f)
        dat = re.search(r'\d{4}-\d{2}-\d{2}',url)
        print('Date'+' : '+dat.group())
    
if __name__=='__main__':
    beinen()

with io.open("/etc/epgimport/beinent.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))


if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    copyfile("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/configs/custom.channels.xml", "/etc/epgimport/custom.channels.xml")
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    copyfile("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/configs/custom.sources.xml", "/etc/epgimport/custom.sources.xml")

print("**************FINISHED******************")