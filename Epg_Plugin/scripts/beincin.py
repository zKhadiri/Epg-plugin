#!/usr/bin/python
# -*- coding: utf-8 -*-

# python3
from __future__ import print_function
from compat import PY3

from elcin import Elcinema,get_tz
import io,requests,sys
from datetime import datetime,timedelta

nb_channel=['1322-BEINMOVIESPREMIERE','1323-BEINMOVIESACTION','1324-BEINMOVIESDRAMA','1325-BEINMOVIESFAMILY','1326-BeInBoxOffice','1327-BeInSeriesHD1'
            ,'1328-BeInSeriesHD2','1309-beINDrama','1330-FOXACTIONMOVIES','1331-FOXFAMILYMOVIESHD']

time_zone=get_tz()

class ElcinB(Elcinema,object):
    
    def __init__(self,channel):
        super(ElcinB, self).__init__(channel)
    
    def Toxml(self,channel):
        for elem,next_elem,title,des in zip(self.Starttime(),self.Endtime(),self.Gettitle(),self.GetDes()):
            ch=''
            startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            ch+= 2 * ' ' +'<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="'+channel.split('-')[1]+'">\n'
            ch+=4*' '+'<title lang="ar">'+title.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and')+'</title>\n'
            ch+=4*' '+'<desc lang="ar">'+des.replace('&#39;',"'").replace('&quot;','"').replace('&amp;','and').replace('(','').replace(')','').strip()+'</desc>\n  </programme>\r'
            with io.open("/etc/epgimport/beinentCin.xml","a",encoding='UTF-8')as f:
                f.write(ch)
        print(channel.split('-')[1]+' epg ends at : '+str(self.Endtime()[-1]))
        sys.stdout.flush()
        
def main():
    with io.open("/etc/epgimport/beinentCin.xml","w",encoding='UTF-8')as f:
        if PY3:
        	f.write('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">')
        else:
        	f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

    for x in nb_channel:
        with io.open("/etc/epgimport/beinentCin.xml","a",encoding='UTF-8')as f:
            if PY3:
            	f.write("\n"+'  <channel id="'+x.split('-')[1]+'">'+"\n"+'    <display-name lang="en">'+x.split('-')[1]+'</display-name>'+"\n"+'  </channel>\r')
            else:
            	f.write(("\n"+'  <channel id="'+x.split('-')[1]+'">'+"\n"+'    <display-name lang="en">'+x.split('-')[1]+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))
        
    print('**************ELCINEMA BEIN ENTERTAINMENT EPG******************')
    sys.stdout.flush()         
    import time
    Hour = time.strftime("%H:%M")
    start='00:00'
    end='02:00'
    if Hour>=start and Hour<end:
        print('Please come back at 2am to download the epg')
        sys.stdout.flush()
    else:
        for nb in nb_channel:
            ElcinB(nb)
        from datetime import datetime
        import json
        with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as f:
            data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"]=="beincin":
                channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'w') as f:
            json.dump(data, f)
            
if __name__=='__main__':
    main()
    with io.open("/etc/epgimport/beinentCin.xml", "a",encoding="utf-8") as f:
        if PY3:
            f.write('</tv>')
        else:
            f.write(('</tv>').decode('utf-8'))

    print('**************FINISHED******************')
    sys.stdout.flush()
