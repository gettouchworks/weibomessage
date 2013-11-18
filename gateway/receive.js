var https = require("https");
var querystring = require("querystring");
var amqp = require('amqp');

var domain = require('domain')
var d = domain.create();
d.on('error', function(err) {
	console.error('domain caught', err);
});

var baseconfig = require('./config.js').base_config

var since_id = "";

var receive = function(uid, sendObj){
	console.log("func receiving......");

	var querys = {};
	querys['source'] = baseconfig.source;
	//querys['uid'] = 2126852741;
	querys['uid'] = uid;

	var options = {
	  hostname: baseconfig.hostname,
	  path: baseconfig.receive_path+'?'+querystring.stringify(querys),
	  auth: baseconfig.auth
	};

	console.log(options)

	var request = https.get(options, function(res){
		res.on('data', function(chunk){
			if(res.statusCode != 200){
				console.log('res.statusCode:', res.statusCode)
				return;
			}
			console.log(chunk.toString());
			sendObj.sendQ(chunk.toString())
		});
		res.on('end', function(){
			console.log("end !!!");
			receive(uid);
		});
	}).on('error', function(e) {
		console.log("Got error: " + e.message);
	})

	
	request.setTimeout( 1000*60*4, function( ) {
		request.abort();
		request.destroy();
		console.log("reload");
		receive(uid);
	});
			

	//	return request;
}

//receive(2126852741);
//receive(2489818573);

var util = require("util");
var event = new require("events").EventEmitter;

var amqp = require('amqp');
// var connection = null;
// var exchange = null;
// var reconnInt;
// var icount = 0

var ReceiveService = function(){
	this.connection = null;
	this.exchange = null;
	this.reconnInt;
	this.icount = 0
}
util.inherits(ReceiveService, event);
ReceiveService.prototype.getConn = function(){
	var self = this;
    self.connection = amqp.createConnection({ host: "localhost", port: 5672 }, {reconnect: false});
    self.connection.on('ready', function () {
    	self.exchange = self.connection.exchange("ex_receive", options={type:'fanout'})
		self.exchange.on('open', function(){
			self.connection.queue('qreceive', {autoDelete: false}, function(queue){
				queue.bind('ex_receive', '');
	            queue.on('queueBindOk', function(){
	            	console.log("wait receive.....")
					self.emit('connected')
	            })
				
			})
			
		})    	
	}).on('error', function(err){
		console.log('conn err', err)
	}).on('end', function(){
		console.log('conn end')
	}).on('close', function(){
		console.log('conn close && todo reconnect')
	})
}
ReceiveService.prototype.sendQ = function(content){
	console.log('add to receive queue', content)
	this.exchange.publish('qreceive', content, {})
}
ReceiveService.prototype.customers = function(){
	customers = [2126852741]
	for(var i in customers){
		uid = customers[i]
		this.receive(uid)
	}
}
ReceiveService.prototype.receive = function(uid){
	console.log("receiving......");
	var self = this;
	var querys = {};
	querys['source'] = baseconfig.source;
	querys['uid'] = uid;
	var options = {
	  hostname: baseconfig.hostname,
	  path: baseconfig.receive_path+'?'+querystring.stringify(querys),
	  auth: baseconfig.auth
	};
	console.log(options)
	var request = https.get(options, function(res){
		res.on('data', function(chunk){
			if(res.statusCode != 200){
				console.log('res.statusCode:', res.statusCode)
				return;
			}
			// console.log(chunk.toString());
			// self.sendQ(chunk.toString())
			self.emit('received', chunk.toString())
		});
		res.on('end', function(){
			console.log("end !!!");
			self.receive(uid);
		});
	}).on('error', function(e) {
		console.log("Got error: " + e.message);
		self.receive(uid);
	})

	
	request.setTimeout( 1000*60*4, function( ) {
		request.abort();
		request.destroy();
		console.log("reload");
		//receive(uid);
	});
}



var recvService = new ReceiveService()
recvService.getConn()
recvService.on('connected', function(ex){
	console.log('msg queue ready');
	this.customers(receive)

})
recvService.on('received', function(content){
	this.sendQ(content)
})

var sendQ = function(content){

	exchange.publish('qreceive', content, {})
}

function receiveQ_init(){
	clearTimeout(reconnInt)
	if(connection != null){
		return
	}

	console.log('queue init....', icount++)
	connection = amqp.createConnection({ host: "localhost", port: 5672 }, {reconnect: false});
	connection.on('ready', function () {
	 
		exchange = connection.exchange("ex_receive", options={type:'fanout'})
		exchange.on('open', function(){
			console.log("wait receive.....")
			receive(2126852741)
		})
	}).on('error', function(err){
		console.log('conn err', err)
	}).on('end', function(){
		console.log('conn end')
	}).on('close', function(){
		console.log('conn close && reconnect')
		reconnInt = setTimeout(function(){
			//console.log(connection)
			connection = null
			receiveQ_init()
		}, 1000)
	})
}

//receiveQ_init()



