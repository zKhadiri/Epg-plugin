import requests, io, re, sys, json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from time import strftime
from __init__ import *


time_zone=tz()


uk_sports=['4010-SkySp PL HD',"3939-SkySp F'ball HD","4049-SkySp News HD",'4002-SkySpMainEvHD',
'3625-BT Sport 1 HD','3627-BT Sport 2 HD','3629-BT Sport 3 HD','4040-BTSpt//ESPNHD','1218-BTSBoxOffWWE',
'4081-SkySpCricketHD','3835-SkySp F1 HD','4022-SkySp NFL HD','3940-SkySp ArenaHD',
'4026-SkySp Golf HD','4032-SkySp Racing HD','4090-SkySp Mix HD','1035-SkySpBoxOffHD','1015-LaLigaTV HD','5153-Premier 1 HD',
'1634-Premier 2 HD','1150-FreeSports HD','1003-MUTV HD']


urls=[]
for i in range(0,7):
    week = (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d 00:00:00')
    days = datetime.strptime(week,'%Y-%m-%d 00:00:00').strftime('%s')
    for code in uk_sports:
        urls.append('https://epgservices.sky.com/5.1.1/api/2.0/channel/json/'+code.split('-')[0]+'/'+str(int(days))+'/86395/4|'+code.split('-')[1])
urls.sort()

def sky():
    for link in urls:
        try:
            with requests.Session() as s:
                s.mount('http://', HTTPAdapter(max_retries=10))
                url = s.get(link.split('|')[0]).json()
                channel_code = re.findall(r'json/(\d+)/',link)
                for data in url['listings'][''.join(channel_code)]:
                    start = datetime.fromtimestamp(data['s']).strftime('%Y%m%d%H%M%S')
                    end = (datetime.strptime(start,'%Y%m%d%H%M%S') + timedelta(seconds=data['m'][1])).strftime('%Y%m%d%H%M%S')
                    epg=''
                    epg+=2 * ' ' + '<programme start="' + start + ' '+time_zone+'" stop="' + end + ' '+time_zone+'" channel="'+link.split('|')[1]+'">\n'
                    epg+=4*' '+'<title lang="en">'+data['t'].replace('&','and')+'</title>\n'
                    epg+=4*' '+'<desc lang="en">'+data['d'].replace('&','and')+'</desc>\n  </programme>\r'
                    with io.open(EPG_ROOT+'/skyuk.xml',"a",encoding='UTF-8')as f:
                        f.write(epg)
            print(link.split('|')[1]+' epg date : '+(datetime.strptime(end,'%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')))
            sys.stdout.flush()
        except:continue

def main():
    print('**************UK SPORTS CHANNELS EPG******************')
    sys.stdout.flush()

    channels = [ch.split('-')[1] for ch in uk_sports]
    xml_header(EPG_ROOT+'/skyuk.xml',channels)
    sky()   
    close_xml(EPG_ROOT+'/skyuk.xml')
    
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
        
    for channel in data['bouquets']:
        if channel["bouquet"]=="skyuk":
            channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)
        
    print('**************FINISHED******************')
    sys.stdout.flush()


if __name__ == "__main__":
    main()
