<?php
	header('Content-Type: application/json');
	header('Access-Control-Allow-Origin: *');

	require 'auth.php';
	require_auth();

    $fn = str_replace("/","",$_SERVER['QUERY_STRING']);

    switch ($fn) {
        case 'file_list':
            $fn = 'python file_list.py';
            $command = escapeshellcmd($fn);
            $output = shell_exec($command);
            echo $output;
            break;
        case 'file_store':
          if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $fn = 'bash file_store.sh';
            $output = shell_exec($fn);
            echo $output;
          } else {
            header("HTTP/1.0 405 Method Not Allowed");
          }
          break;
        case 'file_clear':
          if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $fn = 'bash file_clear.sh';
            $output = shell_exec($fn);
            echo $output;
          } else {
            header("HTTP/1.0 405 Method Not Allowed");
          }
          break;
        case 'cpu_load':
            $fn = 'python cpu_load.py';
            $command = escapeshellcmd($fn);
            $output = shell_exec($command);
            echo $output;
            break;
        case 'commands':
			$fn = "ssh -i /volume2/web/api/id_rsa root@scn arp -a 2>&1";
			//$fn = "chmod 600 id_rsa 2>&1";
            $output = shell_exec($fn);
            echo $output;
            break;
        default:
            header("HTTP/1.0 404 Not Found");
            break;
    }

?>