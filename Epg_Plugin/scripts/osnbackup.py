import os,io,re,sys
reload(sys)
sys.setdefaultencoding('utf8')

def DreamOS():
    if os.path.exists('/var/lib/dpkg/status'):
        return DreamOS

if DreamOS():
	wget = "/usr/bin/wget2 --no-check-certificate"
else:
	wget = "/usr/bin/wget"


with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt','r') as f:
    time_zone = f.read().strip()
    
path = '/etc/epgimport/osn.xml'   

os.system(''+wget+' https://github.com/ziko-ZR1/XML/raw/master/osn.xml -O '+path+'')

f = open(path,'r')
time_of = re.search(r'[+#-]+\d{4}',f.read())
f.close()

print "changing to your timezone please wait...."

if os.path.exists(path):
    if time_of !=None:
        with io.open(path,encoding="utf-8") as f:
            newText=f.read().decode('utf-8').replace(time_of.group(), time_zone)
            with io.open(path, "w",encoding="utf-8") as f:
                f.write((newText).decode('utf-8'))
    else:
        print "file is empty"
                
                
print "osn.xml donwloaded with succes"