# -*- coding: utf-8 -*-

database = {
	'host':'localhost',
	'user':'root',
	'passwd':'',
	'dbname':'weibo_message',
	'charset':'utf8'
}


queue_config = {
	'host' : 'localhost',
	'receive' : {
		'ex_name' : 'ex_receive',
		'ex_type' : 'fanout',
		'queue_name' : 'qreceive',
		'route_key' : ''
	},
	'reply' : {
		'ex_name' : 'ex_reply',
		'ex_type' : 'fanout',
		'queue_name' : 'qreply',
		'route_key' : ''
	}
}

service_config = {
	'DEFAULT':{
		'action' : 'default',
		'templates' : '默认回复'
	},
	'FOLLOW':{
		'action' : 'follow',
		'templates' : '回复DY'
	},
	'UNFOLLOW':{
		'action': 'unfollow',
		'templates' : '感谢关注'
	},
	'DY':{
		'action' : 'subscribe',
		'service_id': 'DY',
		'templates' : '订阅成功'
	},
	'TD':{
		'action' : 'unsubscribe',
		'service_id': 'DY',
		'templates': '取消成功'
	}

}