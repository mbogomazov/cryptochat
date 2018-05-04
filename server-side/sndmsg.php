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
    $msg = decrypt($data)["msg"];
    $msg_id = decrypt($data)["msg_id"];
	$q = mysql_query("SELECT session_key FROM users WHERE id='".$user_id."'");
	if(mysql_num_rows($q) != 0)
    {
		$resp=mysql_fetch_array($q);
        //if sent key equals key on server
		if ($resp[0] == $user_key)
        {
            //not safe
            $q = mysql_query("SELECT * FROM chats WHERE chat_id='".$chat_id."'");
            $resp = mysql_fetch_array($q);
            if(!$resp){
                $q = mysql_query("INSERT INTO chats (chat_id,msg) VALUES('".$chat_id."','".$msg."')");
                if($q == 1)
                {
                    $resp = array("send"=>"successfull","msg_id"=>$msg_id);
	    			echo(encrypt($resp));
                }
                    else
                    {
                        $resp = array("send"=>"failed","reason"=>"can't accept MySQL query");
                        echo(encrypt($resp));
                    }
            }
                else
                {
                    $q = mysql_query("SELECT msg FROM chats WHERE chat_id='".$chat_id."'");
                    $resp = mysql_fetch_array($q)[0];
                    $msg = $resp.$msg;
                    $q = mysql_query("UPDATE chats SET msg='".$msg."' WHERE chat_id='".$chat_id."'");
                    if($q == 1)
                    {
                        $resp = array("send"=>"successfull","msg_id"=>$msg_id);
	    		    	echo(encrypt($resp));
                    }
                        else
                        {
                            $resp = array("send"=>"failed","reason"=>"can't accept MySQL query");
                            echo(encrypt($resp));
                        }


                }

				
		}
			else
            {
				$resp=array("creating_chat"=>"failed","reason"=>"invalid session key");
				echo(encrypt($resp));
			}
	}
	else
    {
		echo(encrypt('ERROR: no user with this ID'));
	}
}
?>
