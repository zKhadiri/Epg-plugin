#!/usr/bin/python
# -*- coding: utf-8 -*-

# python3
from __future__ import print_function
from Plugins.Extensions.EPGGrabber.core.compat import PY3
from Plugins.Extensions.EPGGrabber.core.header import xml_header,close_xml
from Plugins.Extensions.EPGGrabber.core.timezone import tz
from Plugins.Extensions.EPGGrabber.core.paths import *

from elcin import Elcinema
import io,requests,sys
from datetime import datetime,timedelta

nb_channel=['1322-BEINMOVIESPREMIERE','1323-BEINMOVIESACTION','1324-BEINMOVIESDRAMA','1325-BEINMOVIESFAMILY','1326-BeInBoxOffice','1327-BeInSeriesHD1'
            ,'1328-BeInSeriesHD2','1309-beINDrama','1330-FOXACTIONMOVIES','1331-FOXFAMILYMOVIESHD']

time_zone=tz()

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
            with io.open(EPG_ROOT+"/beinentCin.xml","a",encoding='UTF-8')as f:
                f.write(ch)
        print(channel.split('-')[1]+' epg ends at : '+str(self.Endtime()[-1]))
        sys.stdout.flush()
        
def main():
    channels = [nb.split('-')[1] for nb in nb_channel]
    
    xml_header(EPG_ROOT+'/beinentCin.xml',channels)
            
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
        with open(PROVIDERS_ROOT, 'r') as f:
            data = json.load(f)
        for channel in data['bouquets']:
            if channel["bouquet"]=="beincin":
                channel['date']=datetime.today().strftime('%A %d %B %Y at %I:%M %p')
        with open(PROVIDERS_ROOT, 'w') as f:
            json.dump(data, f)
            
if __name__=='__main__':
    main()
    
    close_xml(EPG_ROOT+'/beinentCin.xml')

    print('**************FINISHED******************')
    sys.stdout.flush()
