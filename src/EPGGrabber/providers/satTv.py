# -*- coding: utf-8 -*-
import requests, sys, io
from datetime import datetime, date, timedelta
from requests.adapters import HTTPAdapter
from __init__ import *

time_zone = tz()

CHANNELS = {
    5: 'AD Sports 1', 7: 'Al Arabiya', 8: 'Al Jazeera', 9: 'Al Jazeera English', 11: 'Arryadia', 12: 'Assadissa', 13: 'BBC Arabic', 15: 'BBC World News', 17: 'CNBC Europe',
    19: 'Deutsche Welle', 21: 'Dubai TV', 22: 'Euronews English', 25: 'France 24 (En)', 26: 'France 24 (Fr)', 28: 'NHK WORLD-JAPAN', 42: 'Sky News Arabia',
    49: 'Al Maghribia', 50: 'Al Aoula', 54: 'Al Jazeera Documentary', 66: 'Athaqafia', 67: 'Tamazight', 98: 'CGTN', 151: 'Medi 1 TV', 223: 'Oman TV', 225: 'Qatar TV', 226: 'Sama Dubai', 227: 'Watania 1 (Tunisie 1)',
    228: 'Al Sharqiya TV', 239: 'Al Rayyan Al Qadeem', 246: 'Noursat TV', 259: 'Abu Dhabi TV', 260: '2M Monde', 291: 'iFilm (Ar)', 293: 'Yas TV', 315: 'Al Mayadeen TV', 335: 'Jordan TV', 341: 'KTV 1',
    348: 'Sharjah TV', 349: 'Saudi 1', 358: 'Dubai Sports 1',385: 'Saudi Quran TV', 392: 'Iqraa', 424: 'TRT World',
    427: 'Al Nahar TV', 428: 'Watania 2 (Tunisie 2)', 429: 'Cartoon Network Arabic', 430: 'CBC', 431: 'CBC Drama', 432: 'CBC Sofra', 433: 'Echorouk News', 436: 'LBC Sat',
    437: 'MBC 1', 438: 'MBC 2', 439: 'MBC 4', 440: 'MBC Action', 441: 'MBC Bollywood', 442: 'MBC Drama', 443: 'MBC Max', 445: 'Nat Geo Abu Dhabi', 446: 'Nessma TV', 447: 'Rotana Cinema KSA',
    448: 'Rotana Khalijia', 449: 'Sada El Balad', 450: 'Al Hayah', 451: 'Al Hayah Mosalsalat', 453: 'DMC Drama', 454: 'DMC', 455: 'On Time Sports', 456: 'Al Hayah 2', 458: 'Al Rai TV',
    461: 'On E', 463: 'Al Kahera Wal Nas', 469: 'Dubai One', 470: 'Zee Aflam', 472: 'Echorouk TV', 474: 'MBC Masr', 476: 'Al Anwar TV', 487: 'Rotana Drama',
    488: 'El Hiwar El Tounsi', 491: 'Al Sumaria TV', 494: 'Roya TV', 495: 'Samira TV', 496: 'Zee Alwan',
    498: 'Al Oula (ERTU 1)', 503: 'France 24 (Ar)', 507: 'MBC 3', 508: 'Rotana Classic', 509: 'Al Nahar Drama',
    533: 'TV5Monde MO (Fr)', 534: 'Mazzika', 535: 'Al Araby', 537: 'Saudi Al Ekhbariya',
    554: 'Dubai Zaman', 555: 'B4U Plus', 556: 'Nile Drama', 557: 'Space Toon', 558: 'CNN International',
    561: 'Rotana Clip', 563: 'SBN', 564: 'MBC 5', 566: 'Al Kass One', 567: 'Ennahar TV', 568: 'Panorama Food',
    575: 'Rotana  Cinema Egypt', 576: 'Sada El Balad Drama', 583: 'Karbala Satellite Channel',
    591: 'DW Arabia', 592: 'Al Rayyan', 593: 'MBC Iraq', 594: 'MBC Masr 2', 596: 'Noor Dubai TV',
    611: 'Dijlah TV', 612: 'Dubai Racing', 613: 'eXtra News TV',
    621: 'Dubai Sports 3', 623: 'TRT Arabic', 624: 'Lana TV',
    628: 'Dubai Sports 2', 629: 'AD Sports 2', 630: 'Yemen Shabab TV', 631: 'Al Fujairah TV', 632: 'Chada TV', 633: 'Tunisna', 637: 'SBC', 649: 'Al Sharqiya News',
    652: 'Libya 218 News', 653: 'Al Mamlaka', 654: 'Al Aan TV', 655: 'Alghad', 657: 'Suhail TV', 659: 'Sharjah Sports', 662: 'Nile Comedy', 663: 'Nile Cinema',
    664: 'Nile Life', 665: 'TeN', 666: 'Maspero Zaman', 667: 'Al Dafrah HD', 669: 'Musawa HD',
    685: 'Mix Hollywood', 691: 'Al Emarat TV',
    696: 'Al Mehwar HD', 697: 'On Drama',
    703: 'Dubai Racing 3', 704: 'Zad TV', 705: 'Al Resalah', 707: 'Al Rahma', 708: 'AD Sports 3', 710: 'AD Sports 4', 711: 'Al Kahera Wal Nas +2', 712: 'Cima',
    715: 'Wanasah'
}

HEAD = {
    "Connection": "keep-alive",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}

def appSat():
    f = [2145763335, 1421971178, 1161237944, 1515588017]
    dates = date.today() - timedelta(days=1)
    timestamp = datetime.strptime((datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:00"), "%Y-%m-%d %H:%M:%S").strftime("%s")
    for _ in range(7):
        with requests.Session() as s:
            s.mount('http://', HTTPAdapter(max_retries=10))
            data = s.get('http://s3-eu-central-1.amazonaws.com/eutelsat-prod-content-images/epg/programs-0-{}.json.gz'.format(dates.strftime('%Y%m%d')) ,headers=HEAD).json()
        for service in data:
            if service["ch"] in CHANNELS.keys():
                times = service["ti"]
                for idx,_ in enumerate(times):
                    times[idx] ^= f[3 & idx]
                    if times[idx] >= int(timestamp):
                        event = s.get('http://eutelsat-backend.wiztivi.com/eutelsat-backend/epg/event/{}/{}'.format(service["ch"],times[idx]) ,headers=HEAD, timeout=15)
                        if "content-type" in event.headers and event.headers["content-type"].strip().startswith("application/json"):
                            event = event.json()
                        else:
                            continue
                        start = datetime.fromtimestamp(event['start'] ^ f[0]).strftime('%Y%m%d%H%M%S')
                        end = datetime.fromtimestamp(event['end'] ^ f[1]).strftime('%Y%m%d%H%M%S')
                        epg = ''
                        epg += 2 * ' ' + '<programme start="' + start + ' '+time_zone+'" stop="' + end + ' '+time_zone+'" channel="' + CHANNELS[service["ch"]] + '">\n'
                        epg += 4 * ' ' + '<title lang="en/ar">' + event["name"].replace('&', 'and').strip() + '</title>\n'
                        if not "longDesc" in event or event['longDesc'] == None:
                            epg += 4 * ' ' + '<desc lang="en">No synopsis available for this programme</desc>\n  </programme>\r'
                        else:
                            epg += 4 * ' ' + '<desc lang="en/ar">' + event['longDesc'].replace('&', 'and').strip() + '</desc>\n  </programme>\r'
                        with io.open(EPG_ROOT + '/satTv.xml', "a", encoding='UTF-8')as _file:
                            _file.write(epg)
                print(CHANNELS[service["ch"]],dates)
                sys.stdout.flush()
        dates += timedelta(days=2)

def main():
    print('**************SatTv EPG******************')
    sys.stdout.flush()
 
    xml_header(EPG_ROOT + '/satTv.xml', list(CHANNELS.values()))

    try:
        appSat()
    except Exception as e:
        print(e)
        sys.stdout.flush()

    close_xml(EPG_ROOT + '/satTv.xml')

    provider = __file__.rpartition('/')[-1].replace('.py', '')
    update_status(provider)
    if os.path.exists('/var/lib/dpkg/status'):
        print('Dream os image found\nSorting data please wait.....')
        sortXML('satTv.xml')

    print("**************FINISHED******************")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
