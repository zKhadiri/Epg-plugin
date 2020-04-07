#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests,re,os,io
from time import strftime
from requests.adapters import HTTPAdapter

time_zone = strftime('%z')

import time
os.environ['TZ'] = 'UTC'


headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.100 Chrome/80.0.3987.100 Safari/537.36'
}

channe=[]
urls=[]

for i in range(0,3):
    import datetime
    from datetime import timedelta
    jour = datetime.date.today()
    week = jour + timedelta(days=i)
    urls.append('http://www.alaoula.ma/programmes.php?jr='+week.strftime('%d/%m/%Y')+'&lang=ar')

def snrt():
    channe.append('<?xml version="1.0" encoding="UTF-8"?>'+"\n"+'<tv generator-info-name="By ZR1">'+"\n"+'  <channel id="Aloula.ma">'+"\n"+'    <display-name lang="en">Aloula HD</display-name>'+"\n"+'  </channel>'+"\n")
    channe.append('  <channel id="Arriadia.ma">'+"\n"+'    <display-name lang="en">Arriadia HD</display-name>'+"\n"+'  </channel>'+"\n")
    channe.append('  <channel id="2M.ma">' + "\n" + '    <display-name lang="en">2M</display-name>' + "\n" + '  </channel>' + "\n")
    channe.append('  <channel id="athaqafia.ma">' + "\n" + '    <display-name lang="en">Athaqafia HD</display-name>' + "\n" + '  </channel>' + "\n")
    channe.append('  <channel id="Medi1tv.ma">' + "\n" + '    <display-name lang="en">Medi1tv</display-name>' + "\n" + '  </channel>' + "\r")
    with io.open("/etc/epgimport/aloula.xml","w",encoding='UTF-8')as f:
        f.write(''.join(channe).decode('utf-8'))
    prog = []
    desc = []
    cat = []
    time_chan = []
    try:
        for url in urls:
            prog[:] = []
            desc[:] = []
            cat[:] = []
            time_chan[:] = []
            link = requests.get(url,headers=headers)
            time = re.findall(r'<div class="\w+_\w+_\w+" style=";">(.*?)<\/div>',link.text)
            title= re.findall(r'<a\s+class="grille_item_title_12 grille_item_title_12_ar" style="">(.*?)<\/a>',link.text)
            titles =[re.sub(' +',' ',t).replace('-','') for t in title]
            
            for titl_ in titles:
                prog.append(4*' '+'<title lang="ar">' + titl_ + '</title>' + "\n")
                desc.append(4 * ' ' + '<desc lang="ar">' + titl_ + '</desc>' + "\n")
                cat.append(4 * ' ' + '<category lang="ar">' + titl_ +'</category>'+'\n'+'  </programme>'+'\n')
            from datetime import datetime
            actuel = datetime.now().strftime("%H:%M")
            times=[time_.replace(".", ":").replace("Actuellement", actuel).replace('h',':').replace('H',':').split() for time_ in time]
            for elem, next_elem in zip(times, times[1:] + [times[0]]):
                date = re.search(r'\d{2}/\d{2}/\d{4}',url)
                starttime = datetime.strptime(date.group()+' '+elem[0],'%d/%m/%Y %H:%M').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(date.group() + ' ' + next_elem[0], '%d/%m/%Y %H:%M').strftime('%Y%m%d%H%M%S')
                time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Aloula.ma">' + '\n')

            for tt,p,d,c in zip(time_chan,prog,desc,cat):
                print(tt+p+d+c)
                with io.open("/etc/epgimport/aloula.xml","a",encoding='UTF-8')as f:
                    f.write(tt+p+d+c)
    except:pass

    urls[:] = []
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

            for titl in title_ar:
                prog.append(4 * ' ' + '<title lang="ar">' + titl + '</title>' + "\n")
                desc.append(4 * ' ' + '<desc lang="ar">' + titl + '</desc>' + "\n")
                cat.append(4 * ' ' + '<category lang="ar">' + titl + '</category>' + '\n' + '  </programme>')
            from datetime import datetime
            for elem, next_elem in zip(time_ar, time_ar[1:] + [time_ar[0]]):
                date = re.search(r'\d{4}/\d{2}/\d{2}', url)
                starttime = datetime.strptime(date.group() + ' ' + elem, '%Y/%m/%d %H:%M').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(date.group() + ' ' + next_elem, '%Y/%m/%d %H:%M').strftime('%Y%m%d%H%M%S')
                time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Arriadia.ma">' + '\n')

            for tt,p,d,c in zip(time_chan,prog,desc,cat):
                print(tt+p+d+c)
                with io.open("/etc/epgimport/aloula.xml","a",encoding='UTF-8')as f:
                    f.write(tt+p+d+c)
    except:pass

    urls[:] = []
    for i in range(0, 3):
        import datetime, time
        from datetime import timedelta
        jour = datetime.date.today()
        week = jour + timedelta(days=i)
        from datetime import datetime
        urls.append('http://www.2m.ma/ar/guidetv/?day=' + str(int(time.mktime(datetime.strptime('' + str(week) + ' 00:00:00', "%Y-%m-%d %H:%M:%S").timetuple()))))
    try:
        for url in urls:
            prog[:] = []
            desc[:] = []
            cat[:] = []
            time_chan[:] = []
            with requests.Session() as s:
                s.mount('http://', HTTPAdapter(max_retries=10))
                r = s.get(url, headers=headers)
                title_2m = re.findall(r'bold\">(.*?)<\/h4>\s+<p', r.text)
                des_2m = re.findall(r'<p class="text-size12">(.*?)<\/p>', r.text)
                time_2m = re.findall(r'<span class=\"p-right-15 text-size22 roboto lighter\">(.*?)<\/span>', r.text)

                from datetime import datetime
                for elem, next_elem in zip(time_2m, time_2m[1:] + [time_2m[0]]):
                    date = re.search(r'=(\d+)', url)
                    days = datetime.fromtimestamp(int(date.group().replace('=', ''))).strftime("%Y-%m-%d")
                    starttime = datetime.strptime(days + ' ' + elem, '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    endtime = datetime.strptime(days + ' ' + next_elem, '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                    time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="2m.ma">' + '\n')

                for tit, de in zip(title_2m, des_2m):
                    desc.append(4 * ' ' + '<desc lang="ar">' + de + '</desc>' + "\n")
                    cat.append(4 * ' ' + '<category lang="ar">' + de + '</category>' + '\n' + '  </programme>'+'\n')
                    if tit == '':
                        prog.append(4 * ' ' + '<title lang="ar">' + de + '</title>' + "\n")
                    else:
                        prog.append(4 * ' ' + '<title lang="ar">' +tit.replace('&#39;', "'")+ '</title>' + "\n")
                for tt, p, d, c in zip(time_chan, prog, desc, cat):
                    print(tt + p + d + c)
                    with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
                        f.write(tt + p + d + c)
    except:pass
    urls[:] = []
    week = []
    for i in range(1, 4):
        urls.append('http://www.medi1tv.com/ar/inc/grille.aspx?d=' + str(i))
    try:
        for i in range(0, 3):
            import datetime
            from datetime import timedelta
            jour = datetime.date.today()
            week.append(jour + timedelta(days=i))
        for u, w in zip(urls, week):
            prog[:] = []
            desc[:] = []
            cat[:] = []
            time_chan[:] = []
            m = requests.get(u, headers=headers)
            time_medi = re.findall(r'\d{2}:\d{2}', m.text)
            title_medi = re.findall(r'>(.*?)<\/div>\s+<div\sclass=\"resume', m.text)
            for titlee in title_medi:
                prog.append(4 * ' ' + '<title lang="ar">' + titlee + '</title>' + "\n")
                desc.append(4 * ' ' + '<desc lang="ar">' + titlee + '</desc>' + "\n")
                cat.append(4 * ' ' + '<category lang="ar">' + titlee + '</category>' + '\n' + '  </programme>' + '\n')
            from datetime import datetime
            for elem, next_elem in zip(time_medi, time_medi[1:] + [time_medi[0]]):
                starttime = datetime.strptime(str(w) + ' ' + elem, '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(str(w) + ' ' + next_elem, '%Y-%m-%d %H:%M').strftime('%Y%m%d%H%M%S')
                time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="Medi1tv.ma">' + '\n')
            for tt, p, d, c in zip(time_chan, prog, desc, cat):
                print(tt + p + d + c)
                with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
                    f.write(tt + p + d + c)
    except:pass
    urls[:] = []
    for i in range(0, 3):
        import datetime
        from datetime import timedelta
        jour = datetime.date.today()
        week = jour + timedelta(days=i)
        urls.append('http://www.athaqafia.ma/programmes.php?jr=' + week.strftime('%d/%m/%Y') + '&lang=ar')
    try:
        for url in urls:
            prog[:] = []
            desc[:] = []
            cat[:] = []
            time_chan[:] = []
            link = requests.get(url, headers=headers)
            # title = re.findall(r'<a\s+class="grille_item_title_12 grille_item_title_12_ar" style="">(.*?)<\/a>', link.text)
            time_at = re.findall(r'<div class="\w+_\w+_\w+" style=";">(.*?)<\/div>', link.text)
            title_at = re.findall(r'<a\s+class="grille_item_title_12 grille_item_title_12_ar" style="">(.*?)<\/a>',link.text)
            titles_at = [re.sub(' +', ' ', t).replace('-', '') for t in title_at]

            for titl_ in titles_at:
                prog.append(4 * ' ' + '<title lang="ar">' + titl_ + '</title>' + "\n")
                desc.append(4 * ' ' + '<desc lang="ar">' + titl_ + '</desc>' + "\n")
                cat.append(4 * ' ' + '<category lang="ar">' + titl_ + '</category>' + '\n' + '  </programme>' + '\n')
            from datetime import datetime
            actuel = datetime.now().strftime("%H:%M")
            times_at = [time_.replace(".", ":").replace("Actuellement", actuel).replace('h',':').split() for time_ in time_at]

            for elem, next_elem in zip(times_at, times_at[1:] + [times_at[0]]):
                date = re.search(r'\d{2}/\d{2}/\d{4}', url)
                starttime = datetime.strptime(date.group() + ' ' + elem[0], '%d/%m/%Y %H:%M').strftime('%Y%m%d%H%M%S')
                endtime = datetime.strptime(date.group() + ' ' + next_elem[0], '%d/%m/%Y %H:%M').strftime('%Y%m%d%H%M%S')
                time_chan.append(2 * ' ' + '<programme start="' + starttime + ' '+time_zone+'" stop="' + endtime + ' '+time_zone+'" channel="athaqafia.ma">' + '\n')

            for tt, p, d, c in zip(time_chan, prog, desc, cat):
                print(tt + p + d + c)
                with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
                    f.write(tt + p + d + c)
    except:pass
    with io.open("/etc/epgimport/aloula.xml", "a", encoding='UTF-8')as f:
        f.write(('</tv>').decode('utf-8'))
        
    if not os.path.exists('/etc/epgimport/custom.channels.xml'):
        print('Downloading custom.channels config')
        ur = requests.get('http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/custom.channels.xml',headers=headers)
        if ur.status_code ==200:
            with io.open('/etc/epgimport/custom.channels.xml','w') as f:
                f.write(ur.text)
            print('Done')
        else:
            print('Cannot establish connection to the server')
        
    if not os.path.exists('/etc/epgimport/custom.sources.xml'):
        print('Downloading custom sources config')
        uri = requests.get('http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/custom.sources.xml',headers=headers)
        if uri.status_code==200:
            with io.open('/etc/epgimport/custom.sources.xml','w') as f:
                f.write(uri.text)
            print('Done')
        else:
            print('Cannot establish connection to the server')

    if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
        print('Downloading elcinema channels config')
        uri = requests.get('https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Epg_Plugin/configs/elcinema.channels.xml',headers=headers)
        if uri.status_code ==200:
            with io.open('/etc/epgimport/elcinema.channels.xml','w') as f:
                f.write(uri.text)
            print('Done')
        else:
            print('Cannot establish connection to the server')
    
if __name__ == '__main__':
    snrt()




