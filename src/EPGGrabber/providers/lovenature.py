# -*- coding: utf-8 -*-
import requests, json, sys, io
from datetime import datetime, date , timedelta
from __init__ import *

dst = requests.get('https://tvlistings.gracenote.com/gapzap_webapi/api/Providers/GetDstOffsetForPostalByCountry/M4S1A4/CAN/en').json()

yesterday = date.today() - timedelta(days=1)
timestamp = datetime.strptime(str(yesterday) + ' 06:00:00', "%Y-%m-%d %H:%M:%S").strftime("%s")

payload = {
    "timespan": "336",
    "timestamp": timestamp,
    "prgsvcid": "52745",
    "headendId": "0005580",
    "countryCode": "CAN",
    "postalCode": "M4S1A4",
    "device": "X",
    "userId": "-",
    "aid": "lovenature",
    "DSTUTCOffset": "-240",
    "STDUTCOffset": "-300",
    "DSTStart": dst["DSTStart"],
    "DSTEnd": dst["DSTEnd"],
    "languagecode": "en"
}

synopsis_all = {}


def getSynopsis(id, title):
    synopsis_payload = payload
    synopsis_payload['programSeriesID'] = id
    synopsis_payload['season'] = -1
    synopsis_payload['pageSize'] = 100
    synopsis_payload['pageNo'] = 1
    synopsis_payload['headendId'] = "0005580"
    try:
        if title in synopsis_all:
            return synopsis_all[title]
        else:
            data = requests.post('https://tvlistings.gracenote.com/api/program/episodeGuide',json=synopsis_payload).json()
            synopsis_all[title] = data['episodeGuideTab']['season']['episodes'][0]['synopsis']
            return data['episodeGuideTab']['season']['episodes'][0]['synopsis']
    except KeyError:
        return None

def guide():
    data = requests.post("https://tvlistings.gracenote.com/api/sslgrid",json=payload).json()
    for key in data.keys():
        if datetime.strptime(key,"%Y-%m-%d").date() >= date.today():
            for prog in data[key]:
                prog_start = datetime.fromtimestamp(prog['startTime']).strftime('%Y%m%d%H%M%S')
                prog_end = datetime.fromtimestamp(prog['endTime']).strftime('%Y%m%d%H%M%S')
                epg = ''
                epg += 2 * ' ' + '<programme start="' + prog_start + ' -0800" stop="' + prog_end + ' -0800" channel="lovenature">\n'
                if prog['program']['episodeTitle'] != None:
                    epg += 4 * ' ' + '<title lang="en">' + prog['program']['title'].replace('&', 'and') + ' "'+prog['program']['episodeTitle'].replace('&', 'and')+'"'+'</title>\n'
                else:
                    epg += 4 * ' ' + '<title lang="en">' + prog['program']['title'].replace('&', 'and') + '</title>\n'
                if prog['program']['shortDesc'] == None:
                    _synopsis = getSynopsis(prog['program']['seriesId'], prog['program']['title'])
                    if _synopsis != None:
                        epg += 4 * ' ' + '<desc lang="en">' + _synopsis.replace('&', 'and') + '</desc>\n  </programme>\r'
                    else:
                        epg += 4 * ' ' + '<desc lang="en">Love Nature</desc>\n  </programme>\r'
                else:
                    epg += 4 * ' ' + '<desc lang="en">' + prog['program']['shortDesc'].replace('&', 'and') + '</desc>\n  </programme>\r'
                with io.open(EPG_ROOT + '/lovenature.xml', "a", encoding='UTF-8')as f:
                    f.write(epg)
    print('Love Nature EPG ends at : ' + key)
    sys.stdout.flush()

def main():
    print('**************Love Nature EPG******************')
    sys.stdout.flush()

    xml_header(EPG_ROOT + '/lovenature.xml', ["lovenature"])

    guide()

    close_xml(EPG_ROOT + '/lovenature.xml')
    provider = __file__.rpartition('/')[-1].replace('.py', '')
    update_status(provider)

    print("**************FINISHED******************")
    sys.stdout.flush()


if __name__ == "__main__":
    main()

