var express = require('express');
var cookieSession = require('cookie-session');
var port = 8080;
var server_port = process.env.OPENSHIFT_NODEJS_PORT || port;
var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';

express()
	.set('view engine', 'ejs')
	.use(express.static('./public'))
	.use(require('./accounts'))
	.get('*', function (req, res) {
		res.render('index.ejs', {
			user: JSON.stringify(req.session.user || null)
		});
	})
	//.use(cookieSession({
	//secret: "secret",
	//cookie: {
	//	maxAge: 1000 * 60 * 60
	//}
	//}))
	//.listen(process.env.PORT || port);
	.listen(server_port, server_ip_address, function () {
	console.log( "Listening on " + server_ip_address + ", server_port " + port )
});
// adding process.env.PORT allows heroku deployment
//console.log("Wiki on localhost:"+ port);

//setInterval(sessionCleanup, 1000*60*60*24);
//
//function sessionCleanup() {
//	sessionStore.all(function(err, sessions) {
//		for (var i = 0; i < sessions.length; i++) {
//			sessionStore.get(sessions[i], function() {} );
//		}
//	});
//}
