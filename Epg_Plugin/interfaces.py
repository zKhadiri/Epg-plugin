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
from enigma import loadPNG,gPixmapPtr, RT_WRAP, ePoint, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest

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

def connected_to_internet(): ## to test connection
    import requests
    try:
        _ = requests.get('http://www.google.com', timeout=5)
        print("internet connection available.")
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
        return False
    print connected_to_internet()

class EPGIConfig(Screen):
    if reswidth == 1280:
        skin = """
		<screen position="center,center" size="762,562" title="ZIKO EPG GRABBER" backgroundColor="#16000000" flags="wfNoBorder">
  			<widget source="Title" position="8,10" size="743,35" render="Label" font="Regular;26" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  			<eLabel text="Select providers to install and press red button" position="10,42" size="663,43" font="Regular;24" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000"/>
  			<widget font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="615,5" render="Label" size="143,52" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
    				<convert type="ClockToText">Default</convert>
  			</widget>
  			<ePixmap name="red" position="40,520" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
  			<ePixmap name="green" position="210,520" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
  			<ePixmap name="yellow" position="380,520" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on"/>
  			<ePixmap name="blue" position="557,520" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on"/>
  			<ePixmap position="658,55" size="60,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on" zPosition="5"/>
  			<widget name="key_red" position="40,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  			<widget name="key_green" position="210,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  			<widget name="key_yellow" position="380,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  			<widget name="key_blue" position="557,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,90" size="745,360" scrollbarMode="showOnDemand"/>
  			<widget name="glb" foregroundColor="#00ffffff" position="15,458" size="724,28" font="Regular;24"/>
  			<widget name="status" foregroundColor="#000080ff" position="15,487" size="724,28" font="Regular;24"/>
		</screen>"""
    else:
# 	if os.path.exists('/var/lib/dpkg/status'):
#         	skin = """
#            		<screen position="center,185" size="1222,707" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
#                        <widget source="Title" position="5,6" size="1210,63" render="Label" font="Regular;45" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
#                        <eLabel text = "Select providers to install" position = "0,73" size = "514,45" font = "Regular;36" foregroundColor = "#00ffffff" zPosition = "10"  valign = "center" halign = "left"  backgroundColor = "#16000000"/>
#                        <widget font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="514,73" render="Label" size="177,45" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
#                                <convert type="ClockToText">Default</convert>
#                        </widget>
#                        <ePixmap name="red" position="230,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
#                        <ePixmap name="green" position="420,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/green.png" transparent="1" alphatest="on"/>
#                        <ePixmap name="yellow" position="618,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellow.png" transparent="1" alphatest="on"/>
#                        <ePixmap name="blue" position="810,655" zPosition="2" size="195,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/blue.png" transparent="1" alphatest="on"/>
#                        <ePixmap position="1010,658" size="35,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on"/>
#                        <widget name="key_red" position="202,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
#                        <widget name="key_green" position="395,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
#                        <widget name="key_yellow" position="595,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
#                        <widget name="key_blue" position="784,655" size="200,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
#                        <widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,125" size="1196,388" scrollbarMode="showOnDemand"/>
#                        <widget name="status" foregroundColor="#00ff2525" backgroundColor="#16000000" position="15,579" size="1174,54" font="Regular;35"/>
#                        <widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,519" size="1174,54" font="Regular;35"/>
#            		</screen>""" -->
#	else:
        skin = """
		<screen position="center,center" size="1222,809" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
  			<widget source="Title" position="5,10" size="1210,50" render="Label" font="Regular;40" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  			<eLabel text="Select providers to install and press red button" position="20,67" size="951,60" font="Regular;35" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000"/>
  			<widget font="Regular;55" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="962,8" render="Label" size="259,84" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
    				<convert type="ClockToText">Default</convert>
  			</widget>
  			<ePixmap name="red" position="17,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/redfhd.png" transparent="1" alphatest="on"/>
 			<ePixmap name="green" position="335,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/greenfhd.png" transparent="1" alphatest="on"/>
  			<ePixmap name="yellow" position="640,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/yellowfhd.png" transparent="1" alphatest="on"/>
  			<ePixmap name="blue" position="941,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/bluefhd.png" transparent="1" alphatest="on"/>
  			<ePixmap position="1042,87" size="103,35" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menufhd.png" alphatest="on"/>
  			<widget name="key_red" position="17,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  			<widget name="key_green" position="335,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  			<widget name="key_yellow" position="640,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  			<widget name="key_blue" position="941,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,140" size="1196,488" scrollbarMode="showOnDemand"/>
  			<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,653" size="1174,54" font="Regular;35"/>
  			<widget name="status" foregroundColor="#000080ff" backgroundColor="#16000000" position="15,699" size="1174,54" font="Regular;35"/>
		</screen>"""
###### End 
    def __init__(self, session, args = 0):
        self.session = session
        list = []
        self.installList=[] ## New from mf to make choose list
                                            #py    #times  #xml_file
        list.append(("Bein Sports EPG", "0","bein","bein","bein"))
        list.append(("Bein entertainment EPG", "1","beinent","beinent","beinent"))
        list.append(("ondemand/yahala/yahala oula EPG", "2","osn","osn","osn"))
        list.append(("Osnplay BACKUP", "3","osnplay","osnback","osnplay"))
        list.append(("ELCINEMA WEBSITE EPG", "4","elcin","elcinema","elcinema"))
        list.append(("ELCINEMA Bein entertainment EPG", "5","beincin","entc","beinentCin"))
        list.append(("MBC.NET", "6","mbc","mbc","mbc"))
        list.append(("SNRT EPG", "7","aloula","aloula","aloula"))
        list.append(("Spacetoon epg", "8","spacetoon","space","spacetoon"))
        list.append(("DSTV.ZA", "9","dstv","dstv","dstv"))
        list.append(("SuperSport.ZA BACKUP", "10","dstvback","dstvback","dstv"))
        self.provList=list ## New from mf to make choose list
        Screen.__init__(self, session)
        self.skinName = ["EPGIConfig"]
        self["status"] = Label()
        self["glb"] = Label()
        #self["config"] = MenuList(list)
        self["config"] = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/bein.txt", "r")
        self["status"].setText("Current bein sports time zone  : "+f1.readlines()[0].strip())
        f1.close()
        f2 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
        self["glb"].setText("Global timezone : "+f2.read().strip())
        f2.close()
        self.update()
        self["key_red"] = Button(_("Install"))
        self["key_green"] = Button(_("Timezone"))
        self["key_blue"] = Button(_("Set time"))
        self["key_yellow"] = Button(_("Change time"))
        self["setupActions"] = ActionMap(["EpgColorActions",'EpgMenuActions','EpgWizardActions','EpgShortcutActions'],
        {
            "down": self.down,
            "up": self.up,
            "ok": self.go,
            "red": self.keyRed,
            "green": self.keyGreen,
            "blue": self.KeyBlue,
            "yellow": self.settime,
            "menu":self.showsetup,
            "cancel": self.close,
            "info":self.info
            
        }, -1)
        self.onShown.append(self.onWindowShow)

    def onWindowShow(self):
        self.onShown.remove(self.onWindowShow)
        self.new_version = Ver
        if config.plugins.EpgPlugin.update.value:
            self.checkupdates()
        self.setTitle("EPG GRABBER BY ZIKO V %s" % Ver)
        self["key_red"].hide() ## New from mf to make choose list
        self.iniMenu() ## New from mf to make choose list
        
    def iniMenu(self): ## New from mf to make choose list
        cacolor = 16776960
        cbcolor = 16753920
        cccolor = 15657130
        cdcolor = 16711680
        cecolor = 16729344
        cfcolor = 65407
        cgcolor = 11403055
        chcolor = 13047173
        cicolor = 13789470
        scolor = cbcolor
        res = []        
        gList=[]
        if reswidth == 1280:
            self["config"].l.setItemHeight(50)
            self["config"].l.setFont(0, gFont('Regular', 24))
        else:
            self["config"].l.setItemHeight(80)
            self["config"].l.setFont(0, gFont('Regular', 36))
        for i in range(0, len(self.provList)):
            provider = self.provList[i][0]
            if reswidth == 1280:
                png='/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/epg.png'
            else:
                png='/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/epgfhd.png'
            if provider in self.installList:
                if reswidth == 1280:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/ok.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/okfhd.png'
            res.append(MultiContentEntryText(pos=(0, 1), size=(0, 0), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text='', color=scolor, color_sel=cccolor, border_width=3, border_color=806544))
            if reswidth == 1280:
                res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(35, 35), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(60, 8), size=(723, 40), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(provider), color=16777215, color_sel=16777215))
            else:
                res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(50, 50), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(80, 8), size=(1080, 60), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(provider), color=16777215, color_sel=16777215))
            gList.append(res)
            res = []
        self["config"].l.setList(gList)
        self["config"].show()

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
            self.session.open(Console2, title='Installing last update, enigma will be started after install', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

    def myCallback(self,result=None):
        return

    def up(self):
        self["config"].up()
        self.update()
       
    def down(self):
        self["config"].down()
        self.update()


    def info(self):
        index=self['config'].getSelectionIndex()
        returnValue=self.provList[index][1]
        for i in range(len(self.provList)):
            if returnValue == str(i):
                provTag = self.provList[i][3]
                provName = self.provList[i][0]
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/{}.txt".format(provTag), "r")
                new_time = f.readlines()[1].strip()
                f.close()
                self.session.open(MessageBox,_('{} Last update : \n{} '.format(provName,new_time)),MessageBox.TYPE_INFO,timeout=15)
    
    def update(self):
        index=self['config'].getSelectionIndex()
        returnValue=self.provList[index][1]
        for i in range(len(self.provList)):
            if returnValue == str(i):
                provTag = self.provList[i][3]
                provName = self.provList[i][0]
                f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/"+provTag+".txt", "r")
                self["status"].setText("Current {} time zone  : {}".format(provName,f1.readlines()[0].strip()))
                f1.close()
                
    def KeyBlue(self):
        index=self['config'].getSelectionIndex()
        returnValue=self.provList[index][1]
        for i in range(len(self.provList)):
            if returnValue == str(i):
                provTag = self.provList[i][3]
                provName = self.provList[i][0]
                f = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/offset.txt", "r")
                new_time = f.read().strip()
                f.close()
                with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/{}.txt".format(provTag)) as f:
                    lines1 = f.readlines()
                lines1[0] = new_time+'\n'
                with open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/{}.txt".format(provTag),"w")as f1:
                    f1.writelines(lines1)
                    self.session.open(MessageBox,_("time changed with succes {}".format(new_time)), MessageBox.TYPE_INFO,timeout=10)
                    self["status"].setText("Current {} time zone  : {}".format(provName,new_time))
    
    def settime(self):
        index=self['config'].getSelectionIndex()
        returnValue=self.provList[index][1]
        for i in range(len(self.provList)):
            if returnValue == str(i):
                provTag = self.provList[i][3]
                provName = self.provList[i][0]
                provFile = self.provList[i][4]
                if fileExists("/etc/epgimport/"+provFile+".xml"):
                    f = open('/etc/epgimport/'+provFile+'.xml','r')
                    time_of = re.search(r'[+#-]+\d{4}',f.read())
                    f.close()
                    f1 = open("/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times/"+provTag+".txt", "r")
                    newtime=f1.readlines()[0].strip()
                    f1.close()
                    if time_of !=None:
                        with io.open("/etc/epgimport/"+provFile+".xml",encoding="utf-8") as f:
                            newText=f.read().decode('utf-8').replace(time_of.group(), newtime)
                            with io.open("/etc/epgimport/"+provFile+".xml", "w",encoding="utf-8") as f:
                                f.write((newText).decode('utf-8'))
                                self.session.open(MessageBox,_("current "+provName+" time "+time_of.group()+" replaced by "+newtime), MessageBox.TYPE_INFO,timeout=10)
                    else:
                        self.session.open(MessageBox,_("File is empty"), MessageBox.TYPE_INFO,timeout=10)
                else:
                    self.session.open(MessageBox,_(provFile+".xml not found in path"), MessageBox.TYPE_INFO,timeout=10)

    def keyRed(self): ## New from mf to make choose list
        if len(self.installList)>0:
		if connected_to_internet() == True:  ## Code to find connection internet or not
			self.install()
		else:
			self.session.open(MessageBox,_("No internet connection available. Or github.com Down"), MessageBox.TYPE_INFO,timeout=10)

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
            
    def go(self): ## New from mf to make choose list
        index=self['config'].getSelectionIndex()
        provider=self.provList[index][0]
        if provider in self.installList:
            self.installList.remove(provider)
        else:   
            self.installList.append(provider)
        self.iniMenu()
        if len(self.installList)>0:
            self["key_red"].show()
        else:
            self["key_red"].hide() 
        #self.session.openWithCallback(self.install, MessageBox, _('Do you want to Download now?!'), MessageBox.TYPE_YESNO)

    def install(self): ## New from mf to make choose list
        index = self['config'].getSelectionIndex()
        provider = self.provList[index][0]
        cmdList=[]   
        for i in range(len(self.provList)):
            provider = self.provList[i][0]
            if not provider in self.installList:
                continue
            provTag = self.provList[i][2]    
            cmd="python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/%s.py" % provTag    
            cmdList.append(cmd)    
        self.session.open(Console2,_("EPG install started") , cmdList, closeOnSuccess=False)
