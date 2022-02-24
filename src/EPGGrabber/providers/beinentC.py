#!/usr/bin/python
# -*- coding: utf-8 -*-


try:
	from .__init__ import *
except:
	from __init__ import *

import re
import sys
import io
import json
from datetime import timedelta

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import datetime
week = datetime.date.today() + timedelta(days=7)
from datetime import datetime
from time import strftime

milli = (datetime.strptime('' + str(week) + ' 23:59:59', "%Y-%m-%d %H:%M:%S").strftime("%s")) + '.999'
today = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d')) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").strftime('%s')

ch_code = ['81-beIN Movie 1', '82-beIN Movie 2', '83-beIN Movie 3', '90-beIN Movie 4HD', '112-Series 1HD', '175-beIN Series 2 HD', '174-beIN Drama HD', '170-beIN Gourmet HD', '91-beJuniors', '100-Jeem', '99-Baraem']


time_zone = tz()


head = {
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	"x-an-webservice-identitykey": "t1Th55UviStev8p2urOv4fOtraDaBr1f"
}


def beINent():
    for code in ch_code:
        query = {
            "languageId": "ara",
            "filter": '{"$and":[{"id_channel":{"$in":[' + code.split('-')[0] + ']}},{"endutc":{"$ge":' + today + '}},{"startutc":{"$le":' + milli + '}}]}'
        }
        url = requests.get('https://proxies-beinmena.portail.alphanetworks.be/cms/epg/filtered', headers=head, params=query, verify=False).json()
        if url['status'] == False:
            print('Invalid API Key')
            break
        else:
            for data in url['result']['epg']['chan_' + code.split('-')[0]]:
                start = datetime.fromtimestamp(int(data['startutc'])).strftime('%Y%m%d%H%M%S')
                end = datetime.fromtimestamp(int(data['endutc'])).strftime('%Y%m%d%H%M%S')
                ch = ''
                ch += 2 * ' ' + '<programme start="' + start + ' ' + time_zone + '" stop="' + end + ' ' + time_zone + '" channel="' + code.split('-')[1] + '">\n'
                ch += 4 * ' ' + '<title lang="en">' + data['title'].replace('&', 'and').strip() + '</title>\n'
                ch += 4 * ' ' + '<desc lang="en">' + data['synopsis'].strip().replace('&', 'and') + '</desc>\n  </programme>\r'
                with io.open('/etc/epgimport/ziko_epg/beinentC.xml', 'a', encoding="utf-8") as f:
                    f.write(ch)

            endtime = datetime.strptime(start, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')
            print(code.split('-')[1] + ' epg ends at ' + endtime)
            sys.stdout.flush()


def main():
    print('**************BEIN ENTERTAINMENT EPG******************')
    sys.stdout.flush()

    channels = [ch.split('-')[1] for ch in ch_code]
    xml_header(EPG_ROOT + '/beinentC.xml', channels)

    beINent()

    close_xml(EPG_ROOT + '/beinentC.xml')

    provider = __file__.rpartition('/')[-1].replace('.py', '')
    update_status(provider)

    print("**************FINISHED******************")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
