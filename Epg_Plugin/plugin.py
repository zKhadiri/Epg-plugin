from Plugins.Plugin import PluginDescriptor
from interfaces import EPGGrabber
from Screens.MessageBox import MessageBox
import requests


def connected_to_internet():	
    try:
        _ = requests.get('https://github.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def main(session, **kwargs):
    if connected_to_internet():
        session.open(EPGGrabber)
    else:
        session.open(MessageBox,_("No internet connection available. Or github.com Down"), MessageBox.TYPE_INFO,timeout=10)
  
def Plugins(**kwargs):
    Descriptors=[]
    Descriptors.append(PluginDescriptor(name="EPG GRABBER",description="EPG WEB GRABBER BY ZIKO",where = PluginDescriptor.WHERE_PLUGINMENU,icon="epg.png",fnc=main))
    Descriptors.append(PluginDescriptor(name="EPG GRABBER",where = PluginDescriptor.WHERE_EXTENSIONSMENU,fnc=main))
    return Descriptors

