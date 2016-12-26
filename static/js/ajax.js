var chat = 0;
$( document ).ready(function() {
	$("body").append('<div id="chat" ><div class="button" id="chatbutton">Chat</div></div>');
	$("#chatbutton").click(function (){
		$("#chat").css("bottom")=="32px"?$("#chat").css("bottom", "-290px"):$("#chat").css("bottom", "32px");
		if (chat == 0) $("#chat").append('<iframe src="http://irc.hackcoop.com.ar/" width="100%" id="chatiframe" ></iframe>');
		chat = 1;
	});
});
