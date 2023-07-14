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
path_1 = EPG_ROOT + '/out.xml'
print('**************El_Cinma_iet5 EPG******************')
sys.stdout.flush()
print("Downloading El_Cinma_iet5 EPG guide\nPlease wait....")
sys.stdout.flush()
def Suprim_fil_renom_fil():
    os.remove(path)
    old_name = path_1
    new_name = path
    os.rename(old_name, new_name)
    print(" Cool .... congratulations your arabia.xml")
    print(" file is created -  successfully done     ")
    print("                                          ")
    print("############################################################")   
    print("The time is set to +0200, and if your time is different,    ")
    print("you can modify the elcinmaiet5.py file in the following     ")
    print("path /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/ ")       
    print("providers/                                                  ")    
    print("############################################################")  
    
def Suprim_Doubl():
    lines_seen = set()
    with open(path_1, 'w') as output_file:
        for each_line in open(path, 'r'):
            if each_line not in lines_seen:
                output_file.write(each_line)
                lines_seen.add(each_line)
try:
    response = requests.get('https://www.bevy.be/bevyfiles/arabia.xml', verify=False)
    if response.status_code == 200:
        with io.open(path, 'w', encoding="utf-8") as f:
            f.write(response.text)
        print("##########################################")
        print("                                          ")
        print("Arabia.xml Downloaded Successfully        ")
        print("                                          ")
        print("##########################################")

        import fileinput,sys
        def ChangeDataList(Mege, Megerep, fil):
            Mege = Mege
            Megerep = Megerep
            for line in fileinput.input(path_1, inplace=1):
                if Mege in line:
                    line = line.replace(Mege, Megerep)
                sys.stdout.write(line)
        def Change_arabia_to_elcinema():
            List_Chang = [('<channel','  <channel'),('<display-name>','\n    <display-name lang="ar">'),('<url>','\n    <url>'),('</channel>','\n  </channel>'),
                      ('<programme','  <programme'),('<title','\n    <title'),('<desc','\n    <desc'),('</programme>','\n  </programme>'),('<icon','\n    <icon'),
                      ('<category','\n    <category')]

            for Exprt in List_Chang:
                ChangeDataList(Exprt[0],Exprt[1],'arabia.xml')
        #Change_arabia_to_elcinema()
    else:
        print("Failed to download /arabia.xml. Status code:", response.status_code)
    from datetime import datetime, timedelta
    with io.open(path, 'r', encoding="utf-8") as f:
        xml_data = f.read()
    # Convert the start and stop times to datetime objects and adjust the timezone from +0000 to your desired timezone
    start_time = datetime.strptime(re.search(r'start="(\d{14}) \+0000"', xml_data).group(1), '%Y%m%d%H%M%S') + timedelta(hours=2)
    stop_time = datetime.strptime(re.search(r'stop="(\d{14}) \+0000"', xml_data).group(1), '%Y%m%d%H%M%S') + timedelta(hours=2)
    # Replace the timezone from +0000 to your desired timezone
    xml_data = re.sub(r' \+0000"', ' +0200"', xml_data)
    with io.open(path, 'w', encoding="utf-8") as f:
        f.write(xml_data)
    Suprim_Doubl()
    print("Please wait....out.xml Deletion fil")
    sleep(5)
    Change_arabia_to_elcinema()
    print("Please wait.... rename the file")
    sleep(5)
    Suprim_fil_renom_fil()
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
# Remove lines containing specified data and empty lines
with open(path, 'r') as f:
    lines = f.readlines()
with open(path, 'w') as f:
    for line in lines:
        if '<icon src="https://' not in line and '<url>https://' not in line and line and '<category' not in line and line.strip():
            f.write(line)