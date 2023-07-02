#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from time import sleep
import os
import io
import re
import sys
import requests
import json
try:
    from .__init__ import *
except:
    from __init__ import *

import xml.etree.ElementTree as ET
import subprocess

path = EPG_ROOT + '/Bebawy6.xml'

print('**************Bebawy6 Arabic EPG******************')
sys.stdout.flush()
print("Downloading Bebawy6 EPG guide\nPlease wait....")
sys.stdout.flush()
url = requests.get('https://raw.githubusercontent.com/bebawy6/EPG/master/arEPG.xml')
with io.open(path, 'w', encoding="utf-8") as f:
    f.write(url.text)

print("bebawy6.xml downloaded successfully")

from datetime import datetime
with open(PROVIDERS_ROOT, 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"] == "Bebawy6":
        channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open(PROVIDERS_ROOT, 'w') as f:
    json.dump(data, f)


print('**************FINISHED******************')
sys.stdout.flush()
