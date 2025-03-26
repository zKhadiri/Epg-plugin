#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from .__init__ import *
except:
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

# Define the output directory
output_dir = "/etc/epgimport/ziko_epg"

headers = {
    'Host': 'elcinema.com',
    "Connection": "keep-alive",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
}

nb_channel = [
    '1353-2MTV', '1136-AbuDhabi_TV', '1312-Al_Aoula_MARROC', '1264-Al_Dafrah', '1216-Al_Jadeed_TV',
    '1174-Al_Kahera_Wal_NasTV', '1252-Al_Kahera_Wal_NasTV2', '1321-Al_Manar',
    '1223-Al_NaharDrama', '1193-Al_NaharTV', '1306-Al_Rasheed', '1339-Al_Saeedah',
    '1388-Al_Shams', '1382-AlAraby_2', '1137-Alhayat_TV', '1101-Aloula_Egy_Ch',
    '1269-AlSharqiya', '1301-Alsumaria', '1298-Amman', '1380-Atv', '1368-Bahrain_TV',
    '1309-beIN_Drama_HD1', '1322-beIN_Movies_Premiere_HD1', 
    '1323-beIN_Movies_Action_HD2', '1324-beIN_Movies_Drama_HD3', '1325-beIN_Movies_Family_HD4', 
    '1327-beIN_Series_HD1','1328-beIN_Series_HD2', '1198-CBC', '1199-CBC_Drama', '1260-CBC_sofra', '1176-Cima',
    '1385-Dijlah_TV', '1272-Discovery', '1290-DMC',
    '1292-DMC_DRAMA', '1169-Dubai_TV', '1173-DubaiOne',
    '1315-Echorouk_TV', '1119-Egyption_TV', '1135-Emirates', '1375-ETC_TV',
    '1374-HadarMout_TV', '1204-iFILM_TV', '1349-Iraqia_TV', '1314-Jordan_TV',
    '1310-Kuwait', '1341-LBC', '1168-LBCI', '1246-LDC',
    '1313-Ltv', '1336-Maspero_Zaman', '1127-MBC', '1130-MBC_Action', '1259-MBC_Bollywood',
    '1194-MBC_Drama', '1131-MBC_Drama+', '1239-MBC_MASR', '1278-MBC_MASR2', '1399-MBC_MASR_DRAMA_HD',
    '1340-MBC_Iraq', '1132-MBC_MAX', '1128-MBC2', '1241-MBC3', '1129-MBC4', '1354-MBC5',
    '1145-Mehwar', '1355-Mix', '1371-Mix_Bel_Araby', '1373-Mix_ONE', '1296-MTV-Lebanon',
    '1266-Nat_Geo_AD_HD', '1275-National_Geographic_Ch', '1304-Nessma', '1158-Nile_Comedy',
    '1156-Nile_Drama', '1159-Nile_Life', '1317-Oman', '1134-ON_Drama', '1203-ON_E',
    '1257-OSN_TV_Comedy_Ch', '1395-OSN_TV_Crime_Ch', '1232-OSN_TV_Kids', '1211-OSN_TV_Movies_Action_Ch',
    '1231-OSN_TV_Movies_Comedy_Ch', '1392-OSN_TV_Movies_Family_Ch', '1213-OSN_TV_Movies_Premiere_Ch',
    '1396-OSN_TV_Now_Ch', '1393-OSN_TV_One_Ch', '1394-OSN_TV_Showcase_Ch',
    '1390-OSN_TV_Yahala_Bil_Arabi_Ch', '1391-OSN_TV_Movies_Hollywood_Ch', '1285-Osn_Ya_Hala_Aflam_Ch',
    '1205-OSN_Ya_Hala_Ch', '1319-Qatar_TV', '1218-Rotana_Aflam+_HD_Channel',
    '1148-Rotana_Cinema_EGY', '1289-Rotana_Cinema_KSA', '1217-Rotana_Classic', '1358-Rotana_Comedy',
    '1147-Rotana_Drama', '1149-Rotana_Khalijieah_HD', '1356-Rotana_Kids', '1365-Rotana+_HD_Channel',
    '1299-Roya', '1226-Sada_El_Balad', '1279-Sada_El_Balad2', '1227-Sada_ElBalad_Drama',
    '1360-Salam_TV', '1177-Sama_Dubai', '1352-Saudiya_TV', '1297-SBC',
    '1188-Sharjah_TV', '1338-Syria_TV', '1280-TeN_TV', '1366-Thikrayat_Tv',
    '1367-Utv', '1308-Watania1', '1334-Watania2', '1383-WTV', '1261-Zee_Alwan',
]

print("*****************ELCINEMA EPG********************")
sys.stdout.flush()
# Print the number of channels available for EPG data
print("=================================================")
print("There are {} channels available for EPG data.".format(len(nb_channel)))
print("=================================================")

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
        self.titles = []
        self.now = datetime.today().strftime('%Y %m %d')
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
                        '</li>', '').replace('مساءً', 'PM').replace('صباحًا', 'AM'),'%I:%M %p')
                    hours.append(start.strftime('%H:%M'))
            else:
                if 'مساءً'.decode('utf-8') in time or 'صباحًا'.decode('utf-8') in time:
                    start = datetime.strptime(time.replace('</li>', '').replace('مساءً'.decode(
                        'utf-8'), 'PM').replace('صباحًا'.decode('utf-8'), 'AM'), '%I:%M %p')
                    hours.append(start.strftime('%H:%M'))
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_hr = 0
        for d in hours:
            h, m = list(map(int, d.split(":")))
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

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Create the directory if it doesn't exist

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
            with io.open(os.path.join(output_dir, "elcinema.xml"), "a", encoding='UTF-8') as f:
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
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)

    print('**************ELCINEMA EPG******************')
    sys.stdout.flush()

    channels = [ch.split('-')[1] for ch in nb_channel]
    xml_header(os.path.join(output_dir, "elcinema.xml"), channels)

    import time
    Hour = time.strftime("%H:%M")
    start = '00:00'
    end = '02:00'
    if start <= Hour < end:
        print('Please come back at 2am to download the EPG')
        sys.stdout.flush()
    else:
        for nb in nb_channel:
            try:
                Elcinema(nb)
            except IndexError:
                cprint('No epg found or missing data for: ' + nb.split('-')[1])
                sys.stdout.flush()
                continue


if __name__ == '__main__':
    main()
    close_xml(os.path.join(output_dir, "elcinema.xml"))

print('**************FINISHED******************')
sys.stdout.flush()