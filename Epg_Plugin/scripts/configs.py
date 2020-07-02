import requests,sys,io

print('Downloading custom.sources config')
sys.stdout.flush()
custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/configs/custom.sources.xml?raw=true')
with io.open('/etc/epgimport/custom.channels.xml','w',encoding="utf-8") as f:
    f.write(custom_channels.text)
        
print('Downloading latest channels list')
sys.stdout.flush()
custom_channels=requests.get('https://github.com/ziko-ZR1/Epg-plugin/blob/master/Epg_Plugin/configs/bouquets.json?raw=true')
with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/bouquets.json','w',encoding="utf-8") as f:
    f.write(custom_channels.text)