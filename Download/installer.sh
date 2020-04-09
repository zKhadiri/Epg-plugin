#!/bin/sh
##setup command=wget https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=3.5
description=What is NEW:\n[new update]
##############################################################
AGENT='--header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/8.0 Safari/600.1.17"'
CRT="--debug --no-check-certificate"
# remove old version
# rm -rf /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin

# check depends packges

# opkg update

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
wget -q $AGENT $CRT "https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/Epg_Plugin-"$version".tar.gz"

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
