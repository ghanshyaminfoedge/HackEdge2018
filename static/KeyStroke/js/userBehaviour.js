furthestScrollPosition = 0;
clickCount = 0;

window.onload = function() {
	pageEntryTime = new Date();
}

window.onscroll = function() {
	var element = document.getElementById("mainWrap");
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
	 var request = $.ajax({
  		method: "POST",
  		url: "http://192.168.85.5:5000/user",
		contentType: "application/json",
	 	dataType:"json",
  		data: {"timeOnPage": timeOnPage, "furthestScrollPosition":furthestScrollPosition, "clickCount": clickCount}
	});
  	request.done(function( msg ) {
    		alert( "Data Saved: " + msg );
  	})
	request.fail(function( jqXHR, textStatus ) {
  		alert( "Request failed: " + textStatus );
	});

}
