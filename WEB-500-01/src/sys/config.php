<?php

error_reporting(E_ALL);

if (!file_exists($_SERVER["DOCUMENT_ROOT"].'/sys/install.lock')){
	header("Location: /install/install.php");
    exit;
}

include_once($_SERVER["DOCUMENT_ROOT"].'/sys/lib.php');

$host="127.0.0.1"; 
$username="root"; 
$password="root"; 
$database="vauditdemo";

$conn = mysql_connect($host,$username,$password);
mysql_query('set names utf8',$conn);
mysql_select_db($database, $conn) or die(mysql_error());
if (!$conn)
{
	die('Could not connect: ' . mysql_error());
	exit;
}

session_start();

?>
