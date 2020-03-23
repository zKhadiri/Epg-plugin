from Plugins.Plugin import PluginDescriptor
import interfaces

def main(session, **kwargs):
	session.open(interfaces.EPGImportConfig)

def Plugins(**kwargs):
	return PluginDescriptor(
			name="EPG BY ZIKO",
			description="EPG GRABBER BY ZIKO",
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon="epg.png",
			fnc=main)

