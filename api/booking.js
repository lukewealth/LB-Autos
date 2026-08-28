// api/booking.js — Vercel Serverless Function
// Handles POST submissions from the booking form on booking.html.
// Validates input, anti-spam honeypot, and emails the admin.

const { sendMail, bad, ok, readBody, clientMeta } = require('./_mailer');

const SERVICES = [
    'Routine Maintenance',
    'Engine Diagnostics & Repair',
    'Transmission Service',
    'Brake System Service',
    'Electrical & Electronics',
    'AC / Climate Control',
    'Suspension & Steering',
    'Body & Paintwork',
    'Pre-Purchase Inspection',
    'Other',
];

const VEHICLE_BRANDS = [
    'Mercedes-Benz',
    'BMW',
    'Audi',
    'Volkswagen',
    'Toyota',
    'Honda',
    'Ford',
    'Hyundai',
    'Kia',
    'Other',
];

const TIMES = [
    '08:00 – 10:00',
    '10:00 – 12:00',
    '12:00 – 14:00',
    '14:00 – 16:00',
    '16:00 – 18:00',
];

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return bad(res, 405, 'Method not allowed.');
    }

    const body = readBody(req);

    // Honeypot
    if (body.website) {
        return ok(res, 'Your booking request has been received!');
    }

    const name        = String(body.name        || '').trim();
    const phone       = String(body.phone       || '').trim();
    const email      = String(body.email       || '').trim();
    const brand       = String(body.vehicle_brand || '').trim();
    const model       = String(body.vehicle_model || '').trim();
    const year        = String(body.year        || '').trim();
    const serviceType = String(body.service_type || '').trim();
    const preferredDate = String(body.preferred_date || '').trim();
    const preferredTime = String(body.preferred_time || '').trim();
    const notes       = String(body.notes       || '').trim();

    const errors = [];
    if (name.length < 2)                                      errors.push('Please enter your full name.');
    if (!/^[\d\s\+\-\(\)]{7,20}$/.test(phone))               errors.push('Please enter a valid phone number.');
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email))          errors.push('Please enter a valid email address.');
    if (!VEHICLE_BRANDS.includes(brand))                       errors.push('Please select a valid vehicle brand.');
    if (model.length < 2)                                      errors.push('Please enter your vehicle model.');
    if (!/^\d{4}$/.test(year) || year < 1980 || year > 2030) errors.push('Please enter a valid model year (1980–2030).');
    if (!SERVICES.includes(serviceType))                       errors.push('Please select a valid service type.');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(preferredDate))          errors.push('Please select a valid preferred date.');
    if (!TIMES.includes(preferredTime))                       errors.push('Please select a preferred time slot.');

    if (errors.length) return bad(res, 422, errors.join(' '));

    const { ip, userAgent, timestamp } = clientMeta(req);

    const text =
        `NEW BOOKING REQUEST\r\n` +
        `==================\r\n\r\n` +
        `Customer Name:     ${name}\r\n` +
        `Phone:             ${phone}\r\n` +
        `Email:             ${email}\r\n\r\n` +
        `Vehicle Brand:     ${brand}\r\n` +
        `Vehicle Model:     ${model}\r\n` +
        `Model Year:        ${year}\r\n\r\n` +
        `Service Type:      ${serviceType}\r\n` +
        `Preferred Date:    ${preferredDate}\r\n` +
        `Preferred Time:    ${preferredTime}\r\n\r\n` +
        `Additional Notes:\r\n----------------------------------------\r\n` +
        `${notes || '(none)'}\r\n----------------------------------------\r\n\r\n` +
        `Submitted:  ${timestamp}\r\n` +
        `IP:         ${ip}\r\n` +
        `User-Agent: ${userAgent}\r\n`;

    try {
        await sendMail({
            subject: `Booking request: ${name} — ${serviceType} on ${preferredDate}`,
            body: text,
            replyTo: `${name} <${email}>`,
        });
        return ok(res, `Your booking request for ${preferredDate} has been received! We will confirm your appointment within 24 hours.`);
    } catch (err) {
        console.error('booking sendMail failed:', err);
        return bad(res, 500, 'We could not submit your booking right now. Please call 08035516634 to book directly.');
    }
};
