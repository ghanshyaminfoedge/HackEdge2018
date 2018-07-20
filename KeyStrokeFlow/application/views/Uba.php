<?php
defined('BASEPATH') OR exit('No direct script access allowed');
?><!DOCTYPE html>
<html lang="en"><head>
    <meta charset="utf-8">
    <title>Stop Account Sharing</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/paper/bootstrap.min.css" media="screen">
    <link rel="stylesheet" href="<?php echo base_url(); ?>static/css/main.css" media="screen">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" media="screen">
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </head>
	<body>
	   <div class="container-fluid">
            <div class="">
                <nav class="navbar navbar-default">
                    <div class="container-fluid">
                      <div class="navbar-header">
                        <a class="navbar-brand" href="/">Naukri Profile</a>
                      </div>
                      <ul class="nav navbar-nav">
                        <li class="active"><a href="/">Create</a></li>
                        <li><a href="home">Home</a></li>
                        <li><a href="/uba">UBA Demo</a></li>
                        <li><a href="login">Login</a></li>
                      </ul>
                    </div>
                </nav>
            </div>  
            <div class="row progress">
                <div class="progress-bar" id="progressbar" role="progressbar" aria-valuenow="0"
                    aria-valuemin="0" aria-valuemax="100" style="width:0%">
                        0%
                </div>
            </div>
            <div class="row" id="mainWrap">
                <div class="col-md-offset-2 col-md-8">
                    <div id="ubaForm">
                        <input class="form-control" type="text" placeholder="Add topic name" aria-label="UserName" required>
                        <input class="form-control" type="email" placeholder="Email id" required>
                        <input class="form-control" type="mobile" placeholder="Mobile number" required>
			<input class="form-control" type="textArea" placeholder="Blog Content" required>
			<textarea class="form-control" rows="10" cols="150" placeholder="Enter content for the blog" id="keyphrase" style="margin-top:20px" required></textarea>
                        <button class="btn mt10 pull-right btn-success" id="PostBlog" onclick="postBlog()">Post Blog</button>
                    </div>
                </div>
            </div>
        </div>
	</body>
        <script src="<?php echo base_url(); ?>static/js/Keystrokes.js"></script>
	<script src="<?php echo base_url(); ?>static/js/KeystrokeDynamics.js"></script>
        <script src="<?php echo base_url(); ?>static/js/userBehaviour.js"></script>
</html>
