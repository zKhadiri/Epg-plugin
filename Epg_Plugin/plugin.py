from Plugins.Plugin import PluginDescriptor
import interfaces
from Screens.MessageBox import MessageBox
import requests


def connected_to_internet(): ## to test connection	
    try:
        _ = requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False
    print connected_to_internet()

def main(session, **kwargs):
    if connected_to_internet()==True:
        session.open(interfaces.EPGIConfig)
    else:
        session.open(MessageBox,_("No internet connection available. Or github.com Down"), MessageBox.TYPE_INFO,timeout=10)
  
def Plugins(**kwargs):
	return PluginDescriptor(
			name="EPG GRABBER",
			description="EPG WEB GRABBER BY ZIKO",
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon="epg.png",
			fnc=main)

