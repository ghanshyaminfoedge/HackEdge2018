<?php
error_reporting(0);
defined('BASEPATH') OR exit('No direct script access allowed');

class Login extends CI_Controller {

    /**
     * Index Page for this controller.
     *
     * Maps to the following URL
     * 		http://example.com/index.php/welcome
     * 	- or -
     * 		http://example.com/index.php/welcome/index
     * 	- or -
     * Since this controller is set as the default controller in
     * config/routes.php, it's displayed at http://example.com/
     *
     * So any other public methods not prefixed with an underscore will
     * map to /index.php/welcome/<method_name>
     * @see https://codeigniter.com/user_guide/general/urls.html
     */
    public function index() {
        $this->load->view('login');
    }

    public function perform() {
        $id= $_GET['id'];
        if($id == "UW*1282Kjak129911jasjka91k1k1k19123k0==") {
            redirect("home");
        } else {
            redirect("login");
        }
    }

}
?>
