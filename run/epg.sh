#!/bin/sh

echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

for epgpy in $(find /usr/lib/enigma2/python/Plugins/Extensions/EPGGrabber/providers -name '*.py')
do
 if [[ $epgpy != *'__init__.py'* ]]; then
 python $epgpy
 wait
 fi
done

exit 0
