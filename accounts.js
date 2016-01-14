var Firebase = require('firebase');
var crypto = require('crypto');

var firebase = new Firebase('https://vvc-wiki.firebaseio.com/');
var users = firebase.child('users');
//firebase stores data as a JSON data structure


function hash (password) {
	return crypto.createHash('sha512').update(password).digest('hex');
	//returns hexadecimal digest of password

}

var router = require('express').Router();

router.use(require('body-parser').json());
router.use(require('cookie-parser')());
router.use(require('cookie-session')({
	resave: false,
	saveUninitialized: true,
	secret: 'asdfjasdfarg',
	cookie: {maxAge: 30*24*3600*1000} // 30 day expiration date
}));

//setInterval(sessionCleanup, 1000*60*60*24);
//
//function sessionCleanup() {
//	sessionStore.all(function(err, sessions) {
//		for (var i = 0; i < sessions.length; i++) {
//			sessionStore.get(sessions[i], function() {} );
//		}
//	});
//}

router.post('/api/signup', function (req, res) {
	var username = req.body.username,
	password = req.body.password;

	if (!username || !password)
		return res.json({ signedIn: false, message: 'no username or password' });

	users.child(username).once('value', function (snapshot) {
		if (snapshot.exists())
			return res.json({ signedIn: false, message: 'username already in use' });

		var userObj = {
			username: username, 
			passwordHash: hash(password)
		};

		users.child(username).set(userObj);
		req.session.user = userObj;

		res.json({
			signedIn: true,
			user: userObj
		});
	});
});

router.post('/api/signin', function (req, res) {
	var username = req.body.username,
	password = req.body.password;

	if (!username || !password)
		return res.json({ signedIn: false, message: 'no username or password' });

	users.child(username).once('value', function (snapshot) {
		if (!snapshot.exists() || snapshot.child('passwordHash').val() !== hash(password))
			return res.json({ signedIn: false, message: 'wrong username' });

		var user = snapshot.exportVal();

		req.session.user = user;
		res.json({
			signedIn: true,
			user: user
		});
	});
});

router.post('/api/signout', function (req, res) {
	delete req.session.user;
	res.json({
		signedIn: false,
		message: 'You have been signed out'
	});
});

module.exports = router;
