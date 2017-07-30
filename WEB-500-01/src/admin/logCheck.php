<?php
include_once('../sys/config.php');
include_once('../sys/mdzz.php');

function loginsec($info){
    $iv = get_random_token();
    $plain = serialize($info);
    $cipher = openssl_encrypt($plain, METHOD, SECRET_KEY, OPENSSL_RAW_DATA, $iv);
    $_SESSION['admin'] = $info['admin'];
    setcookie("IV", base64_encode($iv));
    setcookie("ID", base64_encode(base64_encode($plain)));
}

function check_login(){
    if(isset($_COOKIE['IV'])&&isset($_COOKIE['ID'])){
        $iv = base64_decode($_COOKIE["IV"]);
        $info = base64_decode(base64_decode($_COOKIE["ID"]));
        if($plain = openssl_decrypt($info, METHOD, SECRET_KEY, OPENSSL_RAW_DATA, $iv)){
            $info = unserialize($plain);
            $_SESSION['admin'] = $info['admin'];
        }
    }
    var_dump($_SESSION);
}

if (isset($_POST['submit']) && !empty($_POST['user']) && !empty($_POST['pass']) && !empty($_POST['captcha'])) {
	include_once('../header.php');

	if((@$_POST['captcha'] !== $_SESSION['captcha']) && !empty($_SESSION['captcha'])){
        // $_SESSION['captcha'] = null
        // $_POST['captcha'] = null
		echo "captcha error";
        header('Location: login.php');
		exit;
	}
    else{
        echo "captcha succeed";
    }

	$name = $_POST['user'];
	$pass = $_POST['pass'];

    $info = array('user'=>$name,'pass'=>$pass,'admin'=>'0');
    loginsec($info);

    $query = "SELECT * FROM admin WHERE admin_name = '$name' AND admin_pass = MD5('$pass')";
    $data = mysql_query($query, $conn) or die('Error!!');

    if (mysql_num_rows($data) == 1) {
		$_SESSION['admin'] = 233;
        header('Location: manage.php');
        print(':D 看见我淫荡的笑容了没有，考点不在这，本宝宝复现不成功，放弃了。。。。');
    }
	else {
		$_SESSION['error_info'] = '用户名或密码错误';
		header('Location: login.php');
	}
	mysql_close($conn);
    exit;
}
else {
    check_login();
	not_find($_SERVER['PHP_SELF']);
}

?>
