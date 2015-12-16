<?php

$name = $_POST['name'];
$memo = $_POST['memo'];
$date1 = $_POST['date1'];
$date2 = $_POST['date2'];
$date3 = $_POST['date3'];
$id = $_POST['id'];

// 文字列を置換する
$name = trim($name);
$memo = str_replace(array("\r\n","\r","\n"), '<br>', $memo);
$memo = str_replace('\t', '', $memo);
$memo = trim($memo);

// ファイルの名前
$filename = "./data/" . $id . ".txt";

// ファイルの存在確認
if( !file_exists($filename) ){
	// ファイル作成
	touch( $filename );
}else{
	// すでにファイルが存在する為エラーとする
	exit();
}

$handle = fopen( $filename, 'a' );
fwrite( $handle, $name . "\n" );
fwrite( $handle, $memo . "\n" );
fwrite( $handle, $date1 . "\t" . $date2 . "\t" . $date3 . "\n" );
fclose($handle);


// Content-TypeをJSONに指定する
header('Content-Type: application/json');

// 「200 OK」 で {"data":"24歳、学生です"} のように返す

$uri = (empty($_SERVER["HTTPS"]) ? "http://" : "https://") . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"];
$url = substr($uri, 0, strrpos($uri, "/")) . "/detail.cgi?id=" . $id;

$data1 = "<a href=\"" . $url . "\" class=\"alert-link\" target=\"_blank\">" . $url . "</a>";

$data2 = "<a href=\"" . $url . "\" class=\"btn btn-primary\" target=\"_blank\"><i class=\"fa fa-external-link\"></i> イベントページを表示する</a>";

echo json_encode(compact('data1','data2'));


?>
