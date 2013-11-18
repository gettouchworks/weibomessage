#encoding=utf-8

import time
import email.utils
import datetime
import json
import logging

from models import Actions
from models import *

import memcache

LOGGER = logging.getLogger(__name__)

class MenuAction(Actions):

	def __init__(self):
		Actions.__init__(self);
	
	def doAction(self, dmsg):
		data = dmsg.getMsg()
		
		content = dmsg.getText()

		if not content.isnumeric():
			defaultaction = __import__('defaultaction')
			action = defaultaction.DefaultAction()
			action.doAction(dmsg)
			return

		menu_index = int(content)
		reply_content = self.processMenu(menu_index, dmsg.getCustomerId(), dmsg.get('sender_id'))
		#print 'reply content ', reply_content

		smsg = TextMessage(dmsg.getMsgId())
		if reply_content == False: 
			reply_content = self.getTemplates(dmsg)

		smsg.setContent(reply_content)
		self.sendMessage(smsg)


	def processMenu(self, menu_index, customer_id, uid):

		key = 'MENU::%s::%s' % (customer_id, uid)
		mc = memcache.Client(['127.0.0.1:11211'],debug=0)
		# mc.set("foo","bar")
		minfo = mc.get(key)

		if not minfo:
			minfo = {
				'parent_id':0,
				'last_menu':menu_index
			}
			mc.set(key, minfo)

		conn = Db().getConn()
		sql = "select * from wb_menus where parent_id=%d and menu_index='%s'" % (minfo['parent_id'], str(menu_index))
		result = conn.query(sql)
		if not result:
			self.resetMenu(customer_id, uid)
			return False

		sql = 'select id from wb_menus where parent_id=%d' % result[0].id
		print sql
		minfo['parent_id'] = result[0].id if conn.query(sql) else result[0].parent_id
		minfo['last_menu'] = str(menu_index)
		print minfo
		mc.set(key, minfo)

		return result[0].content

	def resetMenu(self, customer_id, uid):
		mc = memcache.Client(['127.0.0.1:11211'],debug=0)
		key = 'MENU::%s::%s' % (customer_id, uid)
		minfo = {
			'parent_id':0,
			'last_menu':0
		}
		mc.set(key, minfo)

if __name__ == '__main__':

	data = '{"id":1311020000761817,"type":"text","receiver_id":2126852741,"sender_id":1149076110,"created_at":"Sat Nov 02 15:47:02 +0800 2013","text":"中文内容判断","data":{}}'
	dj = json.loads(data)
	print dj
	# da = DefaultAction()
	# da.doAction("default")
