<?php

$request = $_REQUEST;

file_put_contents("data.log", print_r($request["data"]."\n", true), FILE_APPEND);
