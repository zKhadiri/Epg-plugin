#!/bin/sh
##setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=21.7
description=What_is_NEW:\n'-some Fix and Update For Script and id channels by (MOHAMED19OS)'
##############################################################

TEMPATH=/tmp

PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber
OLDPLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin
ExtensionsPLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions

# remove old version
rm -rf $OLDPLUGINPATH
rm -rf $PLUGINPATH

# check depends packges
if [ -f /etc/apt/apt.conf ] ; then
   STATUS='/var/lib/dpkg/status'
   OS='DreamOS'
elif [ -f /etc/opkg/opkg.conf ] ; then
   STATUS='/var/lib/opkg/status'
   OS='Opensource'
fi
###############
if python --version 2>&1 | grep -q '^Python 3\.'; then
   echo "You have Python3 image"
   PYTHON='PY3'
   PYTHONPACK='python3-requests'
else
   echo "You have Python2 image"
   PYTHON='PY2'
   PYTHONPACK='python-requests'
fi
################
if grep -q $PYTHONPACK $STATUS; then
    requests='Installed'
fi
################
if grep -q 'enigma2-plugin-extensions-epgimport' $STATUS; then
    epgimport='Installed'
fi
################
if [ $requests = "Installed" -a $epgimport = "Installed" ]; then
     echo ""
else

     if grep -q $PYTHONPACK $STATUS; then
          echo ""
     else
          if [ $OS = "DreamOS" ]; then 
                  echo " Downloading $PYTHONPACK ......"
                  apt-get install python-requests -y
          elif [ $PYTHON = "PY2" ]; then 
                  echo " Downloading $PYTHONPACK ......"
                  opkg install python-requests
          elif [ $PYTHON = "PY3" ]; then 
                  echo " Downloading $PYTHONPACK ......"
                  opkg install python3-requests
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
############################
if grep -q $PYTHONPACK $STATUS; then
	echo ""
else
	echo "#########################################################"
	echo "#         Feed cannot download ($PYTHONPACK)            #"
	echo "#         Epg_Plugin has not been works well            #"
	echo "#########################################################"
#	exit 1
fi
############################
echo ""
# Download and install plugin
cd /tmp
set -e
echo " Downloading And Insallling Epg_Plugin plugin ......"
echo 
# wget -q "--no-check-certificate"  "https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/Epg_Plugin-"$version".tar.gz"
# tar -xzf Epg_Plugin-"$version".tar.gz -C /
wget -O - --no-check-certificate https://github.com/ziko-ZR1/Epg-plugin/archive/master.tar.gz | tar xz "Epg-plugin-master/src/EPGGrabber"
mv Epg-plugin-master/src/EPGGrabber $ExtensionsPLUGINPATH
rm -r Epg-plugin-master
# rm -f Epg_Plugin-"$version".tar.gz
set +e
cd ..
sync
############################
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
