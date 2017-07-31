## WEB300 Kick My ass 

> 首先你得作出安卓题然后才是这道题，但是安卓比较坑据说。

题目copy自ais3-final-2015  
出题初衷是综合渗透，因此就放了git泄漏
download源码以后仔细审计一遍，首先看?action=phpinfo
发现magic_quotes_on 原题是用mysql_real_escape……其实没啥区别0rz

再看登录注册
```
function dologin($username,$password){
	GLOBAL $db;
	if(empty($username)||empty($password)){
		die("<script>alert(\"Check Your Input ^..^\");</script>");
	}
	else{
		$query = "SELECT * FROM user where username='{$username}'";
		$res = $db->kick_query($query);
		
		if(mysql_num_rows($res)===0){
			die("<script>alert('User Don\'t exists!');</script>");
		}

		$rows = mysql_fetch_assoc($res);
		if($rows['password']!==$password){
			die("<script>alert(\"You Password is Wrong!\");</script>");
		}

		$query = "SELECT * FROM isadmin where username='{$username}'";
		$res = $db->kick_query($query);
		if(mysql_num_rows($res)){
			die("<script>alert(\"You cAn't Login.  XD\");</script>");
		}
		else{
			$_SESSION['username'] = $rows['username'];
			echo "<script>alert('Login Success~ have Fun!');</script>";
		}

		if ($username ==='berTrAM'){
			$_SESSION['isadmin']='True';
			//var_dump($_SESSION);
		}
	}
}

function doregister($username,$password){
	echo $username.$password;
	GLOBAL $db;
	if(empty($username)||empty($password)){
		die("<script>alert('Check Your Input ^..^');</script>");
	}
	else{
		$query = "SELECT * FROM user Where username='{$username}'";
		$res = $db->kick_query($query);
		if(mysql_num_rows($res)>0){
			die("<script>alert('Some One has Used this username');</script>");
		}
		$query = "INSERT INTO user(username,password) VALUES('{$username}','{$password}')";
		$res = $db->kick_query($query);
		$query = "INSERT INTO isadmin(username,`is`) VALUES('{$username}',0)";
		$res = $db->kick_query($query);
		echo "<script>alert(\"register Ok\");</script>";
	}
}
```
条件竞争可以利用来登录，写个py成功获取session，登录后可以用
```
function dosend($username,$header,$description){
	GLOBAL $db;
	if(empty($header)||empty($description)){
		die("<script>alert(\"Rubbish string. :(\");</script>");
	}

	if(strlen($header)>20)
		$header = substr($header,0,20);
	if(strlen($description)>255)
		$description = substr($description,0,255);
	$host = $_SERVER['REMOTE_ADDR'];
	$query = "INSERT INTO messagebox(username,header,description,host) VALUES('{$username}','{$header}','{$description}','{$host}')";
	$db->kick_query($query);
}
```
来进行盲注，但是条件
```
function safe_check($string){
	$string=filter_invisible($string); 
	if(preg_match("/insert\b|update\b|drop\b|delete\b|dumpfile\b|outfile\b|rename\b|floor\(|extractvalue|updatexml|name_const|multipoint\(/i", $string)){
        die("<script>alert(\"Be a Good Man :)\")</script>");
    }
    return $string;
}

function filter_invisible($str){
    for($i=0;$i<strlen($str);$i++){
        $ascii = ord($str[$i]);
        if($ascii>126 || $ascii < 32){ 
            if(!in_array($ascii, array(9,10,13))){
                die("<script>alert(\"param error\");</script>");
            }else{
                $str = str_replace($ascii, " ", $str);
            }
        }
    }
    return $str;
}
```
写的比较急就随手百度了，没有仔细的尝试绕过。自己的思路是时间盲注拖延时间

首先读取管理员账户和密码，这个cmd5就可以了，再然后发现如果登录管理员用户会有一个包含功能，原题是可以直接包含session，这里session规则不变因此得换一种思路

老司机都会发现phpmyadmin吧，但是发现phpmyadmin也是401那就再尝试盲注读取`/var/www/html/admin/phpmyadmin/.htaccess`

发现http basic 密码文件在 /var/www/.htpasswd2 里

然后各种姿势都可以解，而且一定可解这里提供3种常规的
- 无视读取的文件 直接burpsuite 
- join
- shell脚本

解出来12345678

phpmyadmin 发现web目录不可写，联想到前面的admin的功能，那就直接写在/tmp/下，然后包含就可以getshell了

美滋滋

