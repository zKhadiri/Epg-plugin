import sys, os

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

from Plugins.Extensions.EPGGrabber.core.compat import PY3
from Plugins.Extensions.EPGGrabber.core.header import xml_header,close_xml
from Plugins.Extensions.EPGGrabber.core.timezone import tz
from Plugins.Extensions.EPGGrabber.core.paths import *
