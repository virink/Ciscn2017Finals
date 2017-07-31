<?php

/*
*************************
**  by Ginkgo          **
**                     **
**          2017.7.26  **
*************************
*
* Oracle Padding Attack
* 
*/

include_once($_SERVER["DOCUMENT_ROOT"].'/sys/lib.php');
include_once($_SERVER["DOCUMENT_ROOT"].'/sys/1024.php');

function get_random_token(){
    $random_token='';
    for($i=0;$i<16;$i++){
        $random_token.=chr(rand(1,255));
    }
    return $random_token;
}

function set_crpo($id)
{   
    $token = get_random_token();
    // var_dump(bin2hex($token));
    $c = openssl_encrypt((string)$id, METHOD, SECRET_KEY, OPENSSL_RAW_DATA, $token);
    $retid = base64_encode(base64_encode($token.'|'.$c));
    return $retid;   
}

function set_decrpo($id)
{
if($c = base64_decode(base64_decode($id)))
{
    if($iv = substr($c,0,16))
    {
        if($pass = substr($c,17))
        {
            if(openssl_decrypt($pass, METHOD, SECRET_KEY, OPENSSL_RAW_DATA,$iv))
            {
                return $u;
            }else
                die("HumenSec paddiiiiiiiiiiiiiiiiiiiiiiiiiiiiiing!");
        }else
            return 1;
    }else
        return 1;
}else
    return 1;
}

function get_by_id($nid){
    $xid = set_decrpo($nid);
    waf($xid);
    if(strlen($xid)>64){
        print "Waf by HumenSec";
    }
    return $xid;
}
