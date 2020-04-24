# -*- coding: utf-8 -*-
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Input import Input
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from urllib2 import Request
from Plugins.Extensions.Epg_Plugin.Console2 import Console2
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigYesNo, configfile
import io,os,re
import gettext
from enigma import getDesktop
################################## Add By RAED


config.plugins.EpgPlugin = ConfigSubsection()
config.plugins.EpgPlugin.update = ConfigYesNo(default=True)

REDC =  '\033[31m'                                                              
ENDC = '\033[m'                                                                 
                                                                                
def cprint(text):                                                               
        print REDC+text+ENDC 

def logdata(label_name = '', data = None):
    try:
        data=str(data)
        fp = open('/tmp/EPG_Plugin.log', 'a')
        fp.write( str(label_name) + ': ' + data+"\n")
        fp.close()
    except:
        trace_error()    
        pass

def getversioninfo():
    currversion = '1.0'
    version_file = '/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/version'
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split('=')[1].strip()
        except:
            pass
    return (currversion)

Ver = getversioninfo()

reswidth = getDesktop(0).size().width()

#def DreamOS():
#    if os.path.exists('/var/lib/dpkg/status'):
#        return DreamOS

class EPGIConfig(Screen):
    if reswidth == 1280:
        skin = """
            <screen position="center,center" size="762,528" title="ZIKO EPG GRABBER" backgroundColor="#16000000" flags="wfNoBorder">
  		<widget source="Title" position="5,6" size="743,41" render="Label" font="Regular;26" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  		<widget font="Regular;28" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="322,47" render="Label" size="122,32" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
    			<convert type="ClockToText">Default</convert>
  		</widget>
  		<ePixmap name="red" position="40,470" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
  		<ePixmap name="green" position="190,470" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
  		<ePixmap name="yellow" position="340,470" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on"/>
  		<ePixmap name="blue" position="490,470" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on"/>
  		<ePixmap position="638,474" size="35,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on"/>
  		<widget name="key_red" position="40,470" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  		<widget name="key_green" position="190,470" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  		<widget name="key_yellow" position="340,470" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  		<widget name="key_blue" position="490,470" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  		<widget name="config" position="10,80" size="745,310" scrollbarMode="showOnDemand"/>
  		<widget name="status" foregroundColor="#00ff2525" position="15,425" size="724,30" font="Regular;20"/>
  		<widget name="glb" foregroundColor="#00ffffff" position="15,395" size="722,25" font="Regular;20"/>
            </screen>"""
    else:
	if os.path.exists('/var/lib/dpkg/status'):
        	skin = """
            		<screen position="center,185" size="1222,707" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
  				<widget source="Title" position="5,6" size="1210,63" render="Label" font="Regular;45" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  				<widget font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="514,73" render="Label" size="177,45" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
    					<convert type="ClockToText">Default</convert>
  				</widget>
  				<ePixmap name="red" position="230,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
  				<ePixmap name="green" position="420,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
  		<ePixmap name="yellow" position="618,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on"/>
  				<ePixmap name="blue" position="810,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on"/>
  				<ePixmap position="1010,658" size="35,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on"/>
  				<widget name="key_red" position="202,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="key_green" position="395,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="key_yellow" position="595,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="key_blue" position="784,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,125" size="1196,388" scrollbarMode="showOnDemand"/>
  				<widget name="status" foregroundColor="#00ff2525" backgroundColor="#16000000" position="15,579" size="1174,54" font="Regular;35"/>
  				<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,519" size="1174,54" font="Regular;35"/>
            		</screen>"""
	else:
        	skin = """
            		<screen position="center,185" size="1222,707" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
  				<widget source="Title" position="5,6" size="1210,63" render="Label" font="Regular;45" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  				<widget font="Regular;40" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="514,73" render="Label" size="177,45" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
    					<convert type="ClockToText">Default</convert>
  				</widget>
  				<ePixmap name="red" position="230,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
  				<ePixmap name="green" position="420,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
  		<ePixmap name="yellow" position="618,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on"/>
  				<ePixmap name="blue" position="810,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on"/>
  				<ePixmap position="1010,658" size="35,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on"/>
  				<widget name="key_red" position="202,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="key_green" position="395,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="key_yellow" position="595,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="key_blue" position="784,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  				<widget name="config" font="Regular;35" itemHeight="45" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,125" size="1196,388" scrollbarMode="showOnDemand"/>
  				<widget name="status" foregroundColor="#00ff2525" backgroundColor="#16000000" position="15,579" size="1174,54" font="Regular;35"/>
  				<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,519" size="1174,54" font="Regular;35"/>
            		</screen>"""
###### End 
    def __init__(self, session, args = 0):
        self.session = session
        list = []
        list.append(("Bein Sports EPG", "1"))
        list.append(("Osn EPG", "2"))
        list.append(("Bein entertainment EPG", "3"))
        list.append(("SNRT EPG", "4"))
        list.append(("ELCINEMA WEBSITE EPG", "5"))
        list.append(("OSN BACKUP EPG", "6"))
        list.append(("MBC.NET", "7"))
        list.append(("DSTV.ZA", "8"))
        Screen.__init__(self, session)
        self.skinName = ["EPGIConfig"]
        self["status"] = Label()
        self["glb"] = Label()
        self["config"] = MenuList(list)
        f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt", "r")
        self["status"].setText("Current bein sports time zone  : "+f1.read().strip())
        f1.close()
        f2 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
        self["glb"].setText("Global timezone : "+f2.read().strip())
        f2.close()
        self.update()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Timezone"))
        self["key_blue"] = Button(_("Set time"))
        self["key_yellow"] = Button(_("Change time"))
        self["setupActions"] = ActionMap(["SetupActions","MovieSelectionActions","ColorActions",'MenuActions','WizardActions','ShortcutActions'],
        {
            "down": self.down,
            "up": self.up,
            "ok": self.go,
            "green": self.keyGreen,
            "blue": self.KeyBlue,
            "yellow": self.settime,
            "menu":self.showsetup,
            "cancel": self.keyRed
        }, -1)
        self.onLayoutFinish.append(self.__layoutFinished)
        
######### Add Update online by RAED (Fairbird) #####
    def showsetup(self):
        choices=[]
        self.list = []
        EnablecheckUpdate = config.plugins.EpgPlugin.update.value
        if EnablecheckUpdate == False:
            choices.append(("Press Ok to [Enable checking for Online Update]","enablecheckUpdate"))
        else:
            choices.append(("Press Ok to [Disable checking for Online Update]","disablecheckUpdate")) 
        from Screens.ChoiceBox import ChoiceBox
        self.session.openWithCallback(self.choicesback, ChoiceBox, _('select task'),choices)

    def choicesback(self, select):
        if select:
            if select[1] == "enablecheckUpdate":
                config.plugins.EpgPlugin.update.value = True
                config.plugins.EpgPlugin.update.save()
                configfile.save()
            elif select[1] == "disablecheckUpdate":
                config.plugins.EpgPlugin.update.value = False
                config.plugins.EpgPlugin.update.save()
                configfile.save()

    def checkupdates(self):
        from twisted.web.client import getPage, error
        url = 'https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh'
        getPage(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10).addCallback(self.parseData).addErrback(self)

    def addErrback(self, result):
        logdata("data-failed",result) 
        if result:
            logdata("Error:",str(result))

    def parseData(self, data):
        if data:
            lines=data.split("\n")
            for line in lines:
                if line.startswith("version"):
                   self.new_version=str(line.split("=")[1])
                if line.startswith("description"):
                   self.new_description = str(line.split("=")[1])
                   break
        if float(Ver)==float(self.new_version) or float(Ver)>float(self.new_version):
            logdata("Updates","No new version available")
        else :
            self.session.openWithCallback(self.installupdate, MessageBox, _('New version %s is available.\n\n%s.\n\nDo you want to install it now.' % (self.new_version, self.new_description)), MessageBox.TYPE_YESNO)

    def installupdate(self,answer=False):
        if answer:
            cmdlist = []
            cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh')
            self.session.open(Console2, title='Installing last update, enigma will be started after install', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False,endstr="")
    def myCallback(self,result):
        return
     
######### End #########
    def up(self):
        self["config"].up()
        self.update()
       
    def down(self):
        self["config"].down()
        self.update()

    def update(self):
        returnValue = self["config"].l.getCurrentSelection()[1]
        if returnValue == "1":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt", "r")
            self["status"].setText("Current bein sports time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="2":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt", "r")
            self["status"].setText("Current osn time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="3":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt", "r")
            self["status"].setText("Current Bein entertainment time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="4":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt", "r")
            self["status"].setText("Current snrt time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="5":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinema.txt", "r")
            self["status"].setText("Current elcinema time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="6":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osnback.txt", "r")
            self["status"].setText("Current osn backup time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="7":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/mbc.txt", "r")
            self["status"].setText("Current mbc time zone  : "+f1.read().strip())
            f1.close()
        elif returnValue =="8":
            f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt", "r")
            self["status"].setText("Current dstv time zone  : "+f1.read().strip())
            f1.close()
        else:
            self["status"].setText("")
            
            
    
    def settime(self):
        returnValue = self["config"].l.getCurrentSelection()[1]
        if returnValue is not None:
            if returnValue == "1":
                if fileExists("/etc/epgimport/bein.xml"):
                    f = open('/etc/epgimport/bein.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/bein.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/bein.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current bein sports time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("bein.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
            
            if returnValue == "2":
                if fileExists("/etc/epgimport/osn.xml"):
                    f = open('/etc/epgimport/osn.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/osn.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/osn.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current osn time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("osn.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
            
            if returnValue == "3":
                if fileExists("/etc/epgimport/beinent.xml"):
                    f = open('/etc/epgimport/beinent.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/beinent.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/beinent.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current Bein entertainment time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("beinent.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
            if returnValue == "4":
                if fileExists("/etc/epgimport/aloula.xml"):
                    f = open('/etc/epgimport/aloula.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/aloula.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/aloula.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current snrt time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("aloula.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
            if returnValue == "5":
                if fileExists("/etc/epgimport/elcinema.xml"):
                    f = open('/etc/epgimport/elcinema.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinema.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/elcinema.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/elcinema.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current elcinema time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("elcinema.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
            if returnValue == "6":
                if fileExists("/etc/epgimport/osn.xml"):
                    f = open('/etc/epgimport/osn.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osnback.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/osn.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/osn.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current osn backup time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("osn.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
            if returnValue == "7":
                if fileExists("/etc/epgimport/mbc.xml"):
                    f = open('/etc/epgimport/mbc.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/mbc.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/mbc.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/mbc.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current mbc time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("mbc.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
            if returnValue == "8":
                if fileExists("/etc/epgimport/dstv.xml"):
                    f = open('/etc/epgimport/dstv.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/dstv.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/dstv.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current dstv time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("dstv.xml not found in path"), MessageBox.TYPE_INFO,timeout=10) 
           
            
    def __layoutFinished(self):
        self.new_version = Ver
        if config.plugins.EpgPlugin.update.value:
            self.checkupdates()
        self.setTitle("EPG GRABBER BY ZIKO V %s" % Ver)

    def KeyBlue(self):
        returnValue = self["config"].l.getCurrentSelection()[1]
        if returnValue is not None:
            if returnValue == "1":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current bein sports time zone  : "+new_time)

            elif returnValue == "2":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current osn time zone  : "+new_time)

            elif returnValue == "3":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/beinent.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current Bein entertainment time zone  : "+new_time)
            elif returnValue == "4":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current snrt time zone  : "+new_time)
            elif returnValue == "5":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinema.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current elcinema time zone  : "+new_time)
            elif returnValue == "6":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osnback.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current osn backup time zone  : "+new_time)
                    
            elif returnValue == "7":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/mbc.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current mbc time zone  : "+new_time)
                    
            elif returnValue == "8":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/dstv.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current dstv time zone  : "+new_time)

    def keyRed(self):
        self.close(None)

    def keyGreen(self):
        f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
        self.session.openWithCallback(self.msg, InputBox,title=_("Please enter your time zone :"), text=f.read(), maxSize=5,type=Input.TEXT)
        f.close()
    
    def msg(self,time):
        if time is None:
            pass
        elif re.match(r'^[\-+\d{4}]+$',time) and time.startswith('+') or time.startswith('-'):
            with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt','w',encoding='UTF-8') as f:
                f.write((time).decode('utf-8'))
                self.session.open(MessageBox,_("Your time offset changed with success : %s ")% (time), MessageBox.TYPE_INFO,timeout=10)
                self["glb"].setText("Global timezone : "+time)
        else:
            self.session.open(MessageBox,_("Not a valide format, exemple : +0000/+0100/-01000 "), MessageBox.TYPE_INFO,timeout=10)
            
    def go(self):
        self.session.openWithCallback(self.install, MessageBox, _('Do you want to Download now?!'), MessageBox.TYPE_YESNO)

    def install(self,answer=False):
        returnValue = self["config"].l.getCurrentSelection()[1]
        if answer:
            if returnValue is not None:
                if returnValue == "1":
                    self.session.open(Console2,_("EPG BEIN SPORTS") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/bein.py"], closeOnSuccess=False)
                    cprint("Downloading EPG BEIN SPORTS")
                elif returnValue == "2":
                    self.session.open(Console2,_("EPG OSN") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/osn.py"], closeOnSuccess=False)
                    cprint("Downloading EPG OSN")
                elif returnValue == "3":
                    self.session.open(Console2,_("EPG Bein entertainment") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/beinent.py"], closeOnSuccess=False)
                    cprint("Downloading EPG Bein entertainment")
                elif returnValue == "4":
                    self.session.open(Console2,_("EPG SNRT") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/aloula.py"], closeOnSuccess=False)
                    cprint("Downloading EPG SNRT")
                elif returnValue == "5":
                    self.session.open(Console2,_("ELCINEMA EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/elcin.py"], closeOnSuccess=False)
                    cprint("Downloading ELECINEMA EPG")
                elif returnValue == "6":
                    self.session.open(Console2,_("OSN BACKUP EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/osnbackup.py"], closeOnSuccess=False)
                    cprint("Downloading OSN BACKUP EPG")
                elif returnValue == "7":
                    self.session.open(Console2,_("MBC EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/mbc.py"], closeOnSuccess=False)
                    cprint("Downloading MBC EPG")
                elif returnValue == "8":
                    self.session.open(Console2,_("DSTV EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/dstv.py"], closeOnSuccess=False)
                    cprint("Downloading DSTV EPG")
                
