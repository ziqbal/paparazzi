
<?php


//print_r($_GET);
//print_r($_FILES);

$filedata = $_FILES["file"];

/*
print_r($filedata);

Array
(
    [name] => f-127-000001-1485964439496.jpg
    [type] => 
    [tmp_name] => /Applications/XAMPP/xamppfiles/temp/php3rJa54
    [error] => 0
    [size] => 285718
)
*/


if($filedata["error"]!=0){
	exit;
}


move_uploaded_file($filedata["tmp_name"],"../../../_cache_/".$filedata["name"]);

print(md5_file("../../../_cache_/".$filedata["name"]));
?>