from Plugins.Plugin import PluginDescriptor
import interfaces
from Screens.MessageBox import MessageBox
import urllib2
from urllib2 import urlopen, Request, URLError, HTTPError 

def checkInternet():
    try:
        response = urllib2.urlopen("http://google.com", None, 5)
        response.close()
    except urllib2.HTTPError:
        return False
    except urllib2.URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True

def main(session, **kwargs):
    if checkInternet:
        session.open(interfaces.EPGIConfig)
    else:
        session.open(MessageBox, "Check your internet", MessageBox.TYPE_INFO)
  
def Plugins(**kwargs):
	return PluginDescriptor(
			name="EPG GRABBER",
			description="EPG WEB GRABBER BY ZIKO",
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon="epg.png",
			fnc=main)

