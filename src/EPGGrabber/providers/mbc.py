#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import warnings
warnings.simplefilter("ignore")

try:
    from .__init__ import *
except:
    from __init__ import *
import requests
import re
import io
import threading
import sys
import os
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
import time
from time import sleep, strftime
import json
if sys.version_info[0] < 3:
    import codecs
    open = codecs.open

EPG_ROOT = "/etc/epgimport/ziko_epg"
time_zone = "+0000"
head = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://api3.shahid.net/"
}
BASE_URL = "https://api3.shahid.net/proxy/v2.1/editorial/carousel?request=%7B%22pageNumber%22:{},%22pageSize%22:100,%22id%22:%22Main%2FEGYPT%2Flivestream%2FEGY-Crm-live-channels%22%7D&country=EG"

def extract_channel_name(product_urls):
    for priority in ["/en/livestream/", "/livestream/"]:
        name = next((re.search(r"/livestream/([^/]+)/", url["url"]).group(1).replace("-", " ").title()
                     for url in product_urls if priority in url["url"]), None)
        if name:
            return name
    return None

def fetch_channels():
    channels_code = []
    for page in range(3):
        try:
            response = requests.get(BASE_URL.format(page), timeout=(5, 10))
            if response.status_code == 200:
                for item in response.json().get("editorialItems", []):
                    channel_id = str(item["item"]["id"])
                    channel_name = extract_channel_name(item["item"].get("productUrls", []))
                    if channel_name:
                        channels_code.append((channel_name, "{}-{}".format(channel_id, channel_name)))
            else:
                print("Failed to fetch data from page {} - Status code: {}".format(page, response.status_code))
        except Exception as e:
            print("Error fetching page {}: {}".format(page, e))
    return [code for _, code in sorted(channels_code)]

channels_code = fetch_channels()
lock = threading.Semaphore(20)

def xml_header(path, channels):
    with io.open(path, 'w', encoding='utf-8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<tv generator-info-name="By ZR1">')
    for channel in channels:
        display_name = channel.replace(" Channel", "").replace(" channel", "")
        with io.open(path, "a", encoding='utf-8') as f:
            f.write("\n  <channel id=\"{}\"><display-name lang=\"en\">{}</display-name></channel>\r".format(channel, display_name))

def close_xml(path):
    with io.open(path, 'a', encoding='utf-8') as file:
        file.write('</tv>')

def mbc_epg(code):
    try:
        lock.acquire()
        channel_id, channel_name = code.split('-', 1)
        channel_name = channel_name.replace(" Channel", "").replace(" channel", "")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_date = today.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        to_date = (today + timedelta(days=6)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=5))
            retries = 3
            for attempt in range(retries):
                try:
                    url = s.get(
                        'https://api3.shahid.net/proxy/v2.1/shahid-epg-api/', params={ "language": "ar", "from": from_date, "to": to_date, "csvChannelIds": channel_id, "country": "EG"},
                        headers=head, timeout=5
                    )
                    if url.status_code == 200:
                        break
                    else:
                        print("Attempt {} failed for {}. Status code: {}".format(attempt + 1, channel_name, url.status_code))
                        sys.stdout.flush()
                        time.sleep(5)
                except Exception as e:
                    time.sleep(5)
            if url.status_code != 200:
                print("Failed to fetch data for {} (ID: {}). Status code: {}".format(channel_name, channel_id, url.status_code))
                return
            try:
                data = url.json()
            except ValueError as e:
                print("Invalid JSON response for {}: {}".format(channel_name, e))
                return
            channels_data = {ch['channelId']: ch for ch in data.get('items', [])}
            if channel_id in channels_data:
                if not channels_data[channel_id].get('items'):
                    print("No EPG data found for: {}".format(channel_name))
                    return
                programs = sorted(channels_data[channel_id].get('items', []), key=lambda x: x.get('from', ''))
                for program in programs:
                    title = (program.get('title') or 'No Title').strip()
                    start_time = (program.get('from') or '').strip()
                    end_time = (program.get('to') or '').strip()
                    description = (program.get('description') or 'No Description').strip()
                    try:
                        start = datetime.strptime(start_time.replace('Z', '').split('+')[0], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y%m%d%H%M%S')
                        end = datetime.strptime(end_time.replace('Z', '').split('+')[0], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y%m%d%H%M%S')
                    except Exception as e:
                        print("Error parsing date for {}: {}".format(channel_name, e))
                        continue
                    ch = '  <programme start="{} {}" stop="{} {}" channel="{}">\n'.format(start, time_zone, end, time_zone, channel_name)
                    ch += '    <title lang="ar">{}</title>\n'.format(title.replace('&', 'and'))
                    ch += '    <desc lang="ar">{}</desc>\n  </programme>\n'.format(description.replace('&', 'and'))
                    with io.open(EPG_ROOT + '/mbc.xml', "a", encoding='UTF-8') as f:
                        f.write(ch)
                print("{} epg ends at: {}".format(channel_name, datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')))
                sys.stdout.flush()
    except Exception as e:
        print("Error in mbc_epg function for {}: {}".format(code, e))
        sys.stdout.flush()
    finally:
        lock.release()

def sort_xml_by_channel_and_time(xml_file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_file)
    root = tree.getroot()
    programmes = root.findall('programme')
    programmes_sorted = sorted(programmes, key=lambda x: (x.attrib['channel'], x.attrib['start']))
    for programme in programmes:
        root.remove(programme)
    for programme in programmes_sorted:
        root.append(programme)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

def main():
    print('*******************MBC_EPG***********************')
    sys.stdout.flush()
    print("=================================================")
    print("Time_zone is set to {}".format(time_zone))
    print("=================================================")
    print("=================================================")
    print("There are {} channels available for EPG data.".format(len(channels_code)))
    print("=================================================")
    sys.stdout.flush()

    # Generate XML header
    xml_header(EPG_ROOT + '/mbc.xml', [ch.split('-')[1] for ch in channels_code])

    # Fetch EPG data for each channel
    thread_pool = []
    for code in channels_code:
        thread = threading.Thread(target=mbc_epg, args=(code,))
        thread_pool.append(thread)
        thread.start()
        sleep(1)
    for thread in thread_pool:
        thread.join()

    # Close XML file
    close_xml(EPG_ROOT + '/mbc.xml')

    # Sort XML file (if Dream OS is detected)
    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream OS image found\nSorting data please wait.....')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/mbc.xml')
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_ROOT + '/mbc.xml', xml_declaration=True, encoding='utf-8')
        sort_xml_by_channel_and_time(EPG_ROOT + '/mbc.xml')

    print('**************FINISHED******************')
    sys.stdout.flush()

def update_providers_json(success):
    try:
        providers_path = "/usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/api/providers.json"
        
        # Read existing data
        if sys.version_info[0] < 3:
            with codecs.open(providers_path, 'r', encoding='utf-8') as f:
                raw_data = f.read()
        else:
            with open(providers_path, 'r', encoding='utf-8') as f:
                raw_data = f.read()

        # Parse JSON data
        try:
            data = json.loads(raw_data)
        except:
            data = []

        current_date = datetime.now().strftime("%A %d %B %Y at %I:%M %p") if success else "You didn't download from this source yet"

        def deep_update(item):
            if isinstance(item, list):
                for element in item:
                    if isinstance(element, dict) and element.get('bouquet', '').lower() == 'mbc':
                        element['date'] = current_date
                        return True
                    elif deep_update(element):
                        return True
                return False
            elif isinstance(item, dict):
                for key in ['providers', 'entries', 'data']:
                    if key in item and deep_update(item[key]):
                        return True
                for val in item.values():
                    if deep_update(val):
                        return True
                return False
            return False

        updated = deep_update(data)

        if sys.version_info[0] < 3:
            with codecs.open(providers_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            with open(providers_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Error updating providers.json: {}".format(e))

if __name__ == "__main__":
    success = False
    try:
        main()
        success = True
    except Exception as e:
        print("EPG generation failed: {}".format(str(e)))
        success = False
    finally:
        update_providers_json(success)