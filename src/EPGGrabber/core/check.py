#!/usr/bin/python
# -*- coding: utf-8 -*-

from Plugins.Extensions.EPGGrabber.core.compat import PY3

import os
import io
import requests
import sys

# General configuration

if not os.path.exists('/etc/epgimport/ziko_config/custom.channels.xml'):
    print('Downloading custom.channels config')
    sys.stdout.flush()
    custom_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/custom.channels.xml', timeout=30)
    custom_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/custom.channels.xml', 'w', encoding="utf-8") as f:
        f.write(custom_channels.text)

if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    sys.stdout.flush()
    custom_source = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/custom.sources.xml', timeout=30)
    custom_source.raise_for_status()
    with io.open('/etc/epgimport/custom.sources.xml', 'w', encoding="utf-8") as f:
        f.write(custom_source.text)

# Countries

if not os.path.exists('/etc/epgimport/ziko_config/egyptiet5.channels.xml'):
    print('Downloading egyptiet5 channels config')
    sys.stdout.flush()
    egyptiet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/egyptiet5.channels.xml', timeout=30)
    egyptiet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/egyptiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(egyptiet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/moroccoiet5.channels.xml'):
    print('Downloading moroccoiet5 channels config')
    sys.stdout.flush()
    moroccoiet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/moroccoiet5.channels.xml', timeout=30)
    moroccoiet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/moroccoiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(moroccoiet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/palestineiet5.channels.xml'):
    print('Downloading palestineiet5 channels config')
    sys.stdout.flush()
    palestineiet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/palestineiet5.channels.xml', timeout=30)
    palestineiet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/palestineiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(palestineiet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/qatariet5.channels.xml'):
    print('Downloading qatariet5 channels config')
    sys.stdout.flush()
    qatariet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/qatariet5.channels.xml', timeout=30)
    qatariet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/qatariet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(qatariet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/saudiarabiaiet5.channels.xml'):
    print('Downloading saudiarabiaiet5 channels config')
    sys.stdout.flush()
    saudiarabiaiet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/saudiarabiaiet5.channels.xml', timeout=30)
    saudiarabiaiet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/saudiarabiaiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(saudiarabiaiet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/uaeiet5.channels.xml'):
    print('Downloading uaeiet5 channels config')
    sys.stdout.flush()
    uaeiet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/uaeiet5.channels.xml', timeout=30)
    uaeiet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/uaeiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(uaeiet5_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/polandiet5.channels.xml'):
    print('Downloading polandiet5 channels config')
    sys.stdout.flush()
    polandiet5_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/polandiet5.channels.xml', timeout=30)
    polandiet5_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/polandiet5.channels.xml', 'w', encoding="utf-8") as f:
        f.write(polandiet5_channels.text)

# Providers and channel sources

if not os.path.exists('/etc/epgimport/ziko_config/aljazeera.channels.xml'):
    print('Downloading aljazeera channels config')
    sys.stdout.flush()
    aljazeera_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/aljazeera.channels.xml', timeout=30)
    aljazeera_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/aljazeera.channels.xml', 'w', encoding="utf-8") as f:
        f.write(aljazeera_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/bein.channels.xml', timeout=30)
    bein_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/bein.channels.xml', 'w', encoding="utf-8") as f:
        f.write(bein_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/discovery.channels.xml'):
    print('Downloading discovery.channels config')
    sys.stdout.flush()
    discovery_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/discovery.channels.xml', timeout=30)
    discovery_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/discovery.channels.xml', 'w', encoding="utf-8") as f:
        f.write(discovery_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/dstv.channels.xml'):
    print('Downloading dstv channels config')
    sys.stdout.flush()
    dstv_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/dstv.channels.xml', timeout=30)
    dstv_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/dstv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/elcinema.channels.xml', timeout=30)
    elcinema_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/elcinema.channels.xml', 'w', encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/freesat.channels.xml'):
    print('Downloading freesat channels config')
    sys.stdout.flush()
    free_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/freesat.channels.xml', timeout=30)
    free_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/freesat.channels.xml', 'w', encoding="utf-8") as f:
        f.write(free_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/mbc.channels.xml'):
    print('Downloading mbc channels config')
    sys.stdout.flush()
    mbc_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/mbc.channels.xml', timeout=30)
    mbc_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/mbc.channels.xml', 'w', encoding="utf-8") as f:
        f.write(mbc_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/osnar.channels.xml'):
    print('Downloading osnar.channels config')
    sys.stdout.flush()
    osnar_channels = requests.get(
        'https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/osnar.channels.xml', timeout=30)
    osnar_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/osnar.channels.xml', 'w', encoding="utf-8") as f:
        f.write(osnar_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/osnen.channels.xml'):
    print('Downloading osnen.channels config')
    sys.stdout.flush()
    osnen_channels = requests.get(
        'https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/osnen.channels.xml', timeout=30)
    osnen_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/osnen.channels.xml', 'w', encoding="utf-8") as f:
        f.write(osnen_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/rotana.channels.xml'):
    print('Downloading rotana channels config')
    sys.stdout.flush()
    free_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/rotana.channels.xml', timeout=30)
    free_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/rotana.channels.xml', 'w', encoding="utf-8") as f:
        f.write(free_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/satTv.channels.xml'):
    print('Downloading satTv.channels config')
    sys.stdout.flush()
    satTv_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/satTv.channels.xml', timeout=30)
    satTv_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/satTv.channels.xml', 'w', encoding="utf-8") as f:
        f.write(satTv_channels.text)

if not os.path.exists('/etc/epgimport/ziko_config/skyit.channels.xml'):
    print('Downloading skyit channels config')
    sys.stdout.flush()
    sky_it = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/skyit.channels.xml', timeout=30)
    sky_it.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/skyit.channels.xml', 'w', encoding="utf-8") as f:
        f.write(sky_it.text)

if not os.path.exists('/etc/epgimport/ziko_config/snrt.channels.xml'):
    print('Downloading Snrt.channels config')
    sys.stdout.flush()
    snrt_channels = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/configs/snrt.channels.xml', timeout=30)
    snrt_channels.raise_for_status()
    with io.open('/etc/epgimport/ziko_config/snrt.channels.xml', 'w', encoding="utf-8") as f:
        f.write(snrt_channels.text)
