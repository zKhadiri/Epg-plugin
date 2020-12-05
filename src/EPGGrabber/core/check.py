#!/usr/bin/python
# -*- coding: utf-8 -*-

# python3
from __future__ import print_function
from compat import PY3

import os,io,requests,sys
if not os.path.exists('/etc/epgimport/ziko_config/custom.channels.xml'):
    print('Downloading custom.channels config')
    sys.stdout.flush()
    custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/custom.channels.xml','w',encoding="utf-8") as f:
        f.write(custom_channels.text)
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    sys.stdout.flush()
    custom_source=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.sources.xml?raw=true')
    with io.open('/etc/epgimport/custom.sources.xml','w',encoding="utf-8") as f:
        f.write(custom_source.text)

if not os.path.exists('/etc/epgimport/ziko_config/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/elcinema.channels.xml','w',encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/dstv.channels.xml'):
    print('Downloading dstv channels config')
    sys.stdout.flush()
    dstv_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/dstv.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/dstv.channels.xml','w',encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/jawwy.channels.xml'):
    print('Downloading jawwy channels config')
    sys.stdout.flush()
    jaw_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/jawwy.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/jawwy.channels.xml','w',encoding="utf-8") as f:
        f.write(jaw_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/freesat.channels.xml'):
    print('Downloading freesat channels config')
    sys.stdout.flush()
    free_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/freesat.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/freesat.channels.xml','w',encoding="utf-8") as f:
        f.write(free_channels.text)
        
if not os.path.exists('/etc/epgimport/ziko_config/skyit.channels.xml'):
    print('Downloading skyit channels config')
    sys.stdout.flush()
    sky_it=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/skyit.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/skyit.channels.xml','w',encoding="utf-8") as f:
        f.write(sky_it.text)
        
if not os.path.exists('/etc/epgimport/ziko_config/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/bein.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/bein.channels.xml','w',encoding="utf-8") as f:
        f.write(bein_channels.text)
        
if not os.path.exists('/etc/epgimport/ziko_config/discovery.channels.xml'):
    print('Downloading discovery.channels config')
    sys.stdout.flush()
    discovery_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/discovery.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/discovery.channels.xml','w',encoding="utf-8") as f:
        f.write(discovery_channels.text)
