var express = require('express');
var cookieSession = require('cookie-session');
var port = 8080;
var server_port = process.env.OPENSHIFT_NODEJS_PORT || port;
var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';

function start (){
	require('dns').lookup(require('os').hostname(), function (err, ip_address, fam) {
		console.log('localhost: ' + ip_address + " PORT: " + port);
	});
}
var favicon = require('serve-favicon');
express()
	.set('view engine', 'ejs')
	.use(express.static('./public'))
	.use(require('./accounts'))
	.get('*', function (req, res) {
		res.render('index.ejs', {
			user: JSON.stringify(req.session.user || null)
		});
	})
	.use(favicon(__dirname + '/public/favicon.ico'))
	.listen(server_port, server_ip_address, function () {
		start();
		console.log( "Listening on " + server_ip_address + ", server_port " + port);
});

