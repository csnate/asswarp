var express = require('express'),
	app = express(),
	_ = require("underscore");

//Server's IP address
app.set("ipaddr", "10.60.3.155");

//Server's port number
app.set("port", 8080);

app.use(express.bodyParser());

//default routing
app.get('/', function(req, res) {
  res.send("Kickass Node Server...");
});

//teams
var teams = [];
app.get('/teams', function(req, res) {
  res.json(teams);
});






//Start the http server at port and IP defined before
app.listen(app.get("port"), function() {
  console.log("Server up and running. Go to http://" + app.get("ipaddr") + ":" + app.get("port"));
});