import requests,re,io,sys,json,ssl
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter
from time import sleep
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


channels_code=['9077', '9074', '318', '9073', '9095', '9103', '9100', '9101', '9034', 
               '129', '9050', '9039', '10254', '10515', '472', '320', '7767', '8714', '931',
                '467', '10135', '461', '9113', '9115', '460', '8128', '9042', '9047', '7427', 
                '9044', '641', '929', '7507','8453','588','364','6624','10458','10469','10464',
                '10454','6601','6621','6602','5007','6622','5023','6608','6623','362','895','445',
                '446','10918','9099','8753','9096','8434','10774','9057','9060','9055','10518',
                '9037','10517','10096','120','8336','8131','9513','9893','10095','10097','10467']
channels_code.sort()
today = (datetime.today() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:00:00Z')

with io.open("/etc/epgimport/skyit.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/bouquets.json', 'r') as f:
    jsData = json.load(f)
for channel in jsData['bouquets']:
    if channel["name"]=="SKY IT":    
        for x in channel['channels']:
            with io.open("/etc/epgimport/skyit.xml","a",encoding='UTF-8')as f:
                f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8')) 
channels=[]
def skyit():
    for code in channels_code:
        with requests.Session() as s:
            s.mount('https://', HTTPAdapter(max_retries=10))
            ssl._create_default_https_context = ssl._create_unverified_context
            url = s.get('https://apid.sky.it/gtv/v1/events?pageSize=380&pageNum=0&from='+today+'&env=DTH&channels='+code,timeout=5,verify=False).json()
            for data in url['events']:
                channel_name =  data["channel"]['name']
                title = re.sub(r"\s+", " ", data['eventTitle'].strip())
                epg =''
                start = datetime.strptime(data['starttime'],'%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d%H%M%S')
                end = datetime.strptime(data['endtime'],'%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d%H%M%S')
                epg+=2 * ' ' + '<programme start="' + start + ' +0000" stop="' + end + ' +0000" channel="'+channel_name+'">\n'
                epg+=4*' '+'<title lang="it">'+title.replace('&','and')+'</title>\n'
                epg+=4*' '+'<desc lang="it">'+data['eventSynopsis'].replace('&','and')+'</desc>\n  </programme>\r'
                with io.open("/etc/epgimport/skyit.xml","a",encoding='UTF-8')as f:
                    f.write(epg)
            print channel_name+' ends at '+data['endtime'].replace('T',' ').replace('Z','')
            channels.append(channel_name)
            sys.stdout.flush()
    channels.sort()
    update(channels)

def update(chan):
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/bouquets.json', 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["name"]=="SKY IT":
            channel['channels']=sorted([ch for ch in list(dict.fromkeys(chan))])
    with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/bouquets.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__': 
    skyit()

with io.open("/etc/epgimport/skyit.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
    data = json.load(f)
for channel in data['bouquets']:
    if channel["bouquet"]=="skyit":
        channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
    json.dump(data, f)