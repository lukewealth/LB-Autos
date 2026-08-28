<?php
/**
 * Lady Benz Automechanic — Newsletter subscription handler
 * Sends the new subscriber's email to the admin Gmail inbox.
 *
 * POST fields:
 *   newsletter_email, website (honeypot, must be empty)
 *
 * Response: JSON { success: bool, message: string }
 */

declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
    exit;
}

if (!empty($_POST['website'] ?? '')) {
    echo json_encode(['success' => true, 'message' => 'Thanks for subscribing!']);
    exit;
}

$email = trim((string)($_POST['newsletter_email'] ?? ''));
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['success' => false, 'message' => 'Please enter a valid email address.']);
    exit;
}

$adminEmail = 'ladybenzautomechnic@gmail.com';
$siteName   = 'Lady Benz Automechanic Ltd';
$ip         = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$timestamp  = date('Y-m-d H:i:s T');

$emailSubject = sprintf('[%s] New newsletter subscriber', $siteName);

$body  = "A new visitor subscribed to the $siteName newsletter.\r\n\r\n";
$body .= "Email:  $email\r\n";
$body .= "Sent:   $timestamp\r\n";
$body .= "IP:     $ip\r\n";

$headers  = "From: $siteName <noreply@ladybenzautomechanic.com>\r\n";
$headers .= "Reply-To: $siteName <$adminEmail>\r\n";
$headers .= "X-Mailer: PHP/" . PHP_VERSION . "\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$sent = false;
$composerAutoload = __DIR__ . '/vendor/autoload.php';
if (is_file($composerAutoload)) {
    require_once $composerAutoload;
    if (class_exists('\\PHPMailer\\PHPMailer\\PHPMailer')) {
        try {
            $mail = new \PHPMailer\PHPMailer\PHPMailer(true);
            $mail->isSMTP();
            $mail->Host       = 'smtp.gmail.com';
            $mail->SMTPAuth   = true;
            $mail->Username   = 'ladybenzautomechnic@gmail.com';
            $mail->Password   = getenv('LB_GMAIL_APP_PASSWORD') ?: '';
            $mail->SMTPSecure = \PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS;
            $mail->Port       = 587;
            $mail->CharSet    = 'UTF-8';

            $mail->setFrom('noreply@ladybenzautomechanic.com', $siteName);
            $mail->addAddress($adminEmail, $siteName);
            $mail->Subject = $emailSubject;
            $mail->Body    = $body;
            $sent = $mail->send();
        } catch (\Throwable $e) {
            error_log('[send-newsletter.php] PHPMailer failed: ' . $e->getMessage());
            $sent = false;
        }
    }
}

if (!$sent) {
    $sent = @mail($adminEmail, $emailSubject, $body, $headers);
}

if ($sent) {
    echo json_encode(['success' => true, 'message' => 'Thanks for subscribing! We will keep you posted.']);
    exit;
}

http_response_code(500);
echo json_encode(['success' => false, 'message' => 'We could not complete your subscription right now. Please try again later.']);
