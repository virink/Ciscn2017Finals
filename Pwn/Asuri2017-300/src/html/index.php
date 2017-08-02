
<?php

if(is_uploaded_file($_FILES['upfile']['tmp_name'])){ 
	$upfile=$_FILES["upfile"];
	$name=time().'.'.$upfile["name"];//上传文件的文件名 
	
	$tmp_name=$upfile["tmp_name"];//上传文件的临时存放路径 

	move_uploaded_file($tmp_name,'upload/'.$name); 

	$error = $_FILES["upfile"]["error"];

	if($error==0){ 
		echo "upload success : upload/$name"; 
	}else{
		 echo "文件上传失败，错误信息：".$_FILES['upfile']['error']."<br>";
	} 

}

?>

<!Doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<script type="text/javascript">
 

Array.prototype.contains = function (obj) {  
    var i = this.length;  
    while (i--) {  
        if (this[i] === obj) {  
            return true;  
        }  
    }  
    return false;  
}  

function check(){
upfile = document.getElementById("upfile");
submit = document.getElementById("submit");
name = upfile.value;
ext = name.replace(/^.+\./,'');

if(['jpg','png'].contains(ext)){
	submit.disabled = false;
}else{
	submit.disabled = true;

	alert('请选择一张图片文件上传!');
}


}

</script>

</head>
<body>



<form enctype='multipart/form-data' id='aa' name='aaa' method='post' action='index.php'> 
<input  id="upfile" name='upfile' type='file' onchange="check();" /> 

<input type='submit'  id ='submit' value='上传'> 
</form> 



</body>


</html>



