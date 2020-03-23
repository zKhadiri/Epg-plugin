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
import io,os,re,sys
reload(sys)
sys.setdefaultencoding('utf8')
##################################
class EPGImportConfig(Screen):
    def __init__(self, session, args = 0):
        self.session = session
        list = []
        list.append(("Bein Sports EPG", "1"))
        list.append(("Osn arabic + english title EPG", "2"))
        list.append(("Osn english title only EPG", "3"))
        list.append(("Osn on demand EPG", "4"))
        list.append(("Bein entertainment EPG", "5"))
        list.append(("SNRT EPG", "6"))
        Screen.__init__(self, session)
        self.skinName = ["E2m3u2bConfig", "EPGImportConfig", "EPGMainSetup"]
        self["status"] = Label()
        self["config"] = MenuList(list)
        self.setup_title = _("EPG GRABBER BY ZIKO ")
        self.update()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Timezone"))
        self["key_blue"] = Button(_("Channels"))
        self["key_yellow"] = Button(_("Change time"))
        self["setupActions"] = ActionMap(["SetupActions","MovieSelectionActions","ColorActions"],
        {
            "ok": self.go,
            "green": self.keyGreen,
            "blue": self.KeyBlue,
            "yellow": self.settime,
            "cancel": self.keyRed
        }, -1)
        self.onLayoutFinish.append(self.__layoutFinished)

    def update(self):
        f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
        self["status"].setText("Current time zone : "+f.read())
        f.close()
    
    def settime(self):
        returnValue = self["config"].l.getCurrentSelection()[1]
        if returnValue is not None:
            if returnValue == "1":
                if fileExists("/etc/epgimport/bein.xml"):
                    f = open('/etc/epgimport/bein.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
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
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/osn.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/osn.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current osn ar+en time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("osn.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
            
            if returnValue == "3":
                if fileExists("/etc/epgimport/osn.xml"):
                    f = open('/etc/epgimport/osn.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/osn.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/osn.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current osn en time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("osn.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
            
            if returnValue == "4":
                if fileExists("/etc/epgimport/osnd.xml"):
                    f = open('/etc/epgimport/osnd.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                    newtime=f1.read()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/osnd.xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/osnd.xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current osn on demand time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_("osnd.xml not found in path"), MessageBox.TYPE_INFO,timeout=10)
                    
            if returnValue == "5":
                if fileExists("/etc/epgimport/beinent.xml"):
                    f = open('/etc/epgimport/beinent.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
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
                    
            if returnValue == "6":
                if fileExists("/etc/epgimport/aloula.xml"):
                    f = open('/etc/epgimport/aloula.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
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
            
    def __layoutFinished(self):
            self.setTitle(self.setup_title)

    def  KeyBlue(self):
        self.session.open(Console,_("CHANNELS") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/show.py"])

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
        returnValue = self["config"].l.getCurrentSelection()[1]
        if returnValue is not None:
            if returnValue == "1":
                self.session.open(Console,_("EPG BEIN SPORTS") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/bein.pyo"])
            elif returnValue == "2":
                self.session.open(Console,_("EPG OSN ARABIC + ENGLISH TITLE") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/osn.pyo"])
            elif returnValue == "3":
                self.session.open(Console,_("EPG OSN ENGLISH TITLE ONLY") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/osnen.pyo"])
            elif returnValue == "4":
                self.session.open(Console,_("EPG OSN ON DEMAND") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/ondemand.pyo"])
            elif returnValue == "5":
                self.session.open(Console,_("EPG Bein entertainment") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/beinent.pyo"])
            elif returnValue == "6":
                self.session.open(Console,_("EPG SNRT") , ["%s" % "python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/aloula.pyo"])
            else:
                self.close(None)