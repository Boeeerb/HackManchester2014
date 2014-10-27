<?php

ini_set('display_errors',1);
require 'class-Clockwork.php';


$get = print_r($_GET,true);
file_put_contents("test.txt",$get);

$keyword = $_GET['keyword'];
$content = $_GET['content'];
$sender = $_GET['from'];

$message = explode(" ",strtolower($content));
$requested = strtolower($message[0]);

if ($_GET["test"] != 1 ) { } else {
        echo "Test<br>";
}


$pnglist = file_get_contents("pngs.txt");
$pnglist = explode("<br />",nl2br($pnglist));

$x = 0;
// Convert array to keys
while ( $x < count($pnglist) ) {
    $list[trim($pnglist[$x])] = 1;
    $x++;
}



if ( $requested == "draw" ) {
    if ( $message[1] == "" ) {
        txt_message("Let me know which pixel (between 0 and 63) and the hex colour you would like.");
    } else {
        $pixel = $message[1];
        if ( 0 <= $pixel && $pixel <= 63 ) {
            $hex = $message[2];
            list($r, $g, $b) = sscanf($hex, "%02x%02x%02x");
            txt_message("Your pixel has been drawn");
            file_put_contents("word.txt","0 ".$pixel." ".$r." ".$g." ".$b);
        } else {
            txt_message("Your pixel should be between 0 and 63");
        }
    }
   
} else if ( $requested == "clear" ) {
    txt_message("Palette has been cleared.");
    file_put_contents("word.txt","clear");
    
} else {

    if ( $list[$requested] == 1 ) {
        print "All ok";
        file_put_contents("word.txt",$requested);
        txt_message("Thank you, drawing has been changed");
    } else {
        print "Failed";
        txt_message("Sorry, word not known. List of known words is available at http://boeeerb.co.uk/hm/");
    }
}




function txt_message($Message) {
    $API_KEY = "CLOCKWORKAPIKEY";
    $clockwork = new Clockwork( $API_KEY );
    $passmessage = array( 'to' => $sender, 'message' => $Message );
    echo $Message;
    if ($_GET["test"] != 1 ) {
        $result = $clockwork->send( $passmessage );
    }
}

?>