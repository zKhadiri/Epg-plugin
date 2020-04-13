#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep,strftime
import os,io,re


with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osnback.txt','r') as f:
    time_zone = f.read().strip()
    
path = '/etc/epgimport/osn.xml'

print "Downloading osn epg guide\nPlease wait...."  

os.system('wget -q "--no-check-certificate" https://github.com/ziko-ZR1/XML/blob/master/osn.xml?raw=true -O '+path+'')

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