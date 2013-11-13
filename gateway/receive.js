var https = require("https");
var querystring = require("querystring");
var amqp = require('amqp');

var baseconfig = require('./config.js').base_config



var since_id = "";

var receive = function(uid){
	console.log("receiving......");


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
			sendQ(chunk.toString())
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

var amqp = require('amqp');
var connection = amqp.createConnection({ host: "localhost", port: 5672 });
var exchange = null;

var sendQ = function(content){

	exchange.publish('qreceive', content, {})
}

connection.on('ready', function () {
 
	exchange = connection.exchange("ex_receive", options={type:'fanout'})
	exchange.on('open', function(){
		console.log("wait receive.....")
		receive(2126852741)
	})
})




