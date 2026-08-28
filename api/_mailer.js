// api/_mailer.js — shared SMTP helper for Vercel Serverless Functions
// Uses Gmail SMTP (smtp.gmail.com:587) when LB_GMAIL_APP_PASSWORD is set,
// otherwise falls back to nodemailer's JSON transport (logs the email to
// the function logs so the form still works during local development).

const nodemailer = require('nodemailer');

const ADMIN_EMAIL = 'ladybenzautomechnic@gmail.com';
const FROM_EMAIL  = 'noreply@ladybenzautomechanic.com';
const SITE_NAME   = 'Lady Benz Automechanic Ltd';
const SITE_URL    = 'https://www.ladybenzautomechanic.com';

let cachedTransport = null;

function getTransport() {
    if (cachedTransport) return cachedTransport;

    const user = process.env.LB_GMAIL_USER     || ADMIN_EMAIL;
    const pass = process.env.LB_GMAIL_APP_PASSWORD;

    if (pass) {
        cachedTransport = nodemailer.createTransport({
            host: 'smtp.gmail.com',
            port: 587,
            secure: false, // STARTTLS
            auth: { user, pass },
        });
    } else {
        // Dev fallback — log to stdout
        cachedTransport = nodemailer.createTransport({ jsonTransport: true });
    }
    return cachedTransport;
}

async function sendMail({ subject, body, replyTo }) {
    const transport = getTransport();
    return transport.sendMail({
        from:    `"${SITE_NAME}" <${FROM_EMAIL}>`,
        to:      ADMIN_EMAIL,
        replyTo: replyTo || undefined,
        subject: `[${SITE_NAME}] ${subject}`,
        text:    body,
    });
}

function bad(res, status, message) {
    res.status(status).json({ success: false, message });
}

function ok(res, message, extra = {}) {
    res.status(200).json({ success: true, message, ...extra });
}

// Trim + collect form fields from either JSON or FormData body
function readBody(req) {
    if (!req.body) return {};
    if (typeof req.body === 'string') {
        try { return JSON.parse(req.body); } catch { return {}; }
    }
    return req.body;
}

function clientMeta(req) {
    return {
        ip:        (req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').toString().split(',')[0].trim(),
        userAgent: req.headers['user-agent'] || 'unknown',
        timestamp: new Date().toISOString(),
    };
}

module.exports = {
    ADMIN_EMAIL,
    FROM_EMAIL,
    SITE_NAME,
    SITE_URL,
    sendMail,
    bad,
    ok,
    readBody,
    clientMeta,
};
