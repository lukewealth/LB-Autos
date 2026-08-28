<?php
/**
 * Lady Benz Automechanic — Contact form handler
 * Sends submissions to the admin Gmail inbox via PHPMailer (SMTP) when
 * available, falling back to PHP mail() if PHPMailer is not installed.
 *
 * POST fields:
 *   name, email, subject, message, website (honeypot, must be empty)
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

// --- Honeypot anti-spam ---------------------------------------------------
if (!empty($_POST['website'] ?? '')) {
    // Silently succeed so bots don't retry, but no email is sent.
    echo json_encode(['success' => true, 'message' => 'Thanks! Your message has been received.']);
    exit;
}

// --- Read & validate inputs ----------------------------------------------
$name    = trim((string)($_POST['name']    ?? ''));
$email   = trim((string)($_POST['email']   ?? ''));
$subject = trim((string)($_POST['subject'] ?? ''));
$message = trim((string)($_POST['message'] ?? ''));

$errors = [];
if ($name === '' || mb_strlen($name) < 2)            $errors[] = 'Please enter your full name.';
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
if ($subject === '' || mb_strlen($subject) < 3)       $errors[] = 'Please enter a subject.';
if ($message === '' || mb_strlen($message) < 10)     $errors[] = 'Please enter a message of at least 10 characters.';

if (!empty($errors)) {
    http_response_code(422);
    echo json_encode(['success' => false, 'message' => implode(' ', $errors)]);
    exit;
}

// --- Compose email --------------------------------------------------------
$adminEmail = 'ladybenzautomechnic@gmail.com';
$siteName   = 'Lady Benz Automechanic Ltd';
$siteUrl    = 'https://www.ladybenzautomechanic.com';
$ip         = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$ua         = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
$timestamp  = date('Y-m-d H:i:s T');

$emailSubject = sprintf('[%s] New contact message: %s', $siteName, $subject);

$body  = "You received a new contact form submission from the $siteName website.\r\n\r\n";
$body .= "Name:    $name\r\n";
$body .= "Email:   $email\r\n";
$body .= "Subject: $subject\r\n\r\n";
$body .= "Message:\r\n----------------------------------------\r\n";
$body .= "$message\r\n----------------------------------------\r\n\r\n";
$body .= "Sent:    $timestamp\r\n";
$body .= "IP:      $ip\r\n";
$body .= "Browser: $ua\r\n";
$body .= "Page:    $siteUrl/contact.html\r\n";

$altBody = "New contact message from $name <$email>\nSubject: $subject\n\n$message\n\nSent $timestamp from $ip";

$headers  = "From: $siteName <noreply@ladybenzautomechanic.com>\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "X-Mailer: PHP/" . PHP_VERSION . "\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

// --- Try PHPMailer via Composer first ------------------------------------
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
            // Use a Google App Password here (NOT the account password).
            // Set in environment so the source code never contains the secret.
            $mail->Password   = getenv('LB_GMAIL_APP_PASSWORD') ?: '';
            $mail->SMTPSecure = \PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS;
            $mail->Port       = 587;
            $mail->CharSet    = 'UTF-8';

            $mail->setFrom('noreply@ladybenzautomechanic.com', $siteName);
            $mail->addAddress($adminEmail, $siteName);
            $mail->addReplyTo($email, $name);

            $mail->Subject = $emailSubject;
            $mail->Body    = $body;
            $mail->AltBody = $altBody;

            $sent = $mail->send();
        } catch (\Throwable $e) {
            error_log('[send-contact.php] PHPMailer failed: ' . $e->getMessage());
            $sent = false;
        }
    }
}

// --- Fall back to PHP mail() ---------------------------------------------
if (!$sent) {
    $sent = @mail($adminEmail, $emailSubject, $body, $headers);
}

if ($sent) {
    echo json_encode([
        'success' => true,
        'message' => 'Thank you! Your message has been sent. We will get back to you within 24 hours.',
    ]);
    exit;
}

http_response_code(500);
echo json_encode([
    'success' => false,
    'message' => 'We could not send your message right now. Please call 08035516634 or 09078966026 to reach us directly.',
]);
