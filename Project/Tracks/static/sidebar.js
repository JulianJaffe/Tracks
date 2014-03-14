function addNav() {
	<!--Check if user is logged on-->
	$("#navbar").html('<div class="container"><div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"><span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><a class="navbar-brand" href="../Tracks">Tracks</a></div><div class="collapse navbar-collapse"><ul id="navbar_options" class="nav navbar-nav"> </ul><form class="navbar-form" role="search"><div class="form-group"><input type="text" class="form-control" placeholder="search"></div><button type="submit" class="btn btn-default"><span class="glyphicon glyphicon-music"></span></button></form></div><!--/.nav-collapse --></div>')
	if (true) {
		$("#navbar_options").html('<li><a href="downbeat">Downbeat</a></li><li><a href="about.html">About</a></li><li><a href="upload">Upload</a></li><li><a href="javascript:signOut()">Sign out</a></li>')
	} else {
		<!-- Show sign in link instead of projects, downbeat, profile, etc. -->
		$("#navbar_options").html('<li><a href="#signin">Sign In</a></li>')
	}
}

function signOut() {
	<!-- End session id. then: -->
	window.location = "../Tracks";
}