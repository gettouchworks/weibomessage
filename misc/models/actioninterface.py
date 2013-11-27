#encoding=utf-8
import logging
import json

from models import *
from models.message import *
import conf.settings as settings

from models.message import *

LOGGER = logging.getLogger(__name__)

class Actions(object):
	conn = None
	queue = None
	serviceconfig = None
	def __init__(self, dmsg=None, auto_send=True):
		LOGGER.info('[Action Init : %s]' %  self.__class__.__name__)
		self.conn = Db().getConn()
		self.queue = MessageQueue()
		self.service = ServiceConfig().getConfig()
		self.dmsg = dmsg
		self.auto_send = auto_send
		
	def doAction(self, dmsg=None):
		pass

	def setDelivered(self, dmsg):
		self.dmsg = dmsg;

	def getDelivered(self):
		return self.dmsg

	def sendMessage(self, smsg):
		if not self.auto_send:
			return
		try:
			if not smsg.getMsgId():
				smsg.setMsgId(self.getMsgId())
			LOGGER.info('sendmsg content: %s' % json.loads(smsg.get('data'))['text'])
			#self.queue.send(json.dumps(smsg.getMsg()))
		except:
			LOGGER.exception('[send message error]')

	def getMsgId(self):
		return self.dmsg.getMsgId()

	def getConfig(self, Cmd=None):
		if Cmd == None and 'config' in self.dmsg.getMsg():
			return self.dmsg.get('config')
		customer_id = self.dmsg.getCustomerId()
		cmd = Cmd if Cmd != None else self.dmsg.getCmd()
		if (customer_id in self.service) and (cmd in self.service[customer_id]):
				return self.service[customer_id][cmd]
		return  settings.service_config[cmd] if cmd in settings.service_config else settings.service_config['DEFAULT']

	def getTemplates(self, Cmd=None):
		return self.getConfig(Cmd)['templates']

	def setState(self, action=None, cmd=None, data=None):
		""" set user current state to memcached and return it
		key format: USER::{receiver_id}::{sender_id}

		Args:
		    action: class of process if None set current action。
		    cmd: command of parse if None set cmd in dmsg.

		Returns:
			a dict, include current process info

		Raises:
		    None
		"""
		mc = Mc().getConn()
		customer_id = self.dmsg.getCustomerId()
		uid = self.dmsg.get('sender_id')

		key = 'USER::{0}::{1}'.format(customer_id, uid)
		state = {
			'action': self.__class__.__name__ if not action else action,
			'cmd': self.dmsg.getCmd() if not cmd else cmd,
			'data': data if data else {}
		}
		mc.set(key, state)
		return state
		#print state

	def getState(self):
		""" get user state from memcached
		if not existed do setState func
		"""
		mc = Mc().getConn()
		customer_id = self.dmsg.getCustomerId()
		uid = self.dmsg.get('sender_id')
		key = 'USER::{0}::{1}'.format(customer_id, uid)
		state = mc.get(key)
		# if not state:
		# 	state = self.setState()
		return state

