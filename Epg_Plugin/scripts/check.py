import os,io,requests,sys
if not os.path.exists('/etc/epgimport/custom.channels.xml'):
    print('Downloading custom.channels config')
    sys.stdout.flush()
    custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.channels.xml?raw=true')
    with io.open('/etc/epgimport/custom.channels.xml','w',encoding="utf-8") as f:
        f.write(custom_channels.text)
        
if not os.path.exists('/etc/epgimport/custom.sources.xml'):
    print('Downloading custom sources config')
    sys.stdout.flush()
    custom_source=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.sources.xml?raw=true')
    with io.open('/etc/epgimport/custom.sources.xml','w',encoding="utf-8") as f:
        f.write(custom_source.text)

if not os.path.exists('/etc/epgimport/elcinema.channels.xml'):
    print('Downloading elcinema channels config')
    sys.stdout.flush()
    elcinema_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/elcinema.channels.xml?raw=true')
    with io.open('/etc/epgimport/elcinema.channels.xml','w',encoding="utf-8") as f:
        f.write(elcinema_channels.text)

if not os.path.exists('/etc/epgimport/dstv.channels.xml'):
    print('Downloading dstv channels config')
    sys.stdout.flush()
    dstv_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/dstv.channels.xml?raw=true')
    with io.open('/etc/epgimport/dstv.channels.xml','w',encoding="utf-8") as f:
        f.write(dstv_channels.text)

if not os.path.exists('/etc/epgimport/jawwy.channels.xml'):
    print('Downloading jawwy channels config')
    sys.stdout.flush()
    jaw_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/jawwy.channels.xml?raw=true')
    with io.open('/etc/epgimport/jawwy.channels.xml','w',encoding="utf-8") as f:
        f.write(jaw_channels.text)

if not os.path.exists('/etc/epgimport/freesat.channels.xml'):
    print('Downloading freesat channels config')
    sys.stdout.flush()
    free_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/freesat.channels.xml?raw=true')
    with io.open('/etc/epgimport/freesat.channels.xml','w',encoding="utf-8") as f:
        f.write(free_channels.text)
        
if not os.path.exists('/etc/epgimport/skyit.channels.xml'):
    print('Downloading skyit channels config')
    sys.stdout.flush()
    sky_it=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/skyit.channels.xml?raw=true')
    with io.open('/etc/epgimport/skyit.channels.xml','w',encoding="utf-8") as f:
        f.write(sky_it.text)
        
if not os.path.exists('/etc/epgimport/bein.channels.xml'):
    print('Downloading bein.channels config')
    sys.stdout.flush()
    bein_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/bein.channels.xml?raw=true')
    with io.open('/etc/epgimport/bein.channels.xml','w',encoding="utf-8") as f:
        f.write(bein_channels.text)