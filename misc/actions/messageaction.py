## -*- coding: utf-8 -*-

import time
import json
import logging
import sys
import email.utils
import datetime

from models import Actions
from models.message import *

LOGGER = logging.getLogger(__name__)

class MessageAction(Actions):

	def __init__(self):
		Actions.__init__(self);

	def doAction(self, dmsg):
		data = dmsg.getMsg()
		stime = data['created_at']
		#Sat Nov 02 15:47:02 +0800 2013
		created_at = int(time.mktime(email.utils.parsedate(stime)))

		sql = "insert into wb_message \
			(receiver_id, sender_id, type, content, data, ori_content, created_at)	\
			values	(%d, %d, '%s', '%s', '%s', '%s', %d)" % \
			(data['receiver_id'], data['sender_id'], data['type'], data['text'], json.dumps(data["data"]), json.dumps(data), created_at)
		#print sql
		#print self.conn.execute(sql)
		customer_id = dmsg.getCustomerId()
		cmd = dmsg.getCmd()
		smsg = TextMessage(dmsg.getMsgId())
		print cmd, self.getConfig(customer_id, cmd)



if __name__ == '__main__':
	da = DefaultAction()
	da.doAction("default")