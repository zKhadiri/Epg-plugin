# -*- coding: utf-8 -*-
import csv
import requests
import sys
import re
import io
from datetime import datetime, timedelta
from __init__ import *

if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

today = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')


def rotana(this_month, channel):
    with requests.Session() as s:
        url = s.get('https://rotana.net/triAssets/uploads/{}/{}.csv'.format(this_month, channel))
    decoded_content = url.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

    start_dt = []
    end_dt = []
    titles = []
    descriptions = []
    actors = []
    genre = []
    for rows in my_list[1:]:
        start_dt.append(' '.join(rows[1:][2:4]))
        end_dt.append(' '.join((rows[1:][4:6])))
        titles.append(rows[1:][1])
        descriptions.append(rows[1:][7])
        actors.append(rows[1:][8])
        genre.append(rows[1:][12])

    for title, des, start, end, ed, actor, g in zip(titles, descriptions, start_dt, start_dt[1:] + [start_dt[0]], end_dt, actors, genre):
        if start >= today:
            ch = ''
            if start_dt[-1] == start and start_dt[0] == end:
                try:
                        startime = datetime.strptime(start, '%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(end, '%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                except:
                        pass
            else:
                try:
                        startime = datetime.strptime(start, '%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(end, '%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                except:
                        pass

            ch += 2 * ' ' + '<programme start="' + startime + ' +0000" stop="' + endtime + ' +0000" channel="' + channel + '">\n'

            if '-' in title:
                ch += 4 * ' ' + '<title lang="ar">' + title.split('-', 1)[0].strip() + '</title>\n'
                ch += 4 * ' ' + '<desc lang="ar">' + title.split('-', 1)[1].strip() + '</desc>\n  </programme>\r'
            else:
                ch += 4 * ' ' + '<title lang="ar">' + title + '</title>\n'
                if des == '' and actor != '':
                    ch += 4 * ' ' + '<desc lang="ar">' + actor + '</desc>\n  </programme>\r'
                elif des != '' and actor == '':
                    ch += 4 * ' ' + '<desc lang="ar">' + des + '</desc>\n  </programme>\r'
                elif des == '' and actor == '' and g != '':
                    ch += 4 * ' ' + '<desc lang="en">' + g + '</desc>\n  </programme>\r'
                else:
                    ch += 4 * ' ' + '<desc lang="ar">يتعذر الحصول على معلومات هذا البرنامج</desc>\n  </programme>\r'

            with io.open(EPG_ROOT + '/rotana.xml', "a", encoding='UTF-8')as f:
                if not PY3:
                    f.write(ch.decode('utf-8'))
                else:
                    f.write(ch)

    print(channel + ' EPG ends at ' + end_dt[-1])
    sys.stdout.flush()


def main():
    print('**************Rotana EPG******************')
    sys.stdout.flush()
    provider = __file__.rpartition('/')[-1].replace('.py', '')
    channels = get_channels("Rotana")
    update_status(provider)
    xml_header(EPG_ROOT + '/rotana.xml', channels)
    url = requests.get('https://rotana.net/%D8%AC%D8%AF%D9%88%D9%84-%D8%A7%D9%84%D8%A8%D8%B1%D8%A7%D9%85%D8%AC/')
    date = re.findall(r'csv\":\"https:\\\/\\\/rotana.net\\\/triAssets\\\/uploads\\\/(\d{4}\W{2}\d{2})\W{2}', url.text)[0].replace('\/', '/')
    channel_code = re.findall(r'/\d+\\/\d+\\/(.*?).csv\"', url.text)
    channel_code = [ch for ch in channel_code if not '.png' in ch]
    for code in channel_code:
        rotana(date, code)
    close_xml(EPG_ROOT + '/rotana.xml')
    update_channels("Rotana", channel_code)
    print('**************FINISHED******************')
    sys.stdout.flush()


if __name__ == "__main__":
    main()
