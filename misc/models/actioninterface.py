#encoding=utf-8
import logging
import json

from models import *
from models.message import *
import conf.settings as settings

from models.message import *

LOGGER = logging.getLogger(__name__)

class Actions:
	conn = None
	queue = None
	serviceconfig = None
	def __init__(self):
		LOGGER.info('[Action Init : %s]' %  self.__class__.__name__)
		self.conn = Db().getConn()
		self.queue = MessageQueue()
		self.service = ServiceConfig().getConfig()
		
	def doAction(self, dmsg):
		pass

	def sendMessage(self, smsg):
		try:
			#pass
			print json.loads(smsg.get('data'))['text']
			self.queue.send(json.dumps(smsg.getMsg()))
		except:
			LOGGER.exception('[send message error]')

	def getConfig(self, dmsg):
		if 'config' in dmsg.getMsg():
			return dmsg.get('config')
		customer_id = dmsg.getCustomerId()
		cmd = dmsg.getCmd()
		if (customer_id in self.service) and (cmd in self.service[customer_id]):
				return self.service[customer_id][cmd]
		return  settings.service_config[cmd] if cmd in settings.service_config else settings.service_config['DEFAULT']

	def getTemplates(self, dmsg):
		return self.getConfig(dmsg)['templates']
