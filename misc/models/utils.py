# -*- coding: utf-8 -*-

import logging
import threading, time, random

import torndb
import pika
import memcache

import conf.settings as settings

logging.getLogger('pika').setLevel(logging.INFO)
LOGGER = logging.getLogger(__name__)

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

			
@singleton
class ServiceConfig:
	def __init__(self):
		self.service = {}
		#db = Db().getConn()
		#self.reloadConfig()
		self.loadConfig()
		# self.lock = threading.Lock()
		# srthread = threading.Thread(target=self.serviceReload)
 	# 	srthread.start() 

	def getConfig(self):
		return self.service

	def loadConfig(self):
		db = Db().getConn()
		#db.execute("set names latin1")
		for wb_service in db.query("SELECT * FROM wb_service"):
			#print type(wb_service)
			print wb_service.customer_id, wb_service.service_name, wb_service.cmd, wb_service.action
			customer_id = str(wb_service.customer_id)
			cmd = wb_service.cmd.upper()
			if customer_id not in self.service:
				self.service[customer_id] = {}
			self.service[customer_id][cmd] = {'id':wb_service.id, 
											'cmd': cmd,
											'service_id':wb_service.service_id,
											'servicename':wb_service.service_name, 
											'action' : wb_service.action, 
											'templates':wb_service.templates}
		print self.service
		print '[Service loaded]', sum([len(value) for key, value in self.service.iteritems()])

	def serviceReload(self):

		while True:
			self.lock.acquire()  
			print 'reload config....'
			ServiceConfig().loadConfig()
			self.lock.release()
			#break
			time.sleep(3600)


@singleton
class Db():
	#conn = None
	def __init__(self):
		dbconfig = settings.database
		#print dbconfig
		self.conn = torndb.Connection(dbconfig['host'], dbconfig['dbname'], user=dbconfig['user'], password=dbconfig['passwd'])
		self.conn.execute("set names %s" % dbconfig['charset'])
		LOGGER.info('[init db] : %s' % self.conn)

	def getConn(self):
		#self.conn = torndb.Connection("localhost", "weibo_message", "root")
		LOGGER.debug(self.conn)
		return self.conn

@singleton
class Mc():
	def __init__(self):
		self.mc = memcache.Client(['127.0.0.1:11211'],debug=1)
		LOGGER.debug('memcached client init')

	def getConn(self):
		LOGGER.debug(self.mc)
		return self.mc

@singleton
class MessageQueue:
	
	qconn = None

	qsconn = None
	qrconn = None
	receive_channel = None
	send_channel = None

	# __RECEIVE_EX_NAME = 'ex_receive'
	# __RECEIVE_Q_NAME = 'qreceive'
	# __SEND_EX_NAME = 'ex_reply'
	# __SEND_Q_NAME = 'qreply'

	def __init__(self):
		qconfig = settings.queue_config
		self.__RECEIVE_EX_NAME = qconfig['receive']['ex_name']
		self.__RECEIVE_Q_NAME = qconfig['receive']['queue_name']
		self.__SEND_EX_NAME = qconfig['reply']['ex_name']
		self.__SEND_Q_NAME = qconfig['reply']['queue_name']

		self.__initQueue()

		# self.__initReceiveQueue()
		# self.__initSendQeueue()
		

	def __initQueue(self):
		self.qconn = pika.BlockingConnection(pika.ConnectionParameters(
			host='localhost'))
		self.channel = self.qconn.channel()
		# self.receive_channel = channel
		# self.send_channel = channel

		#init & bind receive queue
		self.channel.exchange_declare(exchange=self.__RECEIVE_EX_NAME, type='fanout')
		self.channel.queue_declare(queue = self.__RECEIVE_Q_NAME)
		self.channel.queue_bind(exchange=self.__RECEIVE_EX_NAME,
						queue=self.__RECEIVE_Q_NAME,
						)
		#init & bind send queue
		self.channel.queue_declare(queue = self.__SEND_Q_NAME)
		self.channel.exchange_declare(exchange=self.__SEND_EX_NAME, type='fanout')
		self.channel.queue_bind(exchange=self.__SEND_EX_NAME,
						queue=self.__SEND_Q_NAME,
						)

	def __initReceiveQueue(self):
		#self.qrconn = pika.BlockingConnection(pika.ConnectionParameters(
		#	host='localhost'))
		#LOGGER.info('[init msg rqueue] : %s' % self.qrconn)
		#receive_channel = self.qrconn.channel()

		logging.info('[receive queue] : %s' % self.receive_channel)
		self.receive_channel.queue_declare(queue = self.__RECEIVE_Q_NAME)
		self.receive_channel.exchange_declare(exchange=self.__RECEIVE_EX_NAME, type='fanout')
		#bind
		self.receive_channel.queue_bind(exchange=self.__RECEIVE_EX_NAME,
						queue=self.__RECEIVE_Q_NAME,
						)
		#self.receive_channel = receive_channel



	def __initSendQeueue(self):
		#self.qsconn = pika.BlockingConnection(pika.ConnectionParameters(
	    #    host='localhost'))
		#LOGGER.info('[init msg squeue] : %s' % self.qsconn)
		#send_channel = self.qsconn.channel()
		logging.info('[send queue] : %s' % self.send_channel)
		self.send_channel.queue_declare(queue = self.__SEND_Q_NAME)
		self.send_channel.exchange_declare(exchange=self.__SEND_EX_NAME, type='fanout')
		#bind
		self.send_channel.queue_bind(exchange=self.__SEND_EX_NAME,
						queue=self.__SEND_Q_NAME,
						)
		#self.send_channel = send_channel

	def receive( self, process ):

		def callback(ch, method, properties, body):
			process(body)

		#self.receive_channel.basic_consume(callback,
		self.channel.basic_consume(callback,
                          queue= self.__RECEIVE_Q_NAME,
                          no_ack=True)

		try:
			#self.receive_channel.start_consuming()
			self.channel.start_consuming()
		except:
			#LOGGER.exception('receive consuming except')
			pass

	def send(self, message):
		LOGGER.info('qconn is open::%r' % self.qconn.is_open)
		if not self.qconn.is_open:
			self.__initQueue()
		#self.send_channel.basic_publish(exchange=self.__SEND_EX_NAME,
		self.channel.basic_publish(exchange=self.__SEND_EX_NAME,
					  routing_key='',
                      body=message)




if __name__ == '__main__':
	import time
	conn = WMDb().getConn()
	print conn
	conn.close()
	time.sleep(5)

	conn1 = WMDb().getConn()
	print conn1
	conn1.execute("set names latin1")
        for wb_service in conn1.query("SELECT * FROM wb_service"):
            print wb_service.uid, wb_service.cmd, wb_service.action
	time.sleep(3)
	conn1.close()
	time.sleep(5)
