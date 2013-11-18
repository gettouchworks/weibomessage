var https = require("https");
var querystring = require("querystring");
var amqp = require('amqp');

var domain = require('domain')
var d = domain.create();
d.on('error', function(err) {
	console.error('domain caught err: ', err);
});

var baseconfig = require('./config.js').base_config

var connection = amqp.createConnection({ host: "localhost", port: 5672 });

connection.on('ready', function () {

    connection.exchange('ex_reply', {type: 'fanout',
                                 autoDelete: false}, function(exchange){
        connection.queue('qreply', 
        						 {autoDelete: false}, function(queue){
            queue.bind('ex_reply', '');
            queue.on('queueBindOk', function(){
            	console.log(' [*] Waiting for send message. To exit press CTRL+C')
	            queue.subscribe(function(msg){
	                console.log(" [x] %s", msg.data.toString('utf-8'));
	                reply(JSON.parse(msg.data.toString('utf-8')))
	            });

            })
            
        })
    });
}).on('error', function(err){
	console.log('conn err::', err)
})


var reply = function(msg){
	console.log("reply......");
	//console.log(msg);

	source = baseconfig.source;
	msg['source'] = source
	content = querystring.stringify(msg)

	var options = {
	  hostname: baseconfig.hostname,
	  method: 'post',
	  path: baseconfig.reply_path,
	  auth: baseconfig.auth,
	  headers:{
	  	'Content-Type':'application/x-www-form-urlencoded',
		'Content-Length':content.length
	  }
	};

	var request = https.request(options, function(res){
		res.on('data', function(chunk){
			console.log(chunk.toString());
		});
	}).on('error', function(e) {
		console.log("Got error: " + e.message);
	})
	request.write(content);
	request.end();

	//	return request;
}

// var msg = {}
// msg['id'] = 1311090005478735
// //msg['source'] = 352089742
// msg['type'] = "text"
// co = JSON.stringify({"text":"回复"})
// msg['data'] = co

// console.log(msg)
//reply(msg)
