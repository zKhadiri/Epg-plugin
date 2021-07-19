from __future__ import print_function

import requests
import json
import io
import os
import re
import sys
from datetime import datetime, timedelta
from time import strftime
from __init__ import *
    
time_zone = tz()

head = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

def lematin(channels):
    for channel in channels:
        with requests.Session() as s:
            url = s.get('https://lematin.ma/television/' + channel,headers=head)

            for t in re.findall(r'<table class=\"table table-striped\">((.|\n)*?)</table>',url.text):
                time = re.findall(r'(\d{2}:\d{2})',t[0].strip())
                titles = re.findall(r"(.*\s+.*?)<label class=\"badge badge-secondary float",t[0].strip())

                times = []
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
                last_hr = 0
                for d in time:
                    h, m = map(int, d.split(":"))
                    if last_hr > h:
                        today += + timedelta(days=1)
                    last_hr = h
                    times.append(today + timedelta(hours=h, minutes=m))
                    
                for start,end,title in zip(times,times[1:] + [times[0]],cleanhtml(titles)):
                    if start != times[-1] and end != times[0]:
                        ch = ''
                        startime = datetime.strptime(str(start),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                        endtime = datetime.strptime(str(end),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                        ch += 2 * ' ' + '<programme start="' + startime + ' ' + time_zone + '" stop="' + endtime + ' ' + time_zone + '" channel="' + channel + '">\n'
                        
                        if channel == "arryadia":
                            sub_title = title.replace('\n',' ').replace('<td>',' ').strip().split(':')
                            if len(sub_title) == 2:
                                ch += 4 * ' ' + '<title lang="en/fr">' + sub_title[0] + '</title>\n'
                                ch += 4 * ' ' + '<desc lang="en/fr">' + sub_title[1].strip() + '</desc>\n  </programme>\r'
                            else:
                                ch += 4 * ' ' + '<title lang="en/fr">' + sub_title[0] + '</title>\n'
                                ch += 4 * ' ' + '<desc lang="en/fr">Arryadia</desc>\n  </programme>\r'
                        else:
                            ch += 4 * ' ' + '<title lang="en/fr">' + title.replace('&#039;',"'").replace('\n',' ').replace('<td>',' ').strip() + '</title>\n'
                            ch += 4 * ' ' + '<desc lang="en/fr">Not Applicable</desc>\n  </programme>\r'
                        
                        with io.open(EPG_ROOT + '/lematin.xml',"a",encoding='UTF-8')as f:
                            f.write(ch)
                            
                print(channel + ' EPG ends at ' + str(times[-1]))
                sys.stdout.flush()

def cleanhtml(html):
    for elem in html:
        clean_text = re.sub(re.compile('<.*?>'), '', elem)
        yield clean_text
       
def main():
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == "lematin":
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)
        
    print('**************LE MATIN EPG******************')
    sys.stdout.flush()
    
    channels = ['aloula','arryadia','2m','medi1']
    
    xml_header(EPG_ROOT + '/lematin.xml',channels)
    
    lematin(channels)
    
    close_xml(EPG_ROOT + '/lematin.xml')

    print('**************FINISHED******************')
    sys.stdout.flush()
    
    
if __name__ == "__main__":
    main()
