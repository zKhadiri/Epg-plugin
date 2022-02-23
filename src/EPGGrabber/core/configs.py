#!/usr/bin/python
# -*- coding: utf-8 -*-


from Plugins.Extensions.EPGGrabber.core.compat import PY3
from Plugins.Extensions.EPGGrabber.core.paths import BOUQUETS_ROOT
import requests
import sys
import io

print('Downloading custom.sources config')
sys.stdout.flush()
custom_channels = requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.sources.xml?raw=true')
with io.open('/etc/epgimport/custom.sources.xml', 'w', encoding="utf-8") as f:
    f.write(custom_channels.text)

print('Downloading latest channels list')
sys.stdout.flush()
chnnales_lists = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/src/EPGGrabber/api/bouquets.json')
with io.open(BOUQUETS_ROOT, 'w', encoding="utf-8") as f:
    f.write(chnnales_lists.text)
