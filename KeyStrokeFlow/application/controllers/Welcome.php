<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Welcome extends CI_Controller {

    /**
     * Index Page for this controller.
     *
     * Maps to the following URL
     * 		http://example.com/index.php/welcome
     *	- or -
     * 		http://example.com/index.php/welcome/index
     *	- or -
     * Since this controller is set as the default controller in
     * config/routes.php, it's displayed at http://example.com/
     *
     * So any other public methods not prefixed with an underscore will
     * map to /index.php/welcome/<method_name>
     * @see https://codeigniter.com/user_guide/general/urls.html
     */
    public function index()
    {
        $this->load->view('create');
    }
        
    public function create() {
        $username = $_POST['username'];
        $password = $_POST['password'];
        $keyPhrase = $_POST['keyPhrase'];
        if ($username && $password) {
                if($keyPhrase){
                    $fileName = "/data/training_".$username."_".$password.".txt";
                    file_put_contents("/data/test.txt", $keyPhrase);
                    $this->savePattern($fileName);
                }
                $this->load->view('login');//redirect("http://localhost:8000/index.php/login");
        } else {
            $this->showError();
        }
    }
    
    public function validate() {
        $username = $_POST['username'];
        $password = $_POST['password'];
        $keyPhrase = $_POST['keyPhrase'];
	$ubaScore = $_POST['ubaScore'];
	if($ubaScore && $ubaScore <= 70)
		 $this->showError($ubaScore);
        else if ($username && $password) {
                if($keyPhrase){
                    $fileName = "/data/current_attempt_".$username."_".$password.".txt";
                    file_put_contents("/data/test.txt", $keyPhrase);
                    $this->savePatternLogin($fileName);
                }
                $response = $this->validatePattern($username, $password);
                if($response == 1) {
                    $this->load->view('home');
                } else {
                    $this->showError();
                }
        } else {
            $this->showError();
        }
    }
    
    private function validatePattern($username, $password) {
        $ch = curl_init("http://localhost:9090/keystroke/api/score?userName=" . $username . "&keyPass=" . $password);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $response = curl_exec($ch);
        curl_close($ch);
        return $response;
        /*$url = "http://localhost:5000/keystroke/api/score?userName=" . $username . "&keyPass=" . $password;
        $output = $this->curl->simple_get($url, $post_data);*/
    }
    
    private function showError($ubaScore = "") {
        $data['heading'] = "Unauthorized user";
	if($ubaScore)  $data['message'] = "You are not genuine user. your Score is " .$ubaScore;
        else $data['message'] = "Incorrect credentials, please try again!";
        $this->load->view('errors/html/error_general', $data);
    }

    public function savePattern($fileName) {
        $dataArray = file("/data/test.txt", FILE_IGNORE_NEW_LINES);
        $this->extractFeatures(json_decode($dataArray[0], true),$fileName);
    }
	
    public function savePatternLogin($fileName) {
        $dataArray = file("/data/test.txt", FILE_IGNORE_NEW_LINES);
        $this->extractFeaturesLogin(json_decode($dataArray[0], true),$fileName);
    }
    private function extractFeaturesLogin($timingDataArray,$fileName) {
        $result = array();
        file_put_contents($fileName, "");
        foreach ($timingDataArray as $value) {
            $res = $this->parseRawTimingData($value);
            $result = $this->getCSVLineFromTimingData($res);
            file_put_contents($fileName, print_r($result . "\n", 1), FILE_APPEND);
	    file_put_contents($fileName, print_r($result . "\n", 1), FILE_APPEND);
        }
    }

    private function extractFeatures($timingDataArray,$fileName) {
        $result = array();
        file_put_contents($fileName, "");
        foreach ($timingDataArray as $value) {
            $res = $this->parseRawTimingData($value);
            $result = $this->getCSVLineFromTimingData($res);
            file_put_contents($fileName, print_r($result . "\n", 1), FILE_APPEND);
        }
    }

    private function parseRawTimingData($timingDataFromPost) {
        $timingData = array();
        foreach ($timingDataFromPost as $keystroke) {
            // The Javascript sends the data as:
            //    [key code],[time down],[time up]
            // (With each keypress triplet separated by a space)
            // If this is good data (e.g., not just a space)
            $currentKey['keyCode'] = $keystroke["keyCode"];
            $currentKey['timeDown'] = $keystroke["timeDown"];
            $currentKey['timeUp'] = $keystroke["timeUp"];

            $currentKey['timeHeld'] = $currentKey['timeUp'] - $currentKey['timeDown'];
            if ($currentKey['timeHeld'] < 0) {
                $currentKey['timeHeld'] = 0;
            }

            $currentKey['character'] = chr($currentKey['keyCode']);

            // Make non-printing characters readable
            if ($currentKey['keyCode'] == 16) {
                $currentKey['character'] = "SHIFT";
            } else if ($currentKey['keyCode'] == 13) {
                $currentKey['character'] = "ENTER";
            } else if ($currentKey['keyCode'] == 32) {
                $currentKey['character'] = "SPACE";
            }

            // push to the end of the array
            $timingData[] = $currentKey;
        }

        return $timingData;
    }

    function getCSVLineFromTimingData($timingData, $repetition = -1) {
        define("MS_TO_SECONDS", 1.0 / 1000.0);

        $csv = "";
        if ($repetition >= 0) {
            $csv .= $repetition . ",";
        }

        // only care about time held for pos. 0
        $csv .= MS_TO_SECONDS * $timingData[0]['timeHeld'];

        // For each (other) character in the password . . .
        for ($i = 1; $i < sizeof($timingData); $i++) {
            $dd = MS_TO_SECONDS * ($timingData[$i]['timeDown'] - $timingData[$i - 1]['timeDown']);
            $ud = MS_TO_SECONDS * ($timingData[$i]['timeDown'] - $timingData[$i - 1]['timeUp']);
            $h = MS_TO_SECONDS * ($timingData[$i]['timeHeld']);

            if ($h < 0)
                $h = 0;
            if ($ud > 1000)
                $ud = 0.1; // some neutral value


            $csv .= "," . $dd . "," . $ud . "," . $h;
        }

        $csv .= "";

        return $csv;
    }
}
