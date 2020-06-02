# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap
from ServiceReference import ServiceReference
from Components.Button import Button
from enigma import eEnv
from Tools.Directories import fileExists
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
import os
from scripts import ch
from xml.etree import ElementTree as ET
from xml.dom import minidom

LAMEDB = eEnv.resolve('${sysconfdir}/enigma2/lamedb')
cos_path='/etc/epgimport/custom.channels.xml'
elci_path='/etc/epgimport/elcinema.channels.xml'
dstv_path='/etc/epgimport/dstv.channels.xml'
elif_path='/etc/epgimport/eliftv.channels.xml'
jaw_path='/etc/epgimport/jawwy.channels.xml'
bqList=['chann-bein sports-'+cos_path+'','osn-osn-'+cos_path+'','elc_channels-elcinema-'+elci_path+'','net-bein entertainment-'+cos_path+'','mbc-mbc-'+cos_path+'','ent-elcinema bein entertainment-'+elci_path+'','ZA-DSTV-'+dstv_path+'','others-others-'+cos_path+'',
        'eli-eLife TV-'+elif_path+'','Jaw-Jawwy TV-'+jaw_path+'']
class set_ref(Screen):
    skin="""
        <screen position="center,center" size="1000,400" title="GET SERVICE" backgroundColor="#16000000" flags="wfNoBorder">
            <widget name="bouq" position="200,10" size="990,50" font="Regular;40" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1"/>
            <widget name="status" foregroundColor="#00ffffff" backgroundColor="#16000000"  position="10,130" size="700,25" font="Regular;23"/>             
            <widget name="label" foregroundColor="#00ffffff" backgroundColor="#16000000"  position="10,100" size="700,25" font="Regular;23" />
            <widget name="list" foregroundColor="#00ffffff" backgroundColor="#16000000" zPosition="2" position="650,80" size="320,300" scrollbarMode="showOnDemand" transparent="1" />
            <widget name="id" foregroundColor="#008000" backgroundColor="#16000000"  position="30,200" size="700,25" font="Regular;22" />
            <ePixmap name="red" position="17,300" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/redfhd.png" transparent="1" alphatest="on"/>
            <widget name="key_red" position="17,300" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
            <ePixmap name="green" position="335,300" zPosition="2" size="260,49" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Epg_Plugin/icons/greenfhd.png" transparent="1" alphatest="on"/>
            <widget name="key_green" position="335,300" size="260,49" valign="center" halign="center" zPosition="4" foregroundColor="#00ffffff" backgroundColor="#16000000" font="Regular;32" transparent="1"/>
        </screen>"""
        
    def __init__(self, session, services, curservice=None, bouquetname=None):
        self.session = session
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
            "back": self.a,
            "up":self.listUP,
            "last": self.last,
            "next": self.next,
            "down":self.listDOWN,
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
        self.getCurrentService()
        self.bqIndex=0        
        self.changeBQ()
        self["bouq"].setText("Current bouquet  : {}".format(self.bouquetname))
        
    def setCurrentidIndex(self):
        if self.idxList.count((self.id)):
            self.idx = self.idxList.index((self.id))
   
#####################################################

    def last(self):
        self.bqIndex-=1
        self.changeBQ()
        
    def next(self):
        self.bqIndex+=1
        self.changeBQ()
        
    def changeBQ(self):
        if self.bqIndex>(len(bqList)-1):
           self.bqIndex=0
        if self.bqIndex<0:
           self.bqIndex =len(bqList)-1
           
        bqTitle=bqList[self.bqIndex ].split('-')[1]
        self["label"].setText('EPG PROVIDER : {}'.format(bqTitle))
        self.listChannels()
        
    def listChannels(self):
        self.path=bqList[self.bqIndex].split('-')[2]
        bqTitle=bqList[self.bqIndex].split('-')[0]
        channels=ch.chann
        exec "channels=ch."+bqTitle.split('-')[0]
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
            self.remove_duplicates()
            self['id'].setText("{} added successfully to config".format(self.name))
        else:
            self.session.open(MessageBox,_(self.path+" not found in path"), MessageBox.TYPE_INFO,timeout=10)
    
    def remove_duplicates(self):
        with open(self.path, "rb") as fp:
            lines = fp.readlines()
            new_lines = []
            for line in lines:
                line = line.strip()
                if line not in new_lines:
                    new_lines.append(line)
                f = open(self.path, 'w')
                f.write('\n'.join(new_lines))
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
        self["status"].setText("Current channel : {}".format(self.name))
        #self["srf"].setText(self.refstr)

    def setCurrentServiceIndex(self):
		if self.ServicesList.count((self.name,self.refstr)):
			self.sidx = self.ServicesList.index((self.name,self.refstr))
    
    def right(self):
        self.changeService(1)

    def left(self):
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
