import requests,re,io
from time import strftime
from datetime import datetime


fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/space.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()

with io.open("/etc/epgimport/spacetoon.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
    
with io.open("/etc/epgimport/spacetoon.xml","a",encoding='UTF-8')as f:
    f.write(("\n"+'  <channel id="Spacetoon">\n    <display-name lang="en">Spacetoon</display-name>\n  </channel>\r').decode('utf-8'))


title=[]
date=[]
alls=[]

for i in range(1,3):
    url=requests.get('https://spacetoon.com/broadcast?&day='+str(i)+'&zone=+3')
    dates=re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}',url.text)
    titles=re.findall(r'png\" />\s+(.*?)<!--',url.text)
    for title_ in titles:
        title.append(title_)
    for date_ in dates:
        date.append(date_)
    
for elem, next_elem,ti in zip(date, date[1:] + [date[0]],title):
    ch=''
    startime=datetime.strptime(elem,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
    endtime=datetime.strptime(next_elem,'%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
    ch+=2 * ' ' + '<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Spacetoon">\n'
    ch+=4*' '+'<title lang="ar">' + ti.replace('/','').replace('\\','').replace('&','and').strip() + '</title>\n'
    ch+=4 * ' ' + '<desc lang="ar">Kids</desc>\n  </programme>\r'
    alls.append(ch)


print 'Spacetoon epg ends at : '+date[-1]
    
alls.pop(-1)
for prog in alls:
    with io.open("/etc/epgimport/spacetoon.xml","a",encoding='UTF-8')as f:
        f.write(prog)
        
with io.open("/etc/epgimport/spacetoon.xml", "a",encoding="utf-8") as f:
    f.write(('\n'+'</tv>').decode('utf-8'))
    
from datetime import datetime
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/space.txt") as f:
    lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/space.txt", "w") as f:
    f.writelines(lines)