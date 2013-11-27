#!/usr/bin/env python
#encoding=utf-8

import json
import sys
import time
import torndb
import logging
import traceback

from models import Db
from models import ServiceConfig
from models import FactoryCreator
from models.message import DeliverMessage
import conf.settings as settings

LOGGER = logging.getLogger(__name__)

class WBMessage:

	service = {}
	fc = None
	
	def __init__(self):
		#logging.basicConfig(level = logging.INFO)

		LOGGER.info('[initalize......]')	
		LOGGER.info('[loading service......]')

		self.service = ServiceConfig().getConfig()
		self.baseService = settings.service_config
		self.fc = FactoryCreator()
		

	def parse(self, data=''):
		#print service
		content = None
		try:
			content = json.loads(data);
			LOGGER.info('[Message Deliverd : type = %s content = %s]' % (content['type'], content['text']))
		except:
			LOGGER.error('message format error %s' % data, exc_info=False)
			return False

		try:
			
			action_name = ''
			cmd = content['text'].upper()

			msgtype = content['type']
			desId = str(content['receiver_id'])

			actionList = self.service[desId] if desId in self.service else {}

			if msgtype == 'event':
				event_type = content['data']['subtype']
				cmd = event_type.upper()
			elif actionList:			
				#text = content['text']
				if cmd not in actionList:
					cmds = sorted([ i for i in actionList.keys() if cmd.find(i) == 0], key=len, reverse = True)
					if cmds:
						cmd = cmds[0]
					
			if cmd in actionList:						# in user defined service list
				actionInfo = actionList[cmd]
				LOGGER.info('[in user defined service list]')
			elif cmd in self.baseService:				# in base service list
				actionInfo = self.baseService[cmd]
				LOGGER.info('[in base service list]')
			elif 'DEFAULT' in actionList:				# in user defined default service
				actionInfo =  actionList['DEFAULT']
				#cmd = 'DEFAULT'
				LOGGER.info('[in user defined default service]')
			else:										# in base default service
				actionInfo =  self.baseService['DEFAULT']
				#cmd = 'DEFAULT'
				LOGGER.info('[in base default service]')

			#print 'action info', cmd, actionInfo
			LOGGER.info('[CMD :: %s]' % cmd)
			action_name = actionInfo['action']
			dmsg = DeliverMessage()
			dmsg.loads(content)
			dmsg.set('cmd', cmd)
			dmsg.set('config', actionInfo)

			action = self.fc.getInstance(action_name)(dmsg)
			action.doAction()
			
		except :
		 	LOGGER.error('message parse error %s' % data, exc_info=True)
		 	traceback.format_exc()
	

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

