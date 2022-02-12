#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __init__ import *

import requests
import re
import io
import sys
import os
import ssl
from datetime import datetime, timedelta
from time import sleep, strftime
from requests.adapters import HTTPAdapter
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

headers = {
    'Host': 'elcinema.com',
    "Connection": "keep-alive",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
}

nb_channel = ['1173-DubaiOne', '1223-Al_NaharDrama', '1169-Dubai_TV', '1137-Alhayat_TV', '1199-CBC_Drama', '1176-Cima', '1227-Sada_ElBalad_Drama',
              '1198-CBC', '1177-Sama_Dubai', '1193-Al_NaharTV', '1246-LDC', '1135-Emirates', '1159-Nile_Life', '1158-Nile_Comedy',
              '1174-Al_Kahera_Wal_NasTV', '1216-Al_JadeedTV', '1226-Sada_El_Balad', '1168-LBCI', '1252-Al_Kahera_Wal_NasTV2', '1264-Al_Dafrah', '1372-Beurtv',
              '1203-ONE', '1101-Aloula', '1134-ONDrama', '1283-Dubai_Zaman', '1188-Sharjah_TV', '1315-EchoroukTV', '1300-Syria_Drama', '1370-Khallik_Bilbait',
              '1279-Sada_El_Balad2', '1313-Lana', '1269-AlSharqiya', '1242-Network_Arabic', '1280-TeNTV', '1298-Amman', '1343-Musawa', '1145-Mehwar',
              '1156-Nile_Drama', '1292-DMC_DRAMA', '1136-AbuDhabi_TV', '1297-SBC', '1301-Alsumaria', '1312-Al_Aoula_Morocco', '1321-almanar', '1334-Watania2',
              '1299-Roya', '1310-Kuwait', '1304-Nessma', '1336-Maspero_Zaman', '1308-Watania1', '1204-iFILM_TV', '1306-Alrasheed', '1341-LBC',
              '1338-Syria_TV', '1339-AlSaeedah', '1366-Thikrayat_Tv', '1353-2MTV', '1352-Saudiya_TV', '1367-Utv', '1355-Mix', '1350-SamaTV', '1369-Qurain',
              '1296-MTV', '1260-CBC_sofra', '1290-DMC', '1129-MBC4', '1132-MBC_MAX', '1259-MBC_Bollywood', '1130-MBC_Action', '1239-MBC_Egypt', '1340-MBC_Iraq',
              '1127-MBC', '1241-MBC3', '1278-MBC_MASR2', '1194-MBC_Drama', '1354-MBC5', '1128-MBC2', '1131-MBC_Drama+', '1371-Mix_Bel_Araby']


time_zone = tz()

REDC = '\033[31m'
ENDC = '\033[m'


def cprint(text):
    print(REDC + text + ENDC)


class Elcinema:

    def __init__(self, channel):
        self.getData(channel)
        self.prog_start = []
        self.prog_end = []
        self.description = []
        self.now = datetime.today().strftime('%Y %m %d')
        self.titles = []
        self.Toxml(channel)

    def getData(self, ch):
        with requests.Session() as s:
            ssl._create_default_https_context = ssl._create_unverified_context
            s.mount('https://', HTTPAdapter(max_retries=100))
            url = s.get('https://elcinema.com/tvguide/' +
                        ch.split('-')[0] + '/', headers=headers, verify=False)
            self.data = url.text

    def Starttime(self):
        hours = []
        for time in re.findall(r'(\d\d\:\d\d.*)', self.data):
            if PY3:
                if 'مساءً' in time or 'صباحًا' in time:
                    start = datetime.strptime(time.replace(
                        '</li>', '').replace('مساءً', 'PM').replace('صباحًا', 'AM'), '%I:%M %p')
                    hours.append(start.strftime('%H:%M'))
            else:
                if 'مساءً'.decode('utf-8') in time or 'صباحًا'.decode('utf-8') in time:
                    start = datetime.strptime(time.replace('</li>', '').replace('مساءً'.decode(
                        'utf-8'), 'PM').replace('صباحًا'.decode('utf-8'), 'AM'), '%I:%M %p')
                    hours.append(start.strftime('%H:%M'))
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_hr = 0
        for d in hours:
            h, m = map(int, d.split(":"))
            if last_hr > h:
                today += + timedelta(days=1)
            last_hr = h
            self.prog_start.append(today + timedelta(hours=h, minutes=m))

        return self.prog_start

    def Endtime(self):
        minutes = []
        for end in re.findall(r'\"subheader\">\[(\d+)', self.data):
            minutes.append(int(end))
        start = datetime.strptime(datetime.strptime(str(self.Starttime(
        )[0]), '%Y-%m-%d %H:%M:%S').strftime('%Y %m %d %H:%M'), '%Y %m %d %H:%M')
        for m in minutes:
            x = start + timedelta(minutes=m)
            start += timedelta(minutes=m)
            self.prog_end.append(x)

        return self.prog_end

    def GetDes(self):
        for f, l in zip(re.findall(r'<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>', self.data), re.findall(r"<span class='hide'>[^\n]+", self.data)):
            self.description.append(
                f + l.replace("<span class='hide'>", '').replace('</span></li>', ''))
        return self.description

    def Gettitle(self):
        self.title = re.findall(
            r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li', self.data)
        mt = re.findall(
            r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>', self.data)
        for m in mt:
            if m[0] == '' and m[1] == '':
                if PY3:
                    self.titles.append("يتعذر الحصول على معلومات هذا البرنامج")
                else:
                    self.titles.append(
                        "يتعذر الحصول على معلومات هذا البرنامج".decode('utf-8'))
            elif m[0] == '':
                self.titles.append(m[1])
            else:
                self.titles.append(m[0])
        for index, element in enumerate(self.titles):
            if element not in self.title:
                if PY3:
                    self.GetDes().insert(index, "يتعذر الحصول على معلومات هذا البرنامج")
                else:
                    self.GetDes().insert(index, "يتعذر الحصول على معلومات هذا البرنامج".decode('utf-8'))

        return self.titles

    def Toxml(self, channel):
        for elem, next_elem, title, des in zip(self.Starttime(), self.Endtime(), self.Gettitle(), self.GetDes()):
            ch = ''
            startime = datetime.strptime(
                str(elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            endtime = datetime.strptime(
                str(next_elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            ch += 2 * ' ' + '<programme start="' + startime + ' ' + time_zone + '" stop="' + \
                endtime + ' ' + time_zone + '" channel="' + \
                channel.split('-')[1] + '">\n'
            ch += 4 * ' ' + '<title lang="ar">' + \
                title.replace('&#39;', "'").replace(
                    '&quot;', '"').replace('&amp;', 'and') + '</title>\n'
            ch += 4 * ' ' + '<desc lang="ar">' + des.replace('&#39;', "'").replace('&quot;', '"').replace(
                '&amp;', 'and').replace('(', '').replace(')', '').strip() + '</desc>\n  </programme>\r'
            with io.open(EPG_ROOT + "/elcinema.xml", "a", encoding='UTF-8')as f:
                f.write(ch)

        print(channel.split('-')[1] +
              ' epg ends at : ' + str(self.Endtime()[-1]))
        sys.stdout.flush()


def main():
    from datetime import datetime
    import json
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "elcin":
            channel['date'] = datetime.today().strftime(
                '%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    print('**************ELCINEMA EPG******************')
    sys.stdout.flush()

    channels = [ch.split('-')[1] for ch in nb_channel]
    xml_header(EPG_ROOT + "/elcinema.xml", channels)

    import time
    Hour = time.strftime("%H:%M")
    start = '00:00'
    end = '02:00'
    if Hour >= start and Hour < end:
        print('Please come back at 2am to download the epg')
        sys.stdout.flush()
    else:
        for nb in nb_channel:
            try:
                Elcinema(nb)
            except IndexError:
                cprint('No epg found or missing data for : ' +
                       nb.split('-')[1])
                sys.stdout.flush()
                continue


if __name__ == '__main__':
    main()

    close_xml(EPG_ROOT + "/elcinema.xml")

    print('**************FINISHED******************')
    sys.stdout.flush()
