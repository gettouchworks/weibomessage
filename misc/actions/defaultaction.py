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

	def __init__(self):
		Actions.__init__(self);
	
	def doAction(self, dmsg):
		data = dmsg.getMsg()
		# stime = data['created_at']
		# #Sat Nov 02 15:47:02 +0800 2013
		# created_at = int(time.mktime(email.utils.parsedate(stime)))
		# sql = "insert into wb_message \
		# 	(receiver_id, sender_id, type, content, data, ori_content, created_at)	\
		# 	values	(%d, %d, '%s', '%s', '%s', '%s', %d)" % \
		# 	(data['receiver_id'], data['sender_id'], data['type'], data['text'], json.dumps(data["data"]), json.dumps(data), created_at)

		#print self.conn.execute(sql)

		smsg = TextMessage(dmsg.getMsgId())
		reply_content = self.getTemplates(dmsg)
		smsg.setContent(reply_content)
		self.sendMessage(smsg)

if __name__ == '__main__':

	data = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"中文内容判断","data":{}}'
	dj = json.loads(data)
	print dj
	# da = DefaultAction()
	# da.doAction("default")
