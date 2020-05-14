#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from time import sleep
import os,io,re,sys,requests


with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstvback.txt','r') as f:
    time_zone = f.readlines()[0].strip()
    
path = '/etc/epgimport/dstv.xml'

print "Downloading SuperSport epg guide\nPlease wait...."  
sys.stdout.flush()

url = requests.get('http://github.com/ziko-ZR1/XML/blob/master/dstv.xml?raw=true')
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
            with io.open(path,encoding="utf-8") as f:
                newText=f.read().decode('utf-8').replace(time_of.group(), time_zone)
                with io.open(path, "w",encoding="utf-8") as f:
                    f.write((newText).decode('utf-8'))
        else:
            print "file is empty"
            
    print "dstv.xml donwloaded with success"
else:
    print "dstv.xml not found"
    sys.stdout.flush()


from datetime import datetime
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstvback.txt") as f:
    lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstvback.txt", "w") as f:
    f.writelines(lines)

if os.path.exists('/var/lib/dpkg/status'):
    print 'Dream os image found\nSorting data please wait.....'
    sys.stdout.flush()
    import xml.etree.ElementTree as ET
    tree = ET.parse('/etc/epgimport/dstv.xml')
    data = tree.getroot()
    els = data.findall("*[@channel]")
    new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
    data[:] = new_els
    tree.write('/etc/epgimport/dstv.xml', xml_declaration=True, encoding='utf-8')

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