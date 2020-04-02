import requests,re,io,ch,os
from datetime import datetime
from time import sleep
from shutil import copyfile
headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.149 Chrome/80.0.3987.149 Safari/537.36'
}

days=[]
times=[]
titles=[]
des=[]
cat=[]
prog=[]


f=open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt",'r')
time_offset=f.read().replace('\n','')
f.close()

with io.open("/etc/epgimport/elcinema.xml","w",encoding='UTF-8')as f:
    f.write(('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">').decode('utf-8'))

for x in ch.elc_channels:
    with io.open("/etc/epgimport/elcinema.xml","a",encoding='UTF-8')as f:
        f.write(("\n"+'  <channel id="'+x+'">'+"\n"+'    <display-name lang="en">'+x.replace("_",' ')+'</display-name>'+"\n"+'  </channel>\r').decode('utf-8'))

now = datetime.today().year
nb_channel=['1186','1261','1174','1173','1169','1137','1223','1176','1199','1156','1262','1227','1198','1177','1193','1158',
            '1170','1159','1226','1292','1203','1101','1134','1283','1188','1260','1290','1204','1269','1280',
            '1300','1298','1297','1301','1299','1296','1304','1317','1302','1312','1321','1338','1339','1353','1350','1355']
def elci():
    for nb in nb_channel:
        try:
            url = requests.get('http://elcinema.com/en/tvguide/'+nb+'/',headers=headers)
            time_d = re.findall(r'\d{2}:\d{2}\s+\w\w|<div\sclass=\" dates\">\s+(.*)',url.text)
            time = re.findall(r'\d{2}:\d{2}\s+\w\w',url.text)
            channel_name=re.findall(r'<li>(.*?)<\/li>\s+<li\sclass=\"localization\">',url.text)
            print('\n'.join(channel_name))
            days[:]=[]
            times[:]=[]
            titles[:]=[]
            des[:]=[]
            cat[:]=[]
            prog[:]=[]
            for ti in time:
                times.append(datetime.strptime(ti, '%I:%M %p').strftime('%H:%M'))

            for i, val in enumerate(time_d):
                if not val:
                    time_d[i] = time_d[i-1]
                    days.append(time_d[i])      
                    
            url_ar = requests.get('http://elcinema.com/ar/tvguide/'+nb+'/',headers=headers)
            first=re.findall(r'<li>(.*?)<a\shref=\'#\'\sid=\'read-more\'>',url_ar.text)
            last=re.findall(r"<span class='hide'>[^\n]+",url_ar.text)
            desc=re.findall(r'<\/a><\/li>\s+<li>\s+\s+(.*\s+.*?)\s+<\/li>\s+<li>',url_ar.text)
            descc = [re.sub(' +',' ',d).replace('\n','') for d in desc]
            for f,l in zip(first,last):
                des.append(f+l.replace("<span class='hide'>",'').replace('</span></li>',''))
                
            for dess in descc:
                cat.append(dess)  
                
            title_l = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li',url_ar.text)

            mt2 = re.findall(r'<a\shref=\"\/work\/\d+\/\">(.*?)<\/a><\/li|columns small-7 large-11\">\s+<ul class=\"unstyled no-margin\">\s+<li>(.*?)<\/li>',url_ar.text)
            for m in mt2:
                if m[0]=='':
                    titles.append(m[1])
                else:
                    titles.append(m[0])

            for index, element in enumerate(titles):
                if element not in title_l:
                    des.insert(index,titles[index])
                    cat.insert(index,titles[index])
                    
            for elem,next_elem,td1,td2 in zip(times, times[1:]+[times[0]],time_d,time_d[1:]+[time_d[0]]):
                chnm=re.sub(' +', '', ''.join(channel_name)).replace(u'\xa0 Channel','').replace('Channel','')
                startime=datetime.strptime(str(now)+' '+str(td1)+' '+elem,'%Y %A %d %B %H:%M').strftime('%Y%m%d%H%M%S')
                endtime=datetime.strptime(str(now)+' '+str(td2)+' '+next_elem,'%Y %A %d %B %H:%M').strftime('%Y%m%d%H%M%S')
                prog.append(2 * ' ' +'<programme start="' + startime + ' +0100" stop="' + endtime + ' +0100" channel="'+chnm.strip()+'">\n')
                
            
            for p,tt,d,c in zip(prog,titles,des,cat):
                space=re.sub(' +', ' ', d).replace('\r','').replace('\n','').replace('&amp;','and').replace('(','').replace(')','')
                ch='' 
                ch+=p
                ch+='     <title lang="ar">'+tt.replace('&#39;',"'").replace('&quot;','"')+'</title>\n'
                ch+='     <desc lang="ar">'+space+'</desc>\n'
                ch+='     <category lang="ar">'+c+'</category>\n'+'  </programme>\n'
                with io.open("/etc/epgimport/elcinema.xml","a",encoding='UTF-8')as f:
                    f.write(ch)
        except:pass
        
if __name__=='__main__':
    elci()
        
        
with io.open("/etc/epgimport/elcinema.xml", "a",encoding="utf-8") as f:
    f.write(('</tv>').decode('utf-8'))
    
if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    copyfile("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/configs/custom.channels.xml", "/etc/epgimport/custom.channels.xml")
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    copyfile("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/configs/custom.sources.xml", "/etc/epgimport/custom.sources.xml")