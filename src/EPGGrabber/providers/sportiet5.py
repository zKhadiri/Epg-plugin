#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import re
import sys
import json
import requests
from datetime import datetime, timedelta
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import fileinput

# Ignore insecure request warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Constants
try:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT
except ImportError:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT

# Paths
path = os.path.join(EPG_ROOT, 'arabiapremiumar.xml')
path_1 = os.path.join(EPG_ROOT, 'out.xml')

def main():
    print("*****************Sport_iet5 EPG******************")
    sys.stdout.flush()
    print("Downloading Sport_iet5 EPG guide\nPlease wait....")
    sys.stdout.flush()

    try:
        # Download the XML file
        response = requests.get('https://www.open-epg.com/files/arabiapremiumar.xml', verify=False)
        if response.status_code == 200:
            with io.open(path, 'w', encoding="utf-8") as f:
                f.write(response.text)
            print("##########################################")
            print("arabiapremiumar.xml Downloaded Successfully")
            print("##########################################")

            # Adjust times in the XML
            adjust_times()
            # Remove duplicate lines
            remove_duplicates()
            # Rename the file
            rename_file()

            # Change arabiapremiumar.xml format to elcinema format
            Change_arabiapremiumar_to_elcinema()
            # Update providers JSON
            update_providers()

            print('**************FINISHED******************')
            sys.stdout.flush()
        else:
            print("Failed to download /arabiapremiumar.xml. Status code: {}".format(response.status_code))
    except requests.exceptions.RequestException as e:
        print("Failed to download /arabiapremiumar.xml: {}".format(e))

    # Remove specific lines
    remove_specific_lines()

def adjust_times():
    with io.open(path, 'r', encoding="utf-8") as f:
        xml_data = f.read()

    def adjust_start_time(match):
        original_time = datetime.strptime(match.group(1), '%Y%m%d%H%M%S')
        adjusted_time = original_time + timedelta(hours=3)
        return 'start="{} +0300"'.format(adjusted_time.strftime('%Y%m%d%H%M%S'))

    def adjust_stop_time(match):
        original_time = datetime.strptime(match.group(1), '%Y%m%d%H%M%S')
        adjusted_time = original_time + timedelta(hours=3)
        return 'stop="{} +0300"'.format(adjusted_time.strftime('%Y%m%d%H%M%S'))

    # Adjust the start and stop times
    xml_data = re.sub(r'start="(\d{14}) \+0000"', adjust_start_time, xml_data)
    xml_data = re.sub(r'stop="(\d{14}) \+0000"', adjust_stop_time, xml_data)

    with io.open(path, 'w', encoding="utf-8") as f:
        f.write(xml_data)

def remove_duplicates():
    lines_seen = set()
    with open(path_1, 'w') as output_file:
        for each_line in open(path, 'r'):
            if each_line not in lines_seen:
                output_file.write(each_line)
                lines_seen.add(each_line)

def rename_file():
    os.remove(path)
    os.rename(path_1, path)
    print("Cool .... congratulations your arabiapremiumar.xml file is created - successfully done")
    print("############################################################")
    print("The time is set to +0300, and if your time is different,")
    print("you can modify the sportiet5.py file in the following")
    print("path /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/")
    print("providers/")
    print("############################################################")

def update_providers():
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"] == "sportiet5":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f, indent=4)

# Remove lines containing specified data and empty lines
def remove_specific_lines():
    with open(path, 'r') as f:
        lines = f.readlines()
    with open(path, 'w') as f:
        for line in lines:
            if '<icon src="https://' not in line and '<url>https://' not in line and '<category' not in line and line.strip():
                f.write(line)

def ChangeDataList(Mege, Megerep, fil):
    for line in fileinput.input(fil, inplace=True):
        if Mege in line:
            line = line.replace(Mege, Megerep)
        sys.stdout.write(line)

def Change_arabiapremiumar_to_elcinema():
    List_Chang = [('<channel', '  <channel'), ('<display-name>', '\n    <display-name lang="ar">'), ('<url>', '\n    <url>'), ('</channel>', '\n  </channel>'),
                  ('<programme', '  <programme'), ('<title', '\n    <title'), ('<desc', '\n    <desc'), ('</programme>', '\n  </programme>'), ('<icon', '\n    <icon'),
                  ('<category', '\n    <category')]

    for Exprt in List_Chang:
        ChangeDataList(Exprt[0], Exprt[1], path)

if __name__ == "__main__":
    main()