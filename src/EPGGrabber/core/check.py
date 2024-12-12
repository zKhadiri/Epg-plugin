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

if not os.path.exists('/etc/epgimport/ziko_config/nilesatiet5.channels.xml'):
    print('Downloading nilesatiet5 channels config')
    sys.stdout.flush()
    nilesatiet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/nilesatiet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/nilesatiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(nilesatiet5_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/sportiet5.channels.xml'):
    print('Downloading sportiet5 channels config')
    sys.stdout.flush()
    sportiet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/sportiet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/sportiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(sportiet5_channels.text) 

if not os.path.exists('/etc/epgimport/ziko_config/sporteniet5.channels.xml'):
    print('Downloading sporteniet5 channels config')
    sys.stdout.flush()
    sporteniet5_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/sporteniet5.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/sporteniet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(sporteniet5_channels.text)

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

if not os.path.exists('/etc/epgimport/ziko_config/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/elcinema.channels.xml', 'w', encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/dstv.channels.xml'):
    print('Downloading dstv channels config')
    sys.stdout.flush()
    dstv_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/dstv.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/dstv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/jawwy.channels.xml'):
    print('Downloading jawwy channels config')
    sys.stdout.flush()
    jaw_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/jawwy.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/jawwy.channels.xml', 'w', encoding="utf-8") as f:
        f.write(jaw_channels.text)

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

if not os.path.exists('/etc/epgimport/ziko_config/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/bein.channels.xml?raw=true')
    with io.open('/etc/epgimport/ziko_config/bein.channels.xml', 'w', encoding="utf-8") as f:
        f.write(bein_channels.text)

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