# -*- coding: utf-8 -*-
import requests,io,re,ch,os,sys
from datetime import datetime,timedelta
from requests.adapters import HTTPAdapter


channels_code=['4945-Dubai One HD','2250-Abu Dhabi TV HD','2249-Al Emarat TV HD','2248-Abu Dhabi Drama HD','3675-Baynounah TV HD','1656-Dubai TV HD'
               ,'1659-Sama Dubai HD','4930-Noor Dubai','3948-Dubai Zaman TV','4048-Sharjah TV HD','4051-Sharqiya from kalba HD',
               '4928-Ajman TV HD','4525-Al Dafrah HD','5093-Saudi 1 HD','4736-SBC HD','5259-Zikrayat TV HD','4502-MBC+ eLife HD','4450-MBC+ Variety HD']


with io.open("/etc/epgimport/eliftv.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))
for nt in ch.eli:
    with io.open("/etc/epgimport/eliftv.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+nt+'">'+"\n"+'    <display-name lang="en">'+nt+'</display-name>'+"\n"+'  </channel>'+"\r").decode('utf-8'))

next_week= (datetime.now() + timedelta(days=6)).strftime('%Y%m%d%H%M%S')

print('**************eLife TV EPG******************')
headers={
  "Accept": "text/plain, */*; q=0.01",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "en-US,en;q=0.9",
  "Connection": "keep-alive",
  "Content-Length": "83",
  "Content-Type": "application/x-www-form-urlencoded",
  "Cookie": "JSESSIONID=C3EA5DDD803EF9F2EE80589ADCF79B82",
  "Host": "elifetv.etisalat.ae:33100",
  "Origin": "http://elifetv.etisalat.ae:33100",
  "Referer": "http://elifetv.etisalat.ae:33100/EPG/jsp/webtv/index.jsp",
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
for code_ch in channels_code:
  xml="""                                                                     
  <PlayBillListReq><channelid>{}</channelid><begintime></begintime><endtime>{}</endtime><type>2</type></PlayBillListReq>""".format(code_ch.split('-')[0],next_week)
  with requests.Session() as s:
    s.mount('http://', HTTPAdapter(max_retries=100))
    url = s.post('http://elifetv.etisalat.ae:33100/EPG/XML/PlayBillList',headers=headers,data=xml)
    title =re.findall(r'<type>PROGRAM<\/type><name>(.*?)<\/name>',url.text)
    des= re.findall(r'<introduce>(.*?)<\/introduce>',url.text)
    start= re.findall(r'<starttime>(\d+)<\/starttime>',url.text)
    end= re.findall(r'<endtime>(\d+)<\/endtime>',url.text)
    print code_ch.split('-')[1]+' ends at '+end[-1]
    sys.stdout.flush()
    for start_prog ,end_prog,title_pro,des_prog in zip(start,end,title,des):
      ch=''
      ch+=2*' '+'<programme start="{} +0000" stop="{} +0000" channel="{}">\n'.format(start_prog,end_prog,code_ch.split('-')[1])
      ch+=4*' '+'<title lang="en">'+title_pro.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and')+'</title>\n'
      ch+=4*' '+'<desc lang="en">'+des_prog.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and')+'</desc>\n  </programme>\r'
      #print ch
      with io.open("/etc/epgimport/eliftv.xml", "a",encoding="utf-8") as f:
        f.write((ch.encode('ascii', 'ignore').decode('ascii')).decode('utf-8'))
        
        
with io.open("/etc/epgimport/eliftv.xml", "a",encoding="utf-8") as f:
  f.write(('</tv>').decode('utf-8'))
  
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/eliftv.txt") as f:
  lines = f.readlines()
lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/eliftv.txt", "w") as f:
    f.writelines(lines)
    
    
if not os.path.exists('/etc/epgimport/custom.channels.xml'):
  print('Downloading custom.channels config')
  custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.channels.xml?raw=true')
  with io.open('/etc/epgimport/custom.channels.xml','w',encoding="utf-8") as f:
      f.write(custom_channels.text)
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
  print('Downloading custom sources config')
  custom_source=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.sources.xml?raw=true')
  with io.open('/etc/epgimport/custom.sources.xml','w',encoding="utf-8") as f:
      f.write(custom_source.text)

if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
  print('Downloading elcinema channels config')
  elcinema_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/elcinema.channels.xml?raw=true')
  with io.open('/etc/epgimport/elcinema.channels.xml','w',encoding="utf-8") as f:
      f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/dstv.channels.xml'):
  print('Downloading dstv channels config')
  dstv_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/dstv.channels.xml?raw=true')
  with io.open('/etc/epgimport/dstv.channels.xml','w',encoding="utf-8") as f:
      f.write(dstv_channels.text)
        
if not os.path.exists('/etc/epgimport/eliftv.channels.xml'):
  print('Downloading eliftv channels config')
  elif_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/eliftv.channels.xml?raw=true')
  with io.open('/etc/epgimport/eliftv.channels.xml','w',encoding="utf-8") as f:
      f.write(elif_channels.text)
        
        
print("**************FINISHED******************")