#!/usr/bin/python
# -*- coding: utf-8 -*-

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

time_zone = tz()

head = {
    "Content-Type": "application/json; charset=utf-8",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36"
}

channels_code = sorted(['505-BBC ONE SD', '555-BBC ONE HD', '700-BBC TWO HD', '818-BBC Three HD', '1011-ITV', '1500-Channel 4 HD', '1547-Channel 5 HD',
               '819-BBC FOUR HD', '710-BBC Scotland HD', '709-BBC Scotland', '701-BBC THREE', '707-BBC ALBA', '600-BBC TWO', '10005-ITV HD', '1100-itv 2',
               '1101-itv2 +2', '1102-ITV 3', '1103-ITV 3 +1', '1104-ITV 4', '1107-ITV 4 +1', '1109-ITV BE', '1113-ITV BE +1', '20002-S4C HD',
               '1525-Channel 4 +1', '1515-Channel 4 more', '1520-4 FILM', '1521-4 FILM +1', '1541-5 +1', '28008-5 USA +1', '28007-5 USA', '17013-paramount', '27000-5 SELECT', '28005-5 STAR',
               '27000-CBS DRAMA', '27003-CBS REALITY', '4010-CBS REALITY +1', '27001-CBS JUSTICE', '27004-HORROR CHANNELS', '21010-SONY CHANNEL',
               '21007-SONY CHANNEL +7', '4015-TOGHETER TV', '7013-FORCES TV',
               '17009-PICK', '4020-PICK +1', '7009-FOOD', '7010-FOOD +1', '5007-DMAX', '17011-PBS AMERICA', '5005-DAVE', '5003-D DRAMA', '26000-YESTERDAY',
               '19012-REALLY', '4027-BLAZE', '9008-HGTV', '18008-QUEST', '18006-RED QUEST', '702-BBC FOUR SD', '820-BBC NEWS HD',
               '704-BBC PALIAMENT', '20014-SKY NEWS', '2000-ALJAZEERA EN', '7017-FREESPORT HD', '20023-SONY MOVIES', '21000-SONY MOVIES CLASSIC', '14000-SONY MOVIES ACTION',
               '822-CBBC HD', '821-CBEEBIES', '806-BBC 5 RADIO', '703-BBC NEWS', '705-CBBC', '918-BBC Red Button', '21008-talkSPORT'])


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
                        with io.open(EPG_ROOT + '/freesat.xml', "a", encoding='UTF-8')as f:
                            f.write(ch)
                except:
                    continue
        print(code.split('-')[1] + ' epg ends at : ' + (datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')))
        sys.stdout.flush()
        lock.release()
    except:
        pass


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
