from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
#dre
from Screens.MessageBox import MessageBox

class Console(Screen):
	#TODO move this to skin.xml
	skin = """
		<screen position="100,100" backgroundColor="#380038" size="550,400" title="Command execution..." >
			<widget name="text" position="0,0" backgroundColor="#380038" size="550,400" font="Console;14" />
		</screen>"""

	def __init__(self, session, title = "Console", cmdlist = None, finishedCallback = None, closeOnSuccess = False,endstr=''):
		Screen.__init__(self, session)
                self.color = '#800080'
		self.finishedCallback = finishedCallback
		self.closeOnSuccess = closeOnSuccess
                self.endstr=endstr
		self["text"] = ScrollLabel("")
		self["actions"] = ActionMap(["WizardActions", "DirectionActions",'ColorActions'], 
		{   
			"ok": self.cancel,
			"back": self.cancel,
                        "blue": self.restartenigma,
			"up": self["text"].pageUp,
			"down": self["text"].pageDown
		}, -1)
		self.cmdlist = cmdlist
		self.newtitle = title
		self.onShown.append(self.updateTitle)
		self.container = eConsoleAppContainer()
		self.run = 0
		try:
                        self.container.appClosed.append(self.runFinished)
                        self.container.dataAvail.append(self.dataAvail)
                except:        
                        self.appClosed_conn = self.container.appClosed.connect(self.runFinished)
                        self.dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)
		self.onLayoutFinish.append(self.startRun) # dont start before gui is finished

	def updateTitle(self):
		self.setTitle(self.newtitle)

	def startRun(self):
		self["text"].setText(_("Execution Progress:") + "\n\n")
		print "Console: executing in run", self.run, " the command:", self.cmdlist[self.run]
		if self.container.execute(self.cmdlist[self.run]): #start of container application failed...
			self.runFinished(-1) # so we must call runFinished manual

	def runFinished(self, retval):
		self.run += 1
		if self.run != len(self.cmdlist):
			if self.container.execute(self.cmdlist[self.run]): #start of container application failed...
				self.runFinished(-1) # so we must call runFinished manual
		else:
			str = self["text"].getText()
			if not retval and self.endstr.startswith("Swapping"):
                           str += _("\n\n"+self.endstr)     
                           
                        else:
                           str += _("Execution finished!!\n")         
			   
			self["text"].setText(str)
			self["text"].lastPage()
			if self.finishedCallback is not None:
				self.finishedCallback(retval)
			if not retval and self.closeOnSuccess:
				self.cancel()

	def cancel(self):
		if self.run == len(self.cmdlist):
			self.close()
			try:
                                self.appClosed_conn = None
                                self.dataAvail_conn = None
                        except:
                                    self.container.appClosed.remove(self.runFinished)
                                    self.container.dataAvail.remove(self.dataAvail)

	def dataAvail(self, str):
		self["text"].setText(self["text"].getText() + str)
		return
		if self["text"].getText().endswith("Do you want to continue? [Y/n] "):
			msg = self.session.openWithCallback(self.processAnswer, MessageBox, _("Additional packages must be installed. Do you want to continue?"), MessageBox.TYPE_YESNO)
			
	def processAnswer(self, retval):
		if retval:
			self.container.write("Y",1)
		else:
			self.container.write("n",1)
		self.dataSent_conn = self.container.dataSent.connect(self.processInput)

	def processInput(self, retval):
		self.container.sendEOF()
        def restartenigma(self):
                    from Screens.Standby import TryQuitMainloop
                    self.session.open(TryQuitMainloop, 3)
