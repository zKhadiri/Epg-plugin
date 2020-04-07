import requests,io,re

fil = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt','r')
time_zone = fil.read().strip()
fil.close()

url = requests.get('https://raw.githubusercontent.com/ziko-ZR1/XML/master/osn.xml')
if url.status_code !=404:
    old_time = re.search(r'[+#-]+\d{4}',url.text)
    with io.open("/etc/epgimport/osn.xml","w",encoding='UTF-8')as f:
        f.write(url.text.replace(old_time.group(),time_zone))
        print('Finished')
else:
    print('Cannot establish connection to the server')