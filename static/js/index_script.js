$(document).ready(function(){
	$("#register-btn").click(function(e){

		//post request handlers would be here
		
			$('#register').click(function(e){
				e.preventDefault();
				console.log('clicked');
				console.log($("#reg-conf-password"));
				var password = $("#reg-password").val();
				var con_password = $("#reg-conf-password").val();
				console.log(password+con_password);
				if(password===con_password){

					alert("you would be directed to your profile shortly","password matched");
				}else{
					alert("password did'nt match please try again","password didn't match");
				}
			});


	});

	$("#login-btn").click(function(){
		//postrequest handler
	});

});

