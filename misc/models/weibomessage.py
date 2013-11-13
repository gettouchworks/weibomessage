#!/usr/bin/env python
#encoding=utf-8

import json
import sys
import time
import torndb
import logging

from models import Db
from models import ServiceConfig
from models import FactoryCreator
from models.message import DeliverMessage
import conf.settings as settings

class WBMessage:

	service = {}
	fc = None
	
	def __init__(self):
		#logging.basicConfig(level = logging.INFO)

		self.LOGGER = logging.getLogger(self.__class__.__name__)
		self.LOGGER.setLevel(logging.DEBUG)
		self.LOGGER.debug('[initalize......]')	
		self.LOGGER.debug('[loading service......]')

		self.service = ServiceConfig().getConfig()
		self.baseService = settings.service_config
		self.fc = FactoryCreator()
		

	def parse(self, data=''):
		#print service
		content = None
		try:
			content = json.loads(data);
		except:
			self.LOGGER.error('message format error %s' % data, exc_info=False)
			return False
		try:
			
			action_name = ''
			cmd = 'DEFAULT'

			msgtype = content['type']
			desId = str(content['receiver_id'])

			actionList = self.service[desId] if desId in self.service else {}

			if msgtype == 'event':
				event_type = content['data']['subtype']
				cmd = event_type.upper()
			elif actionList:			
				#text = content['text']
				tcmd = content['text'].upper()
				if tcmd in actionList:
					cmd = tcmd
				else:
					cmd = sorted([ i for i in actionList.keys() if tcmd.find(i) == 0], key=len, reverse = True)[0]
					
			if cmd in actionList:
				actionInfo = actionList[cmd]
			else:
				actionInfo = self.baseService[cmd] if cmd in self.baseService else self.baseService['DEFAULT']

			print 'action info', id(actionInfo)
			action_name = actionInfo['action']
			dmsg = DeliverMessage()
			dmsg.loads(content)
			dmsg.set('cmd', cmd)
			dmsg.set('config', actionInfo)
			print dmsg.getMsg()
			action = self.fc.getInstance(action_name)()
			self.LOGGER.info(action)
			action.doAction(dmsg)
		except:
			self.error('message parse error %s' % data, exc_info=True)
	

if __name__ == '__main__':

	from models import MessageQueue
	mqueue = MessageQueue()
	#mqueue = MessageQueue()
	wbMsg = WBMessage()
	mqueue.receive( wbMsg.parse )

	# connection = pika.BlockingConnection(pika.ConnectionParameters(
	#         host='localhost'))
	# channel = connection.channel()

	# channel.queue_declare(queue='hello')

	# print ' [*] Waiting for messages. To exit press CTRL+C'

	# def callback(ch, method, properties, body):
	#     print " [x] Received %r" % (body,)
	#     wbMsg.parse(body)

	# channel.basic_consume(callback,
	#                       queue='hello',
	#                       no_ack=True)

	# try:
	# 	channel.start_consuming()
	# except:
	# 	pass

'''
	wbMsg = WBMessage()
	st = time.time();
	repeat = 1
	#print st
	for i in xrange(repeat):
		data = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"中文内容判断","data":{}}'
		wbMsg.parse(data)
		data = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"hi中文内容判断","data":{}}'
		wbMsg.parse(data)
	print repeat/(time.time()-st)
'''

