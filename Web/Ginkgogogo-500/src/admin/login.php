<?php
include_once('../sys/config.php');
include_once('../header.php');

if(isset($_SESSION['error_info']) && $_SESSION['error_info'] != '') {
	echo $_SESSION['error_info'];
	$_SESSION['error_info'] = '';
}
?>
<form class="bs-example form-horizontal" action="logCheck.php" method="post" name="log">
	<legend>登录</legend>
    <div class="form-group">
        <label for="inputEmail" class="col-lg-2 control-label">用户名：</label>
        <div class="col-lg-3">
            <input type="text" name="user" class="form-control" id="inputEmail">
        </div>
	</div>
	<div class="form-group">
		<label for="inputEmail" class="col-lg-2 control-label">密码：</label>
        <div class="col-lg-3">
			<input type="password" name="pass" class="form-control" id="inputEmail" onblur="check()">
        </div>
        <p>不是'a'*32,也不是'b'*64,弱口令什么的</p>
        <p>给你5个小时，爆破出来算我输</p>
    </div>	
	<div class="form-group">
		<label for="inputEmail" class="col-lg-2 control-label">驗證碼</label>
        <div class="col-lg-3">
			<input type="text" name="captcha" class="form-control" id="inputEmail" onblur="check()">
        </div>
		<div><img src="captcha.php"></div>
    </div>	
	<div class="form-group">
		<label for="inputEmail" class="col-lg-2 control-label"></label>
        <div class="col-lg-3">
			<input type="submit" name="submit" class="btn btn-primary" value="登录"/>
        </div>
    </div>				  
</form>
<?php
require_once('../footer.php');
?>
