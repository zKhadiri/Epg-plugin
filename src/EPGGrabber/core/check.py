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

if not os.path.exists('/etc/epgimport/ziko_config/egypt2iet5.channels.xml'):
    print('Downloading egypt2iet5 channels config')
    sys.stdout.flush()
    egypt2iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/egypt2iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/egypt2iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(egypt2iet5_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/arabiapriet5.channels.xml'):
    print('Downloading arabiapriet5 channels config')
    sys.stdout.flush()
    arabiapriet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/arabiapriet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/arabiapriet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(arabiapriet5_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/qatareniet5.channels.xml'):
    print('Downloading qatareniet5 channels config')
    sys.stdout.flush()
    arabiapreniet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatareniet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatareniet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatareniet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatarpriet5.channels.xml'):
    print('Downloading qatarpriet5 channels config')
    sys.stdout.flush()
    qatarpriet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/qatarpriet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/qatarpriet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatarpriet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uae1iet5.channels.xml'):
    print('Downloading uae1iet5 channels config')
    sys.stdout.flush()
    uae1iet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uae1iet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uae1iet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uae1iet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/elcinema.channels.xml', 'w', encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/bein.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/bein.channels.xml', 'w', encoding="utf-8") as f:
        f.write(bein_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/sportiet5.channels.xml'):
    print('Downloading sportiet5 channels config')
    sys.stdout.flush()
    sportiet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/sportiet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/sportiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(sportiet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uaeariet5.channels.xml'):
    print('Downloading uaeariet5 channels config')
    sys.stdout.flush()
    uaeariet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uaeariet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uaeariet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uaeariet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uaeeniet5.channels.xml'):
    print('Downloading uaeeniet5 channels config')
    sys.stdout.flush()
    uaeeniet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/uaeeniet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/uaeeniet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uaeeniet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/beinsportiet5.channels.xml'):
    print('Downloading beinsportiet5 channels config')
    sys.stdout.flush()
    beinsportiet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/beinsportiet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/beinsportiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(beinsportiet5_channels.text)
