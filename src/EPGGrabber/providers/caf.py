import io
import requests
import sys
from datetime import datetime
from __init__ import *

time_zone = tz()

ch_code = ['80018','80402','80645','80016','80646','80403','80050','80625','80124','80149','80393','80394','80129','80302','80626','80125','80628','80144','80555','80041','80042','60022','60014','60020','60115','60243','60347','60629','60630']

def cplus():
    for code in ch_code:
        for i in range(0,8):
            url = requests.get('https://service.canal-overseas.com/ott-frontend/vector/83001/channel/' + code + '/events?filter.day=' + str(i)).json()
            try:
                for data in url['timeSlices']:
                    for prog in data['contents']:
                        subtitle = 'information non disponible'
                        if 'subtitle' in prog:
                            subtitle = prog['subtitle']
                        title,ch_name,startime,endtime = prog['title'],prog['thirdTitle'],prog['startTime'],prog['endTime']
                        start = datetime.fromtimestamp(startime).strftime('%Y%m%d%H%M%S')
                        end = datetime.fromtimestamp(endtime).strftime('%Y%m%d%H%M%S')
                        ch = ''
                        ch += 2 * ' ' + '<programme start="' + str(start) + ' ' + time_zone + '" stop="' + str(end) + ' ' + time_zone + '" channel="' + ch_name.replace('.','') + '">\n'
                        ch += 4 * ' ' + '<title lang="fr">' + title.replace('&', 'and') + '</title>\n'
                        ch += 4 * ' ' + '<desc lang="fr">' + subtitle.replace('&', 'and') + '</desc>\n  </programme>\r'
                        with io.open(EPG_ROOT + '/caf.xml', "a", encoding='UTF-8')as f:
                            f.write(ch)
            except KeyError:
                pass
        if ch_name and endtime:
            print(ch_name.replace('.','') + ' EPG ends at : ' + str(datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M')))
            sys.stdout.flush()
        
def main():
    print('**************Canal+AF EPG******************')
    sys.stdout.flush()
    provider = __file__.rpartition('/')[-1].replace('.py', '')
    update_status(provider)
    channels = get_channels("Canal+AF")
    xml_header(EPG_ROOT + '/caf.xml', channels)
    cplus()
    close_xml(EPG_ROOT + '/caf.xml')
    print('**************FINISHED******************')
    sys.stdout.flush()


if __name__ == "__main__":
    main()
