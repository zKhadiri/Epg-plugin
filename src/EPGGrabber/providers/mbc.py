#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import warnings
warnings.simplefilter("ignore")

try:
    from .__init__ import *
except:
    try:
        from __init__ import *
    except:
        pass

import requests
import re
import io
import threading
import sys
import os
import glob
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
import time
from time import sleep, strftime
import json
import calendar

if sys.version_info[0] < 3:
    import codecs
    open = codecs.open


EPG_ROOT = "/etc/epgimport/ziko_epg"
CONFIG_ROOT = "/etc/epgimport/ziko_config"
EPG_FILE = EPG_ROOT + "/mbc.xml"
CHANNELS_FILE = CONFIG_ROOT + "/mbc.channels.xml"
SOURCES_FILE = CONFIG_ROOT + "/mbc.sources.xml"
country = os.environ.get("MBC_COUNTRY", "EG").strip().upper() or "EG"


def format_offset(seconds):
    sign = "+" if seconds >= 0 else "-"
    seconds = abs(int(seconds))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return "{}{:02d}{:02d}".format(sign, hours, minutes)


def receiver_offset():
    # Read the standard timezone selected on the receiver.
    # DST is intentionally ignored.
    try:
        if hasattr(time, "tzset"):
            time.tzset()
    except:
        pass

    try:
        return -int(time.timezone)
    except:
        return 0


time_zone = format_offset(receiver_offset())

head = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Linux; Enigma2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Accept-Language": "ar,en;q=0.8",
    "Referer": "https://shahid.mbc.net/"
}

EPG_URLS = [
    "https://api3.shahid.net/proxy/v2.1/shahid-epg-api/",
    "https://api2.shahid.net/proxy/v2.1/shahid-epg-api/",
    "https://api2.shahid.net/proxy/v2/shahid-epg-api/"
]

# name, Shahid ids, common bouquet names
MBC_CHANNELS = [
    # MBC
    ("MBC1", ["387238"], ["MBC1", "MBC 1", "MBC1 HD", "MBC 1 HD", "MBC1 SD", "MBC 1 SD", "MBC"]),
    ("MBC2", ["400917"], ["MBC2", "MBC 2", "MBC2 HD", "MBC 2 HD", "MBC2 SD", "MBC 2 SD"]),
    ("MBC3", ["816771", "409385"], ["MBC3", "MBC 3", "MBC3 HD", "MBC 3 HD", "MBC3 SD", "MBC 3 SD"]),
    ("MBC4", ["400919"], ["MBC4", "MBC 4", "MBC4 HD", "MBC 4 HD", "MBC4 SD", "MBC 4 SD"]),
    ("MBC5", ["387937"], ["MBC5", "MBC 5", "MBC5 HD", "MBC 5 HD"]),
    ("MBC Action", ["400921"], ["MBC ACTION", "MBC ACTION HD", "MBC ACTION SD", "Mbc Action"]),
    ("MBC Bollywood", ["409387"], ["MBC BOLLYWOOD", "MBC BOLLYWOOD HD", "MBC BOLLYWOOD SD", "Mbc Bollywood"]),
    ("MBC Drama", ["387251", "816781"], ["MBC DRAMA", "MBC DRAMA HD", "MBC DRAMA SD", "Mbc Drama"]),
    ("MBC FM", ["388567"], ["MBC FM", "MBCFM", "Mbc Fm"]),
    ("MBC Iraq", ["387294"], ["MBC IRAQ", "MBC IRAQ HD", "MBC IRAQ SD", "Mbc Iraq"]),
    ("MBC Masr", ["387290", "816776"], ["MBC MASR", "MBC MASR HD", "MBC MASR SD", "MBC EGYPT", "Mbc Masr"]),
    ("MBC Masr 2", ["387293"], ["MBC MASR 2", "MBC MASR2", "MBC MASR 2 HD", "MBC MASR2 HD", "Mbc Masr 2"]),
    ("MBC Masr Drama", ["49923122575716"], ["MBC MASR DRAMA", "MBC MASR DRAMA HD", "Mbc Masr Drama"]),
    ("MBC Max", ["400924"], ["MBC MAX", "MBC MAX HD", "MBC MAX SD", "Mbc Max"]),
    ("MBC Persia", ["418308"], ["MBC PERSIA", "MBC PERSIA HD", "Mbc Persia"]),
    ("MBC+ Drama", ["387296"], ["MBC+ DRAMA", "MBC + DRAMA", "MBC PLUS DRAMA", "MBC DRAMA +", "Mbc Plus Drama"]),
    ("MBC Mood", ["49923890387395"], ["MBC MOOD", "MBC MOOD HD", "MBC MOOD SD"]),

    # Shahid / MBC live channels
    ("Abdul Majeed Abdullah", ["986014"], ["ABDUL MAJEED ABDULLAH"]),
    ("Aflam", ["989622"], ["AFLAM"]),
    ("Al Arabiya", ["387286"], ["AL ARABIYA"]),
    ("Al Arabiya Business", ["1003218"], ["AL ARABIYA BUSINESS"]),
    ("Al Asouf", ["977946"], ["AL ASOUF", "AL ASOUF CHANNEL"]),
    ("Al Hadath", ["387288"], ["AL HADATH"]),
    ("Al Quraan Al Kareem", ["946946"], ["AL QURAAN AL KAREEM", "AL QURAAN AL KAREEM HD"]),
    ("Al Sunnah Al Nabawiyah", ["946942"], ["AL SUNNAH AL NABAWIYAH", "AL SUNNAH AL NABAWIYAH HD"]),
    ("Alikhbariya", ["946948"], ["ALIKHBARIYA", "ALEKHBARIYA"]),
    ("Alkhuzama Radio", ["1029746"], ["ALKHUZAMA RADIO"]),
    ("Alsaudia", ["946938"], ["ALSAUDIA", "AL SAUDIA"]),
    ("Asharq", ["862837"], ["ASHARQ"]),
    ("Asharq Discovery", ["1001845"], ["ASHARQ DISCOVERY"]),
    ("Asharq Documentary", ["997605"], ["ASHARQ DOCUMENTARY"]),
    ("Bab Al Hara", ["975435"], ["BAB AL HARA", "BAB AL HARA CHANNEL"]),
    ("Big Time", ["951783"], ["BIG TIME"]),
    ("Big Time Plus", ["49922904934759"], ["BIG TIME PLUS"]),
    ("El Le'Ba", ["992538"], ["EL LE'BA", "EL LE'BA CHANNEL", "EL LEABA"]),
    ("Freej", ["49923088814140"], ["FREEJ", "FREEJ CHANNEL"]),
    ("Ksa Now", ["999927"], ["KSA NOW"]),
    ("Majid Almohandis", ["49922763891977"], ["MAJID ALMOHANDIS"]),
    ("Maraya", ["988045"], ["MARAYA", "MARAYA CHANNEL"]),
    ("Masrah Masr", ["983124"], ["MASRAH MASR", "MASRAH MASR CHANNEL"]),
    ("Mohammed Abdu", ["986346"], ["MOHAMMED ABDU", "MOHAMMAD ABDU"]),
    ("Movies Thriller", ["986069"], ["MOVIES THRILLER"]),
    ("Nasser Al Qassabi", ["969745"], ["NASSER AL QASSABI"]),
    ("Panorama FM", ["388566"], ["PANORAMA FM", "Panorama Fm"]),
    ("Ramez", ["49923088781412"], ["RAMEZ"]),
    ("Rashed Al Majed", ["986024"], ["RASHED AL MAJED"]),
    ("SBC", ["946940"], ["SBC", "Sbc"]),
    ("Seen Channel", ["49923088717401"], ["SEEN CHANNEL"]),
    ("Selfie Channel", ["1005232"], ["SELFIE CHANNEL"]),
    ("Spacetoon", ["409390"], ["SPACETOON", "SPACE TOON"]),
    ("SSC News", ["955107"], ["SSC NEWS", "Ssc News"]),
    ("Tarab", ["49922763510387"], ["TARAB"]),
    ("Tash Channel", ["963543"], ["TASH", "TASH CHANNEL"]),
    ("Thikrayat", ["946945"], ["THIKRAYAT", "Thikrayat"]),
    ("Wanasa", ["414449"], ["WANASA", "WANASAH", "Wanasa"]),

    # Old names with no current livechannel id confirmed yet.
    # They are deliberately ignored until a working id is found.
    # Al Sadma
    # Arabs Got Talent Channel
    # Bedaya Tv
    # Gulf Comedy
    # Nature Time
    # Ramadan Ma'Na Gcc
    # Ramadan Ma'Na Series
    # Red Bull Tv
    # Studio Channel
    # Top Chef Channel
]

lock = threading.Semaphore(20)
write_lock = threading.Lock()


def normalize_name(name):
    try:
        name = name.upper()
    except:
        name = str(name).upper()

    name = name.replace("_", " ").replace("-", " ")
    name = name.replace("MBC PLUS", "MBC+").replace("MBC +", "MBC+")
    name = re.sub(r"\b(UHD|FHD|HD|SD|HEVC|4K|H265|H264)\b", " ", name)
    return " ".join(name.split()).strip()


def get_alias_map():
    result = {}
    for name, ids, aliases in MBC_CHANNELS:
        for alias in aliases + [name]:
            result[normalize_name(alias)] = name
    return result


ALIAS_MAP = get_alias_map()


def get_dates(days_count):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = today.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    to_date = (today + timedelta(days=days_count)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return from_date, to_date


def get_epg_data(api_url, channel_id, days_count):
    from_date, to_date = get_dates(days_count)

    try:
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(
                api_url,
                params={
                    "language": "ar",
                    "from": from_date,
                    "to": to_date,
                    "csvChannelIds": channel_id,
                    "country": country
                },
                headers=head,
                timeout=(5, 15)
            )

        if response.status_code == 200:
            try:
                return response.json(), response.status_code
            except:
                return None, response.status_code

        return None, response.status_code

    except:
        return None, 0


def get_programs(data, channel_id):
    if not isinstance(data, dict):
        return []

    for ch in data.get('items', []):
        if str(ch.get('channelId', '')) == str(channel_id):
            return sorted(ch.get('items', []) or [], key=lambda x: x.get('from', ''))

    return []


def find_epg_api():
    test_id = "387238"

    for api_url in EPG_URLS:
        data, status = get_epg_data(api_url, test_id, 2)
        programs = get_programs(data, test_id)

        if status == 200 and programs:
            return api_url

    return None


def extract_channel_name(product_urls):
    # kept for compatibility with the old script
    for priority in ["/en/livestream/", "/livestream/"]:
        name = next((re.search(r"/livestream/([^/]+)/", url["url"]).group(1).replace("-", " ").title()
                     for url in product_urls if priority in url.get("url", "")), None)
        if name:
            return name
    return None


def fetch_channels():
    channels_code = []

    api_url = find_epg_api()
    if not api_url:
        return channels_code

    for channel_name, channel_ids, aliases in MBC_CHANNELS:
        working_id = None

        for channel_id in channel_ids:
            data, status = get_epg_data(api_url, channel_id, 2)
            programs = get_programs(data, channel_id)

            if status == 200 and programs:
                working_id = channel_id
                break

        if working_id:
            channels_code.append("{}-{}".format(working_id, channel_name))

    return channels_code


channels_code = fetch_channels()


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


def parse_date(value):
    value = (value or '').strip()

    if not value:
        raise ValueError("Empty date")

    source_offset = 0
    base = value

    if base.endswith('Z'):
        base = base[:-1]
    else:
        match = re.search(r'([+-])(\d{2}):?(\d{2})$', base)
        if match and match.start() >= 19:
            sign = 1 if match.group(1) == '+' else -1
            source_offset = sign * (
                int(match.group(2)) * 3600 +
                int(match.group(3)) * 60
            )
            base = base[:match.start()]

    formats = [
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S'
    ]

    dt = None

    for fmt in formats:
        try:
            dt = datetime.strptime(base, fmt)
            break
        except:
            pass

    if dt is None:
        raise ValueError("Bad date: {}".format(value))

    epoch = calendar.timegm(dt.timetuple()) - source_offset
    local_offset = receiver_offset()

    # Add the receiver's fixed standard offset ourselves.
    # gmtime is used here so Python does not add DST again.
    local_tm = time.gmtime(epoch + local_offset)

    return (
        time.strftime('%Y%m%d%H%M%S', local_tm),
        format_offset(local_offset)
    )


def mbc_epg(code):
    try:
        lock.acquire()

        channel_id, channel_name = code.split('-', 1)
        channel_name = channel_name.replace(" Channel", "").replace(" channel", "")

        api_url = find_epg_api()
        if not api_url:
            print("Failed to find a working Shahid EPG API")
            return

        retries = 3
        data = None
        status = 0

        for attempt in range(retries):
            data, status = get_epg_data(api_url, channel_id, 6)

            if status == 200:
                break
            else:
                print("Attempt {} failed for {}. Status code: {}".format(attempt + 1, channel_name, status))
                sys.stdout.flush()
                time.sleep(5)

        if status != 200:
            print("Failed to fetch data for {} (ID: {}). Status code: {}".format(channel_name, channel_id, status))
            return

        programs = get_programs(data, channel_id)

        if not programs:
            print("No EPG data found for: {}".format(channel_name))
            return

        end = None

        for program in programs:
            title = (program.get('title') or 'No Title').strip()
            start_time = (program.get('from') or '').strip()
            end_time = (program.get('to') or '').strip()
            description = (program.get('description') or 'No Description').strip()

            try:
                start, start_zone = parse_date(start_time)
                end, end_zone = parse_date(end_time)
            except Exception as e:
                print("Error parsing date for {}: {}".format(channel_name, e))
                continue

            ch = '  <programme start="{} {}" stop="{} {}" channel="{}">\n'.format(
                start, start_zone, end, end_zone, channel_name
            )
            ch += '    <title lang="ar">{}</title>\n'.format(
                title.replace('&', 'and').replace('<', '').replace('>', '')
            )
            ch += '    <desc lang="ar">{}</desc>\n  </programme>\n'.format(
                description.replace('&', 'and').replace('<', '').replace('>', '')
            )

            with write_lock:
                with io.open(EPG_FILE, "a", encoding='UTF-8') as f:
                    f.write(ch)

        if end:
            print("{} epg ends at: {}".format(
                channel_name,
                datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')
            ))
            sys.stdout.flush()

    except Exception as e:
        print("Error in mbc_epg function for {}: {}".format(code, e))
        sys.stdout.flush()

    finally:
        lock.release()


def service_ref(line):
    line = line.replace("#SERVICE", "", 1).strip()
    parts = line.split(":")

    if len(parts) >= 10:
        return ":".join(parts[:10]) + ":"

    return line


def create_channels_file():
    refs = {}
    files = glob.glob("/etc/enigma2/userbouquet*.tv")
    files += glob.glob("/etc/enigma2/userbouquet*.radio")

    for filename in files:
        try:
            with io.open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                current_ref = ""

                for line in f:
                    line = line.strip()

                    if line.startswith("#SERVICE"):
                        current_ref = service_ref(line)

                    elif line.startswith("#DESCRIPTION") and current_ref:
                        name = line.replace("#DESCRIPTION", "", 1).strip()
                        channel_name = ALIAS_MAP.get(normalize_name(name))

                        if channel_name:
                            if channel_name not in refs:
                                refs[channel_name] = []

                            if current_ref not in refs[channel_name]:
                                refs[channel_name].append(current_ref)

        except:
            pass

    try:
        with io.open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<channels>\n')

            for code in channels_code:
                channel_name = code.split('-', 1)[1]

                for ref in refs.get(channel_name, []):
                    f.write('  <channel id="{}">{}</channel>\n'.format(channel_name, ref))

            f.write('</channels>\n')
    except:
        pass


def create_sources_file():
    try:
        with io.open(SOURCES_FILE, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<sources>\n')
            f.write('  <sourcecat sourcecatname="MBC">\n')
            f.write('    <source type="gen_xmltv" nocheck="1" channels=CHANNELS_FILE>\n')
            f.write('      <description>MBC EPG</description>\n')
            f.write('      <url>{}</url>\n'.format(EPG_FILE))
            f.write('    </source>\n')
            f.write('  </sourcecat>\n')
            f.write('</sources>\n')
    except:
        pass


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
    global time_zone
    time_zone = format_offset(receiver_offset())

    print('********** MBC_Shahid_EPG_BY_iet5 ***************')
    sys.stdout.flush()
    print("=================================================")
    print("Time_zone is set to {} (receiver)".format(format_offset(receiver_offset())))
    print("=================================================")
    print("=================================================")
    print("There are {} channels available for EPG data.".format(len(channels_code)))
    print("=================================================")
    sys.stdout.flush()

    for folder in [EPG_ROOT, CONFIG_ROOT]:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                pass

    create_channels_file()
    create_sources_file()

    xml_header(EPG_FILE, [ch.split('-', 1)[1] for ch in channels_code])

    thread_pool = []

    for code in channels_code:
        thread = threading.Thread(target=mbc_epg, args=(code,))
        thread_pool.append(thread)
        thread.start()
        sleep(1)

    for thread in thread_pool:
        thread.join()

    close_xml(EPG_FILE)

    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream OS image found\nSorting data please wait.....')
        sys.stdout.flush()

        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_FILE)
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_FILE, xml_declaration=True, encoding='utf-8')
        sort_xml_by_channel_and_time(EPG_FILE)
    else:
        try:
            sort_xml_by_channel_and_time(EPG_FILE)
        except:
            pass

    print('**************FINISHED******************')
    sys.stdout.flush()


def update_providers_json(success):
    try:
        providers_files = glob.glob("/usr/lib*/enigma2/python/Plugins/Extensions/EPGGrabber/api/providers.json")

        if not providers_files:
            providers_files = [
                "/usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/api/providers.json"
            ]

        for providers_path in providers_files:
            if not os.path.exists(providers_path):
                continue

            if sys.version_info[0] < 3:
                with codecs.open(providers_path, 'r', encoding='utf-8') as f:
                    raw_data = f.read()
            else:
                with open(providers_path, 'r', encoding='utf-8') as f:
                    raw_data = f.read()

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

            deep_update(data)

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