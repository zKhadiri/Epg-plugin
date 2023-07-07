#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import requests
import os
import io
import re
import sys
import json
try:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT
except:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT

import xml.etree.ElementTree as ET
import subprocess

# Ignore insecure request warnings
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

path = EPG_ROOT + '/arabia.xml'

print('**************El_Cinma_iet5 EPG******************')
sys.stdout.flush()
print("Downloading El_Cinma_iet5 EPG guide\nPlease wait....")
sys.stdout.flush()

try:
    response = requests.get('https://www.bevy.be/bevyfiles/arabia.xml', verify=False)
    if response.status_code == 200:
        with io.open(path, 'w', encoding="utf-8") as f:
            f.write(response.text) 
        print("################################")
        print("                                                        ")
        print("Arabia.xml Downloaded Successfully")
        print("                                                        ")
        print("################################")

    else:
        print("Failed to download /arabia.xml. Status code:", response.status_code)

    from datetime import datetime
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"] == "elcinmaiet5":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    print('**************FINISHED******************')
    sys.stdout.flush()

except requests.exceptions.RequestException as e:
    print("Failed to download /arabia.xml:", e)