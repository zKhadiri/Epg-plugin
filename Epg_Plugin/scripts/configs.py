import requests,sys,io


print('Downloading custom.channels config')
sys.stdout.flush()
custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.channels.xml?raw=true')
with io.open('/etc/epgimport/custom.channels.xml','w',encoding="utf-8") as f:
    f.write(custom_channels.text)
        

print('Downloading custom sources config')
sys.stdout.flush()
custom_source=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/custom.sources.xml?raw=true')
with io.open('/etc/epgimport/custom.sources.xml','w',encoding="utf-8") as f:
    f.write(custom_source.text)


print('Downloading elcinema channels config')
sys.stdout.flush()
elcinema_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/elcinema.channels.xml?raw=true')
with io.open('/etc/epgimport/elcinema.channels.xml','w',encoding="utf-8") as f:
    f.write(elcinema_channels.text)


print('Downloading dstv channels config')
sys.stdout.flush()
dstv_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/dstv.channels.xml?raw=true')
with io.open('/etc/epgimport/dstv.channels.xml','w',encoding="utf-8") as f:
    f.write(dstv_channels.text)

print('Downloading jawwy channels config')
jaw_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/jawwy.channels.xml?raw=true')
with io.open('/etc/epgimport/jawwy.channels.xml','w',encoding="utf-8") as f:
    f.write(jaw_channels.text)


print('Downloading freesat channels config')
free_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/freesat.channels.xml?raw=true')
with io.open('/etc/epgimport/freesat.channels.xml','w',encoding="utf-8") as f:
    f.write(free_channels.text)