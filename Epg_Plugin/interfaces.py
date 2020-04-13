from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Screens.Console import Console
from Components.Input import Input
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from urllib2 import Request
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigYesNo, configfile
import io,os,re,sys
import gettext
reload(sys)
sys.setdefaultencoding('utf8')

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

HD = False
try:
    if enigma.getDesktop(0).size().width() >= 1280:
		HD = True
except:
    pass

def DreamOS():
    if os.path.exists('/var/lib/dpkg/status'):
        return DreamOS

class EPGIConfig(Screen):
    if HD:
		skin = """
			<screen position="center,center" size="600,500" title="EPG Import Configuration">
				<ePixmap name="red" position="0,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on" />
				<ePixmap name="green" position="140,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on" />
				<ePixmap name="yellow" position="280,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on" />
				<ePixmap name="blue" position="420,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on" />
				<ePixmap position="562,0" size="35,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on" />
				<widget name="key_red" position="0,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1" />
				<widget name="key_green" position="140,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1" shadowColor="background" />
				<widget name="key_yellow" position="280,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1" shadowColor="background" />
				<widget name="key_blue" position="420,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1" shadowColor="background" />
				<widget name="config" position="10,70" size="590,320" scrollbarMode="showOnDemand" />
				<widget font="Regular;18" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="left" position="545,480" render="Label" size="55,20" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
					<convert type="ClockToText">Default</convert>
				</widget>
				<widget name="status" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,400" size="580,60" font="Regular;20" />
			</screen>"""
    else:
        skin = """
            <screen position="center,center" size="938,476" title="EPG Import Configuration">
            <ePixmap name="red" position="0,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
            <ePixmap name="green" position="140,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
            <ePixmap name="yellow" position="280,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on"/>
            <ePixmap name="blue" position="420,0" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on"/>
            <ePixmap position="562,0" size="35,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on"/>
            <widget name="key_red" position="0,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;20" transparent="1" shadowColor="background"/>
            <widget name="key_green" position="140,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;20" transparent="1" shadowColor="background"/>
            <widget name="key_yellow" position="280,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;20" transparent="1" shadowColor="background"/>
            <widget name="key_blue" position="420,0" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;20" transparent="1" shadowColor="background"/>
            <widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,60" size="911,321" scrollbarMode="showOnDemand"/>
            <widget name="status" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,396" size="911,71" font="Regular;20"/>
        </screen>"""
###### End 
    def __init__(self, session, args = 0):
        if DreamOS():
		    self.wget = "/usr/bin/wget2 --no-check-certificate"
        else:
		    self.wget = "/usr/bin/wget"
        self.session = session
        list = []
        list.append(("Bein Sports EPG", "1"))
        #list.append(("Osn arabic + english title EPG", "2"))
        list.append(("Osn EPG", "2"))
        #list.append(("Osn on demand EPG", "4"))
        list.append(("Bein entertainment EPG", "3"))
        list.append(("SNRT EPG", "4"))
        list.append(("ELCINEMA WEBSITE EPG", "5"))
        list.append(("OSN BACKUP EPG", "6"))
        list.append(("ELCINEMA BACKUP EPG", "7"))
        Screen.__init__(self, session)
        self.skinName = ["E2m3u2bConfig", "EPGIConfig", "EPGMainSetup"]
        self["status"] = Label()
        self["config"] = MenuList(list)
        #self.setup_title = _("EPG GRABBER BY ZIKO ")
        self.update()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Timezone"))
        self["key_blue"] = Button(_("Set time"))
        self["key_yellow"] = Button(_("Change time"))
        self["setupActions"] = ActionMap(["SetupActions","MovieSelectionActions","ColorActions",'MenuActions'],
        {
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
        #choices.append(("Install New version %s" %self.new_version, "Install"))
        if EnablecheckUpdate == False:
            choices.append(("Press Ok to [Enable checking for Online Update]","enablecheckUpdate"))
        else:
            choices.append(("Press Ok to [Disable checking for Online Update]","disablecheckUpdate")) 
        from Screens.ChoiceBox import ChoiceBox
        self.session.openWithCallback(self.choicesback, ChoiceBox, _('select task'),choices)

    def choicesback(self, select):
        if select:
            #if select[1] == "Install":
            #         self.install(True)
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
            cmdlist.append("%s https://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh -O - | /bin/sh" % self.wget)
            from Plugins.Extensions.Epg_Plugin.Console import Console
            self.session.open(Console, title='Installing last update, enigma will be started after install', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False,endstr="")
    def myCallback(self,result):
         return
######### End #########
    def update(self):
        f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
        self["status"].setText("Current time zone  : "+f1.read())
        f1.close()
    
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
                                self.session.open(MessageBox,_("current ons backup time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("osn.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
                    
            if returnValue == "7":
                if fileExists("/etc/epgimport/elcinema.xml"):
                    f = open('/etc/epgimport/elcinema.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinback.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/elcinema.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/elcinema.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current elcinema backup time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("elcinema.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
            
    def __layoutFinished(self):
            os.chmod("/usr/bin/wget2",0755)
            self.new_version = Ver ### Add By RAED
            if config.plugins.EpgPlugin.update.value:
            	self.checkupdates() ### Add By RAED
            self.setTitle("EPG GRABBER BY ZIKO V %s" % Ver) ### Edit by RAED

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
            elif returnValue == "2":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
            elif returnValue == "3":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
            elif returnValue == "4":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/aloula.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
            elif returnValue == "5":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinema.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
            elif returnValue == "6":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/osn.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)
            elif returnValue == "7":
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/elcinema.txt","w",encoding='UTF-8')as f1:
                    f1.write(new_time.decode('utf-8'))
                    self.session.open(MessageBox,_("time changed with succes "+new_time), MessageBox.TYPE_INFO,timeout=10)

    def keyRed(self):
        self.close(None)

    def keyGreen(self):
        if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt'):
            with io.open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "w",encoding="utf-8") as f:
                f.write(("+0000").decode('utf-8'))
        try:
            f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
            self.session.openWithCallback(self.msg, InputBox,title=_("Please enter your time zone :"), text=f.read(), maxSize=5,type=Input.TEXT)
            f.close()
        except Exception as e:
            self.session.open(MessageBox,_(e), MessageBox.TYPE_INFO,timeout=10)

    def msg(self,time):
        if time is None:
                pass
        elif re.match(r'^[\-+\d{4}]+$',time) and time.startswith('+') or time.startswith('-'):
            with io.open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt','w',encoding='UTF-8') as f:
                f.write((time).decode('utf-8'))
                self.session.open(MessageBox,_("Your time offset changed with success : %s ")% (time), MessageBox.TYPE_INFO,timeout=10)
                self["status"].setText("Current time zone : "+time)
        else:
            self.session.open(MessageBox,_("Not a valide format, exemple : +0000/+0100/-01000 "), MessageBox.TYPE_INFO,timeout=10)

    def go(self):
        self.session.openWithCallback(self.install, MessageBox, _('Do you want to Download now?!'), MessageBox.TYPE_YESNO)

    def install(self,answer=False):
        returnValue = self["config"].l.getCurrentSelection()[1]
        if answer:
            if returnValue is not None:
                if returnValue == "1":
                    self.session.open(Console,_("EPG BEIN SPORTS") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/bein.py"], closeOnSuccess=False)
                    cprint("Downloading EPG BEIN SPORTS")
                elif returnValue == "2":
                    self.session.open(Console,_("EPG OSN") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/osn.py"], closeOnSuccess=False)
                    cprint("Downloading EPG OSN")
                elif returnValue == "3":
                    self.session.open(Console,_("EPG Bein entertainment") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/beinent.py"], closeOnSuccess=False)
                    cprint("Downloading EPG Bein entertainment")
                elif returnValue == "4":
                    self.session.open(Console,_("EPG SNRT") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/aloula.py"], closeOnSuccess=False)
                    cprint("Downloading EPG SNRT")
                elif returnValue == "5":
                    self.session.open(Console,_("ELCINEMA EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/elcin.py"], closeOnSuccess=False)
                    cprint("Downloading ELECINEMA EPG")
                elif returnValue == "6":
                    self.session.open(Console,_("OSN BACKUP EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/osnbackup.py"], closeOnSuccess=False)
                    cprint("Downloading OSN BACKUP EPG")
                elif returnValue == "7":
                    self.session.open(Console,_("elcinema BACKUP EPG") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/elcinemabackup.py"], closeOnSuccess=False)
                    cprint("Downloading elcinema BACKUP EPG")
