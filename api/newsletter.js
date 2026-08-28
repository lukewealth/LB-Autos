// api/newsletter.js — Vercel Serverless Function
// Handles POST from the newsletter form (footer / training.html).
// Honeypot anti-spam, validates email, subscribes admin to a mailing list
// (simulated with an admin email notification; swap in Mailchimp/ConvertKit
// by adding their SDK and API key).

const { ADMIN_EMAIL, sendMail, bad, ok, readBody, clientMeta } = require('./_mailer');

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return bad(res, 405, 'Method not allowed.');
    }

    const body = readBody(req);

    // Honeypot
    if (body.website) {
        return ok(res, 'You have been subscribed!');
    }

    const email = String(body.email || '').trim().toLowerCase();

    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        return bad(res, 422, 'Please enter a valid email address.');
    }

    const { ip, userAgent, timestamp } = clientMeta(req);

    const adminBody =
        `New newsletter subscription\r\n` +
        `=============================\r\n\r\n` +
        `Email:   ${email}\r\n` +
        `IP:      ${ip}\r\n` +
        `Time:    ${timestamp}\r\n` +
        `UA:      ${userAgent}\r\n\r\n` +
        `Action required: Add ${email} to your email marketing platform (Mailchimp, ConvertKit, etc.) if not already added.\r\n`;

    try {
        await sendMail({
            subject: `New subscriber: ${email}`,
            body: adminBody,
        });
        return ok(res, 'You have been subscribed! Expect updates on Mercedes-Benz tips, training programmes and more.');
    } catch (err) {
        console.error('newsletter sendMail failed:', err);
        return bad(res, 500, 'Subscription failed. Please try again later.');
    }
};
