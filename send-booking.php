<?php
// filepath: /Users/admin/Documents/Benz/LB-Autos/send-booking.php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name    = trim($_POST['name'] ?? '');
    $email   = trim($_POST['email'] ?? '');
    $service = trim($_POST['service'] ?? '');
    $date    = trim($_POST['date'] ?? '');
    $message = trim($_POST['message'] ?? '');

    if ($name && $email && $service && $date && $message) {
        $to = 'ladybenzautomechnic@gmail.com';
        $subject = "New Booking Request from $name";
        $body = "Name: $name\nEmail: $email\nService: $service\nDate: $date\nMessage:\n$message";
        $headers = "From: $email\r\nReply-To: $email\r\n";

        if (mail($to, $subject, $body, $headers)) {
            echo json_encode(['success' => true]);
            exit;
        }
    }
    echo json_encode(['success' => false]);
    exit;
}
echo json_encode(['success' => false]);