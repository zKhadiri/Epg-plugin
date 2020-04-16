#!/bin/sh
##setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=3.8
description=What_is_NEW:\n'[new update]'
##############################################################
# remove old version
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin
rm -f /tmp/*epgimport*
rm -f /tmp/*Epg_Plugin*

# check depends packges
if [ -f /etc/apt/apt.conf ] ; then
   STATUS='/var/lib/dpkg/status'
   OS='DreamOS'
elif [ -f /etc/opkg/opkg.conf ] ; then
   STATUS='/var/lib/opkg/status'
   OS='Opensource'
fi
if grep -q 'Package: python-requests' $STATUS; then
    requests='Installed'
fi
if grep -q 'Package: enigma2-plugin-extensions-epgimport' $STATUS; then
    epgimport='Installed'
fi
sleep 2
if [ $requests = "Installed" -a $epgimport = "Installed" ]; then
     echo ""
else
     echo "Need to download Depends packages"
     if [ $OS = "DreamOS" ]; then
          apt-get update
     else
          opkg update
     fi
     if grep -q 'Package: python-requests' $STATUS; then
          echo ""
     else
          if [ $OS = "DreamOS" ]; then 
                  echo " Downloading/Insallling python-requests ......"
                  apt-get install python-requests -y
          else
                  echo " Downloading/Insallling python-requests ......"
                  opkg install python-requests
          fi
     fi
     if grep -q 'Package: enigma2-plugin-extensions-epgimport' $STATUS; then
          echo ""
     else
          if [ $OS = "DreamOS" ]; then
                   echo " Downloading/Insallling epgimport ......"
                   sleep 3
		   wget -q "--no-check-certificate" "https://github.com/ziko-ZR1/Epg-plugin/blob/master/Download/enigma2-plugin-extensions-epgimport_1.0-r203-all.deb?raw=true" -O "/tmp/enigma2-plugin-extensions-epgimport_1.0-r203-all.deb";
                   dpkg -i /tmp/*.deb;
                   apt-get install -f -y;
          else
                   echo " Downloading/Insallling epgimport ......"
                   opkg install enigma2-plugin-extensions-epgimport
          fi
     fi
fi
sleep 2
echo ""
# Download and install plugin
echo " Downloading/Insallling Epg_Plugin plugin ......"
wget -q "--no-check-certificate" "https://github.com/ziko-ZR1/Epg-plugin/blob/master/Download/Epg_Plugin-"$version".tar.gz?raw=true" -O "/tmp/Epg_Plugin-"$version".tar.gz"
tar -xzf /tmp/Epg_Plugin-"$version".tar.gz -C /
rm -f /tmp/Epg_Plugin-"$version".tar.gz
echo ""
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
