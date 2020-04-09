#!/bin/sh
##setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=3.6
description=What is NEW:\n[new update]
##############################################################
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
wget -q "--no-check-certificate"  "https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/Epg_Plugin-"$version".tar.gz"
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
