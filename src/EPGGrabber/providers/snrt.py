# -*- coding: utf-8 -*-
import requests, sys , re , io,json
from datetime import datetime,timedelta
from __init__ import *

time_zone = tz()

def arryadia():
    with requests.Session() as s:
        times = []
        titles = []
        descriptions = []
        live = []
        for i in range(0,2):
            next_day = (datetime.today()+timedelta(days=i)).strftime('%Y/%m/%d')
            url = s.get('http://arryadia.snrt.ma/ar/grilles-des-programmes-ar/eventsbyday/'+next_day)
            
            for hour,title,description,direct in zip(re.findall(r'<div class=\"eventlineitem-time\">(.*?)</div>',url.text),\
                re.findall(r'<span class=\"emissiontitle\">(.*?)</span>',url.text),\
                re.findall(r'<span class=\"emissiontitle\">.*?</span><br\s+/>\s+(.*?)</div>',url.text),\
                re.findall(r'<span class=\"direct\">(.*?)</span>',url.text)):
                times.append(hour)
                titles.append(title)
                descriptions.append(description)            
                live.append(direct)
        
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
        last_hr = 0
        start_dt=[]
        for d in times:
            h, m = map(int, d.split(":"))
            if last_hr > h:
                today += + timedelta(days=1)
            last_hr = h
            start_dt.append(today + timedelta(hours=h, minutes=m))
        
        for start,end,t,d,lv in zip(start_dt,start_dt[1:]+[start_dt[0]],titles,descriptions,live):
            if start != start_dt[-1] and end != start_dt[0]:
                ch=''
                startime=datetime.strptime(str(start),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                endtime=datetime.strptime(str(end),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Arryadia HD">\n'
                if lv != "":
                    
                    ch+=4*' '+'<title lang="ar/en">'+lv+' : '+t+'</title>\n'
                else:
                    ch+=4*' '+'<title lang="ar/en">'+t+'</title>\n'
                
                if d != "" :
                    ch+=4*' '+'<desc lang="en/ar">'+d+'</desc>\n  </programme>\r'
                else:
                    ch+=4*' '+'<desc lang="ar/en">Arryadia HD</desc>\n  </programme>\r'
                    
                with io.open(EPG_ROOT+'/snrt.xml',"a",encoding='UTF-8')as f:
                    if not PY3:
                        f.write(ch.decode('utf-8'))
                    else:
                        f.write(ch)

        print('Arryadia HD EPG ends at '+str(start_dt[-1]))
        sys.stdout.flush()
        
def main():
    print('**************Snrt EPG******************')
    sys.stdout.flush()
    
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"]=="snrt":
            channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)
    
    xml_header(EPG_ROOT+'/snrt.xml',["Arryadia HD"])
    
    arryadia()
        
    close_xml(EPG_ROOT+'/snrt.xml')
    
    print('**************FINISHED******************')
    sys.stdout.flush()
    
    
if __name__ == "__main__":
    main()