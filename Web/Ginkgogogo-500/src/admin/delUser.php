<?php
include_once('../sys/config.php');

if (isset($_SESSION['admin']) && !empty($_GET['id']) && $_SESSION['admin'] == 233) {

	$clean_id = clean_input($_GET['id']);
	$query = "DELETE FROM users WHERE user_id = '$clean_id' LIMIT 1";
	mysql_query($query, $conn) or die('Error');
	mysql_close($conn);
	header('Location: manageUser.php');
    exit;
}else if ($_SESSION['admin'] && $_SESSION['admin'] != 233){
    var_dump("权限不足")；
}
else {
	not_find($_SERVER['PHP_SELF']);
}	
?>