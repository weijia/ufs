import response
import localLiboSys
from localLibs.logSys.logSys import *
import libs.user.sessionV2 as sess
import uuid
import time
import os
import Cookie

class html(response.html):
	def __init__(self):
		response.html.__init__(self)
		self.pa = {}
	def initSession(self, sessionList):
        timeoutSeconds = 60*60*24*15#15 days?
        self.thiscookie = Cookie.SimpleCookie()
        #cl('init session')
        if os.environ.has_key('HTTP_COOKIE'):
			self.thiscookie.load(os.environ['HTTP_COOKIE'])
			#cl('cookie:',thiscookie['aparam'].value)
			#print thiscookie['aparam']
			self.sessionid = self.thiscookie['aparam'].value
			#Check if the sessionID expired
			if sess.session(self.sessionid).expired():
				self.thiscookie = Cookie.SimpleCookie()
        self.sessionid = str(uuid.uuid4())
        #cl('session is:',self.sessionid)
        self.thiscookie['aparam'] = self.sessionid
        self.thiscookie['aparam']['max-age'] = timeoutSeconds
        #print thiscookie['aparam']
        #The following print is necessary. It will send cookie to client.
        #print self.thiscookie
