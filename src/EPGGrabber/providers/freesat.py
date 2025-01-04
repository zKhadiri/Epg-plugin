#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
# python3

try:
	from .__init__ import *
except:
	from __init__ import *

import requests
import io
import threading
import sys
import os
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from time import sleep, strftime

if sys.version_info[0] < 3:
    import codecs
    open = codecs.open

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

# channels_code = sorted(['505-BBC ONE SD', '555-BBC ONE HD', '700-BBC TWO HD', '818-BBC Three HD', '10005-ITV1 HD', '1500-Channel 4 HD', '1547-Channel 5 HD',
               # '819-BBC FOUR HD', '710-BBC Scotland HD', '709-BBC Scotland', '701-BBC THREE', '707-BBC ALBA', '600-BBC TWO', '10005-ITV HD', '1100-itv 2',
               # '1101-itv2 +2', '1102-ITV 3', '1103-ITV 3 +1', '1104-ITV 4', '1107-ITV 4 +1', '1109-ITV BE', '1113-ITV BE +1', '20002-S4C HD',
               # '1525-Channel 4 +1', '1515-Channel 4 more', '1520-4 FILM', '1521-4 FILM +1', '1541-5 +1', '28008-5 USA +1', '28007-5 USA', '17013-paramount', '27000-5 SELECT', '28005-5 STAR',
               # '27000-CBS DRAMA', '27003-CBS REALITY', '4010-CBS REALITY +1', '27001-CBS JUSTICE', '27004-HORROR CHANNELS', '21010-SONY CHANNEL',
               # '21007-SONY CHANNEL +7', '4015-TOGHETER TV', '7013-FORCES TV',
               # '17009-PICK', '4020-PICK +1', '7009-FOOD', '7010-FOOD +1', '5007-DMAX', '17011-PBS AMERICA', '5005-DAVE', '5003-D DRAMA', '26000-YESTERDAY',
               # '19012-REALLY', '4027-BLAZE', '9008-HGTV', '18008-QUEST', '18006-RED QUEST', '702-BBC FOUR SD', '820-BBC NEWS HD',
               # '704-BBC PALIAMENT', '20014-SKY NEWS', '2000-ALJAZEERA EN', '7017-FREESPORT HD', '20023-SONY MOVIES', '21000-SONY MOVIES CLASSIC', '14000-SONY MOVIES ACTION',
               # '822-CBBC HD', '821-CBEEBIES', '806-BBC 5 RADIO', '703-BBC NEWS', '705-CBBC', '918-BBC Red Button', '21008-talkSPORT'])


lock = threading.Semaphore(4)


def freesat(code):
    try:
        for i in range(0, 8):
            with requests.Session() as s:
                s.mount('https://', HTTPAdapter(max_retries=10))
                url = s.get('https://www.freesat.co.uk/tv-guide/api/' + str(i) + '/?channel=' + code.split('-')[0], headers=head)
                try:
                    data = url.json()
                    for d in data[0]['event']:
                        ch = ''
                        start = datetime.fromtimestamp(d['startTime']).strftime('%Y%m%d%H%M%S')
                        end = (datetime.strptime(start, '%Y%m%d%H%M%S') + timedelta(seconds=d['duration'])).strftime('%Y%m%d%H%M%S')
                        ch += 2 * ' ' + '<programme start="' + str(start) + ' ' + time_zone + '" stop="' + str(end) + ' ' + time_zone + '" channel="' + code.split('-')[1] + '">\n'
                        ch += 4 * ' ' + '<title lang="en">' + d['name'].replace('&', 'and') + '</title>\n'
                        ch += 4 * ' ' + '<desc lang="en">' + d['description'].replace('&', 'and') + '</desc>\n  </programme>\r'
                        with io.open(EPG_ROOT + '/freesat.xml', "a", encoding='UTF-8') as f:
                            f.write(ch)
                    if 'end' in locals():
                        print("{} epg ends at : {}".format(code.split('-')[1], datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')))
                    else:
                        print("No valid 'end' found for {}".format(code.split('-')[1]))
                except Exception as e:
                    print("Error processing data: {}".format(e))
                    continue
    except Exception as e:
        print("Error in freesat function for {}: {}".format(code, e))
    finally:
        lock.release()


def main():
    print('**************FREESAT EPG******************')
    sys.stdout.flush()

    import json
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "freesat":
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    channels = [ch.split('-')[1] for ch in channels_code]

    xml_header(EPG_ROOT + '/freesat.xml', channels)

    thread_pool = []
    for url in channels_code:
        thread = threading.Thread(target=freesat, args=(url,))
        thread_pool.append(thread)
        thread.start()
        sleep(1)
        lock.acquire()
    for thread in thread_pool:
        thread.join()

    close_xml(EPG_ROOT + '/freesat.xml')

    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream os image found\nSorting data please wait.....')
        sys.stdout.flush()
        import xml.etree.ElementTree as ET
        tree = ET.parse(EPG_ROOT + '/freesat.xml')
        data = tree.getroot()
        els = data.findall("*[@channel]")
        new_els = sorted(els, key=lambda el: (el.tag, el.attrib['channel']))
        data[:] = new_els
        tree.write(EPG_ROOT + '/freesat.xml', xml_declaration=True, encoding='utf-8')

    print('**************FINISHED******************')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
