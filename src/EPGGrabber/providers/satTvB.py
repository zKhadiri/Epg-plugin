# -*- coding: utf-8 -*-

from time import sleep
import os
import io
import re
import sys
import requests
import json
from __init__ import *

time_zone = tz()

path = EPG_ROOT + '/satTv.xml'

print('**************SAT Tv backup EPG******************')
sys.stdout.flush()
print("Downloading SAT Tv guide\nPlease wait....")
sys.stdout.flush()

os.system("wget http://ipkinstall.ath.cx/EPG/satTv/satTv.xml -O "+path)

if time_zone != "+0000":
    print("changing to your timezone please wait....")
    sys.stdout.flush()
    if os.path.exists(path):
        f = open(path,'r')
        time_of = re.search(r'[+#-]+\d{4}',f.read())
        f.close()
        if time_of !=None:
            with io.open(path,encoding="utf-8") as f:
                if PY3:
                    newText=f.read().replace(time_of.group(), time_zone)
                else:
                    newText=f.read().decode('utf-8').replace(time_of.group(), time_zone)
                with io.open(path, "w",encoding="utf-8") as f:
                    if PY3:
                        f.write(newText)
                    else:
                        f.write((newText).decode('utf-8'))
        else:
            print("file is empty")

if os.path.exists('/var/lib/dpkg/status'):
    print('Dream os image found\nSorting data please wait.....')
    sortXML('satTv.xml')

print("satTv.xml donwloaded with success")

provider = __file__.rpartition('/')[-1].replace('.py', '')
update_status(provider)

print('**************FINISHED******************')
sys.stdout.flush()
