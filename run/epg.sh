#!/bin/sh

echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

python /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers/bein.py &

exit 0