<?php

define("SECRET_KEY", "Ginkgo".substr((string)time(),0,7)."666");
define("METHOD", "aes-128-cbc");


function waf($value){
    $filter = "union|and|updatexml|where|like|left| |,|\x09|\x0a|\x0d|\x0b|\x0c|\xa0|--|\*|\\|or|right|regexp|benchmark|join|sleep|where|=|<|>|sub";
    if (preg_match("/".$filter."/is",$value)==1){   
        print "Waf by HumenSec";
        exit();
    }
}
