

function addNav() {
	<!--Check if user is logged on-->
	/*$("body").append(" <script>function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
 
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
csrftoken= getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*//*.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});
</script>");*/
	$("#navbar").html('<div class="container"><div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"><span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><a id="tracks_home" class="navbar-brand" href="">Tracks</a></div><div class="collapse navbar-collapse"><ul id="navbar_options" class="nav navbar-nav"> </ul><form class="navbar-form" role="search"><div class="form-group"><input type="text" class="form-control" placeholder="search"></div><button type="submit" class="btn btn-default"><span class="glyphicon glyphicon-music"></span></button></form></div><!--/.nav-collapse --></div>')
	if (true) {
		$("#navbar_options").html('<li><a id="downbeat">Downbeat</a></li><li><a id="about">About</a></li><li><a id="upload">Upload</a></li><li> <a id="signout" href="javascript:signOut()">Sign out</a></li>')
	} else {
		<!-- Show sign in link instead of projects, downbeat, profile, etc. -->
		$("#navbar_options").html('<li><a href="#signin">Sign In</a></li>')
	}
	hrefCreate();
}

function hrefCreate() {
	$("#tracks_home").attr('href',window.location.origin+"/Tracks")
	$("#downbeat").attr('href', window.location.origin+"/Tracks/downbeat/")
	$("#about").attr('href', window.location.origin+"/Tracks/about.html")
	$("#upload").attr('href', window.location.origin+"/Tracks/userpage/")
	$("#signout").attr('href', window.location.origin+"/Tracks/logout/")
	}


function signOut() {
	var csrftoken = getCookie('csrftoken');
	$.ajax({
			type: 'POST',
			url: window.location.origin+"/Tracks/logout/",
			data: {},
    	});
}