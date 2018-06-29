<?php

$dataArray = file("/tmp/test.txt", FILE_IGNORE_NEW_LINES);
#$data = (($dataArray)[0]);

#$res = parseRawTimingData($data);
#echo json_encode(getCSVLineFromTimingData($res));

#echo json_encode(extractFeatures($dataArray));

extractFeatures(json_decode($dataArray[0],true));


function extractFeatures($timingDataArray){
	$result = array();
	foreach ($timingDataArray as $value) {
	    $res = parseRawTimingData($value);
	    $result = getCSVLineFromTimingData($res);
	    file_put_contents("/tmp/keyStroke.txt",print_r($result."\n",1),FILE_APPEND);		
	}
}

function parseRawTimingData( $timingDataFromPost ) {
	$timingData =  array();
        foreach( $timingDataFromPost as $keystroke ) {
                // The Javascript sends the data as:
                //    [key code],[time down],[time up]
                // (With each keypress triplet separated by a space)

                // If this is good data (e.g., not just a space)
                        $currentKey['keyCode'] = $keystroke["keyCode"];
                        $currentKey['timeDown'] = $keystroke["timeDown"];
                        $currentKey['timeUp'] = $keystroke["timeUp"];

                        $currentKey['timeHeld'] = $currentKey['timeUp'] - $currentKey['timeDown'];
                        if( $currentKey['timeHeld'] < 0 ) {
                                $currentKey['timeHeld'] = 0;
                        }

                        $currentKey['character'] = chr($currentKey['keyCode']);

                        // Make non-printing characters readable
                        if( $currentKey['keyCode'] == 16 ) {
                                $currentKey['character'] = "SHIFT";
                        } else if( $currentKey['keyCode'] == 13 ) {
                                $currentKey['character'] = "ENTER";
                        } else if( $currentKey['keyCode'] == 32 ) {
                                $currentKey['character'] = "SPACE";
                        }

                        // push to the end of the array
                        $timingData[] = $currentKey;
        }

        return $timingData;
}

function getCSVLineFromTimingData( $timingData, $repetition = -1 ) {
    define( "MS_TO_SECONDS", 1.0/1000.0 );

        $csv = "";
        if( $repetition >= 0 ) {
                $csv .= $repetition . ",";
        }

    // only care about time held for pos. 0
        $csv .= MS_TO_SECONDS * $timingData[0]['timeHeld'];

        // For each (other) character in the password . . .
        for( $i = 1; $i < sizeof($timingData); $i++ ) {
                $dd = MS_TO_SECONDS * ($timingData[$i]['timeDown'] - $timingData[$i-1]['timeDown']);
                $ud = MS_TO_SECONDS * ($timingData[$i]['timeDown'] - $timingData[$i-1]['timeUp']);
                $h = MS_TO_SECONDS * ($timingData[$i]['timeHeld']);

                if( $h < 0 )    $h = 0;
                if( $ud > 1000 ) $ud = 0.1; // some neutral value


                $csv .= "," . $dd . "," . $ud . "," . $h;
        }

        $csv .= "";

        return $csv;
}


?>
