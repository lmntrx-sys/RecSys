<?php
$servename = "localhost";
$username = "root";
$password = "";
$dbname = "simple_post_db";

// Create connection
$conn = new mysqli($servename, $username, $password, $dbname);

// Check connection
if ($conn->connect_error){
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT p.content, p.created_at, u.usernameFROM posts p JOIN users u ON p.user_id = u.id ORDER BY p.created_at DESC";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row  
    while($row = $result->fetch_assoc()) {
        echo  "<div class='post'><strong>".$row['username']. "</strong>:" . $row['content'] . "<br><small>" . $row['created_at'] . "</small></div>";
    }
} else {
    echo "No posts found";
}

$conn->close();
?>