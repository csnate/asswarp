var express = require('express'),
	app = express(),
	http = require("http").createServer(app),
  	io = require("socket.io").listen(http),
	_ = require("underscore");

//Server's IP address
app.set("ipaddr", "10.60.3.155");

//Server's port number
app.set("port", 8080);

//Specify the views folder
app.set("views", __dirname + "/views");

//View engine is Jade
app.set("view engine", "jade");

//Specify where the static content is
app.use(express.static("public", __dirname + "/public"));

//Tells server to support JSON, urlencoded, and multipart requests
app.use(express.bodyParser());

//default routing
app.get("/", function(request, response) {

  //Render the view called "index"
  response.render("index");

});


//teams
var teams = [],
	scores = [];
	
app.get('/teams', function(req, res) {
  res.json(teams);
});


//add teams
app.post("/teams", function(req, res) {

	teams = [];
	scores = [];
	
	//make sure there are two
	var ts = req.body;

	if ( ts instanceof Array && ts.length == 2) {
		for (var i = 0; i < ts.length; i++) {
			var team = ts[i];

			if (team.name && team.members) {

				var newTeam = {
					name : team.name,
					members : team.members
				};
				teams.push(newTeam);

				//push it to score

				scores.push({
					type : "score",
					team : team.name,
					score : 0
				});

				res.statusCode = 200;
				//res.json("Welcome team " + team.name);
				
			} else {
				res.statusCode = 404;
				return res.send('Error 404: Post syntax incorrect.');
			}

		}
		
		//Let our scoreboard know that teams have signed in
  		io.sockets.emit("teamsadded", {teams: teams});
  
		res.statusCode = 200;
		res.send('teams added!');

	}

}); 

//goal!!!
app.post("/goal", function(req, res){
	
	var g = req.body;
	var team = g.team;
	
	var t = _.detect(scores, function (obj) {return obj.team === team;});;
	t.score += 1;
	
	res.json(t);
	
});

//scoreboard
app.get("/scoreboard", function(req, res) {
	res.json(scores);	
});


/* Socket.IO events */
io.on("connection", function(socket){

  /*
   When a client disconnects from the server, the event "disconnect" is automatically
   captured by the server. It will then emit an event called "userDisconnected" to
   all participants with the id of the client that disconnected
   */
  socket.on("connect", function() {
    
  });

});


//Start the http server at port and IP defined before
app.listen(app.get("port"), function() {
  console.log("Server up and running. Go to http://" + app.get("ipaddr") + ":" + app.get("port"));
});