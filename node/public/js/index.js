function init() {

  var serverBaseUrl = document.domain;

  /*
   On client init, try to connect to the socket.IO server.
   Note we don't specify a port since we set up our server
   to run on port 8080
   */
  var socket = io.connect(serverBaseUrl);

  //We'll save our session ID in a variable for later
  var sessionId = '';

  
  /*
   When the client successfuly connects to the server, an
   event "connect" is emitted. Let's get the session ID and
   log it. Also, let the socket.IO server there's a new user
   with a session ID and a name. We'll emit the "newUser" event
   for that.
   */
  socket.on('connect', function () {
    sessionId = socket.socket.sessionid;
    console.log('Connected ' + sessionId);   
  });


  /*
   When the server emits the "teamsadded" event, we'll reset
   the teams section and display the connected teams.   
   */
  socket.on('teamsadded', function (data) {
    updateTeams(data.teams);
  });
  
  /*
   When the server emits the "teamsadded" event, we'll reset
   the teams section and display the connected teams.   
   */
  socket.on('goal', function (data) {
    $('#'+ data.team + '-score').html(data.goals);
  });


  
  /*
   Log an error if unable to connect to server
   */
  socket.on('error', function (reason) {
    console.log('Unable to connect to server', reason);
  });

  //Helper function to update the team list
  function updateTeams(teams) {
    console.log(teams);
    $('#black').html('');
    $('#yellow').html('');
    for (var i = 0; i < teams.length; i++) {
      $('#'+teams[i].name).append('<span id="' + teams[i].name + '">' +
        teams[i].members[0] + ' AND ' + teams[i].members[1] + '<br /></span>');
    }
  }
  
}

$(document).on('ready', init);