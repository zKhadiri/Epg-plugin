#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from Plugins.Extensions.EPGGrabber.core.compat import PY3, compat_URLError
from Plugins.Extensions.EPGGrabber.core.paths import BOUQUETS_ROOT

from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap
from ServiceReference import ServiceReference
from Components.Button import Button
from enigma import eEnv, getDesktop, gRGB, eServiceCenter, eServiceReference
from Tools.Directories import fileExists
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
from xml.etree import ElementTree as ET
from xml.dom import minidom
from Components.config import config
import os
import json

LAMEDB = eEnv.resolve('${sysconfdir}/enigma2/lamedb')

### import class + screens from files inside plugin
from .skin import *

def parseColor(s):
        return gRGB(int(s[1:], 0x10))

def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())

def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280

class AssignRef(Screen):

    def __init__(self, session, services, curservice=None, bouquetname=None):
        self.session = session
        if config.plugins.EpgPlugin.skin.value == 'smallscreen':
                if isHD():
                        self.skin = SKIN_set_ref_Small_HD
                else:
                        self.skin = SKIN_set_ref_Small_FHD
        else:
                if isHD():
                        self.skin = SKIN_set_ref_Full_HD
                else:
                        self.skin = SKIN_set_ref_Full_FHD
        self["status"] = Label()
        self["id"] = Label()
        self["label"] = Label()
        self["bouq"] = Label()
        self['list']=MenuList([])
        self["key_red"] = Button(_("last provider"))
        self["key_green"] = Button(_("next provider"))
        self.services = services
        self.curservice = curservice
        self.bouquetname = bouquetname
        Screen.__init__(self, session)
        self["myActionMap"] = ActionMap(["EpgColorActions","EpgWizardActions",'PiPSetupActions','SrefColorActions'],
        {   
            "back": self.exit,
            "up":self.listUP,
            "last": self.last,
            "next": self.next,
            "down":self.listDOWN,
            "ok":self.ok,
            "right":self.right,
            "left":self.left
        }, -1)
        self.exist= False
        self.ServicesList = []
        self.idxList=[]
        self.bqList=[]
        self.sidx = 0
        self.name = None
        self.refstr = None
        self.id = None
        self.path=None
        self.idx = 0
        self.init() 
        self.getCurrentService()
        self.bqIndex=0
        self.getJson()       
        self["bouq"].setText("Current bouquet  : {}".format(self.bouquetname))
     
#####################################################

    def getJson(self):
        try:
                with open(BOUQUETS_ROOT,'r')as f:
                        self.data=json.load(f)
                        for bouquet in self.data['bouquets']:
                                self.bqList.append(bouquet['name'])
                self.changeBQ()
        except compat_URLError as e:
                        print('File json not found.')
    
    def last(self):
        self.bqIndex-=1
        self.changeBQ()
        self['id'].setText("")
        
    def next(self):
        self.bqIndex+=1
        self.changeBQ()
        self['id'].setText("")
        
    def changeBQ(self):
        if self.bqIndex>(len(self.bqList)-1):
           self.bqIndex=0
        if self.bqIndex<0:
           self.bqIndex =len(self.bqList)-1
           
        bqTitle=self.bqList[self.bqIndex]
        self["label"].setText('EPG Provider : {}'.format(bqTitle))
        self.listChannels()
     
      
    def listChannels(self):
        for data in self.data['bouquets']:
            if data['name']==self.bqList[self.bqIndex]:
                if PY3:
                        channels = [s for s in data['channels']]
                else:
                        channels = [s.encode('ascii', 'ignore') for s in data['channels']]
                self.path = data['path']
                self['list'].setList([])    
                self['list'].setList(channels)
                self['list'].show()
                self.idxList=channels
                self.lenidList=len(self.idxList)
                self.updateServiceID()
                        
    def listDOWN(self):
        self['list'].down()
        self.updateServiceID()
        self['id'].setText("")
        return

    def listUP(self):
        self['list'].up()
        self.updateServiceID()
        self['id'].setText("")
        
    def updateServiceID(self):
        index=self['list'].getSelectionIndex()
        service=self.idxList[index]
        #self['id'].setText(service)
        self.id = service
        return
#########################################        
    
    def init(self):
        for service in self.services:
            self.ServicesList.append((service.getServiceName(), str(service)))
        self.lenServicesList = len(self.ServicesList)
        if not self.bouquetname:
            self.ServicesList.sort()
    
    def ok(self):
        if fileExists(self.path):
            self.exist = False
            
            if len(self.refstr)>60:
                new_id = '<channel id="{}">{}</channel>'.format(self.id,self.refstr.split('/')[0]+'//example.m3u8')
            else:
                new_id = '<channel id="{}">{}</channel>'.format(self.id,self.refstr)
            
            f = open(self.path, 'r')
            data = f.read()
            f.close()
            
            for line in data.split('\n'):
                if new_id == line.strip():
                    self['id'].setText("{} already exist in config".format(self.name))
                    self['id'].instance.setForegroundColor(parseColor("#00ff2525"))
                    self.exist = True
                  
            if not self.exist:
                doc = ET.parse(self.path)
                root = doc.getroot()
                root.append((ET.fromstring(new_id)))
                out = ET.tostring(root)
                dom = minidom.parseString(out)
                f = open(self.path, 'w')
                if PY3:
                        dom_string = dom.toprettyxml()
                else:
                        dom_string = dom.toprettyxml(encoding='UTF-8')
                dom_string = os.linesep.join([s for s in dom_string.splitlines() if s.strip()])
                f.write(dom_string)
                f.close()
                self['id'].setText("{} added successfully to config".format(self.name))
                self['id'].instance.setForegroundColor(parseColor("#008000"))
        else:
            self.session.open(MessageBox,_(str(self.path)+" not found in path"), MessageBox.TYPE_INFO,timeout=10)


    def getCurrentService(self):
        if self.curservice is not None:
            service = self.curservice
        else:
            service = self.session.nav.getCurrentlyPlayingServiceReference()
        if service:
            service = self.session.nav.getCurrentlyPlayingServiceReference()
            self.name = ServiceReference(service).getServiceName()
            self.refstr = ':'.join(service.toString().split(':')[:11])
            self.setCurrentServiceIndex()
            self.displayServiceParams()
            
    
    def displayServiceParams(self):
        self["status"].setText("Current channel : {}".format(self.name))
        #self["srf"].setText(self.refstr)

    def setCurrentServiceIndex(self):
        if self.ServicesList.count((self.name,self.refstr)):
                self.sidx = self.ServicesList.index((self.name,self.refstr))
    
    def right(self):
        self.changeService(1)
        self['id'].setText("")

    def left(self):
        self.changeService(-1)
        self['id'].setText("")

        
    def changeService(self, num):
         if self.lenServicesList:
            self.sidx += num
            self.sidx %= self.lenServicesList
            self.name = self.ServicesList[self.sidx][0]
            self.refstr = self.ServicesList[self.sidx][1]
            self.displayServiceParams()
           
    def exit(self):
        self.close(None)
    

def freeMemory():
        os.system("sync")
        os.system("echo 3 > /proc/sys/vm/drop_caches")

def cleanup():
        global Session
        Session = None
        global Servicelist
        Servicelist = None
        global epg_bouquet
        epg_bouquet = None
        freeMemory()

def closed(ret=False):
        cleanup()

def getBouquetServices(bouquet):
        services = []
        Servicelist = eServiceCenter.getInstance().list(bouquet)
        if Servicelist:
                while True:
                        service = Servicelist.getNext()
                        if not service.valid():
                                break
                        if service.flags & (eServiceReference.isDirectory | eServiceReference.isMarker): 
                                continue
                        services.append(ServiceReference(service))
        return services
