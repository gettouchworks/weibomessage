#encoding=utf-8

import time
import email.utils
import datetime
import json
import logging

from models import Actions
from models import *


LOGGER = logging.getLogger(__name__)

class DefaultAction(Actions):
	
	def doAction(self):

		# dmsg = self.dmsg
		# data = dmsg.getMsg()
		ustate = self.getState()

		if ustate and ustate['action'] != self.__class__.__name__:
			actionModule = __import__(ustate['action'].lower())
			action = getattr(actionModule, ustate['action'])(self.dmsg)
			action.doAction()
			return

		smsg = TextMessage()
		reply_content = self.getTemplates()
		smsg.setContent(reply_content)
		self.sendMessage(smsg)
		return reply_content

if __name__ == '__main__':

	data = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"中文内容判断","data":{}}'
	dj = json.loads(data)
	print dj
	# da = DefaultAction()
	# da.doAction("default")
