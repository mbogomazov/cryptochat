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
    //it's dangerous because of SQL injection
    $q = mysql_query("SELECT session_key FROM users WHERE id='".$user_id."'");
    $msg = "";
	if(mysql_num_rows($q) != 0){
		$resp = mysql_fetch_array($q);
        //if sent key equals key on server
		if ($resp[0] == $user_key){
            while(true){
                $q = mysql_query("SELECT msg FROM chats WHERE chat_id='".$chat_id."'");
                $resp = mysql_fetch_array($q);
                if((count($resp) != 0) and ($resp[0] !="" )){
                    $msg = $resp[0];
                    $resp = array("getting_msg"=>"successfull","msg"=>$msg);
	    	        echo(encrypt($resp));
                    break;
                } 
                    else{
                        sleep(1);
                        continue;
                    }

            }
         
        }
            else{
                $resp = array("getting_msg"=>"failed","reason"=>"invalid session key");
				echo(encrypt($resp));
            }
    }
}
?>
