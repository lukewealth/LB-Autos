# Lady Benz Automechanic Ltd — Web App

Static marketing site for Lady Benz Automechanic Ltd (Mercedes-Benz service & training, Lagos, Nigeria).

## Contact (canonical)

- **Address**: Opposite Eko Akete, Lekki Epe Expressway, Awoyaya, Lagos, Nigeria.
- **Telephone**: 08035516634, 09078966026
- **Email**: ladybenzautomechnic@gmail.com
- **Website**: https://www.ladybenzautomechanic.com

These values are hard-coded in every page. If you change one, search the
repo and update all occurrences:

```bash
grep -r "08035516634\|ladybenzautomechnic@gmail.com\|Eko Akete" *.html
```

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Home (hero, services, impact, FAQ) |
| `about.html` | About the company |
| `service.html` | Services list |
| `booking.html` | Booking form (POSTs to `send-booking.php`) |
| `contact.html` | Contact form (POSTs to `send-contact.php`) |
| `team.html` | Meet-the-team CTA |
| `testimonial.html` | Customer testimonials |
| `training.html` | Training programmes |
| `404.html` | Not-found page |

## Backend

The booking and contact forms POST JSON-compatible form data to two PHP
scripts that email the admin Gmail inbox (`ladybenzautomechnic@gmail.com`).

| Script | Form | Method |
|--------|------|--------|
| `send-booking.php` | `booking.html` | `POST` (expects `name, email, phone, service, preferred_date, preferred_time, message`) |
| `send-contact.php` | `contact.html` | `POST` (expects `name, email, subject, message`) |

Both scripts:

- Validate all fields server-side.
- Reject bots via a hidden `website` honeypot field.
- Try to send via **PHPMailer SMTP** to `smtp.gmail.com:587` first.
- Fall back to PHP's `mail()` if PHPMailer is not installed.
- Return JSON: `{ "success": bool, "message": string }`.

### Recommended SMTP setup (production)

1. Create a Google **App Password** for `ladybenzautomechnic@gmail.com`
   (https://myaccount.google.com/apppasswords).
2. Install Composer and PHPMailer on the server:

   ```bash
   composer require phpmailer/phpmailer
   ```

3. Set the app password as an environment variable (never commit it):

   ```bash
   export LB_GMAIL_APP_PASSWORD='your-16-char-app-password'
   ```

4. Confirm the form works by submitting a test booking; the admin
   should receive an email at `ladybenzautomechnic@gmail.com`.

### Local development

If you don't have PHPMailer installed, the scripts still work via
`mail()` (which on most local dev environments is wired to a logging
mailer — submissions will be appended to the mail log instead of being
delivered).
