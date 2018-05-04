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
    $chat_id = decrypt($data)["chat_id"];
    $hashed_msg = decrypt($data)["hashed_msgs"];
    $q = mysql_query("SELECT session_key FROM users WHERE id='".$user_id."'");
	if(mysql_num_rows($q) != 0)
    {
		$resp = mysql_fetch_array($q);
        //if sent key equals key on server
		if ($resp[0] == $user_key)
        {
            $q = mysql_query("SELECT msg FROM chats WHERE chat_id='".$chat_id."'");
            $resp = mysql_fetch_array($q);
            //echo(encrypt(implode($resp)));
            if(count($resp) != 0)
            {
                $own_hashed=md5($resp[0]);
                if ($own_hashed==$hashed_msg)
                {
                    $empty = '';
                    $q = mysql_query("UPDATE chats SET msg='".$empty."' WHERE chat_id='".$chat_id."'");
                    if($q == 1)
                    {
                        $resp = array("accepting"=>"successfull");
        		        echo(encrypt($resp));
                    }
                }
            }
        }
    }
}
?>
