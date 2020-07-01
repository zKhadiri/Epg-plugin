# -*- coding: utf-8 -*-
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
import io,os,re,requests,gettext,json
from enigma import getDesktop
from enigma import loadPNG,gPixmapPtr, RT_WRAP, ePoint, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from scripts import status

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
		<screen position="center,center" size="762,562" title="ZIKO EPG GRABBER" backgroundColor="#16000000" flags="wfNoBorder">
  			<widget source="Title" position="8,10" size="743,35" render="Label" font="Regular;26" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  			<eLabel text="Select providers to install and press red button" position="10,42" size="663,43" font="Regular;24" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000"/>
  			<widget font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="615,5" render="Label" size="143,52" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
    				<convert type="ClockToText">Default</convert>
  			</widget>
  			<ePixmap name="red" position="40,520" zPosition="2" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/red.png" transparent="1" alphatest="on"/>
  			<ePixmap position="658,55" size="60,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menu.png" alphatest="on" zPosition="5"/>
  			<widget name="key_red" position="40,520" size="140,40" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;19" transparent="1"/>
  			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,90" size="745,360" scrollbarMode="showOnDemand"/>
  			<widget name="glb" foregroundColor="#00ffffff" position="15,458" size="724,28" font="Regular;24"/>
  			<widget name="status" foregroundColor="#000080ff" position="15,487" size="724,28" font="Regular;24"/>
		</screen>"""
    else:
        skin = """
		<screen position="center,center" size="1222,809" title="ZIKO EPG GRABBER" flags="wfNoBorder" backgroundColor="#16000000">
  			<widget source="Title" position="5,10" size="1210,50" render="Label" font="Regular;40" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
  			<eLabel text="Select providers to install and press red button" position="20,67" size="951,60" font="Regular;35" foregroundColor="#00ff2525" zPosition="4" valign="center" backgroundColor="#16000000"/>
  			<widget font="Regular;55" foregroundColor="#00ffffff" backgroundColor="#16000000" halign="center" position="962,8" render="Label" size="259,84" source="global.CurrentTime" transparent="1" valign="center" zPosition="5">
    				<convert type="ClockToText">Default</convert>
  			</widget>
  			<ePixmap name="red" position="17,755" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/redfhd.png" transparent="1" alphatest="on"/>
  			<ePixmap position="1042,87" size="103,35" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/key_menufhd.png" alphatest="on"/>
  			<widget name="key_red" position="17,755" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
  			<widget name="config" foregroundColor="#00ffffff" backgroundColor="#16000000" position="10,140" size="1196,488" scrollbarMode="showOnDemand"/>
  			<widget name="glb" foregroundColor="#00ffffff" backgroundColor="#16000000" position="15,653" size="1174,54" font="Regular;35"/>
  			<widget name="status" foregroundColor="#000080ff" backgroundColor="#16000000" position="15,699" size="1174,54" font="Regular;35"/>
		</screen>"""
###### End 
    def __init__(self, session, args = 0):
        self.session = session
        list = []
        self.installList=[] ## New from mf to make choose list
                                            #py    
        list.append(("Bein Sports EPG", "0","bein"))
        list.append(("Bein entertainment EPG", "1","beinent"))
        list.append(("Osnplay english title arabic description BACKUP", "2","osnplay"))
        list.append(("OSN دليل عربي بالكامل (haxer source)", "3","osnar"))
        list.append(("OSN english only epg BACKUP (haxer source)", "4","osnen"))
        list.append(("ELCINEMA WEBSITE EPG", "5","elcin"))
        list.append(("ELCINEMA Bein entertainment EPG", "6","beincin"))
        list.append(("FILFAN WEBSITE", "7","filfan"))
        list.append(("MBC.NET/QATAR TV/NOOR DUBAI", "8","mbc"))
        list.append(("Jawwy TV", "9","jawwy"))
        list.append(("SNRT EPG", "10","aloula"))
        list.append(("FREESAT UK", "11","freesat"))
        list.append(("UK SPORTS CHANNELS", "12","skyuk"))
        list.append(("DSTV.ZA", "13","dstv"))
        list.append(("SuperSport.ZA BACKUP", "14","dstvback"))
        list.append(("SETANTA eurasia", "15","setanta"))
        self.provList=list ## New from mf to make choose list
        Screen.__init__(self, session)
        self.skinName = ["EPGIConfig"]
        self["status"] = Label()
        self["glb"] = Label()
        #self["config"] = MenuList(list)
        self["config"] = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.update()
        self["key_red"] = Button(_("Install"))
        self["setupActions"] = ActionMap(["EpgColorActions",'EpgMenuActions','EpgWizardActions','EpgShortcutActions'],
        {
            "down": self.down,
            "up": self.up,
            "ok": self.go,
            "red": self.keyRed,
            "menu":self.showsetup,
            "cancel": self.close,
        }, -1)
        self.onShown.append(self.onWindowShow)
        self.check_status()
        
    def check_status(self):
        self.statusOS = status.Statusosn()
        self.statusDS = status.Statusdstv()
        self.StatuseosnAR = status.StatuseosnAR()
        self.StatuseosnEN = status.StatuseosnEN()

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
        choices.append(("ASSIGN SERVICE TO CHANNELS","sref"))
        choices.append(("DOWNLOAD THE LATEST CONFIGS [NOT THAT OLD CONFIGS WILL BE DISCARDED]","config"))
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
            elif select[1]=='sref':
                import ref
                servicelist=None
                global Servicelist
                import Screens.InfoBar
                Servicelist = servicelist or Screens.InfoBar.InfoBar.instance.servicelist
                global epg_bouquet
                epg_bouquet = Servicelist and Servicelist.getRoot()
                if epg_bouquet is not None:
                    from ServiceReference import ServiceReference
                    services = ref.getBouquetServices(epg_bouquet)
                    service = Servicelist.servicelist.getCurrent()
                    self.session.openWithCallback(ref.closed,ref.set_ref, services, service, ServiceReference(epg_bouquet).getServiceName())
            elif select[1]=="config":
                self.session.open(Console2,_("EPG CONFIGS") , ["python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/configs.py"], closeOnSuccess=False)

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

    def update(self):
        index=self['config'].getSelectionIndex()
        returnValue=self.provList[index][1]
        for i in range(len(self.provList)):
            if returnValue == str(i):
                with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as json_file:
                    data = json.load(json_file)
                provName = self.provList[i][2]
                for channel in data['bouquets']:
                    if channel["bouquet"]==provName:
                        self["glb"].setText("last update : {}".format(channel["date"]))
                if provName=="osnplay":
                    self["status"].setText('Last commit : '+self.statusOS)
                elif provName=='osnar':
                    self["status"].setText('Last commit : '+self.StatuseosnAR)
                elif provName=='osnen':
                    self["status"].setText('Last commit : '+self.StatuseosnEN)
                elif provName=='dstvback':
                    self["status"].setText('Last commit : '+self.statusDS)
                else:
                    self["status"].setText("")
          
    def keyRed(self): ## New from mf to make choose list
        if len(self.installList)>0:
		  ## Code to find connection internet or not
		    self.install()
      
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
            if provTag == "jawwy":
                cmd="python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/jawwy.pyc"
            else:
                cmd="python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/%s.py" % provTag
            cmdList.append(cmd)
            cmdList.append("python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/check.py")
        self.session.open(Console2,_("EPG install started") , cmdList, closeOnSuccess=False)