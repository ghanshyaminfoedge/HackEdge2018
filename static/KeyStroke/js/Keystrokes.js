var numTimes = 5;
var current = 0;
var keyStrokeMetricsDataArray = [];
var KSD_FIELD_ID = "keyphrase";
var keyPhraseArr = [];
$( document ).ready(function() {
 	$('#createProfile').attr("disabled", true);
});

$('#next').on('click', function() {
    var max = keyLogs['#keyphrase'].length;
    keyPhraseArr.push(keyLogs['#keyphrase'].slice(current, max));
    current = max;
    markStepCompletion();
    if(numTimes == 0) {
        $('#next').attr("disabled", true);
        $('#createProfile').attr("disabled", false);
    }
});

$( "#createProfile" ).on('click', function() {
	//removing hash for phase - 1
	var keyPhraseArr = keyLogs['#keyphrase'];
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
