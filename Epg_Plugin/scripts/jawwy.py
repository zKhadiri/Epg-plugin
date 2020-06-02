#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from time import sleep
import os,io,re,sys,requests

path = '/etc/epgimport/jawwytv.xml'


with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/jawwy.txt','r') as f:
    time_zone = f.readlines()[0].strip()


print "Downloading Jawwy TV epg guide\nPlease wait...."  
sys.stdout.flush()
url=requests.get('https://raw.githubusercontent.com/ziko-ZR1/XML/jawwy/jawwytv.xml')
with io.open(path,'w',encoding="utf-8") as f:
    f.write(url.text)
    
    
sleep(1)

f = open(path,'r')
time_of = re.search(r'[+#-]+\d{4}',f.read())
f.close()

if os.path.exists(path):
    print "changing to your timezone please wait...."
    sys.stdout.flush()
    if os.path.exists(path):
        if time_of !=None:
            if time_of.group()==time_zone:
                print 'No need to change the timezone : '+time_zone
                sys.stdout.flush()
            else:
                with io.open(path,encoding="utf-8") as f:
                    newText=f.read().decode('utf-8').replace(time_of.group(), time_zone)
                    with io.open(path, "w",encoding="utf-8") as f:
                        f.write((newText).decode('utf-8'))
        else:
            print "file is empty"
            
    print "jawwytv.xml donwloaded with succes"
else:
    print "jawwytv.xml not found"


from datetime import datetime
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/jawwy.txt") as f:
    lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/jawwy.txt", "w") as f:
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
        
if not os.path.exists('/etc/epgimport/eliftv.channels.xml'):
  print('Downloading eliftv channels config')
  elif_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/eliftv.channels.xml?raw=true')
  with io.open('/etc/epgimport/eliftv.channels.xml','w',encoding="utf-8") as f:
      f.write(elif_channels.text)

if not os.path.exists('/etc/epgimport/jawwy.channels.xml'):
    print('Downloading jawwy channels config')
    jaw_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/jawwy.channels.xml?raw=true')
    with io.open('/etc/epgimport/jawwy.channels.xml','w',encoding="utf-8") as f:
        f.write(jaw_channels.text)