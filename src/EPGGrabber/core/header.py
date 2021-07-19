#!/usr/bin/python
# -*- coding: utf-8 -*-

from .compat import PY3
import io


def xml_header(path, channels):
    file = open(path, 'w')
    if PY3:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<tv generator-info-name="By ZR1">')
    else:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n'.decode('utf-8'))
        file.write(('<tv generator-info-name="By ZR1">').decode('utf-8'))
    file.close()
    
    for channel in channels:
        with io.open(path, "a", encoding='UTF-8')as f:
            if PY3:
                f.write("\n" + '  <channel id="' + channel + '">' + "\n" + '    <display-name lang="en">' + channel + '</display-name>' + "\n" + '  </channel>\r')
            else:
                f.write(("\n" + '  <channel id="' + channel + '">' + "\n" + '    <display-name lang="en">' + channel + '</display-name>' + "\n" + '  </channel>\r').decode('utf-8'))
                
                
def close_xml(path):
    file = open(path, 'a')
    if PY3:
        file.write('\n' + '</tv>')
    else:
        file.write(('\n' + '</tv>').decode('utf-8'))
        
    file.close()
    
