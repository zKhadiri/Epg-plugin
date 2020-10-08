# Created BY RAED 18-11-2019

from Screens.Screen import Screen
from Components.Pixmap import Pixmap

SKIN_Small_HD = """
		<screen name="EPGGrabber" position="center,center" size="762,562" title="ZIKO EPG GRABBER" backgroundColor="#16000000" flags="wfNoBorder">
  			<widget source="Title" position="8,10" size="743,35" render="Label" font="Regular;26" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  			<eLabel text="Select providers to install and press red button" position="10,42" size="663,43" font="Regular;24" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000"/>
  			<widget font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="615,5" render="Label" size="143,52" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
    				<convert type="ClockToText">Default</convert>
  			</widget>
  			<ePixmap name="red" position="40,525" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
            		<ePixmap name="green" position="210,525" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
  			<ePixmap position="658,55" size="60,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on" zPosition="5"/>
  			<widget name="key_red" position="40,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
            		<widget name="key_green" position="210,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,85" size="750,370" scrollbarMode="showOnDemand"/>
  			<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,462" size="724,28" font="Regular;24"/>
  			<widget name="status" foregroundColor="#000080ff" backgroundColor="#16000000" position="15,488" size="724,28" font="Regular;24"/>
		</screen>"""

SKIN_Small_FHD = """
		<screen name="EPGGrabber" position="center,center" size="1222,809" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
  			<widget source="Title" position="5,10" size="1210,50" render="Label" font="Regular;40" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  			<eLabel text="Select providers to install and press red button" position="20,67" size="951,60" font="Regular;35" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000"/>
  			<widget font="Regular;55" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="962,8" render="Label" size="259,84" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
    				<convert type="ClockToText">Default</convert>
  			</widget>
  			<ePixmap name="red" position="17,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/redfhd.png" transparent="1" alphatest="on"/>
            <ePixmap name="green" position="335,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/greenfhd.png" transparent="1" alphatest="on"/>
  			<ePixmap position="1042,87" size="103,35" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menufhd.png" alphatest="on"/>
  			<widget name="key_red" position="17,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
             <widget name="key_green" position="335,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,140" size="1196,488" scrollbarMode="showOnDemand"/>
  			<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,653" size="1174,54" font="Regular;35"/>
  			<widget name="status" foregroundColor="#000080ff" backgroundColor="#16000000" position="15,699" size="1174,54" font="Regular;35"/>
		</screen>"""

SKIN_Full_HD = """
		<screen name="EPGGrabber" position="0,0" size="1280,720" title="ZIKO EPG GRABBER" backgroundColor="#16000000" flags="wfNoBorder">
			<widget source="Title" position="center,13" size="782,40" render="Label" font="Regular;26" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1" halign="center"/>
			<eLabel text="Background of VideoPicture" foregroundColor="#00ffffff" backgroundColor="#00ffffff" size="543,272" position="688,100" zPosition="-10"/>
			<widget source="session.VideoPicture" render="Pig" position="693,105" size="532,263" backgroundColor="#ff000000" zPosition="1"/>
			<eLabel text="Select providers to install and press red button" position="25,49" size="591,43" font="Regular;24" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000" halign="center"/>
			<widget font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="1072,0" render="Label" size="206,44" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
			<convert type="ClockToText">Default</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="1072,44" size="206,40" font="Regular;28" halign="center" foregroundColor="#00ffffff" backgroundColor="#16000000" transparent="1">
			<convert type="ClockToText">Format:%d.%m.%Y</convert>
			</widget>
			<widget source="session.CurrentService" render="Label" position="688,372" zPosition="1" size="543,40" font="Regular;24" halign="center" foregroundColor="#00ff2525" backgroundColor="#16000000" transparent="1" valign="center">
			<convert type="ServiceName">Name</convert>
			</widget>
			<widget source="session.Event_Now" render="Label" position="688,408" zPosition="2" size="543,40" font="Regular;25" halign="center" foregroundColor="#00bab329" backgroundColor="#16000000" transparent="1" valign="center">
			<convert type="EventName">Name</convert>
			</widget>
			<ePixmap name="red" position="775,664" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
			<ePixmap name="green" position="966,663" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
			<ePixmap position="1144,671" size="60,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on" zPosition="5"/>
			<widget name="key_red" position="775,663" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
			<widget name="key_green" position="966,663" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="12,100" size="625,595" scrollbarMode="showOnDemand"/>
			<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="645,506" size="626,64" font="Regular;23" valign="center" halign="center" zPosition="1"/>
			<widget name="status" foregroundColor="#000080ff" backgroundColor="#16000000" position="645,551" size="626,64" font="Regular;23" valign="center" halign="center" zPosition="2"/>
		</screen>"""

SKIN_Full_FHD = """
		<screen name="EPGGrabber" position="0,0" size="1920,1080" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
			<widget source="Title" position="319,20" size="1210,65" render="Label" font="Regular;50" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1" halign="center"/>
			<widget source="session.VideoPicture" render="Pig" position="1017,168" size="827,437" backgroundColor="#ff000000" zPosition="1"/>
			<eLabel text="Background of VideoPicture" foregroundColor="#00ffffff" backgroundColor="#00ffffff" size="842,452" position="1010,160" zPosition="-10"/>
			<eLabel text="Select providers to install and press red button" position="22,86" size="933,72" font="Regular;38" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000" halign="center"/>
			<widget font="Regular;55" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="1565,3" render="Label" size="353,84" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
			<convert type="ClockToText">Default</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="1565,78" size="353,65" font="Regular;50" halign="center" foregroundColor="#00ffffff" backgroundColor="#16000000" transparent="1" zPosition="6">
			<convert type="ClockToText">Format:%d.%m.%Y</convert>
			</widget>
			<widget source="session.CurrentService" render="Label" position="1010,611" zPosition="1" size="842,68" font="Regular;34" halign="center" foregroundColor="#00ff2525" backgroundColor="#16000000" transparent="1" valign="center">
						<convert type="ServiceName">Name</convert>
			</widget>
			<widget source="session.Event_Now" render="Label" position="1010,671" zPosition="2" size="842,68" font="Regular;32" halign="center" foregroundColor="#00bab329" backgroundColor="#16000000" transparent="1" valign="center">
			<convert type="EventName">Name</convert>
			</widget>
			<ePixmap name="red" position="1092,999" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/redfhd.png" transparent="1" alphatest="on"/>
			<ePixmap name="green" position="1417,999" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/greenfhd.png" transparent="1" alphatest="on"/>
			<ePixmap position="1716,1006" size="103,35" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menufhd.png" alphatest="on"/>
			<widget name="key_red" position="1092,1005" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
			<widget name="key_green" position="1418,1005" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="20,160" size="932,895" scrollbarMode="showOnDemand"/>
			<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="963,769" size="948,92" font="Regular;32" zPosition="1" halign="center" valign="center"/>
			<widget name="status" foregroundColor="#000080ff" backgroundColor="#16000000" position="963,840" size="948,92" font="Regular;32" zPosition="2" halign="center" valign="center"/>
		</screen>"""
		
SKIN_ChoiceBox_HD = """
		  <screen name="ChoiceBox" position="150,100" size="550,400" title="Input">
    <widget name="text" position="10,10" size="550,25" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;20" transparent="1"/>
    <widget name="list" position="0,30" size="550,335" scrollbarMode="showOnDemand"/>
  </screen>"""

SKIN_ChoiceBox_FHD = """
		  <screen name="ChoiceBox" position="300,200" size="550,400" title="Input">
    <widget name="text" position="10,10" size="550,25" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;28" transparent="1"/>
    <widget name="list" position="0,30" size="750,435" scrollbarMode="showOnDemand"/>
  </screen>"""
