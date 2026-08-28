# Lady Benz Autos — Vercel Deployment Guide

## What was changed

| Before | After |
|--------|-------|
| `send-contact.php` | `api/contact.js` (Vercel Serverless Function) |
| `send-booking.php` | `api/booking.js` (Vercel Serverless Function) |
| `send-newsletter.php` | `api/newsletter.js` (Vercel Serverless Function) |
| `vercel.json` | Routing rewrites so old `.php` URLs still work |

The static HTML/CSS/JS files are unchanged and served directly by Vercel's CDN.

---

## Prerequisites

- [Node.js 18+](https://nodejs.org/) installed
- A [Vercel account](https://vercel.com/signup) (free tier is fine)
- SSH key loaded for GitHub (`ladybenzautomechanic/LB-Autos` repo)

---

## Step 1 — Install dependencies

```bash
cd LadyBenz
npm install
```

This installs `nodemailer` (for sending emails) and `vercel` CLI as a dev dependency.

---

## Step 2 — Set environment variables

Create a `.env` file (never commit this):

```
LB_GMAIL_USER=your-gmail-address@gmail.com
LB_GMAIL_APP_PASSWORD=your-16-character-app-password
```

> **GMail SMTP**: Gmail requires an [App Password](https://support.google.com/accounts/answer/185833),
> not your regular password. Create one at Google Account → Security → 2-Step Verification → App Passwords.

To set on Vercel (Step 4 below), add these in the Vercel dashboard:
`Settings → Environment Variables`.

---

## Step 3 — Deploy to Vercel (one-time setup)

```bash
# Authenticate (opens browser)
npx vercel login

# Link project to GitHub repo
npx vercel link

# Deploy to preview URL
npx vercel

# Deploy to production (yoursite.vercel.app)
npx vercel --prod
```

Alternatively, import directly in the Vercel dashboard:
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import `ladybenzautomechanic/LB-Autos` from GitHub
3. Vercel auto-detects `vercel.json` and deploys

---

## Step 4 — Add environment variables on Vercel

After the first deploy:

1. Go to your project on [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **Settings → Environment Variables**
3. Add each variable from `.env`:

| Name | Value |
|------|-------|
| `LB_GMAIL_USER` | `ladybenzautomechnic@gmail.com` |
| `LB_GMAIL_APP_PASSWORD` | `xxxx xxxx xxxx xxxx` (16-char app password) |

4. Click **Save** and then **Redeploy** (`Deployments → ⋮ → Redeploy`)

---

## Step 5 — Attach custom domain `ladybenzautomechanic.com`

### 5a. Add domain in Vercel

1. Go to **Settings → Domains**
2. Enter `ladybenzautomechanic.com`
3. Click **Add**

Vercel will show DNS records you need to add to your domain registrar.

### 5b. Add DNS records at your registrar

Log into your domain registrar (where you bought `ladybenzautomechanic.com`) and add:

**For `www` subdomain (required):**
```
Type:  CNAME
Name:  www
Value: cname.vercel-dns.com
TTL:   3600 (or Auto)
```

**For the root/apex domain `ladybenzautomechanic.com` (required for HTTPS):**

Option A — ALIAS record (Route 53 / Cloudflare):
```
Type:  ALIAS / ANAME
Name:  @ (or leave empty)
Value: cname.vercel-dns.com
TTL:   3600
```

Option B — A record (if ALIAS not supported):
```
Type:  A
Name:  @
Value: 76.76.21.21
TTL:   3600
```

> `76.76.21.21` is Vercel's anycast IP. Works for most registrars.

### 5c. Wait for SSL certificate

Vercel auto-provisions a **Let's Encrypt** certificate once DNS propagates (typically 5–30 minutes, sometimes up to 48h).

You'll see **Verified** green status in Vercel → Domains when ready.

### 5d. Force HTTPS

In Vercel → **Settings → Domains**, ensure:
- [x] **Redirect `www.ladybenzautomechanic.com` → `ladybenzautomechanic.com`** (if using both)
- [x] **Enforce HTTPS** (automatically enabled)

---

## Step 6 — Test the forms

After deployment:

1. Visit your production URL
2. Submit the contact form, booking form, and newsletter form
3. Confirm you receive emails at `ladybenzautomechnic@gmail.com`

### Troubleshooting email delivery

| Symptom | Fix |
|---------|-----|
| "We could not send your message" | Check `LB_GMAIL_APP_PASSWORD` is correct and is an **App Password** (not your login password) |
| No email received | Check Gmail → Settings → Filters → See if emails are being filtered |
| Forms show JSON on screen | Redeploy after adding environment variables |

---

## File structure

```
LadyBenz/
├── api/
│   ├── _mailer.js       ← shared SMTP helper (imported by all functions)
│   ├── contact.js       ← POST /api/contact
│   ├── booking.js       ← POST /api/booking
│   └── newsletter.js    ← POST /api/newsletter
├── vercel.json          ← routing, headers, function config
├── package.json
├── index.html           ← static (served from root)
├── about.html
├── service.html
├── booking.html
├── team.html
├── testimonial.html
├── training.html
├── contact.html
├── 404.html
├── css/style.css
├── img/
├── send-contact.php     ← kept for reference (not used on Vercel)
├── send-booking.php
├── send-newsletter.php
└── README.md
```

---

## Updating the site

```bash
# Make changes to HTML/CSS/JS
git add . && git commit -m "update description"
git push origin main

# Vercel auto-deploys on every push to main (if GitHub integration enabled)
```

To manually redeploy: Vercel Dashboard → Deployments → latest → ⋮ → Redeploy

---

## Canonical contact info (used everywhere on the site)

- **Address:** Opposite Eko Akete, Lekki Epe Expressway, Awoyaya, Lagos, Nigeria.
- **Phones:** 08035516634, 09078966026
- **Email:** ladybenzautomechnic@gmail.com
- **Website:** www.ladybenzautomechanic.com
- **Social:** `ladybenzautomechanic` (Facebook, Twitter/X, Instagram, LinkedIn)
