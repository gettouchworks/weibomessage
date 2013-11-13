#!/usr/bin/env python
#encoding=utf-8

import json
import sys
import time
import torndb
import logging
from models import MessageQueue
from models import WBMessage

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

	if not "./actions/" in sys.path:
		sys.path.append("./actions/")

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

