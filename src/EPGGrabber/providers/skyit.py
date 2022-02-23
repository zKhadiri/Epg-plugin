import requests
import re
import io
import sys
import json
import ssl
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from time import strftime
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

from __init__ import *

channels_code = sorted(['9077', '9074', '318', '9073', '9095', '9103', '9100', '9101', '9034',
               '129', '9050', '9039', '10254', '10515', '472', '320', '7767', '8714', '931',
                '467', '10135', '461', '9113', '9115', '460', '8128', '9042', '9047', '7427',
                '9044', '641', '929', '7507', '8453', '588', '364', '6624', '10458', '10469', '10464',
                '10454', '6601', '6621', '6602', '5007', '6622', '5023', '6608', '6623', '362', '895', '445',
                '446', '10918', '9099', '8753', '9096', '8434', '10774', '9057', '9060', '9055', '10518',
                '9037', '10517', '10096', '120', '8336', '8131', '9513', '9893', '10095', '10097', '10467', '9098', '9114', '635',
                '8473', '10133', '9774', '10136', '8353', '11055', '8007', '974', '7588', '10914', '10466', '8173', '10465', '8933', '10469', '6000', '807', '10093', '10654', '9059', '331', '125', '9054', '123', '321', '10354', '8329', '6630', '6628', '10653', '10893', '944', '9553', '7527', '7587', '9194', '10916', '10468'])

today = (datetime.today() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:00:00Z')


channels = []


def skyit():
    for code in channels_code:
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=10))
            ssl._create_default_https_context = ssl._create_unverified_context
            url = s.get('https://apid.sky.it/gtv/v1/events?pageSize=380&pageNum=0&from=' + today + '&env=DTH&channels=' + code, timeout=5, verify=False).json()
            for data in url['events']:
                channel_name = data["channel"]['name']
                title = re.sub(r"\s+", " ", data['eventTitle'].strip())
                epg = ''
                start = datetime.strptime(data['starttime'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d%H%M%S')
                end = datetime.strptime(data['endtime'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d%H%M%S')
                epg += 2 * ' ' + '<programme start="' + start + ' +0000" stop="' + end + ' +0000" channel="' + channel_name + '">\n'
                epg += 4 * ' ' + '<title lang="it">' + title.replace('&', 'and') + '</title>\n'
                epg += 4 * ' ' + '<desc lang="it">' + data['eventSynopsis'].replace('&', 'and') + '</desc>\n  </programme>\r'
                with io.open(EPG_ROOT + '/skyit.xml', "a", encoding='UTF-8')as f:
                    f.write(epg)
            try:
                print(channel_name + ' ends at ' + data['endtime'].replace('T', ' ').replace('Z', ''))
                sys.stdout.flush()
                channels.append(channel_name)
            except:
                pass
    channels.sort()
    update_channels("SKY IT",channels)

def main():
    print('**************SKY IT EPG******************')
    sys.stdout.flush()
            
    channels = get_channels("SKY IT")
    xml_header(EPG_ROOT + '/skyit.xml', channels)

    skyit()

    close_xml(EPG_ROOT + '/skyit.xml')
    provider = __file__.rpartition('/')[-1].replace('.py', '')
    update_status(provider)

    print('**************FINISHED******************')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
