#!/usr/bin/python
# -*- coding: utf-8 -*-

# python3
from __future__ import print_function
from .scripts.compat import PY3

from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Input import Input
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from Plugins.Extensions.Epg_Plugin.Console2 import Console2
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigYesNo, configfile, ConfigSelection
import io,os,re,requests,gettext,json
from ServiceReference import ServiceReference
from Screens.ChoiceBox import ChoiceBox
from enigma import loadPNG,gPixmapPtr, RT_WRAP, ePoint, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest

### import class + screens from files inside plugin (Python3)
from .skin import *

try:
    from Plugins.Extensions.EPGImport.plugin import EPGImportConfig
    epgimport = True
except:
    epgimport =False
    pass

config.plugins.EpgPlugin = ConfigSubsection()
config.plugins.EpgPlugin.update = ConfigYesNo(default=True)
config.plugins.EpgPlugin.skin = ConfigSelection(default='smallscreen', choices=[('smallscreen', _('Small Screen')), ('fullscreen', _('Full Screen'))])

REDC =  '\033[31m'                                                              
ENDC = '\033[m'                                                                 
                                                                                
def cprint(text):                                                               
        print(REDC+text+ENDC)

def logdata(label_name = '', data = None):
    try:
        data=str(data)
        fp = open('/tmp/EPG_Plugin.log', 'a')
        fp.write( str(label_name) + ': ' + data+"\n")
        fp.close()
    except:
        trace_error()    
        pass

def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/EPG_PluginrError.log', 'a'))
    except:
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

def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())

def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280

def DataJs():
    file = open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json','r')
    data = json.loads(file.read())
    file.close()
    return data
    
#def DreamOS():
#    if os.path.exists('/var/lib/dpkg/status'):
#        return DreamOS

class EPGGrabber(Screen):

    def __init__(self, session, args = 0):
        self.session = session
        if config.plugins.EpgPlugin.skin.value == 'smallscreen':
                if isHD():
                        self.skin = SKIN_EPGGrabber_Small_HD
                else:
                        self.skin = SKIN_EPGGrabber_Small_FHD
        else:
                if isHD():
                        self.skin = SKIN_EPGGrabber_Full_HD
                else:
                        self.skin = SKIN_EPGGrabber_Full_FHD
        list = []
        self.installList=[] ## New from mf to make choose list
        
        for i in range(len(DataJs()['bouquets'])):
            list.append((DataJs()["bouquets"][i]["title"],i,DataJs()['bouquets'][i]["bouquet"]))
            
        self.provList=list ## New from mf to make choose list
        Screen.__init__(self, session)
        self.skinName = ["EPGGrabber"]
        self["status"] = Label()
        self["glb"] = Label()
        #self["config"] = MenuList(list)
        self["config"] = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.update()
        self["key_red"] = Button(_("Install"))
        self["key_green"] = Button(_("Epgimport"))
        self["setupActions"] = ActionMap(["EpgColorActions",'EpgMenuActions','EpgWizardActions','EpgShortcutActions'],
        {
            "down": self.down,
            "up": self.up,
            "ok": self.go,
            "red": self.keyRed,
            "menu":self.showsetup,
            "green": self.keyGreen,
            "cancel": self.close,
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
        if isHD():
            self["config"].l.setItemHeight(37)
            self["config"].l.setFont(0, gFont('Regular', 22))
        else:
            self["config"].l.setItemHeight(47)
            self["config"].l.setFont(0, gFont('Regular', 32))
        for i in range(0, len(self.provList)):
            provider = self.provList[i][0]
            if isHD():
                png='/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/epg.png'
            else:
                png='/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/epgfhd.png'
            if provider in self.installList:
                if isHD():
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/ok.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/okfhd.png'
            res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text='', color=scolor, color_sel=cccolor, border_width=3, border_color=806544))
            if isHD():
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(35, 35), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(50, 0), size=(723, 40), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(provider), color=16777215, color_sel=16777215))
            else:
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(45, 45), png=loadPNG(png)))
                res.append(MultiContentEntryText(pos=(70, 0), size=(1080, 60), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(provider), color=16777215, color_sel=16777215))
            gList.append(res)
            res = []
        self["config"].l.setList(gList)
        self["config"].show()

    def showsetup(self):
        choices=[]
        self.list = []
        SkinStyle = config.plugins.EpgPlugin.skin.value
        EnablecheckUpdate = config.plugins.EpgPlugin.update.value
        if SkinStyle == "smallscreen":
                choices.append(("Press Ok to [change skin to FullScreen]:","fullscreen"))
        else:
                choices.append(("Press Ok to [change skin to smallscreen]:","smallscreen"))
        if EnablecheckUpdate == False:
            choices.append(("Press Ok to [Enable checking for Online Update]","enablecheckUpdate"))
        else:
            choices.append(("Press Ok to [Disable checking for Online Update]","disablecheckUpdate"))
        choices.append(("Assign Service to channel","sref"))
        choices.append(("Download The Latest Channels List","config"))
        self.session.openWithCallback(self.choicesback, ChoiceBox, _('Select Task'),choices)

    def choicesback(self, select):
        if select:
            if select[1]=='smallscreen':
                config.plugins.EpgPlugin.skin.value = "smallscreen"
                config.plugins.EpgPlugin.skin.save()
                configfile.save()
                self.close()
            elif select[1] == "fullscreen":
                config.plugins.EpgPlugin.skin.value = "fullscreen"
                config.plugins.EpgPlugin.skin.save()
                configfile.save()
                self.close()
            elif select[1] == "enablecheckUpdate":
                config.plugins.EpgPlugin.update.value = True
                config.plugins.EpgPlugin.update.save()
                configfile.save()
            elif select[1] == "disablecheckUpdate":
                config.plugins.EpgPlugin.update.value = False
                config.plugins.EpgPlugin.update.save()
                configfile.save()
            elif select[1]=='sref':
                from Plugins.Extensions.Epg_Plugin import ref
                servicelist=None
                global Servicelist
                import Screens.InfoBar
                Servicelist = servicelist or Screens.InfoBar.InfoBar.instance.servicelist
                global epg_bouquet
                epg_bouquet = Servicelist and Servicelist.getRoot()
                if epg_bouquet is not None:
                    services = ref.getBouquetServices(epg_bouquet)
                    service = Servicelist.servicelist.getCurrent()
                    self.session.openWithCallback(ref.closed,ref.set_ref, services, service, ServiceReference(epg_bouquet).getServiceName())
            elif select[1]=="config":
                self.session.open(Console2,_("EPG Configs") , ["python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/configs.py"], closeOnSuccess=False)

    def checkupdates(self):
        try:
                from twisted.web.client import getPage, error
                url = 'http://raw.githubusercontent.com/ziko-ZR1/Epg-plugin/master/Download/installer.sh'
                getPage(str.encode(url), headers={b'Content-Type': b'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.addErrback)
        except Exception as error:
                trace_error()

    def addErrback(self,error=None):
        logdata("addErrback",error)

    def parseData(self, data):
        if PY3:
                data = data.decode("utf-8")
        else:
                data = data.encode("utf-8")
        if data:
            lines=data.split("\n")
            for line in lines:
                if line.startswith("version"):
                   self.new_version = line.split("=")[1]
                if line.startswith("description"):
                   self.new_description = line.split("=")[1]
                   break
        if float(Ver) == float(self.new_version) or float(Ver)>float(self.new_version):
            logdata("Updates","No new version available")
        else :
            new_version = self.new_version
            new_description = self.new_description
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
    
    def keyGreen(self):
        if epgimport:
            self["key_green"].show()
            self.session.open(EPGImportConfig)
        else:
            self["key_green"].hide()
            self.session.open(MessageBox,_("Epgimport is not installed"), MessageBox.TYPE_INFO,timeout=10)
    
    def readJs(self):
        import json
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/epg_status.json'):
            with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/epg_status.json','r')as f:
                try:
                    return json.loads(f.read())
                except ValueError:
                    os.remove('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/epg_status.json')
        else:
            return None
        
    def update(self):
        index=self['config'].getSelectionIndex()
        returnValue=self.provList[index][1]
        js = self.readJs()
        for i in range(len(self.provList)):
            if returnValue == i:
                with open('/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/times.json', 'r') as json_file:
                    data = json.load(json_file)
                provName = self.provList[i][2]
                for channel in data['bouquets']:
                    if channel["bouquet"]==provName:
                        self["glb"].setText("last update : {}".format(channel["date"]))
                if js != None:
                    if provName=="osnplay":
                        self["status"].setText('Last commit : {}'.format(js['osn']))
                    elif provName=='osnar':
                        self["status"].setText('Last commit : {}'.format(js['FullArabicXML']))
                    elif provName=='osnen':
                        self["status"].setText('Last commit : {}'.format(js['FullEnglishXML']))
                    elif provName=='jawwy':
                        self["status"].setText('Last commit : {}'.format(js['jawwy']))
                    elif provName=='dstvback':
                        self["status"].setText('Last commit : {}'.format(js['master']))
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
            cmd="python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/%s.py" % provTag
            cmdList.append(str(cmd))
            cmdList.append("python /usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/scripts/check.py")
        self.session.open(Console2,_("EPG install started") , cmdList, closeOnSuccess=False)
