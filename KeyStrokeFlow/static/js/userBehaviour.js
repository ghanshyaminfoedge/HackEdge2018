furthestScrollPosition = 0;
clickCount = 0;

window.onload = function() {
	pageEntryTime = new Date();
}

window.onscroll = function() {
	var element = document.documentElement;
	if(element.scrollTop > furthestScrollPosition) 
		furthestScrollPosition = element.scrollTop;
	else
		finalScrollPosition = element.scrollTop;
}

window.onclick = function() {
	clickCount++;
}

function generateDumpString() {
	timeOnPage = (new Date()) - pageEntryTime;

	
	str = "{";
	str = str + "\"url\":\"" + window.location.href + "\",";
	str = str + "\"timeOnPage\":\"" + timeOnPage + "\",";
	str = str + "\"furthestScrollPosition\":\"" + furthestScrollPosition + "\",";
	str = str + "\"finalScrollPosition\":\"" + finalScrollPosition + "\"";
	str = str + "\"clickCount\":\"" + clickCount + "\"";
	str = str + "}";
	return str;
}

function postBlog() {
	timeOnPage = (new Date()) - pageEntryTime;
        var keyStrokeData = JSON.stringify(keyLogs['#keyphrase']);
	 var request = $.ajax({
                type: 'POST',
  		url: 'http://localhost:5000/user',
		contentType: 'application/json',
	 	dataType:'json',
  		data: JSON.stringify({
                    "keyStrokeLog": keyStrokeData, 
                    "timeOnPage": timeOnPage, 
                    "furthestScrollPosition":furthestScrollPosition, 
                    "clickCount": clickCount})
            
	});
  	request.done(function( msg ) {
		alert( "UBA Score: " + msg.totalScore + "\n"+"KeyStroke Score: "+msg.keyStrokeScore);
                window.location.href=window.location.href;
  	})
	request.fail(function( jqXHR, textStatus ) {
	});

}

function postLogin() {
        timeOnPage = (new Date()) - pageEntryTime;
         return $.ajax({
                method: "POST",
                url: "http://localhost:5000/user/login",
                contentType: "application/json",
                dataType:"json",
		async:false,
                data: JSON.stringify({"timeOnPage": timeOnPage, "furthestScrollPosition":furthestScrollPosition, "clickCount": clickCount})
        }).responseText;
}
