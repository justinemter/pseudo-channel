<?php
header("HTTP/1.1 200 OK");

if (isset($_GET['command'])) {
    echo $_GET['command'];
    $command = $_GET['command'];
} else {
    // Fallback behaviour goes here
}

$old_path = getcwd();
chdir('/home/justin/channels/');

if ($command == "KEY_PLAY"){
	$output = shell_exec('./manual.sh 01');
} else if ($command == "KEY_STOP"){
	$output = shell_exec('./stop-all-channels.sh');
} else if ($command == "KEY_CHANNELUP"){
	$output = shell_exec('./channelup.sh');
} else if ($command == "KEY_CHANNELDOWN"){
	$output = shell_exec('./channeldown.sh');
} else if ($command == "KEY_1"){
	$output = shell_exec('./manual.sh 01');
} else if ($command == "KEY_2"){
	$output = shell_exec('./manual.sh 02');
} else if ($command == "KEY_3"){
	$output = shell_exec('./manual.sh 03');
} else if ($command == "KEY_4"){
	$output = shell_exec('./manual.sh 04');
} else if ($command == "KEY_5"){
	$output = shell_exec('./manual.sh 05');
} else if ($command == "KEY_6"){
	$output = shell_exec('./manual.sh 06');
} else if ($command == "KEY_7"){
	$output = shell_exec('./manual.sh 07');
} else if ($command == "KEY_8"){
	$output = shell_exec('./manual.sh 08');
} else if ($command == "KEY_9"){
	$output = shell_exec('./manual.sh 09');
} else {
	//$output = shell_exec('./manual.sh 01');
}

chdir($old_path);

echo "<pre>$output</pre>";

?>

