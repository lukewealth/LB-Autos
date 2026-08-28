// api/contact.js — Vercel Serverless Function
// Handles POST submissions from the contact form on contact.html.
// Validates input, anti-spam honeypot, and emails the admin.

const { sendMail, bad, ok, readBody, clientMeta } = require('./_mailer');

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return bad(res, 405, 'Method not allowed.');
    }

    const body = readBody(req);

    // Honeypot
    if (body.website) {
        return ok(res, 'Thanks! Your message has been received.');
    }

    const name    = String(body.name    || '').trim();
    const email   = String(body.email   || '').trim();
    const subject = String(body.subject || '').trim();
    const message = String(body.message || '').trim();

    const errors = [];
    if (name.length < 2)                                    errors.push('Please enter your full name.');
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email))         errors.push('Please enter a valid email address.');
    if (subject.length < 3)                                 errors.push('Please enter a subject.');
    if (message.length < 10)                                errors.push('Please enter a message of at least 10 characters.');

    if (errors.length) return bad(res, 422, errors.join(' '));

    const { ip, userAgent, timestamp } = clientMeta(req);

    const text =
        `You received a new contact form submission from the Lady Benz Automechanic website.\r\n\r\n` +
        `Name:    ${name}\r\n` +
        `Email:   ${email}\r\n` +
        `Subject: ${subject}\r\n\r\n` +
        `Message:\r\n----------------------------------------\r\n` +
        `${message}\r\n----------------------------------------\r\n\r\n` +
        `Sent:    ${timestamp}\r\n` +
        `IP:      ${ip}\r\n` +
        `Browser: ${userAgent}\r\n`;

    try {
        await sendMail({
            subject: `New contact message: ${subject}`,
            body: text,
            replyTo: `${name} <${email}>`,
        });
        return ok(res, 'Thank you! Your message has been sent. We will get back to you within 24 hours.');
    } catch (err) {
        console.error('contact sendMail failed:', err);
        return bad(res, 500, 'We could not send your message right now. Please call 08035516634 or 09078966026 to reach us directly.');
    }
};
