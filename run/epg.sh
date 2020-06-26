#!/bin/sh

echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/bein.py
wait 
python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/mbc.py
wait 
python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/beinent.py
exit 0
