# -*- coding: utf-8 -*-
import csv, requests, sys , re , io,json
from datetime import datetime,timedelta
from __init__ import *

if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

today = (datetime.now()-timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')

channels = ['Khalijiah-v2|Rotana Khalijiah','ROTANA-HD-2|Rotana HD','LBC-12|LBC','Drama-12|Rotana Drama',\
    'Classic-12|Rotana Classic','cinema-KSA-12|Rotana cinema KSA','Cinema-masr-12|Rotana cinema masr','Rotana-Amrica-12|Rotana Amarica'\
        ,'Aflam-|Rotana aflam','Comdey|Rotana Comedy','KIDs|Rotana KIDS']

def rotana(this_month,channel):
    with requests.Session() as s:
        url = s.get('https://rotana.net/assets/uploads/{}/{}.csv'.format(this_month,channel.split('|')[0]))
        
    decoded_content = url.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

    start_dt = []
    end_dt = []
    titles = []
    descriptions = []
    for rows in my_list[1:]:
        start_dt.append(' '.join(rows[1:][2:4]))
        end_dt.append(' '.join((rows[1:][4:6])))
        titles.append(rows[1:][1])
        descriptions.append(rows[1:][7])
        
        
    for title,des,start,end,ed in zip(titles,descriptions,start_dt,start_dt[1:]+[start_dt[0]],end_dt):
        if start >= today:
            ch=''
            if start_dt[-1] == start and start_dt[0] == end :
                startime= datetime.strptime(start,'%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                endtime= datetime.strptime(ed,'%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
            else:
                startime= datetime.strptime(start,'%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                endtime= datetime.strptime(end,'%d/%m/%Y %H:%M:%S:%f').strftime('%Y%m%d%H%M%S')
                
            ch+=2*' '+'<programme start="'+startime+' +0000" stop="'+endtime+' +0000" channel="'+channel.split('|')[1]+'">\n'
            ch+=4*' '+'<title lang="ar">'+title+'</title>\n'
            if des == '':
                ch+=4*' '+'<desc lang="ar">يتعذر الحصول على معلومات هذا البرنامج</desc>\n  </programme>\r'
            else:
                ch+=4*' '+'<desc lang="ar">'+des+'</desc>\n  </programme>\r'
                
            with io.open(EPG_ROOT+'/rotana.xml',"a",encoding='UTF-8')as f:
                f.write(ch)
    
    print(channel.split('|')[1]+' EPG ends at '+ end_dt[-1])
    sys.stdout.flush()

def main():
    print('**************Rotana EPG******************')
    sys.stdout.flush()
    
    
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"]=="rotana":
            channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)
    
    xml_header(EPG_ROOT+'/rotana.xml',[ch.split('|')[1] for ch in channels])
    
    url = requests.get('https://rotana.net/%D8%AC%D8%AF%D9%88%D9%84-%D8%A7%D9%84%D8%A8%D8%B1%D8%A7%D9%85%D8%AC/')
    date = re.findall(r'\/(\d{4}\W{2}\d{2})\W{2}',url.text)[0].replace('\/','/')
    for channel in channels:
        rotana(date,channel)
        
        
   
    close_xml(EPG_ROOT+'/rotana.xml')
    
    print('**************FINISHED******************')
    sys.stdout.flush()
    
    
if __name__ == "__main__":
    main()