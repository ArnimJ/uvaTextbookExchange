$(document).ready(function() {
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
})

function handleLoginSubmit(elem) {
	var username = $("#login_username").val();
	var password = $("#login_password").val();
	var data = {
		"username": username,
		"password": password
	};
	
	console.log(data);
	
	Promise.resolve($.post("/process_login", data))
	.then(function(res) {
		if (res.status == "success") {
			window.location.href = "/";
		} else {
			$("#login-message").text(res.message);
		}
	})
	.catch(function(res) {
		alert("Something went wrong. Please try again.");
		console.log(res);
	})
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}