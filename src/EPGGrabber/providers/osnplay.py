#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from time import sleep
import os
import io
import re
import sys
import requests
import json
from __init__ import *

path = EPG_ROOT+'/osnplay.xml'

print('**************OSN backup EPG******************')
sys.stdout.flush()
print ("Downloading OsnPlay epg guide\nPlease wait...." ) 
sys.stdout.flush()
url=requests.get('http://raw.githubusercontent.com/ziko-ZR1/XML/osn/osn.xml')
with io.open(path,'w',encoding="utf-8") as f:
    f.write(url.text)
    
print ("osnplay.xml donwloaded with succes")    

from datetime import datetime
with open(PROVIDERS_ROOT, 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"]=="osnplay":
        channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open(PROVIDERS_ROOT, 'w') as f:
    json.dump(data, f)
    
print('**************FINISHED******************')
sys.stdout.flush()
