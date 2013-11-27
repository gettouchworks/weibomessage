#encoding=utf-8

import time
import email.utils
import datetime
import json
import logging

from models import Actions
from models import *


LOGGER = logging.getLogger(__name__)

class FollowAction(Actions):

	def __init__(self):
		Actions.__init__(self);
	
	def doAction(self):
		data = self.dmsg.getMsg()
		reply_content = self.getTemplates()
		smsg = TextMessage(self.dmsg.getMsgId())
		smsg.setContent(reply_content)
		#print 'smsg', smsg.getMsg()
		self.sendMessage(smsg)

if __name__ == '__main__':

	data = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"中文内容判断","data":{}}'
	dj = json.loads(data)
	print dj
	# da = DefaultAction()
	# da.doAction("default")
