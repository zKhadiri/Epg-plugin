import requests,os,json
from time import strftime
from datetime import datetime
from paths import API_PATH

def get_tz():
    try:
        url_content = requests.get('http://worldtimeapi.org/api/ip').json()
        js =  {'tz':url_content['utc_offset'].replace(':', '')}
        file = open(API_PATH+'/tz.json','w')
        json.dump(js, file, indent = 4)
        file.close()
    except:
        js = {'tz':strftime('%z')}
        file = open(API_PATH+'/tz.json','w')
        json.dump(js, file, indent = 4)
        file.close()
    
    
def tz():
    if os.path.exists(API_PATH+'/tz.json'):
        this_month = datetime.today().strftime('%Y-%m')
        file_date = datetime.fromtimestamp(os.stat(API_PATH+'/tz.json').st_mtime).strftime('%Y-%m')
        if this_month != file_date:
            get_tz()
            file = open(API_PATH+'/tz.json','r')
            timezone = file.read()
            file.close()
            return json.loads(timezone)['tz']
        else:
            file = open(API_PATH+'/tz.json','r')
            timezone = file.read()
            file.close()
            return json.loads(timezone)['tz']
    else:
        get_tz()
        file = open(API_PATH+'/tz.json','r')
        timezone = file.read()
        file.close()
        return json.loads(timezone)['tz']
    