#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import requests, os, json
from enigma import eTimer
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from Screens.Screen import Screen
from datetime import datetime
from .interface import EPGGrabber
from Plugins.Extensions.EPGGrabber.core.paths import API_PATH

def connected_to_internet():	
    try:
        _ = requests.get('https://github.com', timeout=5)
        return True
    except :
        return False
    
glb_session = None
glb_startDelay = None

def autostart(reason, **kwargs): 
    global glb_session
    global glb_startDelay

    if reason == 0 and "session" in kwargs:   
        glb_session = kwargs["session"]         
        glb_startDelay = StartTimer()
        glb_startDelay.start()

    elif reason == 1:         
        glb_startDelay.stop()
        glb_startDelay = None
	

class StartTimer:
    def __init__(self):
        self.timer = eTimer()
        self.today = datetime.today().strftime('%Y-%m-%d')

    def start(self):
        delay = 5
        if self.query: #not in self.timer.callback: no need 
            try:
                self.timer.callback.append(self.query)
            except:
                self.timer_conn = self.timer.timeout.connect(self.query)
            self.timer.startLongTimer(delay)
        
    def stop(self):
        if self.query: #in self.timer.callback: no need 
            try:
                self.timer.callback.remove(self.query)
            except:
                self.timer_conn = None		
			
    def query(self):
        if fileExists(API_PATH+'/epg_status.json'):
            file_date = datetime.fromtimestamp(os.stat(API_PATH+'/epg_status.json').st_mtime).strftime('%Y-%m-%d')
            if file_date != self.today :
                os.remove(API_PATH+'/epg_status.json')
                self.getStatus()
        else:
            self.getStatus()
                
    def getStatus(self):
        allData=[]
        branches = ['osn-ziko-ZR1','master-ziko-ZR1','jawwy-ziko-ZR1','FullArabicXML-Haxer','FullEnglishXML-Haxer']
        for branch in branches:
            try:
                if branch.split('-')[1]=="Haxer":
                    url = requests.get('https://api.github.com/repos/Haxer/EPG-XMLFiles/branches/'+branch.split('-')[0],timeout=5).json()
                else:
                    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/'+branch.split('-')[0],timeout=5).json()
                
                try:
                    result = url['commit']['commit']['message']+' '+url['commit']['commit']['committer']['date'].replace('T',' ').replace('Z','')
                except KeyError:
                    result = url['message'].split('. (')[0]
                     
            except:
                result = "Unable to Fetch Data Error 404"
                
            allData.append(str(branch.split('-')[0]+' '+result))
        self.toJson(allData)
        
        
    def toJson(self,data):
        dict1 = {} 
        for line in data: 
            prov, description = line.strip().split(None, 1)
            dict1[prov] = description.strip()
        out_file = open(API_PATH+"/epg_status.json", "w") 
        json.dump(dict1, out_file, indent = 4, sort_keys = False) 
        out_file.close()

def main(session, **kwargs):
    if connected_to_internet():
        session.open(EPGGrabber)
    else:
        session.open(MessageBox,_("No internet connection available. Or github.com Down"), MessageBox.TYPE_INFO,timeout=10)
  
def Plugins(**kwargs):
    Descriptors=[]
    Descriptors.append(PluginDescriptor(name="EPG Grabber",description="EPG WEB Grabber",where = PluginDescriptor.WHERE_PLUGINMENU,icon="epg.png",fnc=main))
    Descriptors.append(PluginDescriptor(name="EPG Grabber",where = PluginDescriptor.WHERE_EXTENSIONSMENU,fnc=main))
    Descriptors.append(PluginDescriptor(where = [PluginDescriptor.WHERE_AUTOSTART,PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart))
    return Descriptors
