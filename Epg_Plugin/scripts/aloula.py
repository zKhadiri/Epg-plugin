import requests,re,os,io,sys
from shutil import copyfile
from requests.adapters import HTTPAdapter
headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt','r')
time_zone = fil.readlines()[0].strip()
fil.close()

channe=[]
urls=[]
from datetime import datetime
now = datetime.now().strftime('%Y/%m/%d')
for i in range(0,7):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('http://www.alaoula.ma/programmes.php?jr='+week.strftime('%d/%m/%Y')+'&lang=ar')

def snrt():
    channe.append('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">'+"\n"+'  <channel id="Aloula.ma">'+"\n"+'    <display-name lang="en">Aloula HD</display-name>'+"\n"+'  </channel>'+"\n")
    channe.append('  <channel id="Arriadia.ma">'+"\n"+'    <display-name lang="en">Arriadia HD</display-name>'+"\n"+'  </channel>'+"\n")
    channe.append('  <channel id="2M.ma">' + "\n" + '    <display-name lang="en">2M</display-name>' + "\n" + '  </channel>' + "\n")
    #channe.append('  <channel id="athaqafia.ma">' + "\n" + '    <display-name lang="en">Athaqafia HD</display-name>' + "\n" + '  </channel>' + "\n")
    channe.append('  <channel id="Medi1tv.ma">' + "\n" + '    <display-name lang="en">Medi1tv</display-name>' + "\n" + '  </channel>' + "\n")
    with io.open("/etc/epgimport/aloula.xml","w",encoding='UTF-8')as f:
        f.write(''.join(channe).decode('utf-8'))
    prog = []
    desc = []
    cat = []
    times_all=[]
    time_chan=[]
    alls=[]
    glb_title=[]
    glb_des=[]
    glb_time=[]
    end_date=[]
    for url in urls:
        prog[:] = []
        desc[:] = []
        cat[:] = []
        link = requests.get(url,headers=headers)
        time = re.findall(r'<div class="\w+_\w+_\w+" style=";">(.*?)<\/div>',link.text)
        title= re.findall(r'<a\s+class="grille_item_title_12 grille_item_title_12_ar" style="">(.*?)<\/a>',link.text)
        titles =[re.sub(' +',' ',t).replace('-','') for t in title]
        
        for titl_ in titles:
            glb_title.append(4*' '+'<title lang="ar">' + titl_.replace('(',' ').replace(')',' ') + '</title>' + "\n")
            glb_des.append(4 * ' ' + '<desc lang="ar">No description found for this program</desc>\n  </programme>\r')
            
        from datetime import datetime
        actuel = datetime.now().strftime("%H:%M")
        times=[time_.replace(".", ":").replace("Actuellement", actuel).replace('h',':').replace('H',':').split() for time_ in time]
        for tt in times:
            times_all.append(''.join(tt))
    
    date = re.search(r'\d{2}/\d{2}/\d{4}',urls[0])
    nn=datetime.strptime(date.group(),'%d/%m/%Y')
    toda = nn.replace(hour=0, minute=0, second=0, microsecond=0)
    last_hr = 0
    for d in times_all:
        h, m = map(int, d.split(":"))
        if last_hr > h:
            toda = toda + timedelta(days=1)
        last_hr = h
        glb_time.append(toda + timedelta(hours=h, minutes=m))
    
    for elem, next_elem in zip(glb_time, glb_time[1:] + [glb_time[0]]):
        startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        time_chan.append(2 * ' ' + '<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Aloula.ma">' + '\n')
        date_end =datetime.strptime(startime,'%Y%m%d%H%M%S').strftime('%Y/%m/%d')
        day = datetime.strptime(date_end,'%Y/%m/%d')
        date_now = datetime.strptime(now,'%Y/%m/%d')
        nb_days = day - date_now
        end_date.append(nb_days.days) 
    for tt,p,d in zip(time_chan,glb_title,glb_des):
        alls.append(tt+p+d)
    
    try:
        alls.pop(-1)
        for progr in alls:           
            with io.open("/etc/epgimport/aloula.xml","a",encoding='UTF-8')as f:
                f.write(progr)
        print 'Aloula epg downloaded for : '+str(end_date[-1])+' days'
        sys.stdout.flush()
    except IndexError:
        print 'No data found for or missing data for aloulaTV'          
        sys.stdout.flush()
def arriadia():
    prog = []
    urls=[]
    desc = []
    cat = []
    time_chan = []
    alls=[]
    time_all=[]
    grp_time=[]
    grp_desc=[]
    grp_title=[]
    end_date=[]
    for i in range(0, 7):
        import datetime
        from datetime import timedelta
        jour = datetime.date.today()
        week = jour + timedelta(days=i)
        urls.append('http://arryadia.snrt.ma/ar/grilles-des-programmes-ar/eventsbyday/'+week.strftime('%Y/%m/%d')+'/')
    for url in urls:
        prog[:] = []
        desc[:] = []
        cat[:] = []
        ur = requests.get(url,headers=headers)
        title_ar = re.findall(r'<span class="emissiontitle">(.*?)<\/span>',ur.text)
        time_ar=re.findall(r'<div class="eventlineitem-time">(.*?)<\/div>',ur.text)
        des=re.findall(r'<\/span><br \/>(\s.*)</div>',ur.text)
        for ri_ in time_ar:
            time_chan.append(ri_)
        for titl,d in zip (title_ar,des):
            grp_title.append(4 * ' ' + '<title lang="ar">' + titl.replace('&','and') + '</title>' + "\n")
            grp_desc.append(4 * ' ' + '<desc lang="ar">' + d.replace('&','and').strip() +'</desc>\n  </programme>\r')
    date = re.search(r'\d{4}/\d{2}/\d{2}',urls[0])
    nn=datetime.datetime.strptime(date.group(),'%Y/%m/%d')
    toda = nn.replace(hour=0, minute=0, second=0, microsecond=0)
    last_hr = 0
    for d in time_chan:
        h, m = map(int, d.split(":"))
        if last_hr > h:
            toda = toda + timedelta(days=1)
        last_hr = h
        grp_time.append(toda + timedelta(hours=h, minutes=m))
        from datetime import datetime
    for elem, next_elem in zip(grp_time, grp_time[1:] + [grp_time[0]]):
        startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        time_all.append(2 * ' ' + '<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Arriadia.ma">' + '\n')
        date_end =datetime.strptime(startime,'%Y%m%d%H%M%S').strftime('%Y/%m/%d')
        day = datetime.strptime(date_end,'%Y/%m/%d')
        date_now = datetime.strptime(now,'%Y/%m/%d')
        nb_days = day - date_now
        end_date.append(nb_days.days)
        
    for tt,p,d in zip(time_all,grp_title,grp_desc):
        alls.append(tt+p+d)
    
    try:
        alls.pop(-1)
        for progr in alls:           
            with io.open("/etc/epgimport/aloula.xml","a",encoding='UTF-8')as f:
                f.write(progr)
        print 'Arryadia epg downloaded for : '+str(end_date[-1])+' days'
        sys.stdout.flush()
    except IndexError:
        print 'No data found for or missing data for Arryadia'
        sys.stdout.flush()
   
def mm():
    prog = []
    urls=[]
    desc = []
    time_chan = []
    alls=[]
    titi=[]
    descrip=[]
    ti_=[]
    starts=[]
    end_date=[]
    for i in range(0, 7):
        import datetime, time
        from datetime import timedelta
        jour = datetime.date.today()
        week = jour + timedelta(days=i)
        from datetime import datetime
        urls.append('http://www.2m.ma/ar/guidetv/?day=' + str(int(time.mktime(datetime.strptime('' + str(week) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").timetuple()))))

    for url in urls:
        with requests.Session() as s:
            s.mount('http://', HTTPAdapter(max_retries=10))
            r = s.get(url, headers=headers)
            title_2m = re.findall(r'bold\">(.*?)<\/h4>\s+<p', r.text)
            des_2m = re.findall(r'<p class="text-size12">(.*?)<\/p>', r.text)
            time_2m = re.findall(r'<span class=\"p-right-15 text-size22 roboto lighter\">(.*?)<\/span>', r.text)
            for time_ in time_2m:
                titi.append(time_)
            for d in des_2m:
                descrip.append(d)
            for f in title_2m:
                ti_.append(f)
    date = re.search(r'=(\d+)',urls[0])  
    aa= datetime.fromtimestamp(int(date.group().replace('=',''))).strftime('%Y/%m/%d')  
    nn=datetime.strptime(aa,'%Y/%m/%d')    
    toda = nn.replace(hour=0, minute=0, second=0, microsecond=0) 
    last_hr = 0
    for d in titi:
        h, m = map(int, d.split(":"))
        if last_hr > h:
            toda = toda + timedelta(days=1)
        last_hr = h
        starts.append(toda + timedelta(hours=h, minutes=m))
    from datetime import datetime
    for elem, next_elem in zip(starts, starts[1:] + [starts[0]]):
        starttime = datetime.strptime(str(elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        endtime = datetime.strptime(str(next_elem), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="2m.ma">' + '\n')
        date_end =datetime.strptime(endtime,'%Y%m%d%H%M%S').strftime('%Y/%m/%d')
        day = datetime.strptime(date_end,'%Y/%m/%d')
        date_now = datetime.strptime(now,'%Y/%m/%d')
        nb_days = day - date_now
        end_date.append(nb_days.days)
    for tit, de in zip(ti_, descrip):
        desc.append(4 * ' ' + '<desc lang="ar">' + de + '</desc>\n  </programme>\r')
        if tit == '':
            prog.append(4 * ' ' + '<title lang="ar">' + de + '</title>' + "\n")
        else:
            prog.append(4 * ' ' + '<title lang="ar">' +tit.replace('&#39;', "'")+ '</title>' + "\n")
    for tt, p, d in zip(time_chan, prog, desc):
        alls.append(tt + p + d )
        
    try:       
        alls.pop(-1)
        for x in alls:
            with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
                f.write(x)
        print '2M epg downloaded for : '+str(end_date[-2])+' days'
        sys.stdout.flush()
    except IndexError:
        print 'No data found for or missing data for 2M'
        sys.stdout.flush()
        
def medi():
    times=[]
    descrip=[]
    titles=[]
    glb_time=[]
    time_chan=[]
    alls=[]
    from datetime import datetime,timedelta
    i= datetime.today().weekday()
    for j in range(i,7):
        url = requests.get('http://www.medi1tv.com/ar/inc/grille.aspx?d='+str(j))
        for des in re.findall(r'id=\"resumegrille-\d+\"\s+>(.*)',url.text):
            if des==u'\r':
                descrip.append(4 * ' ' + '<desc lang="ar">No description found for this program</desc>\n  </programme>\r')
            else:
                descrip.append(4 * ' ' + '<desc lang="ar">'+des.strip()+'</desc>\n  </programme>\r')
                
        for time in re.findall(r'\d{2}:\d{2}',url.text):
            times.append(time)
        
        for title in re.findall(r'id=\"titregrille-\d+\"\s+>(.*?)</div>',url.text):
            titles.append(4*' '+'<title lang="ar">' + title + '</title>' + "\n")
        
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
    last_hr = 0
    for d in times:
        h, m = map(int, d.split(":"))
        if last_hr > h:
            today += + timedelta(days=1)
        last_hr = h
        glb_time.append(today + timedelta(hours=h, minutes=m))
    
    for elem, next_elem in zip(glb_time, glb_time[1:] + [glb_time[0]]):
        startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        time_chan.append(2 * ' ' + '<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Medi1tv.ma">' + '\n')   

    for tt,p,d in zip(time_chan,titles,descrip):
        alls.append(tt+p+d)
    try:   
        alls.pop(-1)
        print 'Mediatv epg ends at : '+str(glb_time[-1])
        sys.stdout.flush()
        for progr in alls:
            with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
                f.write(progr)       
    except IndexError:
        print 'No data found for or missing data for Mediatv'
        sys.stdout.flush()

if __name__ == '__main__': 
    snrt()
    arriadia()
    mm()
    medi()
    from datetime import datetime
    with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt") as f:
        lines = f.readlines()
    lines[1] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt", "w") as f:
        f.writelines(lines)

with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
    f.write(('</tv>').decode('utf-8'))
    
    
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