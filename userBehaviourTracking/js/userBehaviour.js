furthestScrollPosition = 0;
clickCount = 0;

window.onload = function() {
	pageEntryTime = new Date();
}

window.onscroll = function() {
	var element = document.body;
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

window.onbeforeunload=function() {
	dumpString = generateDumpString();
	var http = new XMLHttpRequest();
	var url = "userBehaviourTracking.php";
	var params = "data=" + dumpString;
	http.open("POST", url, false);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	http.send(params);
}
