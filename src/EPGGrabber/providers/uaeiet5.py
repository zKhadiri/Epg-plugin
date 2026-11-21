#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script created by iet5
#
from __future__ import print_function, unicode_literals

import os
import io
import re
import sys
import json
import time
import warnings
import requests
import fileinput
from datetime import datetime, timedelta
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Timezone initialization
# Calculate timezone offset using receiver's local time (Python 2.7 compatible)
is_dst = time.localtime().tm_isdst > 0
utc_offset_seconds = - (time.altzone if is_dst else time.timezone)
offset_hours = utc_offset_seconds // 3600
offset_minutes = (abs(utc_offset_seconds) % 3600) // 60
time_zone = "{0:+03d}{1:02d}".format(offset_hours, offset_minutes)

# Ignore insecure request warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# Constants
try:
    from __init__ import EPG_ROOT, PROVIDERS_ROOT
except ImportError:
    EPG_ROOT = "./"  # Default if __init__ is not available
    PROVIDERS_ROOT = "./providers.json"  # Default if __init__ is not available

# Paths
input_path = os.path.join(EPG_ROOT, 'uae.xml')
output_path = os.path.join(EPG_ROOT, 'out.xml')

# List of changes to apply
List_Chang = [
    # Example: ('old_text', 'new_text'),
    # Add your specific changes here
]

def main():
    # Added code snippet
    print("***************Uae_iet5_EPG*****************")
    sys.stdout.flush()  # Flush after the initial print
    sleep(1)  # Add a 1-second delay
    print("=============================================")
    print("Downloading Uae_iet5 EPG guide...\nPlease wait...")
    sys.stdout.flush()
    try:
        download_start = time.time()
        # Download the XML file
        # Stream the response to avoid buffering the entire EPG in RAM.
        response = requests.get(
            'https://www.open-epg.com/files/uae.xml',
            verify=False,
            timeout=(8, 30),
            stream=True,
            headers={'Accept-Encoding': 'gzip, deflate'}
        )
        if response.status_code == 200:
            # Decode incrementally (also handles a UTF-8 BOM).
            import codecs
            decoder = codecs.getincrementaldecoder('utf-8-sig')()
            with io.open(input_path, 'w', encoding='utf-8') as f:
                for chunk in response.iter_content(chunk_size=256 * 1024):
                    if chunk:
                        f.write(decoder.decode(chunk))
                f.write(decoder.decode(b'', final=True))
                print("============================================")
            response.close()

            # Fetch the number of channels (replace this with your actual logic)
            with io.open(input_path, 'r', encoding="utf-8") as f:
                xml_data = f.read()

            # Count the number of channels
            channel_count = xml_data.count('<channel id="')  # Example: Count channels in XML

            print("There are {0} channels available for EPG data.".format(channel_count))
            print("============================================")
            file_size_mb = os.path.getsize(input_path) / (1024.0 * 1024.0)
            elapsed = time.time() - download_start
            print("uae.xml Downloaded Successfully ({:.2f} MB)".format(file_size_mb))
            print("Download Time : {:.2f} seconds".format(elapsed))
            sys.stdout.flush()  # Flush after printing the channel count
            sleep(1)  # Add a 1-second delay
            # Apply the transformations
            apply_changes()
            # Adjust times in the XML
            adjust_times()
            # Remove duplicate lines
            remove_duplicates()
            # Rename the file
            rename_file()
            # Update providers JSON
            update_providers()
            # Remove specific lines
            remove_specific_lines()
            print('*****************FINISHED*******************')
            sys.stdout.flush()
        else:
            print("Failed to download /uae.xml. Status code: {}".format(response.status_code))
            sys.exit(1)  # Exit if download fails
    except requests.exceptions.RequestException as e:  # Corrected exception syntax
        print("Failed to download /uae.xml: {}".format(e))
        sys.exit(1)  # Exit if an exception occurs during download

def apply_changes():
    for old_text, new_text in List_Chang:
        for line in fileinput.input(input_path, inplace=True):
            if old_text in line:
                line = line.replace(old_text, new_text)
            sys.stdout.write(line)

def adjust_times():
    with io.open(input_path, 'r', encoding="utf-8") as f:
        xml_data = f.read()

    def adjust_time(match, time_type):
        original_time = datetime.strptime(match.group(1), '%Y%m%d%H%M%S')
        sign = 1 if time_zone[0] == '+' else -1
        hours = int(time_zone[1:3])
        minutes = int(time_zone[3:5])
        delta = timedelta(hours=sign*hours, minutes=sign*minutes)
        adjusted_time = original_time + delta
        return '{0}="{1} {2}"'.format(time_type, adjusted_time.strftime('%Y%m%d%H%M%S'), time_zone)

    xml_data = re.sub(
        r'start="(\d{14}) \+0000"',
        lambda m: adjust_time(m, 'start'),
        xml_data
    )
    xml_data = re.sub(
        r'stop="(\d{14}) \+0000"',
        lambda m: adjust_time(m, 'stop'),
        xml_data
    )

    with io.open(input_path, 'w', encoding="utf-8") as f:
        f.write(xml_data)

def remove_duplicates():
    # Preserve XML structure: repeated lines can be valid XMLTV elements.
    # Keep output_path for the existing rename_file() workflow.
    with open(input_path, 'rb') as source:
        with open(output_path, 'wb') as destination:
            while True:
                chunk = source.read(256 * 1024)
                if not chunk:
                    break
                destination.write(chunk)

def rename_file():
    os.remove(input_path)
    os.rename(output_path, input_path)
    print("============================================")
    print("Time_zone is set to {}".format(time_zone))
    print("============================================")

def update_providers():
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"] == "uaeiet5":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f, indent=4)

# Remove lines containing specified data and empty lines
def remove_specific_lines():
    # Remove only the unwanted XML elements, not the entire line.
    with io.open(input_path, 'r', encoding='utf-8') as f:
        xml_data = f.read()
    xml_data = re.sub(r'<icon\b[^>]*/>', '', xml_data)
    xml_data = re.sub(r'<url\b[^>]*>.*?</url\s*>', '', xml_data, flags=re.DOTALL)
    xml_data = re.sub(r'<category\b[^>]*>.*?</category\s*>', '', xml_data, flags=re.DOTALL)
    xml_data = re.sub(r'(?m)^[ \t]*\r?\n', '', xml_data)
    with io.open(input_path, 'w', encoding='utf-8') as f:
        f.write(xml_data)

def change_data_list(old_text, new_text, file_path):
    for line in fileinput.input(file_path, inplace=True):
        if old_text in line:
            line = line.replace(old_text, new_text)
        sys.stdout.write(line)

def change(list_changes):
    for change_expr in list_changes:
        change_data_list(change_expr[0], change_expr[1], input_path)

if __name__ == "__main__":
    main()
    sys.stdout.flush()