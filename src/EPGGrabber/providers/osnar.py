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

path = EPG_ROOT + '/osnplay.xml'


print("Downloading OSN arabic epg guide\nPlease wait....")
sys.stdout.flush()
url = requests.get('http://raw.githubusercontent.com/Haxer/EPG-XMLFiles/FullArabicXML/osn.xml')
with io.open(path, 'w', encoding="utf-8") as f:
    f.write(url.text)

print("osnplay.xml donwloaded with succes")

from datetime import datetime
with open(PROVIDERS_ROOT, 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"] == "osnar":
        channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open(PROVIDERS_ROOT, 'w') as f:
    json.dump(data, f)
