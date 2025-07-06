#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

try:
    from .__init__ import *
except:
    from __init__ import *

import requests
import io
import threading
import sys
import os
import re
import json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from time import sleep, strftime
from xml.sax.saxutils import escape

if sys.version_info[0] < 3:
    import codecs
    open = codecs.open

# Regex to remove invalid XML 1.0 control characters
invalid_xml_re = re.compile(u'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

time_zone = tz()

head = {
    "Content-Type": "application/json; charset=utf-8",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36"
}

channels_code = sorted(['560-BBC ONE London HD', '700-BBC TWO HD', '10005-ITV1 HD', '1540-Channel 4 HD', '1547-Channel 5 HD',
                '818-BBC THREE HD', '819-BBC FOUR HD', '712-BBC ALBA HD', '710-BBC Scotland HD', '1030-ITV1 +1', '1118-ITV2 HD',
                '1101-ITV2 +1', '1119-ITV3 HD', '1103-ITV3 +1', '1120-ITV4 HD', '1107-ITV4 +1', '1121-ITVBe HD', '20002-S4C HD',
                '1525-Channel 4 +1', '1510-E4', '1511-E4 +1', '1515-More4', '1516-More4 + 1', '28010-E4 Extra', '28009-4seven',
                '1541-Channel 5+1', '28007-5USA', '28008-5USA +1', '28005-5STAR', '17013-5ACTION', '4017-5SELECT', '27000-TRUE CRIME XTR',
                '27003-TRUE CRIME', '4010-TRUE CRIME +1', '27001-LEGEND', '27004-LEGEND XTRA', '27002-LEGEND XTRA +1', '28006-5Star+1',
                '20028-Sky Mix HD', '4013-Challenge', '20026-Sky Arts', '18008-QUEST HD', '19012-Really', '18006-Quest Red', '5007-DMAX',
                '7009-Food Network', '9008-HGTV', '18004-Quest', '18005-Quest +1', '18007-Quest Red +1', '5008-DMAX+1',
                '7010-Food Network +1', '17011-PBS America', '24004-U\u0026W', '5005-U\u0026Dave', '5003-U\u0026Drama',
                '26000-U\u0026Yesterday', '22000-U\u0026Eden', '4027-BLAZE', '4015-Together TV', '4034-Court TV', '21259-That\u0027s TV ',
                '21262-That\u0027s TV 2', '820-BBC NEWS HD', '711-BBC Parliament HD', '20014-Sky News', '2005-Al Jazeera English',
                '7016-FRANCE 24 (in English)', '3020-Bloomberg TV', '15005-NHK WORLD-JAPAN', '4036-CNBC HD', '4026-Arirang TV',
                '21257-TRT World', '8005-GB News', '1520-Film4', '1521-Film4 +1', '21013-Talking Pictures TV', '822-CBBC HD',
                '821-CBeebies HD', '5004-DAYSTAR HD', '8003-Revelation', '8004-GODTV', '20012-Sonlife TV', '837-BBC Radio 1',
                '831-BBC Radio 1Xtra', '838-BBC Radio 2', '839-BBC Radio 3', '840-BBC Radio 4', '841-BBC Radio 5Live',
                '830-BBC Radio 5 Sports Extra', '844-BBC Radio 6Music', '845-BBC Radio 4 Extra', '842-BBC Asian Network',
                '846-BBC World Service', '834-BBC Radio Scotland', '835-BBC Radio nan Gaidhael', '836-BBC Radio Wales',
                '843-BBC Radio Cymru', '847-BBC Radio Ulster', '848-BBC Radio Foyle', '833-BBC Radio London', '4001-Capital',
                '4004-Capital Xtra', '4002-Classic FM', '8001-Gold Radio ', '25000-Radio X', '21008-talkSPORT', '20011-Smooth RadioUK',
                '9000-Heart', '13000-LBC 97.3', '832-BBC Radio Cymru 2', '23007-Virgin Radio', '19002-RTE Radio 1', '19003-RTE  2fm',
                '19004-RTE Lyric fm', '19005-RTE RnaG', '3003-BFBS Radio', '21006-TWR', '18009-QVC HD', '18001-QVC Beauty', '18002-QVC Extra',
                '18010-QVC Style HD', '8002-Gems TV', '9009-HobbyMaker', '11006-Jewellery Maker', '21258-TJC HD', '10704-IDEAL WORLD',
                '14008-Must Have Ideas', '105-Freesat Info'])
lock = threading.Semaphore(4)

def sanitize_xml(text):
    """Remove invalid XML characters and escape special entities"""
    return escape(invalid_xml_re.sub('', text))

def freesat(code):
    try:
        channel_id, channel_name = code.split('-', 1)
        safe_channel = sanitize_xml(channel_name)
        
        for i in range(0, 8):
            with requests.Session() as s:
                s.mount('https://', HTTPAdapter(max_retries=10))
                url = s.get('https://www.freesat.co.uk/tv-guide/api/{0}/?channel={1}'.format(i, channel_id), headers=head)
                try:
                    data = url.json()
                    for event in data[0]['event']:
                        start = datetime.fromtimestamp(event['startTime']).strftime('%Y%m%d%H%M%S')
                        end_dt = datetime.strptime(start, '%Y%m%d%H%M%S') + timedelta(seconds=event['duration'])
                        end = end_dt.strftime('%Y%m%d%H%M%S')
                        
                        title = sanitize_xml(event['name'])
                        desc = sanitize_xml(event.get('description', ''))
                        
                        programme = '  <programme start="{start} {tz}" stop="{end} {tz}" channel="{channel}">\n'.format(
                            start=start, tz=time_zone, end=end, channel=safe_channel
                        )
                        programme += '    <title lang="en">{0}</title>\n'.format(title)
                        programme += '    <desc lang="en">{0}</desc>\n'.format(desc)
                        programme += '  </programme>\n'
                        
                        with io.open(EPG_ROOT + '/freesat.xml', "a", encoding='UTF-8') as f:
                            f.write(programme)
                            
                    if data[0]['event']:
                        last_event = data[0]['event'][-1]
                        end_time = datetime.fromtimestamp(last_event['startTime'] + last_event['duration'])
                        print("{0} epg ends at: {1}".format(safe_channel, end_time.strftime('%Y-%m-%d %H:%M')))
                    else:
                        print("No events found for {0}".format(safe_channel))
                except Exception as e:
                    print("Error processing {0}: {1}".format(safe_channel, str(e)))
                    continue
    except Exception as e:
        print("Fatal error for {0}: {1}".format(channel_name, str(e)))
    finally:
        lock.release()

def main():
    print('***************FREESAT EPG*********************')
    # Read generated XML and display channel count
    print("================================================")
    print("This script have amended and corrected by # iet5")
    print("Total channels to process: {0}".format(len(channels_code)))
    print("================================================")
    sys.stdout.flush()
    
    # Update provider timestamp
    with open(PROVIDERS_ROOT, 'r+') as f:
        data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"] == "freesat":
                channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    # Generate XML header
    channels = [sanitize_xml(ch.split('-', 1)[1]) for ch in channels_code]
    xml_header(EPG_ROOT + '/freesat.xml', channels)

    # Process channels with thread pool
    threads = []
    for code in channels_code:
        lock.acquire()
        thread = threading.Thread(target=freesat, args=(code,))
        threads.append(thread)
        thread.start()
        sleep(0.5)
    
    for thread in threads:
        thread.join()

    close_xml(EPG_ROOT + '/freesat.xml')

    # Sort XML if needed
    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream OS detected, sorting XML...')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/freesat.xml')
        root = tree.getroot()
        root[:] = sorted(root, key=lambda elem: elem.get('channel', ''))
        tree.write(EPG_ROOT + '/freesat.xml', encoding='utf-8', xml_declaration=True)

    print("\Freesat.xml Downloaded Successfully")
    print('**************EPG Freesat COMPLETE******************')
    sys.stdout.flush()


if __name__ == "__main__":
    main()
    sys.stdout.flush()
