# -*- coding: utf-8 -*-

import urllib
import json
import logging

LOGGER = logging.getLogger(__name__)

class Message :

	def __init__(self):
		LOGGER.info('[%s init]' % self.__class__.__name__)
		self.__msg = {}

	def getMsg(self):
		return self.__msg

	def setMsg(self, msg):
		self.__msg = msg

	def loads(self, data):
		if type(data) is dict:
			for i in data.keys() :
				self.__msg[i] = data[i]
				#self.set(i, data[i])
			return True
		else:
			return False
	def dumps(self):
		try:
			return json.dumps(self.__msg)
		except:
			return ''

	def set(self, name, value):
		self.__msg[name] = value

	def get(self, name):
		return self.__msg[name]

	def __del__(self):  
		LOGGER.info('%s deleted' % self.__class__.__name__ )


class DeliverMessage(Message):
	#__msg = {}
	def __init__(self):
		Message.__init__(self)
		#self.__msg = Message.getMsg(self)

	def getMsgId(self):
		return self.get('id')

	def getCustomerId(self):
		return str(self.get('receiver_id'))

	def getCmd(self):
		return self.get('cmd')


class SendMessage(Message):

	def __init__(self, msgId=''):
		Message.__init__(self)
		#self.__msg = Message.getMsg(self)
		self.setMsgId(msgId)

	def setMsgId(self, msgId):
		self.set('id', msgId)

	def getMsgId(self):
		return self.get('id')

	def setType(self, msgtype):
		self.set('type', msgtype)

	def setData(self, data):
		#print data
		#print type(json.dumps(data))
		#dj = json.dumps(data, ensure_ascii=False)
		#print dj
		#self.__msg['data'] = urllib.quote(dj)
		self.set('data', json.dumps(data))

	def typeToText(self):
		self.setType('text')

	def typeToArticles(self):
		self.setType('articles')

	def typeToPosition(self):
		self.setType('position')


class TextMessage(SendMessage):
	def __init__(self, msgId=''):
		SendMessage.__init__(self, msgId)
		SendMessage.typeToText(self)

	def setContent(self, content):
		data = {}
		data['text'] = content
		self.setData(data)




if __name__ == '__main__':
	
	msg = TextMessage('123')
	msg.setContent("纯文本回复")
	print msg.dumps()
	# dd = {}
	# cc = "纯文本回复"
	# dd["text"] = cc
	# print dd
	# js = json.dumps(dd, ensure_ascii=False)
	# print urllib.quote(js)

	# msg = DeliverMessage()
	# ss = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"hi","data":{}}'
	# data = json.loads(ss)
	# #print data
	# msg.loads(data)
	# print msg.getMsg()