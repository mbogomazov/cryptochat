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
	$user_key = decrypt($data)["key"];
	$user_id = decrypt($data)["id"];
	$q = mysql_query("SELECT session_key FROM users WHERE id='".$user_id."'");
	if(mysql_num_rows($q) != 0)
    {
		$resp = mysql_fetch_array($q);
		if($resp[0] == $user_key)
        {
			$new_key = session_key_gen();
			$q = mysql_query("UPDATE users SET session_key='".$new_key."' WHERE id='".$user_id."'");
			if($q == 1)
            {
				$resp = array("login"=>"confirmed","session_key"=>$new_key);
				echo(encrypt($resp));
			}
				else
                {
					echo('ERROR: can\'t send accept MySQL query');
				}
		}
			else
            {
				$resp = array("login"=>"fails","reason"=>"invalid session key");
				echo(encrypt($resp));
			}
	}
	else
    {
		echo(encrypt('ERROR: no user with this ID'));
	}
}
?>
