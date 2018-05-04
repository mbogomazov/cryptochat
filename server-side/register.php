<?php
$login="";
$passwd="";
$dbname="";
$dbhost="";
header("Access-Control-Allow-Origin: *");
$link = mysql_connect($dbhost, $login, $passwd ) or die("connection error");
mysql_select_db($dbname,$link) or die("connection error");

function decrypt($data)
{
	return json_decode(base64_decode($data), true);
}

function encrypt($data)
{
	return base64_encode(json_encode($data, JSON_UNESCAPED_UNICODE));
}

function session_key_gen()
{
	return base64_encode(md5((string)rand(-9999999,9999999)));
}

#start mainloop
if(isset($_POST['data']))
{
	if($_POST['data'] == "")
			echo('ERROR');
		else
			$data = $_POST['data'];
}
	else
		echo('ERROR');	
if(isset($data))
{
	$user_data=decrypt($data);
	$q = mysql_query("SELECT * FROM users WHERE id='".$user_data["id"]."'");
	if(mysql_num_rows($q) == 0)
    {
    	$session_key = session_key_gen();
	    $q = mysql_query("INSERT INTO users (id,session_key) VALUES('".$user_data["id"]."','".$session_key."')");
		if($q == 1)
        {
			$resp = array("registration"=>"complete", "session_key"=>$session_key);
			echo(encrypt($resp));
		}
	}
		else
        {
			$resp = array("registration"=>"fails", "reason"=>"this user already exists");
			echo(encrypt($resp));
	    }
	
	
}
?>
