<?php 
include_once('../sys/config.php');

if (isset($_SESSION['admin']) && $_SESSION['admin'] == 233) {
	include_once('../header.php');

?>
<div class="span10">
	<div id="content">
		<div class="page-header">
			<h4>进程监控系统</h4>
			<hr>
			<form name="ping" action="" method="post">
				<p>输入需要检测的服务</p>
				<input type="text" name="target" size="30" class="form-control">
				<input type="submit" value="submit" name="submit" class="btn btn-primary">
			</form>
			<?php

				function hwaf($value){
				    $filter = "<|>|php|0x|\\|python|gcc|less|root|etc|pass|http|ftp|cd|bash|[\w\d]+\.[\w\d]+|tcp|udp|cat|×|fl|ag|flag|ph|hp|wget";

				    if (preg_match("/".$filter."/is",$value)==1){  
				        exit('Waf by HumenSec');
				    }
				}

				if( isset( $_POST[ 'submit' ] ) ) {
					$cmd = $_POST['target'];
					hwaf($cmd);
					exec('ps -ax | grep '.$cmd, $result);
					foreach($result as $k){
						if(strpos($k, $cmd)){
							echo "<br /><pre>$cmd\r\n".$k."</pre>";
						}
					}
				}
			?>
		</div>
	</div>
</div>


<a href="manage.php">返回</a>
	<?php 
	require_once('../footer.php');
}else if ($_SESSION['admin'] && $_SESSION['admin'] != 233){
	var_dump("权限不足")；
}
else {
	not_find($_SERVER['PHP_SELF']);
}
 ?>
