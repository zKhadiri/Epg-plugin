#!/bin/sh
##setup command=wget https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=2.9
description=What is NEW:\n[Add option Yes/No Before downlod job]
##############################################################
#### EDit By RAED To DreamOS OE2.5/2.6
if [ -f /var/lib/dpkg/status ]; then
      if [ -f /usr/bin/wget2 ]; then
            chmod 755 /usr/bin/wget2
            WGET='/usr/bin/wget2 --no-check-certificate'
      else
            echo "[Your image can not download wget2]"
            echo "[Please downoad it manually from (https://github.com/ziko-ZR1/Epg-plugin/blob/master/Download/wget2)]"
            echo "[Then send it to /usr/bin, And try again to dowload plugin]"
            exit 1
       fi
else
      WGET='/usr/bin/wget'
fi
# remove old version
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin

# check depends packges

opkg update

if [ -f /var/lib/dpkg/status ]; then
   STATUS=/var/lib/dpkg/status
else
   STATUS=/var/lib/opkg/status
fi
if grep -q python-requests $STATUS ; then
     echo ""
else
     echo "Need to download python-requests"
     opkg install python-requests
fi
echo ""
if grep -q enigma2-plugin-extensions-epgimport $STATUS ; then
     echo ""
else
     echo "Need to download epgimport plugin"
     opkg install enigma2-plugin-extensions-epgimport
fi

# Download and install plugin

cd /tmp
set -e
$WGET "https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/Epg_Plugin-"$version".tar.gz"

tar -xzf Epg_Plugin-"$version".tar.gz -C /
set +e
rm -f Epg_Plugin-"$version".tar.gz
cd ..

sync
echo "#########################################################"
echo "#          Epg_Plugin INSTALLED SUCCESSFULLY            #"
echo "#                BY ZIKO - support on                   #"
echo "#   https://www.tunisia-sat.com/forums/threads/4062301/ #"
echo "#########################################################"
echo "#           your Device will RESTART Now                #"
echo "#########################################################"
sleep 3
killall -9 enigma2
exit 0
