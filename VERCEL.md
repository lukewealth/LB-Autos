# Vercel Deployment

This is a static site (HTML/CSS/JS) configured for deployment on Vercel.

## Deploy via Vercel Dashboard (Recommended)

1. Push this folder to a Git repository (GitHub, GitLab, or Bitbucket).
2. Go to https://vercel.com/new and import the repository.
3. Vercel will auto-detect it as a static site. Leave the build settings blank:
   - **Framework Preset**: Other
   - **Build Command**: (leave empty)
   - **Output Directory**: `.` (project root)
4. Click **Deploy**.

## Deploy via Vercel CLI

```bash
npm i -g vercel
vercel login
vercel        # preview deployment
vercel --prod # production deployment
```

## Configuration

- `vercel.json` enables clean URLs (e.g. `/about` instead of `/about.html`),
  applies security headers, and caches static assets for 1 year.
- All HTML files in the project root are served as pages.
- `css/`, `js/`, `img/`, `lib/`, and `scss/` folders are served as static assets.
