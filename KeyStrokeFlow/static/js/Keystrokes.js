
var numTimes = 10;
var current = 0;
var keyStrokeMetricsDataArray = [];
var KSD_FIELD_ID = "keyphrase";
var keyPhraseArr = [];
$( document ).ready(function() {
 	$('#createProfile').attr("disabled", true);
});

$('#next, #login ').on('click', function() {
    var max = keyLogs['#keyphrase'].length;
    keyPhraseArr.push(keyLogs['#keyphrase'].slice(current, max));
    current = max;
    markStepCompletion();
    postLogin();
    if(numTimes == 0) {
        $('#next').attr("disabled", true);
        $('#createProfile').attr("disabled", false);
    }
});

$("#autoFill").on('click',function(){
	$("#username").val("ghanshyam");	
	$("#password").val("ghanshyam");
	$("#keyPhraseLog").val("ghanshyam");
//	$("#ubaScore").val(10);
	postLogin(function(result){
		("#ubaScore").val(res.totalScore);
		$("#loginForm").submit();
	})
	//alert(res);
//	$("#ubaScore").val(res);
})
$( "#createProfile, #login" ).on('click', function() {
	//removing hash for phase - 1
	$('#keyPhraseLog').val(JSON.stringify(keyPhraseArr));
});

// $( "#createProfile" ).submit(function( event ) {
//   alert( "Handler for .submit() called." );
//   event.preventDefault();
// });

function markStepCompletion() {
	$('#keyphrase').val("");
	$('#keyphrase').attr("placeholder", "Enter again to complete your authenticity");
	var percentage = 100/numTimes;
	$("#progressbar").text(percentage);
	$("#progressbar").css('width', percentage + '%');
	$('#next').text("Next (" + --numTimes + ")");
}

function submitForm(){
        event.preventDefault();
	$("#username").val("ghanshyam");
        $("#password").val("ghanshyam");
        $("#keyPhraseLog").val("ghanshyam");
//      $("#ubaScore").val(10);
       	var res =  postLogin();
       	var ubaScore = JSON.parse(res).totalScore;
        console.log(ubaScore);
        if(ubaScore < 70) {
            event.preventDefault();
            alert("Malicious login attempt! Score - " + ubaScore);
        } else {
            $("#loginForm").submit();
        }
}

//
////var numTimes = 2;
//var current = 0;
//var keyStrokeMetricsDataArray = [];
//var KSD_FIELD_ID = "keyphrase";
//var keyPhraseArr = [];
//$( document ).ready(function() {
//    $('#createProfile').attr("disabled", true);
//});
//
//$('#next').on('click', function() {
//    var max = keyLogs['#keyphrase'].length;
//    keyPhraseArr.push(keyLogs['#keyphrase'].slice(current, max));
//    current = max;
//    markStepCompletion();
//    if(numTimes == 0) {
//        $('#next').attr("disabled", true);
//        $('#createProfile').attr("disabled", false);
//    }
//});
//
//$( "#loginForm" ).submit(function() {
//    //removing hash for phase - 1
//    var keyPhraseArr = keyLogs['#keyphrase'];
//    $('#keyPhraseLog').val(JSON.stringify(keyPhraseArr));
//    $('#loginForm').serialize();
//});
//
//// $( "#createProfile" ).submit(function( event ) {
////   alert( "Handler for .submit() called." );
////   event.preventDefault();
//// });
//
//function markStepCompletion() {
//    $('#keyphrase').val("");
//    $('#keyphrase').attr("placeholder", "Enter again to complete your authenticity");
//    var percentage = 100/numTimes;
//    $("#progressbar").text(percentage);
//    $("#progressbar").css('width', percentage + '%');
//    $('#next').text("Next (" + --numTimes + ")");
//}
