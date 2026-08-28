#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    from .__init__ import *
except Exception:
    try:
        from __init__ import *
    except Exception:
        EPG_ROOT = '/etc/epgimport/ziko_epg'
        PROVIDERS_ROOT = '/etc/epgimport/ziko_epg/providers.json'

import io
import json
import os
import sys
import time
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

import requests

try:
    from multiprocessing.dummy import Pool as ThreadPool
except Exception:
    ThreadPool = None

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


# =========================================================
# OSN English EPG grabber - By iet5
# =========================================================
BASE_URL = 'https://www.osn.com'
API_BASE = BASE_URL + '/api/TVScheduleWebService.asmx'
TV_GUIDE_URL = BASE_URL + '/en-eg/watch/tv-schedule'

COUNTRY_CODE = 'AE'
CULTURE = 'en-AE'
DAYS_TO_GRAB = 7
REQUEST_TIMEOUT = 15
MAX_RETRIES = 2
DETAIL_WORKERS = 3
FETCH_DETAILS = True
SLEEP_BETWEEN_CHANNELS = 0.02
DETAILS_CACHE = {}

try:
    xml_file = os.path.join(EPG_ROOT, 'osnen.xml')
except Exception:
    xml_file = '/etc/epgimport/ziko_epg/osnen.xml'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': TV_GUIDE_URL,
    'X-Requested-With': 'XMLHttpRequest',
    'Accept-Language': 'en-EG,en;q=1.0',
    'Connection': 'keep-alive',
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

CHANNELS = [('OTO', 'OSNtv One'),
 ('OFH', 'OSNtv Showcase'),
 ('OM1', 'OSNtv Movies Premiere'),
 ('POP', 'OSNtv Pop Up'),
 ('AHD', 'OSNtv Movies Action'),
 ('OFM', 'OSNtv Movies Family'),
 ('OPR', 'OSNtv Movies Hollywood'),
 ('OMC', 'OSNtv Movies Comedy'),
 ('OCM', 'OSNtv Movies Horror'),
 ('OST', 'OSNtv Showcase Classics'),
 ('OBG', 'OSNtv Crime'),
 ('OLH', 'OSNtv Now'),
 ('OCO', 'OSNtv Comedy'),
 ('OMZ', 'OSNtv Mezze'),
 ('FTF', 'Fatafeat'),
 ('TLC', 'TLC HD'),
 ('OYH', 'OSNtv Yahala'),
 ('OYA', 'OSNtv Yahala Bil Arabi'),
 ('OYC', 'OSNtv Yahala Aflam'),
 ('OIQ', 'OSNtv iQIYI'),
 ('OMK', 'OSNtv Kids'),
 ('NIC', 'Nickelodeon HD'),
 ('NKT', 'NickToons HD'),
 ('NJR', 'Nick Jr HD'),
 ('TCN', 'Cartoon Network HD'),
 ('MBU', 'Moonbug Kids'),
 ('BAF', 'Blippi and Friends'),
 ('DSC', 'Discovery Channel HD'),
 ('DCX', 'Discovery IDX HD'),
 ('HIS', 'History HD'),
 ('HI2', 'H2 HD'),
 ('CAI', 'C & I'),
 ('APL', 'Animal Planet HD'),
 ('CNN', 'CNN HD'),
 ('BTV', 'Bloomberg'),
 ('BLO', 'Bloomberg Originals'),
 ('MCM', 'MCM TOP'),
 ('RFM', 'RFM TV'),
 ('MOT', 'MOTORVISION'),
 ('PDT', 'Padel TV'),
 ('ECL', 'eClutch LIVE'),
 ('EC2', 'eClutch LIVE 2'),
 ('ELA', 'eClutch Arabic'),
 ('ECA', 'eClutch Access'),
 ('ES2', 'Esport 24'),
 ('GMT', 'Gametoon'),
 ('GNX', 'Ginx'),
 ('DOC', 'OSNtv Documentary')]

ALIASES = {'Animal Planet': 'Animal Planet HD',
 'Bloomberg Originals HD': 'Bloomberg Originals',
 'CNN': 'CNN HD',
 'Cartoon Network': 'Cartoon Network HD',
 'Crime & Investigation Network': 'C & I',
 'Discovery HD': 'Discovery Channel HD',
 'Discovery ID': 'Discovery IDX HD',
 'MCM Top': 'MCM TOP',
 'Motorvision': 'MOTORVISION',
 'Nick Jr': 'Nick Jr HD',
 'OSN TV Documentary': 'OSNtv Documentary',
 'OSNtv Iqiyi': 'OSNtv iQIYI',
 'OSNtv Pop up': 'OSNtv Pop Up',
 'Padeltime': 'Padel TV',
 'eClutch LIVE 1': 'eClutch LIVE'}
CODE_TO_NAME = dict(CHANNELS)
TARGET_NAMES = [name for code, name in CHANNELS]


def cprint(text):
    try:
        print('\033[31m' + text + '\033[m')
    except Exception:
        print(text)


def clean_text(value):
    if value is None:
        return ''
    if not isinstance(value, string_types):
        try:
            value = str(value)
        except Exception:
            return ''
    return value.replace('\\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()


def first_value(data, keys, default=''):
    if not isinstance(data, dict):
        return default
    for key in keys:
        value = data.get(key)
        if value not in (None, ''):
            return value
    return default


def normalize_name(value):
    value = clean_text(value)
    try:
        for char in (u'\xa0', u'\u200b', u'\u200c', u'\u200d', u'\ufeff'):
            value = value.replace(char, u' ' if char == u'\xa0' else u'')
    except Exception:
        pass
    return ' '.join(value.split()).strip().lower()


TARGET_LOOKUP = dict((normalize_name(name), name) for name in TARGET_NAMES)
ALIAS_LOOKUP = dict((normalize_name(name), target) for name, target in ALIASES.items())


def match_channel(code, name):
    code = clean_text(code).upper()
    if code in CODE_TO_NAME:
        return CODE_TO_NAME[code]

    name = normalize_name(name)
    return TARGET_LOOKUP.get(name) or ALIAS_LOOKUP.get(name)


def request_json(url, params=None):
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = SESSION.get(
                url, params=params, timeout=REQUEST_TIMEOUT, verify=False
            )

            if response.status_code == 204:
                return []

            response.raise_for_status()
            try:
                data = response.json()
            except Exception:
                data = json.loads(response.text)

            if isinstance(data, dict) and 'd' in data:
                data = data['d']

            if isinstance(data, string_types):
                text = data.strip()
                if text and text[0] in '[{':
                    try:
                        data = json.loads(text)
                    except Exception:
                        pass

            return data

        except Exception as error:
            last_error = error
            if attempt + 1 < MAX_RETRIES:
                time.sleep(0.7 * (attempt + 1))

    raise last_error


def as_list(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ('Data', 'data', 'Items', 'items', 'Channels', 'channels',
                    'Programs', 'programs', 'Result', 'result'):
            value = data.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, string_types):
                try:
                    value = json.loads(value)
                    if isinstance(value, list):
                        return value
                except Exception:
                    pass
    return []


def get_local_offset():
    is_dst = time.localtime().tm_isdst
    seconds = -(time.altzone if is_dst else time.timezone)
    sign = '+' if seconds >= 0 else '-'
    seconds = abs(seconds)
    return '%s%02d%02d' % (sign, seconds // 3600, (seconds % 3600) // 60)


TIME_ZONE = get_local_offset()


def fetch_channels():
    found = {}
    seen_codes = set()
    today = datetime.now().strftime('%m/%d/%Y')

    # The current OSN API exposes the required list through this feed.
    for page in range(1, 21):
        params = {
            'pg': page,
            'pk': 0,
            'gn': 0,
            'cu': CULTURE,
            'bx': 0,
            'dt': today,
        }

        try:
            data = request_json(API_BASE + '/chnl', params)
            items = as_list(data)
            if not items and isinstance(data, dict):
                items = [v for v in data.values() if isinstance(v, dict)]
        except Exception as error:
            cprint('OSN channel request error: %s' % error)
            break

        if not items:
            break

        for item in items:
            if not isinstance(item, dict):
                continue

            code = clean_text(first_value(item, [
                'ChannelCode', 'channelCode', 'Code', 'code'
            ]))
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)

            api_name = clean_text(first_value(item, [
                'Name', 'name', 'ChannelName', 'channelName',
                'ChannelNameEnglish', 'channelNameEnglish'
            ], code))

            name = match_channel(code, api_name)
            if not name or name in found:
                continue

            icon = clean_text(first_value(item, [
                'ChannelLogo', 'channelLogo', 'Logo', 'logo',
                'Image', 'image', 'ChannelImage', 'channelImage'
            ]))

            if not icon:
                icon = 'https://content.osn.com/logo/channel/cropped/%s.png' % code
            elif icon.startswith('/'):
                icon = BASE_URL + icon

            found[name] = {'code': code, 'name': name, 'icon': icon}

            if len(found) == len(CHANNELS):
                break

        if len(found) == len(CHANNELS):
            break

    return [found[name] for name in TARGET_NAMES if name in found]


def parse_datetime(value):
    if value is None:
        return None

    text = clean_text(value).replace(',', '')

    if text.startswith('/Date('):
        try:
            stamp = text.split('(')[1].split(')')[0].split('+')[0]
            if '-' in stamp[1:]:
                stamp = stamp.split('-', 1)[0]
            return datetime.fromtimestamp(int(stamp) / 1000.0)
        except Exception:
            pass

    formats = (
        '%d %b %Y %H:%M:%S',
        '%d %b %Y %H:%M',
        '%d %B %Y %H:%M:%S',
        '%d %B %Y %H:%M',
        '%m/%d/%Y %I:%M:%S %p',
        '%m/%d/%Y %I:%M %p',
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
    )

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            pass

    try:
        return datetime.strptime(text.split('.')[0].replace('Z', ''),
                                 '%Y-%m-%dT%H:%M:%S')
    except Exception:
        return None


def fetch_schedule(channel_code, day):
    params = {
        'dt': day.strftime('%m/%d/%Y'),
        'co': COUNTRY_CODE,
        'ch': channel_code,
        'mo': 'false',
        'hr': 0,
    }

    data = request_json(API_BASE + '/time', params)
    items = as_list(data)

    if not items and isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                items = value
                break

    return [item for item in items if isinstance(item, dict)]


def fetch_details(epg_id):
    if not epg_id or not FETCH_DETAILS:
        return {}

    if epg_id in DETAILS_CACHE:
        return DETAILS_CACHE[epg_id]

    try:
        data = request_json(API_BASE + '/GetProgramDetails', {
            'countryCode': COUNTRY_CODE,
            'prgmEPGUNIQID': epg_id,
        })

        if isinstance(data, list) and data and isinstance(data[0], dict):
            data = data[0]
        elif not isinstance(data, dict):
            data = {}

        DETAILS_CACHE[epg_id] = data
        return data
    except Exception:
        return {}


def stop_from_duration(start, details):
    if start is None or not isinstance(details, dict):
        return None

    duration = clean_text(first_value(details, ['DurationTime', 'durationTime', 'DurationTimeAr']))
    if '-' not in duration:
        return None

    try:
        end = datetime.strptime(duration.split('-')[-1].strip(), '%H:%M')
        stop = start.replace(hour=end.hour, minute=end.minute,
                             second=0, microsecond=0)
        if stop <= start:
            stop += timedelta(days=1)
        return stop
    except Exception:
        return None


def programme_from_item(item):
    start = parse_datetime(first_value(item, [
        'StartDateTime', 'startDateTime', 'Start', 'start'
    ]))
    stop = parse_datetime(first_value(item, [
        'EndDateTime', 'endDateTime', 'StopDateTime', 'stopDateTime',
        'End', 'end'
    ]))

    title = clean_text(first_value(item, ['Title', 'title', 'EpisodeEn', 'EnglishTitle', 'TitleEn', 'TitleEN']))
    epg_id = clean_text(first_value(item, [
        'EPGUNIQID', 'EpgUniqId', 'EPGUniqueID', 'ProgramId', 'programId'
    ]))

    details = fetch_details(epg_id)
    if stop is None:
        stop = stop_from_duration(start, details)

    if details:
        title = clean_text(first_value(details, ['Title', 'EpisodeEn', 'EnglishTitle', 'TitleEn', 'TitleEN'], title)) or title

    desc = clean_text(first_value(details, ['Synopsis', 'Description', 'EnglishSynopsis', 'SynopsisEn', 'SynopsisEN']))
    if not desc:
        desc = clean_text(first_value(item, ['Synopsis', 'Description', 'EnglishSynopsis', 'SynopsisEn', 'SynopsisEN']))

    rating = clean_text(first_value(details, [
        'ParentalRating', 'Parental_Rating', 'Rating', 'rating',
        'AgeRating', 'ageRating', 'PG'
    ]))
    if not rating:
        rating = clean_text(first_value(item, [
            'ParentalRating', 'Parental_Rating', 'Rating', 'rating',
            'AgeRating', 'ageRating', 'PG'
        ]))

    return {
        'start': start,
        'stop': stop,
        'title': title or 'Unknown programme',
        'desc': desc,
        'rating': rating,
    }


def parse_items(items):
    if DETAIL_WORKERS <= 1 or ThreadPool is None or len(items) < 2:
        return [programme_from_item(item) for item in items]

    pool = ThreadPool(DETAIL_WORKERS)
    try:
        return pool.map(programme_from_item, items)
    finally:
        pool.close()
        pool.join()


def xml_escape(value):
    return escape(clean_text(value), {'"': '&quot;'})


def write_xml(channels, programmes_by_channel):
    folder = os.path.dirname(xml_file)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with io.open(xml_file, 'w', encoding='utf-8') as f:
        f.write(u"<?xml version='1.0' encoding='UTF-8'?>\n<tv>\n")

        for channel in channels:
            name = xml_escape(channel['name'])
            icon = xml_escape(channel.get('icon', ''))
            f.write(u'  <channel id="%s">\n' % name)
            f.write(u'    <display-name lang="en">%s</display-name>\n' % name)
            if icon:
                f.write(u'    <icon src="%s"></icon>\n' % icon)
            f.write(u'  </channel>\n')

        for channel in channels:
            rows = programmes_by_channel.get(channel['code'], [])
            rows.sort(key=lambda item: item.get('start') or datetime.max)

            for index, item in enumerate(rows):
                start = item.get('start')
                if start is None:
                    continue

                stop = item.get('stop')
                if stop is None:
                    if index + 1 < len(rows) and rows[index + 1].get('start'):
                        stop = rows[index + 1]['start']
                    else:
                        stop = start + timedelta(minutes=60)

                name = xml_escape(channel['name'])
                f.write(
                    u'  <programme channel="%s" start="%s %s" stop="%s %s">\n' %
                    (name, start.strftime('%Y%m%d%H%M%S'), TIME_ZONE,
                     stop.strftime('%Y%m%d%H%M%S'), TIME_ZONE)
                )
                f.write(u'    <title lang="en">%s</title>\n' %
                        xml_escape(item.get('title', '')))
                f.write(u'    <desc lang="en">%s</desc>\n' %
                        xml_escape(item.get('desc', '')))

                rating = xml_escape(item.get('rating', ''))
                if rating:
                    f.write(u'    <rating system="Parental Rating">%s</rating>\n' % rating)

                f.write(u'  </programme>\n')

        f.write(u'</tv>\n')


def update_provider_date():
    try:
        with open(PROVIDERS_ROOT, 'r') as f:
            data = json.load(f)

        for item in data.get('bouquets', []):
            if item.get('bouquet') == 'osnen':
                item['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')

        with open(PROVIDERS_ROOT, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass


def print_header():
    print('***************** OSN_English_EPG_By_iet5 *******************')
    print('=============================================================')
    print('Downloading OSN English EPG guide...')
    print('Please wait...')
    print('=============================================================')

def print_channel_count(channel_count):
    print('There are %d channels available for EPG data.' % channel_count)
    print('=============================================================')

def main():
    print_header()

    try:
        channels = fetch_channels()
    except Exception as error:
        cprint('Unable to fetch OSN channels: ' + str(error))
        sys.exit(1)

    if not channels:
        cprint('No OSN channels found. OSN may have changed the API.')
        sys.exit(1)

    print('There are %d channels available for EPG data.' % len(channels))
    print('=============================================================')
    print('Downloading EPG data .............')
    print('=============================================================')

    all_programmes = {}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for index, channel in enumerate(channels, 1):
        print('Downloading [%02d/%02d] %s' %
              (index, len(channels), channel['name']))
        sys.stdout.flush()

        rows = []
        seen = set()

        for offset in range(DAYS_TO_GRAB):
            day = today + timedelta(days=offset)
            try:
                for item in parse_items(fetch_schedule(channel['code'], day)):
                    if item['start'] is None:
                        continue
                    key = (item['start'], item['title'])
                    if key not in seen:
                        seen.add(key)
                        rows.append(item)
            except Exception as error:
                cprint('  %s failed: %s' % (day.strftime('%Y-%m-%d'), error))

        all_programmes[channel['code']] = rows

        if rows:
            last = max(item['stop'] or item['start'] for item in rows)
            print('  %d programmes, ends at %s' % (len(rows), last))
        else:
            cprint('  No EPG found')

        if SLEEP_BETWEEN_CHANNELS:
            time.sleep(SLEEP_BETWEEN_CHANNELS)

    write_xml(channels, all_programmes)
    update_provider_date()

    print('Saved: ' + xml_file)
    print('************** FINISHED ******************')
    sys.stdout.flush()


if __name__ == '__main__':
    main()