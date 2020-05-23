# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap
from ServiceReference import ServiceReference
from enigma import eEnv
from Components.MenuList import MenuList
import os
from scripts import ch
from xml.etree import ElementTree as ET
from xml.dom import minidom

LAMEDB = eEnv.resolve('${sysconfdir}/enigma2/lamedb')

class set_ref(Screen):
    skin="""
        <screen position="center,center" size="760,190" title="SET SERVICE" backgroundColor="#16000000" flags="wfNoBorder">
            <widget name="status" backgroundColor="#16000000" position="300,60" size="911,90" font="Regular;30"/>
            <widget name="srf" backgroundColor="#16000000" position="100,60" size="200,35" font="Regular;30" />
            <widget name="id" backgroundColor="#16000000"  position="250,100" size="911,40" font="Regular;30" />
            <widget name="label" backgroundColor="#16000000"  position="100,100" size="911,40" font="Regular;30" />
            <widget name="bouq" foregroundColor="#00ffa500" backgroundColor="#16000000"  position="100,10" size="911,40" font="Regular;35" />
        </screen>"""
        
    def __init__(self, session, services, curservice=None, bouquetname=None):
        self.session = session
        self["srf"] = Label()
        self["status"] = Label()
        self["id"] = Label()
        self["label"] = Label()
        self["bouq"] = Label()
        self.services = services
        self.curservice = curservice
        self.bouquetname = bouquetname
        Screen.__init__(self, session)
        self["myActionMap"] = ActionMap(["EpgColorActions","EpgWizardActions"],
        {   
            "back": self.a,
            "up":self.prevService,
            "down":self.nextService,
            "ok":self.ok,
            "right":self.right,
            "left":self.left
        }, -1)
        
        self.ServicesList = []
        self.idxList=[]
        self.sidx = 0
        self.name = None
        self.refstr = None
        self.id = None
        self.path=None
        self.idx = 0
        self.init()
        self.get_idx()
        self.getCurrentid()
        self.getCurrentService()
        self["label"].setText("Bein :")
        self["srf"].setText("Channels :")
        self["bouq"].setText("Current bouquet  : {}".format(self.bouquetname))
    
    def get_idx(self):
        for chan in ch.chann:
            self.idxList.append(chan)
        for c in ch.elc_channels:
            self.idxList.append(c)
        for m in ch.mbc:
            self.idxList.append(m)
        for o in ch.osn:
            self.idxList.append(o)
        for n in ch.net:
            self.idxList.append(n)
        for e in ch.ent:
            self.idxList.append(e)
        for other in ch.ent:
            self.idxList.append(other)
        for d in ch.ZA:
            self.idxList.append(d)
        self.lenidList = len(self.idxList)
        
        
    def getCurrentid(self):
        self.id = self.idxList[0]
        self.setCurrentidIndex()
        self.displayidParams()
        
    def setCurrentidIndex(self):
		if self.idxList.count((self.id)):
			self.idx = self.idxList.index((self.id))
   
    def displayidParams(self):
        self["id"].setText(self.id)


    def left(self):
        self.changeid(-1)
        
    def right(self):
        self.changeid(1)
    
    def changeid(self, num):
        if self.lenidList:
            self.idx += num
            self.idx %= self.lenidList
            self.id = self.idxList[self.idx]
            self.displayidParams()
        if self.id in ch.chann:
            self["label"].setText("Bein Sports :")
            self.path="/etc/epgimport/custom.channels.xml"
        elif self.id in ch.elc_channels:
            self["label"].setText("elcinema :")
            self.path="/etc/epgimport/elcinema.channels.xml"
        elif self.id in ch.mbc:
            self["label"].setText("MBC :")
            self.path="/etc/epgimport/custom.channels.xml"
        elif self.id in ch.osn:    
            self["label"].setText("osn :")
            self.path="/etc/epgimport/custom.channels.xml"
        elif self.id in ch.net:
            self["label"].setText("bein entertainment :")
            self.path="/etc/epgimport/custom.channels.xml"
        elif self.id in ch.ent:
            self["label"].setText("elcinema bein entertainment :")
            self.path="/etc/epgimport/elcinema.channels.xml"
        elif self.id in ch.others:
            self["label"].setText("Others :")
            self.path="/etc/epgimport/custom.channels.xml"
        elif self.id in ch.ZA:
            self["label"].setText("DSTV :")
            self.path="/etc/epgimport/dstv.channels.xml"
        else:
            self["label"].setText("")
        
    def init(self):
        for service in self.services:
            self.ServicesList.append((service.getServiceName(), str(service)))
        self.lenServicesList = len(self.ServicesList)
        if not self.bouquetname:
            self.ServicesList.sort()
      

    def ok(self):
        doc = ET.parse(self.path)
        root = doc.getroot()
        root.append((ET.fromstring('<channel id="{}">{}</channel>'.format(self.id,self.refstr))))
        out = ET.tostring(root)
        dom = minidom.parseString(out)
        f = open(self.path, 'w')
        dom_string = dom.toprettyxml(encoding='UTF-8')
        dom_string = os.linesep.join([s for s in dom_string.splitlines() if s.strip()])
        f.write(dom_string)
        f.close()
    
    def getCurrentService(self):
        from ServiceReference import ServiceReference
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
        self["status"].setText(self.name)

    def setCurrentServiceIndex(self):
		if self.ServicesList.count((self.name,self.refstr)):
			self.sidx = self.ServicesList.index((self.name,self.refstr))
    
       
    def nextService(self):
        self.changeService(1)

    def prevService(self):
        self.changeService(-1)

    def changeService(self, num):
        if self.lenServicesList:
            self.sidx += num
            self.sidx %= self.lenServicesList
            self.name = self.ServicesList[self.sidx][0]
            self.refstr = self.ServicesList[self.sidx][1]
            self.displayServiceParams()
            

    def a(self):
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



from enigma import eServiceCenter, eServiceReference
from ServiceReference import ServiceReference

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