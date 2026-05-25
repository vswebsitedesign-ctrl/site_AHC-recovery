<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }
$name    = htmlspecialchars(strip_tags($_POST['name'] ?? ''));
$email   = filter_var($_POST['email'] ?? '', FILTER_SANITIZE_EMAIL);
$message = htmlspecialchars(strip_tags($_POST['message'] ?? ''));
$phone   = htmlspecialchars(strip_tags($_POST['phone'] ?? ''));
if (!$email || !$message) { http_response_code(400); echo json_encode(['error' => 'Missing fields']); exit; }
$to      = 'info@ahchouseclearances.co.uk';
$subject = 'New Enquiry from Cornwall Auction House Clearances';
$body    = "Name: $name\nEmail: $email\nPhone: $phone\nMessage:\n$message";
$headers = "From: noreply@cornwallauctionhouseclearance.co.uk\r\nReply-To: $email";
if (mail($to, $subject, $body, $headers)) {
    echo json_encode(['success' => true]);
} else {
    http_response_code(500);
    echo json_encode(['error' => 'Mail failed']);
}
