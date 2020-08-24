#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,sys,io,json
from datetime import timedelta


import datetime
week = datetime.date.today() + timedelta(days=7)
from datetime import datetime
milli = (datetime.strptime('' + str(week) + ' 23:59:59', "%Y-%m-%d %H:%M:%S").strftime("%s"))+'.999'
today = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d'))+' 00:00:00',"%Y-%m-%d %H:%M:%S").strftime('%s')

ch_code =['74-SportsGlobalHD','75-News_ar','65-HD1','66-HD2','67-HD3','68-HD4',
          '69-HD5','70-HD6','71-HD7','72-HD8','73-HD9','58-HD10','59-SportsHD11'
          ,'60-SportsHD12','61-SportsHD13','62-SportsHD14','63-SportsHD15','64-SportsHD16','80-SportsHD17']

with io.open("/etc/epgimport/bein.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for code in ch_code:
    with io.open("/etc/epgimport/bein.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+code.split('-')[1]+'">'+"\n"+'    <display-name lang="en">'+code.split('-')[1]+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8')) 
print('**************BEIN SPORTS EPG******************')
sys.stdout.flush()
for code in ch_code: 
    query ={
        "languageId": "ara",
        "filter": '{"$and":[{"id_channel":{"$in":['+code.split('-')[0]+']}},{"endutc":{"$ge":'+today+'}},{"startutc":{"$le":'+milli+'}}]}'
    }
    url = requests.get('https://proxies-beinmena.portail.alphanetworks.be/cms/epg/filtered',params=query).json()
    for data in url['result']['epg']['chan_'+code.split('-')[0]]:
        start= datetime.fromtimestamp(int(data['startutc'])).strftime('%Y%m%d%H%M%S') 
        end = datetime.fromtimestamp(int(data['endutc'])).strftime('%Y%m%d%H%M%S')
        title = data['title'].replace('   ',' ').split('- ')[0]
        if 'Qatar Stars League' in data['title']:
            extra = 'دوري نجوم قطر'.decode('utf-8')
        elif 'Moroccan League' in data['title']:
            extra = 'الدوري المغربي الممتاز'.decode('utf-8')
        elif 'Review' in data['title']:
            extra = 'حصيلة الدوريات'.decode('utf-8')
        elif 'English Premier League' in data['title']:
            extra = 'الدوري الإنجليزي الممتاز'.decode('utf-8')
        elif 'Spanish La Liga' in data['title']:
            extra = 'الدوري الإسباني لكرة القدم'.decode('utf-8')
        elif 'Italian Serie A' in data['title']:
            extra = 'الدوري الإيطالي لكرة القدم'.decode('utf-8')
        elif 'French Ligue 1' in data['title']:
            extra = 'الدوري الفرنسي'.decode('utf-8')
        elif 'Copa Libertadores' in data['title']:
            extra = 'كأس ليبرتادوريس'.decode('utf-8')
        elif 'Indy' in data['title']:
            extra = 'رياضة السيارات'.decode('utf-8')
        elif 'MotoGP' in data['title']:
            extra = 'بطولة العالم للدراجات النارية'.decode('utf-8')
        elif 'Pre Season Friendly' in data['title']:
            extra = 'كرة قدم'.decode('utf-8')
        elif 'NBA' in data['title']:
            extra = 'الدوري الأميركي لكرة السلة'.decode('utf-8')
        elif 'WTA' in data['title']:
            extra = 'تنس'.decode('utf-8')
        elif 'Mini Match' in data['title']:
            extra = 'مباريات قصيرة'.decode('utf-8')
        elif 'Major League Baseball' in data['title']:
            extra = 'كرة القاعدة'.decode('utf-8')
        elif 'UEFA Champions League' in data['title']:
            extra = 'دوري أبطال أوروبا لكرة القدم'.decode('utf-8')
        elif 'UEFA Europa League' in data['title']:
            extra = 'الدوري الأوروبي'.decode('utf-8')
        elif 'Cricket' in data['title']:
            extra = 'كريكيت'.decode('utf-8')
        elif 'Sports News' in data['title']:
            extra = 'الأخبار الرياضية'.decode('utf-8')
        elif 'Handball' in data['title']:
            extra = 'كرة اليد'.decode('utf-8')
        elif 'EPL World' in data['title']:
            extra = 'عالم الدوري الانجليزي الممتاز'.decode('utf-8')
        elif 'CAF Champions League' in data['title']:
            extra = 'دوري أبطال أفريقيا'.decode('utf-8')
        else:
            extra = 'الرياضة العام'.decode('utf-8')
        spl = re.search(r'-\s(.*)',title)
        ch = ''
        ch+=2*' '+'<programme start="'+start+' +0000" stop="'+end+' +0000" channel="'+code.split('-')[1]+'">\n'
        if spl != None:
            ch+=4*' '+'<title lang="en">'+spl.group().replace('&','and')+' - '+extra+'</title>\n'
        else:
            ch+=4*' '+'<title lang="en">'+title.replace('&','and').strip()+' - '+extra+'</title>\n'
        if data['synopsis'].strip()==u'' and ' -' in data['title']:
            ch+=4*' '+'<desc lang="en">'+data['title'].split(' -')[1].strip().replace('&','and')+'</desc>\n  </programme>\r'
        elif data['synopsis'].strip() == u'':
            ch+=4*' '+'<desc lang="en">'+title.replace('&','and')+'</desc>\n  </programme>\r'
        else:
            ch+=4*' '+'<desc lang="en">'+data['synopsis'].strip().replace('&','and')+'</desc>\n  </programme>\r'
        endtime = datetime.strptime(start,'%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M')
        
        with io.open('/etc/epgimport/bein.xml','a',encoding="utf-8") as f:
            f.write(ch)
    print code.split('-')[1]+' epg ends at '+endtime
    sys.stdout.flush()

with io.open("/etc/epgimport/bein.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    

with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
    data = json.load(f)
for bouquet in data['bouquets']:
    if bouquet["bouquet"]=="bein":
        bouquet['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
    json.dump(data, f)    

print("**************FINISHED******************")
sys.stdout.flush()