<?php
$servername = "localhost";
$username = "root";
$password = ""; 
$dbname = "simple_post_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $postText = $_POST['postText'];
    $user_id = 1; // Assuming a logged in user with id 1

    $sql = "INSERT INTO posts (user_id, content) VALUES ('$user_id', '$postText')";

    if ($conn->query($sql) === TRUE) {
        echo "New post created successfully!";
        header("Location: index.html"); // Redirect to home page
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>
