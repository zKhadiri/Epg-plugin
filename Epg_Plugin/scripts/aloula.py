import requests,re,os,io
from shutil import copyfile
from requests.adapters import HTTPAdapter


headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt','r')
time_zone = fil.read().strip()
fil.close()

channe=[]
urls=[]
from datetime import datetime
now = datetime.now().strftime('%Y/%m/%d')
for i in range(0,6):
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
    #channe.append('  <channel id="Medi1tv.ma">' + "\n" + '    <display-name lang="en">Medi1tv</display-name>' + "\n" + '  </channel>' + "\n")
    with io.open("/etc/epgimport/aloula.xml","w",encoding='UTF-8')as f:
        f.write(''.join(channe).decode('utf-8'))
    prog = []
    desc = []
    cat = []
    time_chan = []
    time_r=[]
    alls=[]
    end_date=[]
    try:
        for url in urls:
            prog[:] = []
            desc[:] = []
            cat[:] = []
            time_chan[:] = []
            time_r[:]=[]
            #alls[:]=[]
            link = requests.get(url,headers=headers)
            time = re.findall(r'<div class="\w+_\w+_\w+" style=";">(.*?)<\/div>',link.text)
            title= re.findall(r'<a\s+class="grille_item_title_12 grille_item_title_12_ar" style="">(.*?)<\/a>',link.text)
            titles =[re.sub(' +',' ',t).replace('-','') for t in title]
            
            for titl_ in titles:
                prog.append(4*' '+'<title lang="ar">' + titl_.replace('(',' ').replace(')',' ') + '</title>' + "\n")
                desc.append(4 * ' ' + '<desc lang="ar">No descrption found for this program</desc>\n  </programme>\r')
                
            from datetime import datetime,timedelta
            actuel = datetime.now().strftime("%H:%M")
            times=[time_.replace(".", ":").replace("Actuellement", actuel).replace('h',':').replace('H',':').split() for time_ in time]
            date = re.search(r'\d{2}/\d{2}/\d{4}',url)
            nn=datetime.strptime(date.group(),'%d/%m/%Y')
            toda = nn.replace(hour=0, minute=0, second=0, microsecond=0)
            last_hr = 0
            for d in times:
                    h, m = map(int, d[0].split(":"))
                    if last_hr > h:
                        toda = toda + timedelta(days=1)
                    last_hr = h
                    time_r.append(toda + timedelta(hours=h, minutes=m))
                    
            for elem, next_elem in zip(time_r, time_r[1:] + [time_r[0]]):
                if time_r[0]==next_elem and time_r[-1]==elem:
                    fixed= next_elem + timedelta(days=1)
                    startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    endtime=datetime.strptime(str(fixed),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    time_chan.append(2 * ' ' + '<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Aloula.ma">' + '\n')
                    date_end =datetime.strptime(startime,'%Y%m%d%H%M%S').strftime('%Y/%m/%d')
                    day = datetime.strptime(date_end,'%Y/%m/%d')
                    date_now = datetime.strptime(now,'%Y/%m/%d')
                    nb_days = day - date_now
                    end_date.append(nb_days.days) 
                else:
                    startime=datetime.strptime(str(elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    endtime=datetime.strptime(str(next_elem),'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
                    time_chan.append(2 * ' ' + '<programme start="' + startime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Aloula.ma">' + '\n')
            for tt,p,d in zip(time_chan,prog,desc):
                alls.append(tt+p+d)
                
        
        alls.pop(-1)
        for progr in alls:           
            with io.open("/etc/epgimport/aloula.xml","a",encoding='UTF-8')as f:
                f.write(progr)
        print 'Aloula epg downloaded for : '+str(end_date[-1])+' days'           
    except:pass
    
def arriadia():
    prog = []
    urls=[]
    desc = []
    cat = []
    time_chan = []
    alls=[]
    end_date=[]
    for i in range(0, 3):
        import datetime
        from datetime import timedelta
        jour = datetime.date.today()
        week = jour + timedelta(days=i)
        urls.append('http://arryadia.snrt.ma/ar/grilles-des-programmes-ar/eventsbyday/'+week.strftime('%Y/%m/%d')+'/')

    try:
        for url in urls:
            prog[:] = []
            desc[:] = []
            cat[:] = []
            time_chan[:] = []
            ur = requests.get(url,headers=headers)
            title_ar = re.findall(r'<span class="emissiontitle">(.*?)<\/span>',ur.text)
            time_ar=re.findall(r'<div class="eventlineitem-time">(.*?)<\/div>',ur.text)
            des=re.findall(r'<\/span><br \/>(\s.*)</div>',ur.text)
        
            for titl,d in zip (title_ar,des):
                prog.append(4 * ' ' + '<title lang="ar">' + titl.replace('&','and') + '</title>' + "\n")
                desc.append(4 * ' ' + '<desc lang="ar">' + d.replace('&','and').strip() +'</desc>\n  </programme>\r')
            from datetime import datetime
            for elem, next_elem in zip(time_ar, time_ar[1:] + [time_ar[0]]):
                date = re.search(r'\d{4}/\d{2}/\d{2}', url)
                if time_ar[0]==next_elem and time_ar[-1]==elem:
                    dat = datetime.strptime(date.group() + ' ' + next_elem, '%Y/%m/%d %H:%M')
                    fixed= (dat + timedelta(days=1)).strftime('%Y/%m/%d %H:%M')
                    starttime = datetime.strptime(date.group() + ' ' + elem, '%Y/%m/%d %H:%M').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.strptime(fixed, '%Y/%m/%d %H:%M').strftime('%Y%m%d%H%M%S')
                    time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Arriadia.ma">' + '\n')
                    date_end =datetime.strptime(endtime,'%Y%m%d%H%M%S').strftime('%Y/%m/%d')
                    day = datetime.strptime(date_end,'%Y/%m/%d')
                    date_now = datetime.strptime(now,'%Y/%m/%d')
                    nb_days = day - date_now
                    end_date.append(nb_days.days) 
                else:
                    starttime = datetime.strptime(date.group() + ' ' + elem, '%Y/%m/%d %H:%M').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.strptime(date.group() + ' ' + next_elem, '%Y/%m/%d %H:%M').strftime('%Y%m%d%H%M%S')
                    time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Arriadia.ma">' + '\n')

            for tt,p,d in zip(time_chan,prog,desc):
                alls.append(tt+p+d)
                
        alls.pop(-1)
        for x in alls:
            with io.open("/etc/epgimport/aloula.xml","a",encoding='UTF-8')as f:
                f.write(x)
        print 'arriada epg downloaded for : '+str(end_date[-2])+' days'
    except:pass
  
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
    try:
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
                    
        toda = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
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
            #print nb_days.days
        for tit, de in zip(ti_, descrip):
            desc.append(4 * ' ' + '<desc lang="ar">' + de + '</desc>\n  </programme>\r')
            if tit == '':
                prog.append(4 * ' ' + '<title lang="ar">' + de + '</title>' + "\n")
            else:
                prog.append(4 * ' ' + '<title lang="ar">' +tit.replace('&#39;', "'")+ '</title>' + "\n")
        for tt, p, d in zip(time_chan, prog, desc):
            alls.append(tt + p + d )
            
                
        alls.pop(-1)
        for x in alls:
            with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
                f.write(x)
        print '2M epg downloaded for : '+str(end_date[-2])+' days'
    except:pass
   
if __name__ == '__main__': 
    snrt()
    arriadia()
    mm()

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