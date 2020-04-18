import requests,re,io,os,ch
from time import sleep,strftime
from requests.adapters import HTTPAdapter


fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/beinent.txt','r')
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

print('**************STARTING******************')
urls=[]
for i in range(0,3):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('http://epg.beinsports.com/utctime.php?cdate='+str(week)+'&category=entertainment')

desc=[]
title_chan=[]
titles=[]
prog=[]

with io.open("/etc/epgimport/beinent.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
for nt in ch.net:
    with io.open("/etc/epgimport/beinent.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+nt+'">'+"\n"+'    <display-name lang="en">'+nt.replace("_"," ")+'</display-name>'+"\n"+'  </channel>'+"\r").decode('utf-8'))

def beinen():
    for url in urls:
        from datetime import datetime
        desc[:]=[]
        title_chan[:]=[]
        titles[:]=[]
        prog[:]=[]
        with requests.Session() as s:
            s.mount('http://', HTTPAdapter(max_retries=10))
            link = s.get(url,headers=headers)
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
                starttime = datetime.strptime(date.group()+' '+time_[0],'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(date.group() + ' ' + time_[1], '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                prog.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+chann_.replace('Star_World_HD','Star_World_B').replace('Star_Movies_HD','Star_Movies_B').replace('Bloomberg','Bloomberg_B')+'">'+'\n')
            if len(title) !=0:
                for ttt,d,f,p in zip(titles,desc,format_,prog):
                    with io.open("/etc/epgimport/beinent.xml","a",encoding='UTF-8')as fil:
                        fil.write(p+ttt+d+f)
                dat = re.search(r'\d{4}-\d{2}-\d{2}',url)
                print('Date'+' : '+dat.group())
            else:
                print('No data found')
                break
            
if __name__=='__main__':
    beinen()

with io.open("/etc/epgimport/beinent.xml", "a",encoding="utf-8") as f:
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



print("**************FINISHED******************")