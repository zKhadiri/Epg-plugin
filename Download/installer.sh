#!/bin/sh
##setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=10.2
description=What_is_NEW:\n'[NEW UPDATE]'
##############################################################

TEMPATH=/tmp
PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin

# remove old version
mv $PLUGINPATH/times.json $TEMPATH  > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin

# check depends packges
if [ -f /etc/apt/apt.conf ] ; then
   STATUS='/var/lib/dpkg/status'
   OS='DreamOS'
elif [ -f /etc/opkg/opkg.conf ] ; then
   STATUS='/var/lib/opkg/status'
   OS='Opensource'
fi
if grep -q 'python-requests' $STATUS; then
    requests='Installed'
fi
if grep -q 'enigma2-plugin-extensions-epgimport' $STATUS; then
    epgimport='Installed'
fi
if [ $requests = "Installed" -a $epgimport = "Installed" ]; then 
     echo ""
else
     echo "Need to download Depends packages"
     if [ $OS = "DreamOS" ]; then
          apt-get update
     else
          opkg update
     fi
     if grep -q 'python-requests' $STATUS; then
          echo ""
     else
          if [ $OS = "DreamOS" ]; then 
                  echo " Downloading python-requests ......"
                  apt-get install python-requests -y
          else
                  echo " Downloading python-requests ......"
                  opkg install python-requests
          fi
     fi
     if grep -q 'enigma2-plugin-extensions-epgimport' $STATUS; then
          echo ""
     else
          if [ $OS = "DreamOS" ]; then
                   echo " Downloading/Insallling epgimport ......"
                   sleep 3
                   wget -q "--no-check-certificate" "https://github.com/ziko-ZR1/Epg-plugin/blob/master/Download/enigma2-plugin-extensions-epgimport_2.0-r219_all.deb?raw=true" -O "/tmp/enigma2-plugin-extensions-epgimport_2.0-r219_all.deb";
                   dpkg -i /tmp/*.deb;
                   apt-get install -f -y;
          else
                   echo " Downloading/Insallling epgimport ......"
                   opkg install enigma2-plugin-extensions-epgimport
          fi
     fi
fi
echo ""
# Download and install plugin
cd /tmp
set -e
echo " Downloading And Insallling Epg_Plugin plugin ......"
echo 
wget -q "--no-check-certificate"  "https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/Epg_Plugin-"$version".tar.gz"
tar -xzf Epg_Plugin-"$version".tar.gz -C /
set +e
rm -f Epg_Plugin-"$version".tar.gz
mv $TEMPATH/times.json $PLUGINPATH  > /dev/null 2>&1
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
