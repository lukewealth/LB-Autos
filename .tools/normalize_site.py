#!/usr/bin/env python3
"""
Lady Benz — site-wide normaliser.

Applies the canonical contact block (address, phones, email, website),
social handles, and a unified header/footer/CTA to every page so the
whole site is consistent.

Run from the project root:
    python3 .tools/normalize_site.py
"""
from __future__ import annotations
import os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Canonical strings
# ---------------------------------------------------------------------------
ADDRESS       = "Opposite Eko Akete, Lekki Epe Expressway, Awoyaya, Lagos, Nigeria."
PHONE1        = "08035516634"
PHONE1_TEL    = "+2348035516634"
PHONE2        = "09078966026"
PHONE2_TEL    = "+2349078966026"
EMAIL         = "ladybenzautomechnic@gmail.com"
WEBSITE       = "www.ladybenzautomechanic.com"
WEBSITE_URL   = "https://www.ladybenzautomechanic.com"

SOCIAL = [
    ("https://facebook.com/ladybenzautomechanic",     "Facebook",    "fab fa-facebook-f"),
    ("https://twitter.com/ladybenzautomechanic",      "Twitter",     "fab fa-twitter"),
    ("https://instagram.com/ladybenzautomechanic",    "Instagram",   "fab fa-instagram"),
    ("https://linkedin.com/company/ladybenzautomechanic", "LinkedIn", "fab fa-linkedin-in"),
]

NAV_LINKS = [
    ("index.html",       "Home",        "index.html"),
    ("about.html",       "About",       "about.html"),
    ("service.html",     "Services",    "service.html"),
    ("contact.html",     "Contact",     "contact.html"),
]

DROPDOWN_LINKS = [
    ("booking.html",     "Booking"),
    ("team.html",        "Technicians"),
    ("testimonial.html", "Testimonial"),
    ("index.html#faq",   "FAQ"),
    ("training.html",    "Training"),
]

# ---------------------------------------------------------------------------
# Component builders
# ---------------------------------------------------------------------------
def topbar() -> str:
    social_html = "\n".join(
        f'                    <a class="btn btn-sm-square me-{"" if i==0 else "1" if i < len(SOCIAL)-1 else "0" if i==len(SOCIAL)-1 else "1"}" href="{url}" aria-label="{name}"><i class="{icon}" aria-hidden="true"></i></a>'
        for i, (url, name, icon) in enumerate(SOCIAL)
    )
    return f"""    <!-- Topbar -->
    <div class="container-fluid topbar p-0">
        <div class="row gx-0 d-none d-lg-flex align-items-center">
            <div class="col-lg-7 px-5 text-start">
                <div class="h-100 d-inline-flex align-items-center py-3 me-4">
                    <small class="fa fa-map-marker-alt me-2" aria-hidden="true"></small>
                    <small>{ADDRESS}</small>
                </div>
                <div class="h-100 d-inline-flex align-items-center py-3">
                    <small class="far fa-clock me-2" aria-hidden="true"></small>
                    <small>MON &ndash; FRI: 09.00 AM &ndash; 06.00 PM</small>
                </div>
            </div>
            <div class="col-lg-5 px-5 text-end">
                <div class="h-100 d-inline-flex align-items-center py-3 me-4">
                    <small class="fa fa-phone-alt me-2" aria-hidden="true"></small>
                    <small>
                        <a href="tel:{PHONE1_TEL}" class="text-decoration-none text-reset">{PHONE1}</a>
                        <span class="mx-1">|</span>
                        <a href="tel:{PHONE2_TEL}" class="text-decoration-none text-reset">{PHONE2}</a>
                    </small>
                </div>
                <div class="h-100 d-inline-flex align-items-center">
{social_html}
                </div>
            </div>
        </div>
    </div>"""


def navbar(active: str) -> str:
    nav_items = []
    for href, label, key in NAV_LINKS:
        cls = "nav-item nav-link active" if key == active else "nav-item nav-link"
        nav_items.append(f'                <a href="{href}" class="{cls}">{label}</a>')

    dropdown_items = "\n".join(
        f'                        <a href="{href}" class="dropdown-item">{label}</a>'
        for href, label in DROPDOWN_LINKS
    )

    return f"""    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light shadow sticky-top p-0">
        <a href="index.html" class="navbar-brand d-flex align-items-center px-4 px-lg-5">
            <img src="img/logo.png" alt="Lady Benz Logo" height="48" class="me-2"/>
            <span class="font-size-1 text-secondary fw-bold">Lady Benz Automechanic<sup>&reg;</sup></span>
        </a>
        <button type="button" class="navbar-toggler me-4" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-label="Toggle navigation" id="menuToggle">
            <span class="navbar-toggler-icon"></span>
            <span class="close-icon d-none" style="font-size: 1.5rem;">&times;</span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <div class="navbar-nav ms-auto p-4 p-lg-0 align-items-lg-center">
{chr(10).join(nav_items)}
                <div class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">More</a>
                    <div class="dropdown-menu fade-up m-0">
{dropdown_items}
                    </div>
                </div>
                <a href="booking.html" class="btn booking-btn ms-lg-3">Book a Session<i class="fa fa-arrow-right ms-2" aria-hidden="true"></i></a>
            </div>
        </div>
    </nav>"""


def footer() -> str:
    social_html = "\n".join(
        f'                        <a class="btn btn-outline-light" href="{url}" aria-label="{name}"><i class="{icon}" aria-hidden="true"></i></a>'
        for url, name, icon in SOCIAL
    )
    return f"""    <!-- Footer -->
    <footer class="footer">
        <div class="container py-5">
            <div class="row g-4">
                <div class="col-lg-4 col-md-6">
                    <h4 class="text-light mb-3">Lady Benz Automechanic Ltd</h4>
                    <p class="mb-3">Nigeria's leading Mercedes-Benz service and training center. Certified diagnostics, OEM repairs, and the next generation of auto engineers.</p>
                    <p class="mb-2"><i class="fa fa-map-marker-alt me-2" aria-hidden="true"></i>{ADDRESS}</p>
                    <p class="mb-2">
                        <i class="fa fa-phone-alt me-2" aria-hidden="true"></i>
                        <a href="tel:{PHONE1_TEL}">{PHONE1}</a> &middot;
                        <a href="tel:{PHONE2_TEL}">{PHONE2}</a>
                    </p>
                    <p class="mb-2"><i class="fa fa-envelope me-2" aria-hidden="true"></i><a href="mailto:{EMAIL}">{EMAIL}</a></p>
                    <p class="mb-0"><i class="fa fa-globe me-2" aria-hidden="true"></i><a href="{WEBSITE_URL}" target="_blank" rel="noopener">{WEBSITE}</a></p>
                </div>
                <div class="col-lg-2 col-md-6">
                    <h5 class="text-light mb-3">Quick Links</h5>
                    <a class="d-block mb-2" href="index.html">Home</a>
                    <a class="d-block mb-2" href="about.html">About</a>
                    <a class="d-block mb-2" href="service.html">Services</a>
                    <a class="d-block mb-2" href="training.html">Training</a>
                    <a class="d-block mb-2" href="contact.html">Contact</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5 class="text-light mb-3">Business Hours</h5>
                    <p class="mb-1"><strong>Monday &ndash; Friday:</strong> 09.00 AM &ndash; 06.00 PM</p>
                    <p class="mb-1"><strong>Saturday:</strong> 09.00 AM &ndash; 02.00 PM</p>
                    <p class="mb-3"><strong>Sunday:</strong> Closed</p>
                    <div class="d-flex pt-2">
{social_html}
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h5 class="text-light mb-3">Newsletter</h5>
                    <p class="mb-3">Subscribe for service tips, training updates, and special offers.</p>
                    <form id="newsletterForm" class="position-relative mx-auto" style="max-width: 360px;" novalidate>
                        <input class="form-control border-0 w-100 py-3 ps-4 pe-5" type="email" name="newsletter_email" placeholder="Your email" required aria-label="Email address">
                        <button type="submit" class="btn btn-warning py-2 px-3 position-absolute top-0 end-0 mt-2 me-2">Subscribe</button>
                    </form>
                    <div id="newsletterStatus" class="alert-status mt-2" role="status" aria-live="polite" hidden></div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="copyright">
                <div class="row align-items-center">
                    <div class="col-md-6 text-center text-md-start mb-2 mb-md-0">
                        &copy; <span id="copyrightYear"></span>
                        <a href="index.html" class="text-reset">Lady Benz Automechanic Ltd</a>. All Rights Reserved.
                    </div>
                    <div class="col-md-6 text-center text-md-end">
                        <div class="footer-menu">
                            <a href="index.html">Home</a>
                            <a href="index.html#faq">FAQs</a>
                            <a href="contact.html">Contact</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <!-- Floating Call / WhatsApp CTA -->
    <div class="lb-float-cta" aria-label="Quick contact options">
        <a class="lb-float-call" href="tel:{PHONE1_TEL}" aria-label="Call Lady Benz at {PHONE1}">
            <i class="fa fa-phone-alt" aria-hidden="true"></i>
        </a>
        <a class="lb-float-wa" href="https://wa.me/2348035516634" target="_blank" rel="noopener" aria-label="Chat with Lady Benz on WhatsApp">
            <i class="fab fa-whatsapp" aria-hidden="true"></i>
        </a>
    </div>"""


# ---------------------------------------------------------------------------
# Pattern matching
# ---------------------------------------------------------------------------
TOPBAR_RE = re.compile(
    r"<!-- Topbar Start -->.*?<!-- Topbar End -->",
    re.DOTALL,
)
NAVBAR_RE = re.compile(
    r"<!-- Navbar Start -->.*?<!-- Navbar End -->",
    re.DOTALL,
)
FOOTER_RE = re.compile(
    r"<!-- Footer Start -->.*?<!-- Footer End -->",
    re.DOTALL,
)


def replace_block(html: str, regex: re.Pattern, replacement: str, label: str) -> str:
    new_html, count = regex.subn(replacement + "\n", html, count=1)
    if count == 0:
        print(f"  ! {label} not found")
    return new_html


def normalize_page(path: pathlib.Path, active: str) -> None:
    print(f"-- {path.name}")
    text = path.read_text()
    text = replace_block(text, TOPBAR_RE, topbar(), "Topbar")
    text = replace_block(text, NAVBAR_RE, navbar(active), "Navbar")
    text = replace_block(text, FOOTER_RE, footer(), "Footer")

    # Add the copyright-year + WOW init script just before </body>
    # (idempotent: skip if already present)
    if "copyrightYear" not in text:
        text = text.replace(
            "</body>",
            """    <script>
    (function () {
        var y = document.getElementById('copyrightYear');
        if (y) y.textContent = new Date().getFullYear();
        if (window.WOW) new WOW().init();
    })();
    </script>
</body>""",
        )

    path.write_text(text)
    print(f"   ok")


def main() -> None:
    os.chdir(ROOT)
    pages = {
        "index.html":       "index.html",
        "about.html":       "about.html",
        "service.html":     "service.html",
        "booking.html":     "booking.html",
        "team.html":        "team.html",
        "testimonial.html": "testimonial.html",
        "training.html":    "training.html",
        "contact.html":     "contact.html",
        "404.html":         "404.html",
    }
    for name, active in pages.items():
        p = ROOT / name
        if p.exists():
            normalize_page(p, active)
        else:
            print(f"-- {name}: missing")


if __name__ == "__main__":
    main()
