#!/usr/bin/python
# -*- coding: utf-8 -*-

from Plugins.Extensions.EPGGrabber.core.compat import PY3

import os
import io
import requests
import sys
if not os.path.exists('/etc/epgimport/ziko_config/custom.channels.xml'):
    print('Downloading custom.channels config')
    sys.stdout.flush()
    custom_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/custom.channels.xml', 'w', encoding="utf-8") as f:
        f.write(custom_channels.text)

if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    sys.stdout.flush()
    custom_source = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.sources.xml?raw=true')
    with io.open('/etc/epgimport/custom.sources.xml', 'w', encoding="utf-8") as f:
        f.write(custom_source.text)

if not os.path.exists('/etc/epgimport/ziko_config/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/bein.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/bein.channels.xml', 'w', encoding="utf-8") as f:
        f.write(bein_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/elcinema.channels.xml', 'w', encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/egypt2iet5.channels.xml'):
    print('Downloading egypt2iet5 channels config')
    sys.stdout.flush()
    egypt2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/egypt2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/egypt2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(egypt2iet5_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/uae1iet5.channels.xml'):
    print('Downloading uae1iet5 channels config')
    sys.stdout.flush()
    uae1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae2iet5.channels.xml'):
    print('Downloading uae2iet5 channels config')
    sys.stdout.flush()
    uae2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae2iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae3iet5.channels.xml'):
    print('Downloading uae3iet5 channels config')
    sys.stdout.flush()
    uae3iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae3iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae3iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae3iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae4iet5.channels.xml'):
    print('Downloading uae4iet5 channels config')
    sys.stdout.flush()
    uae4iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae4iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae4iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae4iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/saudiarabia1iet5.channels.xml'):
    print('Downloading saudiarabia1iet5 channels config')
    sys.stdout.flush()
    saudiarabia1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/saudiarabia1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/saudiarabia1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(saudiarabia1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/saudiarabia2iet5.channels.xml'):
    print('Downloading saudiarabia2iet5 channels config')
    sys.stdout.flush()
    saudiarabia2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/saudiarabia2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/saudiarabia2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(saudiarabia2iet5_channels.text)        
        
if not os.path.exists('/etc/epgimport/ziko_config/saudiarabia3iet5.channels.xml'):
    print('Downloading saudiarabia3iet5 channels config')
    sys.stdout.flush()
    saudiarabia3iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/saudiarabia3iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/saudiarabia3iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(saudiarabia3iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/saudiarabia4iet5.channels.xml'):
    print('Downloading saudiarabia4iet5 channels config')
    sys.stdout.flush()
    saudiarabia4iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/saudiarabia4iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/saudiarabia4iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(saudiarabia4iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar1iet5.channels.xml'):
    print('Downloading qatar1iet5 channels config')
    sys.stdout.flush()
    qatar1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar2iet5.channels.xml'):
    print('Downloading qatar2iet5 channels config')
    sys.stdout.flush()
    qatar2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar2iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar3iet5.channels.xml'):
    print('Downloading qatar3iet5 channels config')
    sys.stdout.flush()
    qatar3iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar3iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar3iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar3iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar4iet5.channels.xml'):
    print('Downloading qatar4iet5 channels config')
    sys.stdout.flush()
    qatar4iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar4iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar4iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar4iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar5iet5.channels.xml'):
    print('Downloading qatar5iet5 channels config')
    sys.stdout.flush()
    qatar5iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar5iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar5iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar5iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatar6iet5.channels.xml'):
    print('Downloading qatar6iet5 channels config')
    sys.stdout.flush()
    qatar6iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatar6iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatar6iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatar6iet5_channels.text)         
        
if not os.path.exists('/etc/epgimport/ziko_config/arabiapriet5.channels.xml'):
    print('Downloading arabiapriet5 channels config')
    sys.stdout.flush()
    arabiapriet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/arabiapriet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/arabiapriet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(arabiapriet5_channels.text)        
    
if not os.path.exists('/etc/epgimport/ziko_config/poland1iet5.channels.xml'):
    print('Downloading poland1iet5 channels config')
    sys.stdout.flush()
    poland1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/poland1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/poland1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(poland1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/poland2iet5.channels.xml'):
    print('Downloading poland2iet5 channels config')
    sys.stdout.flush()
    poland2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/poland2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/poland2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(poland2iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/dstv.channels.xml'):
    print('Downloading dstv channels config')
    sys.stdout.flush()
    dstv_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/dstv.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/dstv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/rotana.channels.xml'):
    print('Downloading rotana channels config')
    sys.stdout.flush()
    free_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/rotana.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/rotana.channels.xml', 'w', encoding="utf-8") as f:
        f.write(free_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/aljazeera.channels.xml'):
    print('Downloading aljazeera channels config')
    sys.stdout.flush()
    aljazeera_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/aljazeera.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/aljazeera.channels.xml', 'w', encoding="utf-8") as f:
        f.write(aljazeera_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/freesat.channels.xml'):
    print('Downloading freesat channels config')
    sys.stdout.flush()
    free_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/freesat.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/freesat.channels.xml', 'w', encoding="utf-8") as f:
        f.write(free_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/skyit.channels.xml'):
    print('Downloading skyit channels config')
    sys.stdout.flush()
    sky_it = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/skyit.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/skyit.channels.xml', 'w', encoding="utf-8") as f:
        f.write(sky_it.text)

if not os.path.exists('/etc/epgimport/ziko_config/discovery.channels.xml'):
    print('Downloading discovery.channels config')
    sys.stdout.flush()
    discovery_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/discovery.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/discovery.channels.xml', 'w', encoding="utf-8") as f:
        f.write(discovery_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/snrt.channels.xml'):
    print('Downloading Snrt.channels config')
    sys.stdout.flush()
    snrt_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/snrt.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/snrt.channels.xml', 'w', encoding="utf-8") as f:
        f.write(snrt_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/satTv.channels.xml'):
    print('Downloading satTv.channels config')
    sys.stdout.flush()
    satTv_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/satTv.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/satTv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(satTv_channels.text)