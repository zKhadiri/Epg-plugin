# -*- coding: utf-8 -*-

import requests
import re
import io
import json
import sys
from datetime import datetime, timedelta
from __init__ import *

urls = ['https://www.setantaeurasia.com/en/tv-schedule.html|SETANTA1', 'https://www.setantaeurasia.com/en/tv-schedule.html?channel=plus|SETANTA2']


def setanta():
    times = []
    epg = []
    for link in urls:
        url = requests.get(link.split('|')[0])
        time = re.findall(r'\d+\">(\d{2}:\d{2})', url.text)
        titles = re.findall(r'\d+\">\d{2}:\d{2}\s+(.*?)<\/div', url.text)
        des = re.findall(r'rel=\"descr\d+\">(.*?)<\/div>', url.text)

        times[:] = []
        epg[:] = []

        if len(time) > 0:
            if time[0] <= '23:59':
                today = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            if time[0] == '00:00':
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            last_hr = 0
            for d in time:
                h, m = map(int, d.split(":"))
                if last_hr > h:
                    today += + timedelta(days=1)
                last_hr = h
                times.append(today + timedelta(hours=h, minutes=m))

            for elem, next_elem, title, des in zip(times, times[1:] + [times[0]], titles, des):
                ch = ''
                startime = datetime.strptime(str(elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(str(next_elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                ch += 2 * ' ' + '<programme start="' + startime + ' +0000" stop="' + endtime + ' +0000" channel="' + link.split('|')[1] + '">\n'
                ch += 4 * ' ' + '<title lang="en">' + title.replace('არ გადაიცემა საქართველოში'.decode('utf-8'), "").replace('&', 'and').strip() + '</title>\n'
                if des.strip() == "":
                    ch += 4 * ' ' + '<desc lang="en">Setanta Sports Eurasia</desc>\n  </programme>\r'
                else:
                    ch += 4 * ' ' + '<desc lang="en">' + des.replace('&', "and").strip() + '</desc>\n  </programme>\r'
                epg.append(ch)

            print(link.split('|')[1].lower() + ' epg ends at ' + str(times[-1]))
            sys.stdout.flush()
            epg.pop(-1)
            for prog in epg:
                with io.open(EPG_ROOT + '/setanta.xml', "a", encoding='UTF-8')as f:
                    f.write(prog)
        else:
            print('no data found for ' + link.split('|')[1].lower())


def main():
    print('**************SETANTA Eurasia EPG******************')
    sys.stdout.flush()

    channels = [ch.split('|')[1] for ch in urls]
    xml_header(EPG_ROOT + '/setanta.xml', channels)
    setanta()

    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "setanta":
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    close_xml(EPG_ROOT + '/setanta.xml')

    print('**************FINISHED******************')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
