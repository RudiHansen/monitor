<html> 
<body> 
<?php
$logtype = $_GET["logtype"];
$logtext = $_GET["logtext"];
$date = date('Y/m/d H:i:s', time());
$logoutput = $date . " - " . $logtext;

if($logtype || $logtext)
{
    // Create connection
    $conn = new mysqli("localhost", "webLog", "", "webLogSql");

    // Check connection
    if ($conn->connect_error) 
    {
        die("Connection failed: " . $conn->connect_error);
    } 

    $sql = "INSERT INTO WebLogTable (LogDate, LogType, LogText) VALUES ('$date', '$logtype', '$logtext')";

    if ($conn->query($sql) === TRUE) 
    {
        echo "New record created successfully";
    } 
    else 
    {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    $conn->close();
}
?>
</body>
</html>