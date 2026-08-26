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

import os
import sys
import io
import json
import time
import requests

try:
    from multiprocessing.dummy import Pool as ThreadPool
except Exception:
    ThreadPool = None

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)

from datetime import datetime, timedelta
from xml.sax.saxutils import escape

# =========================================================
# OSN English EPG grabber - By iet5
# =========================================================

BASE_URL = 'https://www.osn.com'
TV_GUIDE_URL = BASE_URL + '/en-eg/watch/tv-schedule'
API_BASE = BASE_URL + '/api/TVScheduleWebService.asmx'

COUNTRY_CODE = 'AE'  # OSN API region only; NOT receiver timezone
CULTURE = 'en-AE'  # English OSN API culture
DAYS_TO_GRAB = 7
REQUEST_TIMEOUT = 15
MAX_RETRIES = 2
SLEEP_BETWEEN_CHANNELS = 0.02
FETCH_DETAILS = True
DETAIL_WORKERS = 3
FAST_DISCOVERY = True
DETAILS_CACHE = {}

DEBUG = False

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


def dlog(message):
    """Debug logging disabled in the production version."""
    return


def response_preview(text):
    try:
        if text is None:
            return ''
        if not isinstance(text, string_types):
            text = str(text)
        return text[:500]
    except Exception:
        return ''


def describe_data(data):
    if isinstance(data, list):
        return 'list(len=%d)' % len(data)
    if isinstance(data, dict):
        return 'dict'
    return type(data).__name__


def cprint(text):
    try:
        print('\033[31m' + text + '\033[m')
    except Exception:
        print(text)


def get_local_offset():
    """Return receiver local UTC offset in XMLTV form, e.g. +0300."""
    is_dst = time.localtime().tm_isdst
    utc_offset_sec = -(time.altzone if is_dst else time.timezone)
    sign = '+' if utc_offset_sec >= 0 else '-'
    utc_offset_sec = abs(utc_offset_sec)
    hours = utc_offset_sec // 3600
    minutes = (utc_offset_sec % 3600) // 60
    return '%s%02d%02d' % (sign, hours, minutes)


TIME_ZONE = get_local_offset()


# =========================================================
# Fixed OSN English 48-channel target list
# =========================================================
TARGET_48 = [
    'OSNtv One',
    'OSNtv Showcase',
    'OSNtv Movies Premiere',
    'OSNtv Pop Up',
    'OSNtv Movies Action',
    'OSNtv Movies Family',
    'OSNtv Movies Hollywood',
    'OSNtv Movies Comedy',
    'OSNtv Movies Horror',
    'OSNtv Showcase Classics',
    'OSNtv Crime',
    'OSNtv Now',
    'OSNtv Comedy',
    'OSNtv Mezze',
    'Fatafeat',
    'TLC HD',
    'OSNtv Yahala',
    'OSNtv Yahala Bil Arabi',
    'OSNtv Yahala Aflam',
    'OSNtv iQIYI',
    'OSNtv Kids',
    'Nickelodeon HD',
    'NickToons HD',
    'Nick Jr HD',
    'Cartoon Network HD',
    'Moonbug Kids',
    'Blippi and Friends',
    'Discovery Channel HD',
    'Discovery IDX HD',
    'History HD',
    'H2 HD',
    'C & I',
    'Animal Planet HD',
    'CNN HD',
    'Bloomberg',
    'Bloomberg Originals',
    'MCM TOP',
    'RFM TV',
    'MOTORVISION',
    'Padel TV',
    'eClutch LIVE',
    'eClutch LIVE 2',
    'eClutch Arabic',
    'eClutch Access',
    'Esport 24',
    'Gametoon',
    'Ginx',
    'OSNtv Documentary',
]

# Known names returned by OSN that differ from the names expected
# by osnar.channels.xml / bouquet configuration.
API_NAME_TO_TARGET = {
    'OSNtv Pop up': 'OSNtv Pop Up',
    'OSNtv Iqiyi': 'OSNtv iQIYI',
    'Nick Jr': 'Nick Jr HD',
    'Cartoon Network': 'Cartoon Network HD',
    'Discovery HD': 'Discovery Channel HD',
    'Discovery ID': 'Discovery IDX HD',
    'Crime & Investigation Network': 'C & I',
    'Animal Planet': 'Animal Planet HD',
    'CNN': 'CNN HD',
    'Bloomberg Originals HD': 'Bloomberg Originals',
    'MCM Top': 'MCM TOP',
    'Motorvision': 'MOTORVISION',
    'Padeltime': 'Padel TV',
    'eClutch LIVE 1': 'eClutch LIVE',
    'eClutch LIVE 2': 'eClutch LIVE 2',
    'eClutch Arabic': 'eClutch Arabic',
    'eClutch Access': 'eClutch Access',
    'Gametoon': 'Gametoon',
    'Ginx': 'Ginx',
    'OSN TV Documentary': 'OSNtv Documentary',
}

# Strong fallback matching by OSN ChannelCode / logo code.
# These codes were verified against the working OSN XML.
CODE_TO_TARGET = {
    'OTO': 'OSNtv One',
    'OFH': 'OSNtv Showcase',
    'OM1': 'OSNtv Movies Premiere',
    'POP': 'OSNtv Pop Up',
    'AHD': 'OSNtv Movies Action',
    'OFM': 'OSNtv Movies Family',
    'OPR': 'OSNtv Movies Hollywood',
    'OMC': 'OSNtv Movies Comedy',
    'OCM': 'OSNtv Movies Horror',
    'OST': 'OSNtv Showcase Classics',
    'OBG': 'OSNtv Crime',
    'OLH': 'OSNtv Now',
    'OCO': 'OSNtv Comedy',
    'OMZ': 'OSNtv Mezze',
    'FTF': 'Fatafeat',
    'TLC': 'TLC HD',
    'OYH': 'OSNtv Yahala',
    'OYA': 'OSNtv Yahala Bil Arabi',
    'OYC': 'OSNtv Yahala Aflam',
    'OIQ': 'OSNtv iQIYI',
    'OMK': 'OSNtv Kids',
    'NIC': 'Nickelodeon HD',
    'NKT': 'NickToons HD',
    'NJR': 'Nick Jr HD',
    'TCN': 'Cartoon Network HD',
    'MBU': 'Moonbug Kids',
    'BAF': 'Blippi and Friends',
    'DSC': 'Discovery Channel HD',
    'DCX': 'Discovery IDX HD',
    'HIS': 'History HD',
    'HI2': 'H2 HD',
    'CAI': 'C & I',
    'APL': 'Animal Planet HD',
    'CNN': 'CNN HD',
    'BTV': 'Bloomberg',
    'BLO': 'Bloomberg Originals',
    'MCM': 'MCM TOP',
    'RFM': 'RFM TV',
    'MOT': 'MOTORVISION',
    'PDT': 'Padel TV',
    'ECL': 'eClutch LIVE',
    'EC2': 'eClutch LIVE 2',
    'ELA': 'eClutch Arabic',
    'ECA': 'eClutch Access',
    'ES2': 'Esport 24',
    'GMT': 'Gametoon',
    'GNX': 'Ginx',
    'DOC': 'OSNtv Documentary',
}


def normalize_channel_name(value):
    """Normalize OSN naming quirks for reliable 48-channel matching."""
    s = clean_text(value or '')
    try:
        s = s.replace(u'\xa0', u' ')
        s = s.replace(u'\u200b', u'')
        s = s.replace(u'\u200c', u'')
        s = s.replace(u'\u200d', u'')
        s = s.replace(u'\ufeff', u'')
    except Exception:
        pass
    s = ' '.join(s.split())
    return s.strip().lower()


def match_target_channel(code, name):
    """
    Return the exact bouquet/receiver target name for an OSN API channel.
    Priority:
      1) verified ChannelCode
      2) exact normalized target name
      3) known API name alias
    """
    clean_code = clean_text(code or '').strip().upper()
    if clean_code in CODE_TO_TARGET:
        return CODE_TO_TARGET[clean_code]

    n = normalize_channel_name(name)
    if n in TARGET_BY_NORMALIZED:
        return TARGET_BY_NORMALIZED[n]
    if n in ALIAS_BY_NORMALIZED:
        return ALIAS_BY_NORMALIZED[n]

    return None


def request_json(url, params=None, context=''):
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        r = None
        try:
            dlog('=' * 90)
            dlog('REQUEST context=%s attempt=%d/%d' % (context, attempt, MAX_RETRIES))
            dlog('BASE URL: %s' % url)
            dlog('PARAMS: %s' % repr(params))

            r = SESSION.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT,
                verify=False
            )

            dlog('FINAL URL: %s' % getattr(r, 'url', ''))
            dlog('HTTP STATUS: %s' % getattr(r, 'status_code', ''))
            dlog('CONTENT-TYPE: %s' % r.headers.get('Content-Type', ''))
            dlog('CONTENT-LENGTH HEADER: %s' % r.headers.get('Content-Length', ''))
            dlog('RESPONSE ENCODING: %s' % getattr(r, 'encoding', ''))

            text_body = getattr(r, 'text', '') or ''
            dlog('BODY LENGTH: %d' % len(text_body))

            # 204 means there are no more channel pages. This is normal.
            if r.status_code == 204:
                dlog('HTTP 204 -> empty result (normal end of pagination)')
                return []

            # Always log body for errors/non-JSON. For valid JSON, a shorter sample
            # is still useful to identify the exact schema returned by OSN.
            content_type = (r.headers.get('Content-Type', '') or '').lower()
            if (r.status_code != 200 or
                    'json' not in content_type or
                    context.startswith('time')):
                dlog('RAW BODY: %s' % response_preview(text_body))
            else:
                dlog('BODY SAMPLE: %s' % response_preview(text_body[:800]))

            r.raise_for_status()

            data = None
            json_error = None
            try:
                data = r.json()
                dlog('r.json() OK -> %s' % describe_data(data))
            except Exception as e:
                json_error = e
                dlog('r.json() FAILED -> %s' % repr(e))

            if data is None:
                try:
                    data = json.loads(text_body)
                    dlog('json.loads(text) OK -> %s' % describe_data(data))
                except Exception as e:
                    dlog('json.loads(text) FAILED -> %s' % repr(e))
                    raise

            # ASP.NET ASMX commonly wraps result inside {"d": ...}
            if isinstance(data, dict) and 'd' in data:
                dlog('ASMX wrapper "d" detected. d type=%s' % type(data.get('d')).__name__)
                data = data['d']
                dlog('AFTER d unwrap -> %s' % describe_data(data))

            # Sometimes "d" itself is a JSON string.
            if isinstance(data, string_types):
                s = data.strip()
                dlog('STRING PAYLOAD detected. first chars=%s' % response_preview(s[:300]))
                if s and s[0] in '[{':
                    try:
                        data = json.loads(s)
                        dlog('Nested JSON string decoded -> %s' % describe_data(data))
                    except Exception as e:
                        dlog('Nested JSON decode FAILED -> %s' % repr(e))

            dlog('RETURN DATA -> %s' % describe_data(data))
            return data

        except Exception as e:
            last_error = e
            dlog('REQUEST FAILED: %s' % repr(e))
            if r is not None:
                try:
                    dlog('FAILED RESPONSE STATUS=%s BODY=%s' %
                         (r.status_code, response_preview(getattr(r, 'text', '') or '')))
                except Exception:
                    pass

            if attempt < MAX_RETRIES:
                time.sleep(0.7 * attempt)

    raise last_error


def normalize_list(data):
    """Try to obtain a list from different ASMX response shapes."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ('Data', 'data', 'Items', 'items', 'Channels', 'channels',
                    'Programs', 'programs', 'Result', 'result'):
            v = data.get(key)
            if isinstance(v, list):
                return v
            if isinstance(v, string_types):
                try:
                    x = json.loads(v)
                    if isinstance(x, list):
                        return x
                except Exception:
                    pass
    return []


def clean_text(value):
    if value is None:
        return ''
    if not isinstance(value, string_types):
        try:
            value = str(value)
        except Exception:
            return ''
    return value.replace('\\n', ' ').replace('\r', ' ').replace('\n', ' ').strip()


# Build normalized lookup tables only after clean_text() exists.
TARGET_BY_NORMALIZED = dict(
    (normalize_channel_name(name), name) for name in TARGET_48
)

ALIAS_BY_NORMALIZED = dict(
    (normalize_channel_name(api_name), target)
    for api_name, target in API_NAME_TO_TARGET.items()
)


def first_value(obj, keys, default=''):
    if not isinstance(obj, dict):
        return default
    for key in keys:
        if key in obj and obj.get(key) not in (None, ''):
            return obj.get(key)
    return default



def fetch_channels():
    """
    Discover OSN channels but return ONLY the fixed 48 channels required
    by osnar.channels.xml / bouquet configuration.

    Unlike the old implementation, this does NOT stop at the first
    48 arbitrary API channels. It keeps scanning OSN API combinations
    until all target channels are matched or all searches are exhausted.
    """
    found_by_target = {}
    seen_codes = set()
    today = datetime.now().strftime('%m/%d/%Y')

    searches = []

    # box/package groups
    for bx in range(0, 16):
        searches.append((bx, 0, 0))

    # package variants
    for pk in range(1, 11):
        for bx in range(0, 8):
            searches.append((bx, pk, 0))

    # genre/category variants
    for gn in range(1, 11):
        for bx in range(0, 8):
            searches.append((bx, 0, gn))

    unique_searches = []
    seen_searches = set()
    for combo in searches:
        if combo not in seen_searches:
            seen_searches.add(combo)
            unique_searches.append(combo)

    if FAST_DISCOVERY:
        # Current OSN API returns the same primary channel list across the
        # tested box/package/genre combinations. Avoid 176 duplicate scans.
        unique_searches = [(0, 0, 0)]

    dlog('TARGET-48 DISCOVERY START combinations=%d' % len(unique_searches))

    for bx, pk, gn in unique_searches:
        if len(found_by_target) >= len(TARGET_48):
            break

        for page in range(1, 21):
            params = {
                'pg': page,
                'pk': pk,
                'gn': gn,
                'cu': CULTURE,
                'bx': bx,
                'dt': today,
            }

            try:
                data = request_json(
                    API_BASE + '/chnl',
                    params=params,
                    context='chnl bx=%d pk=%d gn=%d page=%d' %
                            (bx, pk, gn, page)
                )
            except Exception as e:
                dlog(
                    'CHANNEL DISCOVERY ERROR bx=%d pk=%d gn=%d page=%d error=%r' %
                    (bx, pk, gn, page, e)
                )
                break

            items = normalize_list(data)

            if not items and isinstance(data, dict):
                items = [v for v in data.values() if isinstance(v, dict)]

            if not items:
                break

            page_new = 0

            for item in items:
                if not isinstance(item, dict):
                    continue

                code = clean_text(first_value(item, [
                    'ChannelCode', 'channelCode', 'Code', 'code'
                ]))

                api_name = clean_text(first_value(item, [
                    'Name', 'name', 'ChannelName', 'channelName',
                    'ChannelNameEnglish', 'channelNameEnglish'
                ]))

                if not code:
                    continue

                if code in seen_codes:
                    continue
                seen_codes.add(code)

                if not api_name:
                    api_name = code

                target_name = match_target_channel(code, api_name)

                if not target_name:
                    dlog(
                        'IGNORED NON-TARGET CHANNEL code=%r name=%r' %
                        (code, api_name)
                    )
                    continue

                if target_name in found_by_target:
                    dlog(
                        'DUPLICATE TARGET MATCH target=%r code=%r name=%r' %
                        (target_name, code, api_name)
                    )
                    continue

                icon = clean_text(first_value(item, [
                    'ChannelLogo', 'channelLogo', 'Logo', 'logo',
                    'Image', 'image', 'ChannelImage', 'channelImage'
                ]))

                if not icon:
                    icon = 'https://content.osn.com/logo/channel/cropped/%s.png' % code
                elif icon.startswith('/'):
                    icon = BASE_URL + icon

                found_by_target[target_name] = {
                    'code': code,
                    # IMPORTANT: output the exact receiver/bouquet name.
                    'name': target_name,
                    'api_name': api_name,
                    'icon': icon
                }

                page_new += 1

                dlog(
                    'TARGET CHANNEL MATCHED %02d/%02d target=%r '
                    'api_name=%r code=%r bx=%d pk=%d gn=%d page=%d' %
                    (
                        len(found_by_target), len(TARGET_48),
                        target_name, api_name, code,
                        bx, pk, gn, page
                    )
                )

                if len(found_by_target) >= len(TARGET_48):
                    break

            dlog(
                'CHANNEL PAGE DONE bx=%d pk=%d gn=%d page=%d '
                'items=%d new_targets=%d matched=%d/%d' %
                (
                    bx, pk, gn, page, len(items), page_new,
                    len(found_by_target), len(TARGET_48)
                )
            )

            if len(found_by_target) >= len(TARGET_48):
                break

    # Force final output into the exact requested 48-channel order.
    channels = []
    missing = []

    for target_name in TARGET_48:
        ch = found_by_target.get(target_name)
        if ch:
            channels.append(ch)
        else:
            missing.append(target_name)

    dlog(
        'TARGET-48 DISCOVERY FINISHED matched=%d missing=%d' %
        (len(channels), len(missing))
    )

    for i, ch in enumerate(channels, 1):
        dlog(
            'FINAL CHANNEL %02d target=%r api_name=%r code=%r' %
            (
                i, ch.get('name'),
                ch.get('api_name'),
                ch.get('code')
            )
        )

    if missing:
        dlog('MISSING TARGET CHANNELS: %s' % repr(missing))

    return channels


def parse_osn_datetime(value):
    """Parse common OSN/ASP.NET datetime values."""
    if value is None:
        return None
    s = clean_text(value).replace(',', '')

    # /Date(1690000000000)/
    if s.startswith('/Date('):
        try:
            ms = int(s.split('(')[1].split(')')[0].split('+')[0].split('-')[0])
            return datetime.fromtimestamp(ms / 1000.0)
        except Exception:
            pass

    formats = (
        # Current OSN API format, e.g. 23 Aug 2026, 22:00
        # The comma is removed above, so this becomes: 23 Aug 2026 22:00
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
            return datetime.strptime(s, fmt)
        except Exception:
            pass

    # ISO value with milliseconds / timezone suffix
    try:
        base = s.split('.')[0].replace('Z', '')
        return datetime.strptime(base, '%Y-%m-%dT%H:%M:%S')
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
    data = request_json(API_BASE + '/time', params=params, context='time channel=%s date=%s' % (channel_code, day.strftime('%Y-%m-%d')))
    items = normalize_list(data)

    # OSN occasionally wraps the programme array in a JSON string/dict.
    if not items and isinstance(data, string_types):
        try:
            decoded = json.loads(data)
            items = normalize_list(decoded)
            if isinstance(decoded, list):
                items = decoded
        except Exception:
            pass

    if not items and isinstance(data, dict):
        # Last-resort: find a list nested one level deep.
        for key, value in data.items():
            if isinstance(value, list):
                dlog('SCHEDULE fallback list found under key=%r len=%d' % (key, len(value)))
                items = value
                break

    result = [x for x in items if isinstance(x, dict)]
    dlog('SCHEDULE RESULT channel=%r date=%s raw=%s normalized=%d dict_rows=%d' %
         (channel_code, day.strftime('%Y-%m-%d'), describe_data(data),
          len(items), len(result)))

    if result:
        try:
            dlog('FIRST PROGRAM KEYS: %s' % repr(list(result[0].keys())))
            dlog('FIRST PROGRAM RAW: %s' % response_preview(json.dumps(result[0], ensure_ascii=False)))
        except Exception as e:
            dlog('FIRST PROGRAM LOG FAILED: %s' % repr(e))
    else:
        dlog('*** NO PROGRAMMES EXTRACTED FOR channel=%r date=%s ***' %
             (channel_code, day.strftime('%Y-%m-%d')))

    return result


def fetch_details(epg_id):
    if not epg_id or not FETCH_DETAILS:
        return {}

    # Many programmes repeat during the 7-day guide.
    # Cache by EPG id so the same details are downloaded only once.
    cached = DETAILS_CACHE.get(epg_id)
    if cached is not None:
        return cached

    try:
        data = request_json(API_BASE + '/GetProgramDetails', params={
            'countryCode': COUNTRY_CODE,
            'prgmEPGUNIQID': epg_id,
        }, context='details epg_id=%s' % epg_id)

        if isinstance(data, list) and data:
            result = data[0] if isinstance(data[0], dict) else {}
        elif isinstance(data, dict):
            result = data
        else:
            result = {}

        DETAILS_CACHE[epg_id] = result
        return result
    except Exception:
        # Do not cache transient failures, so a later repeat can retry.
        return {}


def stop_from_duration(start, details):
    """
    OSN GetProgramDetails returns values such as:
      DurationTime: "22:00 - 22:55"
      DurationTimeAr: "23:45 - 00:30"
    Use the right-hand time as the programme stop.
    """
    if start is None or not isinstance(details, dict):
        return None

    duration = clean_text(first_value(details, [
        'DurationTime', 'durationTime', 'DurationTimeAr'
    ]))

    if not duration or '-' not in duration:
        return None

    try:
        end_part = duration.split('-')[-1].strip()
        end_time = datetime.strptime(end_part, '%H:%M')

        stop = start.replace(
            hour=end_time.hour,
            minute=end_time.minute,
            second=0,
            microsecond=0
        )

        # Programme crosses midnight.
        if stop <= start:
            stop += timedelta(days=1)

        return stop
    except Exception as e:
        dlog('STOP FROM DURATION FAILED duration=%r error=%r' % (duration, e))
        return None

def programme_from_item(item):
    start = parse_osn_datetime(first_value(item, ['StartDateTime', 'startDateTime', 'Start', 'start']))
    stop = parse_osn_datetime(first_value(item, ['EndDateTime', 'endDateTime', 'StopDateTime', 'stopDateTime', 'End', 'end']))

    title = clean_text(first_value(item, [
        'Title', 'title', 'EpisodeEn', 'EnglishTitle', 'TitleEn', 'TitleEN'
    ]))
    epg_id = clean_text(first_value(item, ['EPGUNIQID', 'EpgUniqId', 'EPGUniqueID', 'ProgramId', 'programId']))

    details = fetch_details(epg_id)

    # Current /time API normally gives StartDateTime but no EndDateTime.
    # Get stop from GetProgramDetails -> DurationTime/DurationTimeAr.
    if stop is None and details:
        stop = stop_from_duration(start, details)

    if details:
        title = clean_text(first_value(details, [
            'Title', 'EpisodeEn', 'EnglishTitle', 'TitleEn', 'TitleEN'
        ], title)) or title

    desc = clean_text(first_value(details, [
        'Synopsis', 'Description', 'EnglishSynopsis', 'SynopsisEn', 'SynopsisEN'
    ]))
    if not desc:
        desc = clean_text(first_value(item, [
            'Synopsis', 'Description', 'EnglishSynopsis', 'SynopsisEn', 'SynopsisEN'
        ]))

    category = clean_text(first_value(details, [
        'GenreName', 'GenreEnglishName', 'EnglishGenreName', 'Genre'
    ]))

    icon = clean_text(first_value(details, ['ProgramImage', 'Image', 'image']))
    year = clean_text(first_value(details, ['Year', 'year']))
    rating = clean_text(first_value(details, [
        'ParentalRating', 'Parental_Rating', 'Rating', 'rating',
        'AgeRating', 'ageRating', 'PG'
    ]))
    if not rating:
        rating = clean_text(first_value(item, [
            'ParentalRating', 'Parental_Rating', 'Rating', 'rating',
            'AgeRating', 'ageRating', 'PG'
        ]))

    dlog(
        'PROGRAM PARSED epg_id=%r start=%r stop=%r title=%r' %
        (epg_id, start, stop, title)
    )

    return {
        'start': start,
        'stop': stop,
        'title': title or 'Unknown programme',
        'desc': desc,
        'category': category,
        'icon': icon,
        'year': year,
        'rating': rating,
    }


def xml_escape(text):
    return escape(clean_text(text), {'"': '&quot;'})


def write_xml(channels, all_programmes):
    """Write XMLTV matching the supplied osnara.xml.xz structure/order."""
    folder = os.path.dirname(xml_file)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with io.open(xml_file, 'w', encoding='utf-8') as f:
        f.write(u"<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write(u'<tv>\n')

        # All channels first
        for ch in channels:
            cid = xml_escape(ch.get('name', ''))
            cname = xml_escape(ch.get('name', ''))
            icon = xml_escape(ch.get('icon', ''))

            f.write(u'  <channel id="%s">\n' % cid)
            f.write(u'    <display-name lang="en">%s</display-name>\n' % cname)
            if icon:
                f.write(u'    <icon src="%s"></icon>\n' % icon)
            f.write(u'  </channel>\n')

        # All programmes after channels
        for ch in channels:
            programmes = all_programmes.get(ch.get('code'), [])
            programmes.sort(key=lambda p: p.get('start') or datetime.max)

            for i, p in enumerate(programmes):
                if p.get('start') is None:
                    continue

                if p.get('stop') is None:
                    if i + 1 < len(programmes) and programmes[i + 1].get('start'):
                        p['stop'] = programmes[i + 1]['start']
                    else:
                        p['stop'] = p['start'] + timedelta(minutes=60)

                start_text = p['start'].strftime('%Y%m%d%H%M%S')
                stop_text = p['stop'].strftime('%Y%m%d%H%M%S')
                cid = xml_escape(ch.get('name', ''))

                f.write(
                    u'  <programme channel="%s" start="%s %s" stop="%s %s">\n'
                    % (cid, start_text, TIME_ZONE, stop_text, TIME_ZONE)
                )
                f.write(
                    u'    <title lang="en">%s</title>\n'
                    % xml_escape(p.get('title', ''))
                )
                f.write(
                    u'    <desc lang="en">%s</desc>\n'
                    % xml_escape(p.get('desc', ''))
                )

                rating = xml_escape(p.get('rating', ''))
                if rating:
                    f.write(
                        u'    <rating system="Parental Rating">%s</rating>\n'
                        % rating
                    )

                f.write(u'  </programme>\n')

        f.write(u'</tv>\n')

    dlog('XML WRITTEN: %s' % xml_file)


def update_provider_date():
    try:
        with open(PROVIDERS_ROOT, 'r') as f:
            data = json.load(f)
        for channel in data.get('bouquets', []):
            if channel.get('bouquet') == 'osnen':
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        with open(PROVIDERS_ROOT, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass



def print_execution_header():
    """Compact progress banner suitable for DreamOS and open-source images."""
    print('***************** OSN_English_EPG_By_iet5 *******************')
    print('=============================================================')
    print('Downloading OSN English EPG guide...')
    print('Please wait...')
    print('=============================================================')

def print_channel_count(channel_count):
    print('There are %d channels available for EPG data.' % channel_count)
    print('=============================================================')

def main():
    print_execution_header()
    if DEBUG:
        try:
            folder = os.path.dirname(DEBUG_LOG)
            if folder and not os.path.exists(folder):
                os.makedirs(folder)
            with io.open(DEBUG_LOG, 'w', encoding='utf-8') as lf:
                lf.write(u'OSN ENGLISH EPG DEBUG LOG\n')
                lf.write(u'Generated: %s\n\n' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception:
            pass

    dlog('Python: %s' % sys.version)
    dlog('requests: %s' % getattr(requests, '__version__', 'unknown'))
    dlog('TV_GUIDE_URL=%s' % TV_GUIDE_URL)
    dlog('API_BASE=%s' % API_BASE)
    dlog('COUNTRY_CODE=%s CULTURE=%s DAYS_TO_GRAB=%s' %
         (COUNTRY_CODE, CULTURE, DAYS_TO_GRAB))

    sys.stdout.flush()

    try:
        channels = fetch_channels()
        print_channel_count(len(channels))
        print('Downloading EPG data .............')
        print('=============================================================')
    except Exception as e:
        cprint('Unable to fetch OSN channels: ' + str(e))
        sys.exit(1)

    if not channels:
        cprint('No OSN channels found. OSN may have changed the API.')
        sys.exit(1)

    all_programmes = {}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for idx, ch in enumerate(channels, 1):
        print('Downloading [%02d/%02d] %s' % (idx, len(channels), ch['name']))
        dlog('PROCESS CHANNEL index=%d/%d code=%r name=%r' %
             (idx, len(channels), ch.get('code'), ch.get('name')))
        sys.stdout.flush()
        rows = []
        seen = set()
        for day_offset in range(DAYS_TO_GRAB):
            day = today + timedelta(days=day_offset)
            try:
                items = fetch_schedule(ch['code'], day)

                if DETAIL_WORKERS > 1 and ThreadPool is not None and len(items) > 1:
                    pool = ThreadPool(DETAIL_WORKERS)
                    try:
                        parsed_items = pool.map(programme_from_item, items)
                    finally:
                        try:
                            pool.close()
                            pool.join()
                        except Exception:
                            pass
                else:
                    parsed_items = [programme_from_item(item) for item in items]

                for p in parsed_items:
                    if p['start'] is None:
                        continue
                    key = (p['start'], p['title'])
                    if key not in seen:
                        seen.add(key)
                        rows.append(p)
            except Exception as e:
                cprint('  %s failed: %s' % (day.strftime('%Y-%m-%d'), e))
        all_programmes[ch['code']] = rows
        if rows:
            last = max([p['stop'] or p['start'] for p in rows])
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
