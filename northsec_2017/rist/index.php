<html>
<style>
body {
background-color:red;
color:yellow;
font-family: Courier;
}

#list {
border-style: solid;
border-color:yellow;
color:yellow;
border-radius: 25px;
width:60%;
}
</style>
<title>Rao Institute of technology</title>
<body>
<h1>Welcome to RAO's Institute of Standards and Technologies (RIST)</h1>
<div id='list'>



<?php
//this challenge is a hommage to a challenge made by : f50ddbee36051c48d09d9ba4b0932c7e216731aa

error_reporting(E_ALL);
ini_set('display_errors', 1);


//random 4 byte key, in accordance to RIST standard on cryptography
$key='CENSORED';

$servername = "localhost";
$username = "CENSORED";
$password = "CENSORED";
$dbname = "rist";


if (isset($_GET['raofc'])) {

try{
$f = openssl_decrypt($_GET['raofc'],'AES-256-ECB',$key);
$s = explode('|',$f);
$sql = 'select file from path where id=' . $s[0] . ' and clearance="' . $s[1] .'"';

$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$result = $conn->query($sql);
$RAOfc  = $result->fetch_assoc();


// TODO SELECT PATH

?> <plaintext><?php
include($RAOfc['file']);
?></plaintext> <?php




if  (($s[1] === 'Admin')) {
echo 'flag';

};

} catch (Exception $e) {
    echo 'Caught exception: ',  $e->getMessage(), "\n";
}



} else {


?>
<ul>
<li><a href='?raofc=<?php echo urlencode(openssl_encrypt('CENSORED','AES-256-ECB',$key)); ?>'> RaoFC about Key Entropy Requirements </a></li>
<li><a href='?raofc=<?php echo urlencode(openssl_encrypt('CENSORED','AES-256-ECB',$key)); ?>'> RaoFC about Key Management Requirements </a></li>
<li><a href='?raofc=<?php echo urlencode(openssl_encrypt('CENSORED','AES-256-ECB',$key)); ?>'> RaoFc on RaoFc </a></li>
<li><a href='?raofc=<?php echo urlencode(openssl_encrypt('CENSORED','AES-256-ECB',$key)); ?>'> RaoFC on Hashing Requirements </a></li>
</ul>
</div>



<?php
} ?>
