#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from time import sleep
import os,io,re,sys,requests

path = '/etc/epgimport/dstv.xml'

print "Downloading SuperSport epg guide\nPlease wait...."  
sys.stdout.flush()

url = requests.get('http://github.com/ziko-ZR1/XML/blob/master/dstv.xml?raw=true')
with io.open(path,'w',encoding="utf-8") as f:
    f.write(url.text)

         
print "dstv.xml donwloaded with success"



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

if not os.path.exists('/etc/epgimport/freesat.channels.xml'):
    print('Downloading freesat channels config')
    free_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/freesat.channels.xml?raw=true')
    with io.open('/etc/epgimport/freesat.channels.xml','w',encoding="utf-8") as f:
        f.write(free_channels.text)