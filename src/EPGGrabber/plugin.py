#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import os
import json
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
    except:
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
        if glb_startDelay:
            glb_startDelay.stop()
            glb_startDelay = None

class StartTimer:
    def __init__(self):
        self.timer = eTimer()
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.query = None

    def start(self):
        delay = 5
        if self.query:
            try:
                self.timer.callback.append(self.query)
            except:
                self.timer_conn = self.timer.timeout.connect(self.query)
            self.timer.startLongTimer(delay)

    def stop(self):
        if self.query:
            try:
                self.timer.callback.remove(self.query)
            except:
                pass

    def process_data(self, allData):
        for link in allData:
            try:
                pass
            except:
                result = "Unable to Fetch Data Error 404"
        self.toJson(allData)

    def toJson(self, data):
        dict1 = {}
        for line in data:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                prov, description = parts
                dict1[prov] = description.strip()
            else:
                continue
        
        try:
            with open(API_PATH + "/epg_status.json", "w") as out_file:
                json.dump(dict1, out_file, indent=4, sort_keys=False)
        except Exception as e:
            print("EPGGrabber: Error writing json file - %s" % e)

def main(session, **kwargs):
    if connected_to_internet():
        session.open(EPGGrabber)
    else:
        session.open(MessageBox, _("No internet connection available. Or github.com Down"), MessageBox.TYPE_INFO, timeout=10)

def Plugins(**kwargs):
    Descriptors = []
    Descriptors.append(PluginDescriptor(name="EPG Grabber", description="EPG WEB Grabber", where=PluginDescriptor.WHERE_PLUGINMENU, icon="epg.png", fnc=main))
    Descriptors.append(PluginDescriptor(name="EPG Grabber", where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
    return Descriptors
