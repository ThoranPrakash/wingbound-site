#!/usr/bin/env python3
"""
WingBound site generator.

All page content lives in this file. Run from the repo root:

    python3 src/build.py

It writes the .html pages, sitemap.xml and robots.txt into the repo root.
Needs only Python 3.8+ (no packages). Icons come from src/icons.json;
add new ones with:  python3 src/fetch_icons.py <icon-name>
"""
import hashlib, html, json, os, sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = json.load(open(os.path.join(ROOT, "src", "icons.json")))
MISSING = set()

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
SITE_URL = "https://thoranprakash.github.io/wingbound-site"  # change when the domain is ready
SITE_PATH = (urlparse(SITE_URL).path.rstrip("/") + "/") or "/"

PHONE_1 = ("Nikhil Kalyan", "+916281843302", "+91 62818 43302", "writetonikhilkalyan@gmail.com")
PHONE_2 = ("Thoran Prakash", "+919581546640", "+91 95815 46640", "thoranprakash23@gmail.com")
PHONE_3 = ("Sai Supreeth Varma", "+916300032574", "+91 63000 32574", None)
WHATSAPP = PHONE_1[1].lstrip("+")  # WhatsApp goes to Nikhil
WA_TEXT = "Hi WingBound, I'd like to know more about your workshops."

# Downloads only appear once the file exists in /downloads
PROPOSAL = "downloads/wingbound-proposal.pdf"
FLYER = "downloads/wingbound-flyer.pdf"
HAS_PROPOSAL = os.path.exists(os.path.join(ROOT, PROPOSAL))
HAS_FLYER = os.path.exists(os.path.join(ROOT, FLYER))

# ---------------------------------------------------------------------------
# Social proof. Only real, permitted content goes here.
# Empty lists render as dashed "to add" slots so the gaps are obvious.
# Set SHOW_EMPTY_SLOTS = False to hide empty sections on the live site.
# ---------------------------------------------------------------------------
SHOW_EMPTY_SLOTS = False
# ("500+", "students taught")
NUMBERS = []
# ("Event name", "Organised by …", "Year", "Result")
COMPETITIONS = []
# ("Quote text", "Name", "Role", "Institution")
QUOTES = []

NAV = [
    ("workshop.html", "The Workshop"),
    ("ai-aviation.html", "AI &amp; Aviation"),
    ("safety.html", "Safety"),
    ("schools.html", "For Schools"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
]
CTA_LABEL = "Get in touch"
CONTACT = "contact.html"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def icon(name, cls="icon"):
    if name not in ICONS:
        MISSING.add(name)
        return ""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


def badge(name, extra=""):
    return f'<span class="badge {extra}">{icon(name)}</span>'


def asset_version(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def wa_link(text=WA_TEXT):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"


WA_SVG = ('<svg class="icon" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16.04 3C8.86 3 3.03 8.82 3.03 16c0 2.3.6 4.53 1.74 6.5L3 29l6.68-1.75A13 13 0 0 0 16.04 29C23.2 29 29 23.18 29 16S23.2 3 16.04 3Zm0 23.8c-2 0-3.94-.53-5.64-1.55l-.4-.24-3.97 1.04 1.06-3.86-.26-.4A10.77 10.77 0 0 1 5.24 16c0-5.95 4.85-10.8 10.8-10.8 5.94 0 10.77 4.85 10.77 10.8 0 5.96-4.83 10.8-10.77 10.8Zm5.92-8.08c-.33-.16-1.93-.95-2.23-1.06-.3-.11-.52-.16-.73.17-.22.32-.84 1.05-1.03 1.27-.19.22-.38.24-.7.08-.33-.16-1.38-.51-2.62-1.62-.97-.86-1.62-1.93-1.81-2.25-.19-.33-.02-.5.14-.66.15-.15.33-.38.49-.57.16-.19.22-.33.33-.54.11-.22.05-.41-.03-.57-.08-.16-.73-1.76-1-2.41-.26-.63-.53-.55-.73-.56h-.62c-.22 0-.57.08-.87.41-.3.32-1.14 1.11-1.14 2.71s1.17 3.15 1.33 3.36c.16.22 2.3 3.5 5.56 4.91.78.34 1.39.54 1.86.69.78.25 1.49.21 2.05.13.63-.09 1.93-.79 2.2-1.55.27-.76.27-1.42.19-1.55-.08-.14-.3-.22-.62-.38Z"/></svg>')

PLANE_SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="rc-plane" viewBox="-32 -32 64 64" fill="currentColor">
    <path d="M-26 -2.6 L17 -3.2 Q27 -3.2 29.5 0 Q27 3.2 17 3.2 L-26 2.6 Z"/>
    <rect x="-4" y="-28" width="12" height="56" rx="2.5"/>
    <rect x="-27" y="-11" width="7" height="22" rx="1.5"/>
    <rect x="-4" y="-28" width="12" height="5" rx="2" fill="#fff" opacity=".9"/>
    <rect x="-4" y="23" width="12" height="5" rx="2" fill="#fff" opacity=".9"/>
    <rect x="29.5" y="-9" width="1.8" height="18" rx=".9" opacity=".75"/>
  </symbol>
</svg>"""

# Decorative flight paths (viewBox, path, duration, plane size)
SKIES = {
    "hero": ("0 0 1200 640", "M-80 560 C 180 520, 330 380, 470 330 C 600 285, 700 150, 620 110 C 540 70, 500 190, 610 220 C 760 260, 900 120, 1300 70", "15s", 56),
    "page": ("0 0 1200 320", "M-60 250 C 220 290, 400 110, 640 150 S 1000 70, 1280 110", "17s", 44),
    "figure8": ("0 0 1200 420", "M600 210 C 700 90, 920 90, 920 210 C 920 330, 700 330, 600 210 C 500 90, 280 90, 280 210 C 280 330, 500 330, 600 210 Z", "18s", 44),
}


def sky(kind, cls=""):
    vb, d, dur, size = SKIES[kind]
    pid = f"fp-{kind}"
    h = size / 2
    if kind == "figure8":
        motion = f'<animateMotion dur="{dur}" repeatCount="indefinite" rotate="auto"><mpath href="#{pid}"/></animateMotion>'
        trail = f'<path d="{d}" class="sky-path" stroke-dasharray="2 10"/>'
    else:
        kt = "0;0.7;1"
        motion = (f'<animateMotion dur="{dur}" repeatCount="indefinite" rotate="auto" calcMode="linear" '
                  f'keyPoints="0;1;1" keyTimes="{kt}"><mpath href="#{pid}"/></animateMotion>')
        trail = (f'<path d="{d}" class="sky-path" stroke-dasharray="2 10"/>'
                 f'<path d="{d}" class="sky-trail" pathLength="1" stroke-dasharray="1 1">'
                 f'<animate attributeName="stroke-dashoffset" values="1;0;0" keyTimes="{kt}" dur="{dur}" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.7;0.95" dur="{dur}" repeatCount="indefinite"/></path>')
    return (f'<svg class="sky sky--{kind} {cls}" viewBox="{vb}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<path id="{pid}" d="{d}" fill="none" stroke="none"/>{trail}'
            f'<g class="sky-plane"><use href="#rc-plane" x="-{h}" y="-{h}" width="{size}" height="{size}"/>{motion}</g></svg>')


def section_head(label, title, text="", center=False, hid=None):
    c = " center" if center else ""
    i = f' id="{hid}"' if hid else ""
    p = f"<p>{text}</p>" if text else ""
    return f'<div class="section-head{c}" data-reveal><span class="label">{label}</span><h2{i}>{title}</h2>{p}</div>'


def slot(title, text):
    return f'<div class="slot" data-reveal><strong>{icon("circle-plus")} To add: {title}</strong><span>{text}</span></div>'


# ---------------------------------------------------------------------------
# Page frame
# ---------------------------------------------------------------------------
CSS_V = asset_version("assets/css/styles.css")
JS_V = asset_version("assets/js/main.js")


def head(page, title, desc, ld=None, base=False):
    url = f"{SITE_URL}/" + ("" if page == "index.html" else page)
    lds = ld if isinstance(ld, list) else ([ld] if ld else [])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds)
    base_tag = f'<base href="{SITE_PATH}">\n' if base else ""
    robots = '<meta name="robots" content="noindex">\n' if page in ("404.html",) else ""
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base_tag}<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0F1115">
<meta property="og:type" content="website">
<meta property="og:site_name" content="WingBound">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="64x64" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/lato-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/lato-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css?v={CSS_V}">
<script>document.documentElement.classList.add("js")</script>
<script src="assets/js/main.js?v={JS_V}" defer></script>
{ld_html}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{PLANE_SPRITE}
"""


def header(page):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if page == CONTACT else ""
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html" aria-label="WingBound home">
      <picture><source srcset="assets/img/logo-240.webp" type="image/webp"><img src="assets/img/logo-240.png" alt="" width="240" height="165"></picture>
      <span class="brand-word">WINGBOUND</span>
    </a>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul class="nav-links">
        {"".join(items)}
      </ul>
      <a class="btn btn--primary nav-cta" href="{CONTACT}"{cur}>{CTA_LABEL} {icon("arrow-right")}</a>
      <div class="nav-quick">
        <a href="tel:{PHONE_1[1]}">{icon("phone")} Call {PHONE_1[2]}</a>
        <a href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG} WhatsApp us</a>
      </div>
    </nav>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span class="burger" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
  </div>
  <div class="flight-progress" aria-hidden="true"><span class="fp-trail"></span><svg class="fp-plane" viewBox="-32 -32 64 64"><use href="#rc-plane"/></svg></div>
</header>
"""


def footer():
    dl = ""
    if HAS_PROPOSAL:
        dl += f'<li><a href="{PROPOSAL}" download>Proposal (PDF)</a></li>'
    if HAS_FLYER:
        dl += f'<li><a href="{FLYER}" download>Flyer (PDF)</a></li>'
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="index.html" aria-label="WingBound home">
          <picture><source srcset="assets/img/logo-240.webp" type="image/webp"><img src="assets/img/logo-240.png" alt="" width="240" height="165" loading="lazy"></picture>
          <span class="brand-word">WINGBOUND</span>
        </a>
        <p>Hands-on RC aircraft and AI workshops for schools and colleges across Andhra Pradesh. Based in Visakhapatnam.</p>
        <div class="btn-row">
          <a class="btn btn--primary btn--sm" href="{CONTACT}">{CTA_LABEL} {icon("arrow-right")}</a>
          <a class="btn btn--ghost btn--sm" href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>
        </div>
      </div>
      <nav class="footer-col" aria-label="Footer: workshop">
        <h2>Workshop</h2>
        <ul>
          <li><a href="workshop.html">The Workshop</a></li>
          <li><a href="ai-aviation.html">AI &amp; Aviation</a></li>
          <li><a href="safety.html">Safety</a></li>
          <li><a href="gallery.html">Gallery</a></li>
        </ul>
      </nav>
      <nav class="footer-col" aria-label="Footer: schools">
        <h2>Schools</h2>
        <ul>
          <li><a href="schools.html">For Schools &amp; Colleges</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="about.html">About us</a></li>
          <li><a href="{CONTACT}">Contact</a></li>
          {dl}
        </ul>
      </nav>
      <div class="footer-col">
        <h2>Talk to us</h2>
        <ul class="footer-contacts">
          <li><strong>{PHONE_1[0]}</strong><a href="tel:{PHONE_1[1]}">{PHONE_1[2]}</a><a href="mailto:{PHONE_1[3]}">{PHONE_1[3]}</a></li>
          <li><strong>{PHONE_2[0]}</strong><a href="tel:{PHONE_2[1]}">{PHONE_2[2]}</a><a href="mailto:{PHONE_2[3]}">{PHONE_2[3]}</a></li>
        </ul>
      </div>
    </div>
    <svg class="footer-mark" viewBox="0 0 1000 104" aria-hidden="true" focusable="false"><text x="2" y="96" textLength="996" lengthAdjust="spacingAndGlyphs">DESIGN. BUILD. FLY.</text></svg>
    <div class="footer-bottom">
      <p>Student photos are shared only with parental consent.</p>
      <p>&copy; <span data-year>2026</span> WingBound, Visakhapatnam</p>
    </div>
  </div>
</footer>
<aside aria-label="Quick contact">
  <a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Chat with WingBound on WhatsApp (opens in a new tab)">{WA_SVG}<span>WhatsApp us</span></a>
</aside>
</body>
</html>
"""


def page_hero(label, title, text, facts=None, crumb=None):
    bc = f'<p class="breadcrumb"><a href="index.html">Home</a> <span aria-hidden="true">/</span> {crumb}</p>' if crumb else ""
    f = ""
    if facts:
        f = '<ul class="hud hud--page">' + "".join(
            f'<li><span class="hud-k">{k}</span><span class="hud-v">{v}</span></li>' for k, v in facts) + "</ul>"
    return f"""<section class="page-hero">
  <div class="glow" aria-hidden="true"></div>
  {sky("page")}
  <div class="container">
    {bc}
    <span class="label">{label}</span>
    <h1>{title}</h1>
    <p class="page-hero-sub">{text}</p>
    {f}
  </div>
</section>
"""


def cta_band(title="Bring WingBound to your campus", text="Tell us about your school or college and the dates you have in mind. We will visit to check your hall and ground, then plan the rest with you."):
    second = (f'<a class="btn btn--ghost" href="{PROPOSAL}" download>{icon("download")} Download proposal (PDF)</a>'
              if HAS_PROPOSAL else
              f'<a class="btn btn--ghost" href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG} WhatsApp us</a>')
    return f"""<section class="section section--dark cta-band" aria-labelledby="cta-title">
  <div class="glow" aria-hidden="true"></div>
  <div class="container" data-reveal>
    <span class="label">Ready for take-off?</span>
    <h2 id="cta-title">{title}</h2>
    <p>{text}</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{CONTACT}">{CTA_LABEL} {icon("arrow-right")}</a>
      {second}
    </div>
  </div>
</section>
"""


def write(page, title, desc, body, ld=None, base=False):
    body = body.replace("100 m × 50 m", "100&nbsp;m&nbsp;×&nbsp;50&nbsp;m")
    out = head(page, title, desc, ld, base) + header(page) + '<main id="main">\n' + body + "</main>\n" + footer()
    with open(os.path.join(ROOT, page), "w", encoding="utf-8") as f:
        f.write(out)


def crumbs(name, page):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE_URL}/{page}"},
        ],
    }


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "@id": SITE_URL + "/#org",
    "name": "WingBound",
    "slogan": "Design. Build. Fly.",
    "description": "Hands-on aeromodelling (RC aircraft) and AI workshops run on school and college campuses in Andhra Pradesh.",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/assets/img/wingbound-logo.png",
    "areaServed": {"@type": "State", "name": "Andhra Pradesh"},
    "address": {"@type": "PostalAddress", "addressLocality": "Visakhapatnam", "addressRegion": "Andhra Pradesh", "addressCountry": "IN"},
    "email": PHONE_1[3],
    "telephone": PHONE_1[1],
    "contactPoint": [
        {"@type": "ContactPoint", "name": PHONE_1[0], "telephone": PHONE_1[1], "email": PHONE_1[3], "contactType": "customer service", "areaServed": "IN", "availableLanguage": ["en"]},
        {"@type": "ContactPoint", "name": PHONE_2[0], "telephone": PHONE_2[1], "email": PHONE_2[3], "contactType": "customer service", "areaServed": "IN", "availableLanguage": ["en"]},
    ],
}

# ---------------------------------------------------------------------------
# Shared content
# ---------------------------------------------------------------------------
MODULES = [
    ("01", "Flight basics", "Forces of flight, lift, airfoils and the types of RC planes.", "wind"),
    ("02", "Anatomy &amp; control", "Aircraft parts, control surfaces and stability.", "plane"),
    ("03", "Electronics &amp; power", "Motor, ESC, servos, LiPo battery and radio.", "cpu"),
    ("04", "Materials &amp; design", "Build materials and sizing a trainer aircraft.", "ruler"),
    ("05", "Fabrication", "Build plans for the fuselage, wing and tail.", "scissors"),
    ("06", "AI &amp; aviation", "How AI makes aircraft smarter and helps people.", "brain-circuit"),
]

FAQS = [
    ("For schools and colleges", [
        ("What does the school need to provide?",
         "<ul><li>A hall or lab with tables and power sockets</li><li>A projector</li><li>An open ground at least 100 m × 50 m</li><li>One teacher present throughout</li><li>Signed consent forms</li></ul><p>We bring everything else. <a href=\"schools.html\">See who provides what</a>.</p>",
         "A hall or lab with tables and power sockets, a projector, an open ground at least 100 m × 50 m, one teacher present throughout, and signed consent forms. We bring everything else."),
        ("How long does it take?",
         "<p>The full build workshop runs over 2 days: about 5½ hours on Day 1 and 6 hours on Day 2. There is also a 1-day version with theory, a live build demo and a flight demo, without student fabrication. <a href=\"workshop.html#schedule\">See the schedule</a>.</p>",
         "The full build workshop runs over 2 days: about 5½ hours on Day 1 and 6 hours on Day 2. There is also a 1-day version with theory, a live build demo and a flight demo, without student fabrication."),
        ("Which classes can join?",
         "<p>Students from Class 8 through engineering and diploma. We work in batches of 30–60 students, in teams of 4–5, with one instructor for every 12 students.</p>",
         "Students from Class 8 through engineering and diploma. We work in batches of 30–60 students, in teams of 4–5, with one instructor for every 12 students."),
        ("Is there a minimum group size?",
         "<p>Yes, the minimum is 30 students. Each batch is 30–60 students.</p>",
         "Yes, the minimum is 30 students. Each batch is 30–60 students."),
        ("Who pays, and how?",
         "<p>We invoice the institution, not students. 50% is due on booking and 50% within 7 days after the workshop. For fees, <a href=\"contact.html\">get in touch</a>.</p>",
         "We invoice the institution, not students. 50% is due on booking and 50% within 7 days after the workshop."),
        ("Can it fit around exams?",
         "<p>Yes. You choose the dates, and the 1-day version suits a busy term. Get in touch early so we have time to visit your campus before the workshop.</p>",
         "Yes. You choose the dates, and the 1-day version suits a busy term. Get in touch early so we have time to visit your campus before the workshop."),
        ("Where do you run workshops?",
         "<p>On school and college campuses across Andhra Pradesh. We are based in Visakhapatnam.</p>",
         "On school and college campuses across Andhra Pradesh. We are based in Visakhapatnam."),
    ]),
    ("Safety", [
        ("Is it safe?",
         "<p>Yes. Only experienced WingBound pilots fly, and students stay behind a marked flight line. We check your campus on the DGCA Digital Sky airspace map before confirming a date. LiPo batteries are charged only by instructors in fire-safe bags, propellers go on only for the flight demo, and a first-aid kit and a school teacher are present throughout. <a href=\"safety.html\">Read our full safety plan</a>.</p>",
         "Yes. Only experienced WingBound pilots fly, and students stay behind a marked flight line. We check the campus on the DGCA Digital Sky airspace map before confirming a date. LiPo batteries are charged only by instructors in fire-safe bags, propellers go on only for the flight demo, and a first-aid kit and a school teacher are present throughout."),
        ("Do students fly the plane?",
         "<p>Our pilots fly the aircraft. Students can try the controls through a trainer link, under supervision. The instructor holds the master radio and can take over at any moment.</p>",
         "Our pilots fly the aircraft. Students can try the controls through a trainer link, under supervision. The instructor holds the master radio and can take over at any moment."),
        ("Do you need parental consent?",
         "<p>Yes. We need signed parental consent for every student under 18. Student photos are shared only with parental consent.</p>",
         "Yes. We need signed parental consent for every student under 18. Student photos are shared only with parental consent."),
    ]),
    ("Students and learning", [
        ("Do students keep anything?",
         "<p>Every participant receives a certificate. Students also keep what they learn: how to design and size a trainer, and how the electronics fit together. Ask us if your institution would like to keep the team aircraft.</p>",
         "Every participant receives a certificate. Students also keep what they learn: how to design and size a trainer, and how the electronics fit together. Ask us if your institution would like to keep the team aircraft."),
        ("What is the AI part?",
         "<p>Module 6 shows how AI makes aircraft smarter (self-levelling, return to home, obstacle detection) and where AI-powered drones already help people, such as in agriculture and medical delivery. We also share a project path students can follow in an Atal Tinkering Lab or computer lab, using free tools like ArduPilot, INAV and Google Teachable Machine. <a href=\"ai-aviation.html\">Learn more</a>.</p>",
         "Module 6 shows how AI makes aircraft smarter, such as self-levelling, return to home and obstacle detection, and where AI-powered drones already help people. We also share a project path students can follow in an Atal Tinkering Lab or computer lab, using free tools like ArduPilot, INAV and Google Teachable Machine."),
        ("Which subjects does it link to?",
         "<p>Physics, mathematics, design and technology, and computer science (AI).</p>",
         "Physics, mathematics, design and technology, and computer science (AI)."),
    ]),
]
FAQ_INDEX = {q: (a, p) for _, items in FAQS for q, a, p in items}


def faq_list(questions):
    return '<div class="faq">' + "".join(
        f'<details data-reveal><summary>{q}</summary><div class="answer">{FAQ_INDEX[q][0]}</div></details>' for q in questions) + "</div>"


def proof_section(heading_id="record-title"):
    """Track record + any real numbers, competitions and quotes."""
    nums = ""
    if NUMBERS:
        nums = '<div class="proof-numbers">' + "".join(
            f'<div class="proof-num" data-reveal><span class="big">{n}</span><span>{t}</span></div>' for n, t in NUMBERS) + "</div>"
    elif SHOW_EMPTY_SLOTS:
        nums = slot("workshop numbers", "Real totals so far, e.g. students taught, workshops run, institutions visited.")

    comps = ""
    if COMPETITIONS:
        rows = "".join(f'<li data-reveal><span class="comp-year">{y}</span><span class="comp-name"><strong>{e}</strong>{o}</span><span class="comp-result">{r}</span></li>'
                       for e, o, y, r in COMPETITIONS)
        comps = f'<h3 class="sub-head mt-3">Competitions</h3><ul class="comp-list">{rows}</ul>'
    elif SHOW_EMPTY_SLOTS:
        comps = slot("competition results", "For each win: event name, organiser, year and placing.")

    quotes = ""
    if QUOTES:
        quotes = '<div class="quotes">' + "".join(
            f'<figure class="quote-card" data-reveal>{icon("quote", "icon quote-mark")}<blockquote><p>{q}</p></blockquote>'
            f'<figcaption><strong>{n}</strong>{r}, {i}</figcaption></figure>' for q, n, r, i in QUOTES) + "</div>"
    elif SHOW_EMPTY_SLOTS:
        quotes = slot("feedback quotes", "Real words from teachers, HODs or students at VIIT or MRCET, with their name, role and permission.")

    return f"""<section class="section" aria-labelledby="{heading_id}">
  <div class="container">
    {section_head("Track record", "Built and flown by people who compete", "WingBound is a team of four RC aircraft builders and pilots from Visakhapatnam.", hid=heading_id)}
    <div class="proof-grid">
      <article class="proof-hero" data-reveal>
        <span class="proof-big">10<small>years</small></span>
        <p>Designing, building and flying RC aircraft.</p>
      </article>
      <article class="card" data-reveal>{badge("trophy")}<h3>Competition winners</h3><p>We have competed in, and won, multiple competitions organised by Boeing in partnership with IIT Madras, NIT Warangal and Vignan University.</p></article>
      <article class="card" data-reveal>{badge("school")}<h3>Workshops delivered</h3>
        <ul class="plain-list"><li><strong>Vignan's Institute of Information Technology</strong>Visakhapatnam</li><li><strong>Malla Reddy College of Engineering and Technology</strong>Hyderabad</li></ul>
      </article>
    </div>
    {nums}
    {comps}
    {quotes}
    <p class="note">Boeing organised these competitions. Boeing is not a partner or sponsor of WingBound.</p>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Illustrations (inline SVG, drawn from the real specifications)
# ---------------------------------------------------------------------------
def blueprint(compact=False):
    """Top-view outline of the WingBound trainer, with parts named but no measurements (those are taught in the workshop)."""
    cls = "blueprint blueprint--compact" if compact else "blueprint"
    return f"""<figure class="{cls}" data-draw>
  <svg viewBox="0 0 760 560" role="img" aria-labelledby="bp-title bp-desc">
    <title id="bp-title">Top-view drawing of the WingBound trainer aircraft</title>
    <desc id="bp-desc">An outline of the foam-board trainer students build, seen from above, with its parts labelled: propeller, motor, wing, ailerons, wing span, fuselage, tailplane, elevator, and fin and rudder.</desc>
    <defs>
      <pattern id="bp-grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="rgba(255,255,255,.06)" stroke-width="1"/></pattern>
      <marker id="bp-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#F7923A"/></marker>
    </defs>
    <rect width="760" height="560" fill="url(#bp-grid)"/>
    <!-- aircraft -->
    <g class="bp-air">
      <path pathLength="1" d="M316 52 H444"/>
      <path pathLength="1" d="M372 60 Q380 50 388 60"/>
      <path pathLength="1" d="M360 78 Q380 56 400 78 L400 255 L388 435 L372 435 L360 255 Z"/>
      <path pathLength="1" d="M118 130 H642 Q650 130 650 138 V207 Q650 215 642 215 H118 Q110 215 110 207 V138 Q110 130 118 130 Z"/>
      <path pathLength="1" d="M305 395 H455 V435 H305 Z"/>
      <path pathLength="1" d="M377 380 H383 V442 H377 Z"/>
      <path class="bp-hinge" d="M120 197 H250 M510 197 H640 M307 420 H453"/>
    </g>
    <!-- part names only: no values -->
    <g class="bp-dim">
      <path pathLength="1" d="M110 222 V512 M650 222 V512 M352 60 H44 M366 435 H44"/>
      <path pathLength="1" marker-start="url(#bp-arrow)" marker-end="url(#bp-arrow)" d="M112 500 H648"/>
      <path pathLength="1" marker-start="url(#bp-arrow)" marker-end="url(#bp-arrow)" d="M56 62 V433"/>
      <path pathLength="1" d="M444 52 L520 30 H624"/>
      <path pathLength="1" d="M398 74 L520 96 H580"/>
      <path pathLength="1" d="M590 192 L650 112 H720"/>
      <path pathLength="1" d="M330 422 L262 462 H170"/>
      <path pathLength="1" d="M448 410 L520 438 H624"/>
      <path pathLength="1" d="M386 392 L520 352 H650"/>
    </g>
    <g class="bp-text">
      <text x="380" y="490" text-anchor="middle">WING SPAN</text>
      <text x="44" y="250" transform="rotate(-90 44 250)" text-anchor="middle">FUSELAGE</text>
      <text x="290" y="178" text-anchor="middle" class="bp-sm">WING</text>
      <text x="524" y="22" class="bp-sm">PROPELLER</text>
      <text x="524" y="88" class="bp-sm">MOTOR</text>
      <text x="720" y="104" text-anchor="end" class="bp-sm">AILERON</text>
      <text x="170" y="454" class="bp-sm">ELEVATOR</text>
      <text x="524" y="430" class="bp-sm">TAILPLANE</text>
      <text x="524" y="344" class="bp-sm">FIN &amp; RUDDER</text>
    </g>
    <g class="bp-block">
      <rect x="20" y="518" width="210" height="30" rx="4"/>
      <text x="32" y="538">WB TRAINER · TOP VIEW</text>
    </g>
  </svg>
</figure>"""


def forces_diagram():
    return f"""<div class="forces" data-forces>
  <div class="forces-art">
    <svg viewBox="0 0 600 340" role="img" aria-labelledby="fo-title">
      <title id="fo-title">Side view of an aeroplane with the four forces of flight: lift up, weight down, thrust forward and drag backward</title>
      <defs>
        <marker id="fo-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker>
      </defs>
      <g class="fo-plane">
        <path d="M190 178 Q186 168 200 166 L392 162 Q422 162 430 172 Q422 182 392 182 L200 184 Q186 186 190 178 Z"/>
        <path d="M238 156 Q250 148 300 150 L322 152 Q326 157 320 160 L240 161 Z"/>
        <path d="M196 166 L184 128 L200 128 L222 165 Z"/>
        <path d="M188 177 L236 176 L236 182 L190 183 Z" opacity=".7"/>
        <rect x="432" y="146" width="4" height="52" rx="2" opacity=".75"/>
      </g>
      <g class="fo-force" data-force="lift"><line x1="285" y1="140" x2="285" y2="46"/><text x="300" y="98">LIFT</text></g>
      <g class="fo-force" data-force="weight"><line x1="285" y1="196" x2="285" y2="292"/><text x="300" y="256">WEIGHT</text></g>
      <g class="fo-force" data-force="thrust"><line x1="446" y1="172" x2="560" y2="172"/><text x="486" y="160">THRUST</text></g>
      <g class="fo-force" data-force="drag"><line x1="176" y1="172" x2="56" y2="172"/><text x="62" y="160">DRAG</text></g>
    </svg>
  </div>
  <div class="forces-copy">
    <div class="forces-tabs" role="group" aria-label="Choose a force">
      <button type="button" class="force-btn" data-force="lift" aria-pressed="true"><span class="dot dot--lift"></span>Lift</button>
      <button type="button" class="force-btn" data-force="weight" aria-pressed="false"><span class="dot dot--weight"></span>Weight</button>
      <button type="button" class="force-btn" data-force="thrust" aria-pressed="false"><span class="dot dot--thrust"></span>Thrust</button>
      <button type="button" class="force-btn" data-force="drag" aria-pressed="false"><span class="dot dot--drag"></span>Drag</button>
    </div>
    <div class="force-text" aria-live="polite">
      <p data-force="lift"><strong>Lift</strong> holds the aeroplane up. It comes from the wing as air flows over it.</p>
      <p data-force="weight" hidden><strong>Weight</strong> is gravity pulling the whole aircraft down. The wing has to make enough lift to hold it up.</p>
      <p data-force="thrust" hidden><strong>Thrust</strong> moves the aeroplane forward. The motor spins the propeller, which pulls the aircraft through the air.</p>
      <p data-force="drag" hidden><strong>Drag</strong> is the air resisting the aeroplane's motion. Smooth, light shapes keep drag low.</p>
    </div>
    <p class="forces-note">{icon("scale")} In steady, level flight, lift balances weight and thrust balances drag.</p>
  </div>
</div>"""


PARTS = [
    ("tx", "Transmitter", "The pilot's sticks send commands by radio."),
    ("rx", "Receiver", "Picks up the commands and passes them on."),
    ("servo", "Servos", "Small motors that move the control surfaces."),
    ("batt", "Battery", "Stores the energy. Charged only by instructors."),
    ("esc", "Speed controller", "Sets how fast the motor spins."),
    ("motor", "Motor", "Spins the propeller to make thrust."),
]


def wiring_diagram():
    def node(pid, x, y, w, h, title, sub):
        return (f'<g class="wd-node" data-parts="{pid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>'
                f'<text x="{x + w / 2}" y="{y + h / 2 - 4}" text-anchor="middle" class="wd-title">{title}</text>'
                f'<text x="{x + w / 2}" y="{y + h / 2 + 20}" text-anchor="middle" class="wd-sub">{sub}</text></g>')
    svg = f"""<svg viewBox="0 0 680 400" role="img" aria-labelledby="wd-title">
  <title id="wd-title">How the aircraft's electronics connect: the battery powers the speed controller, which drives the motor; the transmitter talks to the receiver by radio, and the receiver controls the speed controller and the servos</title>
  <g class="wd-links">
    <path class="wd-radio" data-parts="tx rx" d="M182 85 H258"/>
    <path class="wd-sig" data-parts="rx servo" d="M422 85 H498"/>
    <path class="wd-sig" data-parts="rx esc" d="M340 125 V275"/>
    <path class="wd-pow" data-parts="batt esc" d="M182 315 H258"/>
    <path class="wd-pow" data-parts="esc motor" d="M422 315 H498"/>
  </g>
  <g class="wd-waves" data-parts="tx rx" aria-hidden="true"><path d="M204 70 q8 15 0 30 M216 64 q12 21 0 42 M228 58 q16 27 0 54"/></g>
  {node("tx", 20, 45, 162, 80, "Transmitter", "Pilot")}
  {node("rx", 258, 45, 164, 80, "Receiver", "In the plane")}
  {node("servo", 498, 45, 162, 80, "Servos", "Control surfaces")}
  {node("batt", 20, 275, 162, 80, "Battery", "Energy")}
  {node("esc", 258, 275, 164, 80, "Controller", "Motor speed")}
  {node("motor", 498, 275, 162, 80, "Motor", "Propeller")}
  <text x="348" y="205" class="wd-lbl">THROTTLE</text>
</svg>"""
    items = "".join(
        f'<li><button type="button" class="part-btn" data-part="{pid}" aria-pressed="false"><strong>{t}</strong><span>{d}</span></button></li>'
        for pid, t, d in PARTS)
    return f"""<div class="wiring" data-wiring>
  <div class="wiring-art" data-active="">{svg}
    <ul class="wd-legend" aria-label="Legend"><li><span class="lg lg--pow"></span>Power</li><li><span class="lg lg--sig"></span>Signal</li><li><span class="lg lg--radio"></span>Radio</li></ul>
  </div>
  <ul class="parts">{items}</ul>
</div>"""


def field_diagram():
    return """<figure class="flightfield" data-reveal>
  <svg viewBox="0 0 640 420" role="img" aria-labelledby="fd-title fd-desc">
    <title id="fd-title">Flight-day layout on the school ground</title>
    <desc id="fd-desc">An open ground at least 100 metres by 50 metres. The aircraft flies over the open flight area. A marked flight line separates it from the students, who stay behind the line. The pilot and instructor stand at the line.</desc>
    <rect x="10" y="10" width="620" height="400" rx="18" class="fd-ground"/>
    <rect x="34" y="34" width="572" height="232" rx="12" class="fd-zone"/>
    <text x="320" y="64" text-anchor="middle" class="fd-k">FLIGHT AREA · NOBODY BELOW</text>
    <path id="fd-path" d="M170 160 C 170 90, 300 90, 320 150 S 470 210, 470 150 S 340 90, 320 150 S 170 230, 170 160 Z" class="fd-route"/>
    <g class="fd-plane"><use href="#rc-plane" x="-16" y="-16" width="32" height="32"/><animateMotion dur="10s" repeatCount="indefinite" rotate="auto"><mpath href="#fd-path"/></animateMotion></g>
    <line x1="34" y1="290" x2="606" y2="290" class="fd-line"/>
    <text x="606" y="314" text-anchor="end" class="fd-k fd-k--orange">MARKED FLIGHT LINE</text>
    <g class="fd-pilot"><circle cx="300" cy="306" r="9"/><circle cx="336" cy="306" r="9"/></g>
    <text x="290" y="311" text-anchor="end" class="fd-s">Pilot + instructor</text>
    <g class="fd-people">
      <circle cx="90" cy="356" r="7"/><circle cx="112" cy="356" r="7"/><circle cx="134" cy="356" r="7"/><circle cx="156" cy="356" r="7"/><circle cx="178" cy="356" r="7"/><circle cx="200" cy="356" r="7"/><circle cx="222" cy="356" r="7"/><circle cx="244" cy="356" r="7"/>
      <circle cx="101" cy="378" r="7"/><circle cx="123" cy="378" r="7"/><circle cx="145" cy="378" r="7"/><circle cx="167" cy="378" r="7"/><circle cx="189" cy="378" r="7"/><circle cx="211" cy="378" r="7"/><circle cx="233" cy="378" r="7"/>
    </g>
    <text x="268" y="372" class="fd-s">Students and teacher stay behind the line</text>
    <text x="320" y="404" text-anchor="middle" class="fd-xs">Open ground · at least 100 m × 50 m · not drawn to scale</text>
  </svg>
</figure>"""


def sta_diagram():
    return f"""<div class="sta-loop" data-reveal>
  <svg viewBox="0 0 520 460" role="img" aria-labelledby="sta-svg-title">
    <title id="sta-svg-title">A loop: sense, then think, then act, then sense again</title>
    <path id="sta-ring" d="M260 70 A170 170 0 1 1 259.9 70" class="sta-ring"/>
    <circle r="7" class="sta-dot"><animateMotion dur="6s" repeatCount="indefinite"><mpath href="#sta-ring"/></animateMotion></circle>
    <g class="sta-node"><circle cx="260" cy="70" r="58"/><text x="260" y="78" text-anchor="middle">SENSE</text></g>
    <g class="sta-node"><circle cx="407" cy="325" r="58"/><text x="407" y="333" text-anchor="middle">THINK</text></g>
    <g class="sta-node"><circle cx="113" cy="325" r="58"/><text x="113" y="333" text-anchor="middle">ACT</text></g>
    <text x="260" y="236" text-anchor="middle" class="sta-c1">THE LOOP</text>
    <text x="260" y="262" text-anchor="middle" class="sta-c2">many times a second</text>
  </svg>
</div>"""


def timeline(day, total, rows):
    segs = "".join(f'<span class="tl-seg tl-seg--{ph}" style="flex-grow:{m}" title="{s}: {t}"></span>' for s, d, t, m, ph in rows)
    items = "".join(
        f'<li class="tl-row"><span class="tl-dot tl-dot--{ph}" aria-hidden="true"></span><div><strong>{s}</strong><span>{d}</span></div><span class="tl-time">{t}</span></li>'
        for s, d, t, m, ph in rows)
    return f"""<article class="tl" data-reveal>
  <header class="tl-head"><h3>{day}</h3><span>about {total}</span></header>
  <div class="tl-bar" aria-hidden="true">{segs}</div>
  <ol class="tl-list">{items}</ol>
</article>"""


# ===========================================================================
# HOME
# ===========================================================================
AUDIENCES = [
    ("principals", "Principals &amp; management", "school",
     "A flagship STEM programme with no hassle.",
     ["We bring every tool, part and safety item.",
      "You provide a hall, an open ground and one teacher.",
      "We invoice the institution, not students.",
      "Maps to physics, maths, design-and-technology and computer science (AI)."],
     ("schools.html", "How hosting works")),
    ("teachers", "Teachers &amp; HODs", "presentation",
     "Clear outcomes you can point to.",
     ["Five learning outcomes, from lift and drag to AI.",
      "One instructor for every 12 students, in teams of 4–5.",
      "Slides and worksheets provided.",
      "A follow-up AI project for your Atal Tinkering Lab or computer lab."],
     ("workshop.html", "See outcomes and schedule")),
    ("parents", "Parents", "heart-handshake",
     "Safe, supervised and consent-first.",
     ["Only experienced WingBound pilots fly.",
      "Students stay behind a marked flight line.",
      "LiPo batteries are charged only by instructors, in fire-safe bags.",
      "Signed consent for every student under 18. Photos only with consent."],
     ("safety.html", "Read the safety plan")),
    ("students", "Students", "rocket",
     "You'll build a real aircraft and watch it fly.",
     ["Design and calculate your own trainer.",
      "Cut and assemble a foam-board airframe with your team.",
      "Fit the motor, ESC and servos, and bind the radio.",
      "Try the controls on a trainer link, and get a certificate."],
     ("workshop.html", "What you'll do")),
]


def audience_tabs():
    tabs, panels = [], []
    for i, (key, name, ic, head_, pts, (href, link)) in enumerate(AUDIENCES):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button type="button" role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{icon(ic)}<span>{name}</span></button>')
        hidden = "" if i == 0 else " hidden"
        lis = "".join(f'<li>{icon("check")}<span>{p}</span></li>' for p in pts)
        panels.append(f'<div role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" tabindex="0" class="aud-panel"{hidden}>'
                      f'<h3>{head_}</h3><ul class="check-list">{lis}</ul>'
                      f'<a class="link-arrow" href="{href}">{link} {icon("arrow-right")}</a></div>')
    return f'<div class="aud" data-tabs><div class="aud-tabs" role="tablist" aria-label="Choose who you are">{"".join(tabs)}</div><div class="aud-panels">{"".join(panels)}</div></div>'


home = f"""<section class="hero" aria-labelledby="hero-title">
  {sky("hero")}
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="pill">{icon("map-pin")} On-campus workshops · Andhra Pradesh</span>
      <h1 id="hero-title">
        <span class="silver">Design.</span>
        <span class="silver">Build.</span>
        <span class="orange-text">Fly.</span>
      </h1>
      <p class="hero-sub">A hands-on aeromodelling and AI workshop, run on your campus. Students design, build and fly a real RC aircraft.</p>
    </div>
    <div class="hero-visual">
      <div class="glow" aria-hidden="true"></div>
      <picture>
        <source type="image/webp" srcset="assets/img/plane-760.webp 760w, assets/img/plane-1400.webp 1400w" sizes="(min-width: 900px) 700px, 92vw">
        <img src="assets/img/plane-760.png" width="760" height="419" alt="An orange-and-white RC aerobatic aeroplane" fetchpriority="high">
      </picture>
    </div>
  </div>
  <div class="container">
    <ul class="hud" aria-label="Workshop at a glance">
      <li><span class="hud-k">Duration</span><span class="hud-v">2 days</span><span class="hud-s">or a 1-day option</span></li>
      <li><span class="hud-k">Batch</span><span class="hud-v">30–60</span><span class="hud-s">students, in teams of 4–5</span></li>
      <li><span class="hud-k">Ratio</span><span class="hud-v">1 : 12</span><span class="hud-s">instructor to students</span></li>
      <li><span class="hud-k">Level</span><span class="hud-v">Class 8+</span><span class="hud-s">through engineering &amp; diploma</span></li>
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="why-title">
  <div class="container split split--top">
    <div class="sticky-head">
      {section_head("Why schools choose us", "Real engineering, on your campus, with no hassle", "Students learn by building something that actually flies. You provide the space. We bring everything else.", hid="why-title")}
    </div>
    <div class="pillars">
      <article class="pillar" data-reveal>{badge("hammer")}<div><h3>Learning by doing</h3><p>Physics and maths come alive as students build a real aircraft.</p></div></article>
      <article class="pillar" data-reveal>{badge("brain-circuit")}<div><h3>AI, made real</h3><p>Students see how AI flies smart drones, with a lab project to follow.</p></div></article>
      <article class="pillar" data-reveal>{badge("shield-check")}<div><h3>Safety first</h3><p>Only our pilots fly, students stay behind a marked line, and airspace is checked.</p></div></article>
      <article class="pillar" data-reveal>{badge("package-check")}<div><h3>No hassle</h3><p>We bring every tool and part. The school provides a hall and a ground.</p></div></article>
    </div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="modules-title">
  <div class="glow" aria-hidden="true" style="left:-20%;top:10%"></div>
  {sky("figure8", "sky--faint")}
  <div class="container">
    {section_head("The programme", "Six modules, three stages, one real aircraft", "Each stage builds on the last. By the end of Day 2, every team has built an airframe and watched it fly.", hid="modules-title")}
    <div class="phases">
      <article class="phase" data-reveal>
        <header><span class="phase-n">Stage 1</span><h3 class="phase-word silver">Design.</h3><p>Understand the aeroplane before you build it.</p></header>
        <ol class="mod-list">
          {"".join(f'<li><span class="mod-n">{n}</span><div><strong>{t}</strong><span>{d}</span></div></li>' for n, t, d, _ in MODULES[:4])}
        </ol>
      </article>
      <article class="phase" data-reveal>
        <header><span class="phase-n">Stage 2</span><h3 class="phase-word silver">Build.</h3><p>Turn a flat build plan into a real airframe.</p></header>
        <ol class="mod-list">
          <li><span class="mod-n">05</span><div><strong>Fabrication</strong><span>Build plans for the fuselage, wing and tail.</span></div></li>
          <li><span class="mod-n">{icon("scissors")}</span><div><strong>Mark, cut, assemble</strong><span>Teams of 4–5 build the airframe, with all tools provided.</span></div></li>
          <li><span class="mod-n">{icon("cable")}</span><div><strong>Electronics integration</strong><span>Fit motor, ESC, servos and linkages; bind the radio.</span></div></li>
        </ol>
      </article>
      <article class="phase phase--fly" data-reveal>
        <header><span class="phase-n">Stage 3</span><h3 class="phase-word orange-text">Fly.</h3><p>Check it carefully, then watch it fly.</p></header>
        <ol class="mod-list">
          <li><span class="mod-n">{icon("clipboard-check")}</span><div><strong>Pre-flight checks</strong><span>Centre of gravity, control directions, battery checks.</span></div></li>
          <li><span class="mod-n">{icon("plane-takeoff")}</span><div><strong>Supervised flight demo</strong><span>Our pilots fly; students try the controls on a trainer link.</span></div></li>
          <li><span class="mod-n">{icon("award")}</span><div><strong>Q&amp;A and certificates</strong><span>A certificate for every participant.</span></div></li>
        </ol>
      </article>
    </div>
    <a class="ai-strip" href="ai-aviation.html" data-reveal>
      <span class="mod-n mod-n--lg">06</span>
      <span class="ai-strip-copy"><strong>AI &amp; aviation</strong><span>How AI makes aircraft smarter and helps people, with a lab project to follow.</span></span>
      <span class="ai-strip-go">Explore {icon("arrow-right")}</span>
    </a>
    <div class="btn-row mt-2"><a class="btn btn--ghost" href="workshop.html#schedule">See the full 2-day schedule {icon("arrow-right")}</a></div>
  </div>
</section>

<section class="section section--blueprint" aria-labelledby="trainer-title">
  <div class="container split">
    <div>
      {section_head("Meet the trainer", "The aircraft every team builds", "A foam-board trainer, cut from a scaled build plan and fitted with real RC electronics. Built in two days.", hid="trainer-title")}
      <ul class="spec-chips" data-reveal>
        <li><span>Airframe</span><strong>Foam board</strong></li>
        <li><span>Power</span><strong>Electric motor</strong></li>
        <li><span>Control</span><strong>RC radio</strong></li>
        <li><span>Build time</span><strong>2 days</strong></li>
      </ul>
      <a class="link-arrow mt-2" href="workshop.html#aircraft">More about the build {icon("arrow-right")}</a>
    </div>
    <div data-reveal>{blueprint(compact=True)}</div>
  </div>
</section>

<section class="section section--white" aria-labelledby="aud-title">
  <div class="container">
    {section_head("Made for everyone on campus", "What it means for you", "", hid="aud-title")}
    {audience_tabs()}
  </div>
</section>

{proof_section()}

<section class="section section--white" aria-labelledby="faq-teaser-title">
  <div class="container split split--top">
    <div class="sticky-head">
      {section_head("Good questions", "Before you ask", "Short answers to what principals and parents ask us most.", hid="faq-teaser-title")}
      <a class="link-arrow" href="faq.html">All questions {icon("arrow-right")}</a>
    </div>
    {faq_list(["Is it safe?", "Do students fly the plane?", "What does the school need to provide?", "Which classes can join?"])}
  </div>
</section>

{cta_band()}
"""

# ===========================================================================
# WORKSHOP
# ===========================================================================
DAY1 = [
    ("Flight basics", "Forces of flight, lift, airfoils, types of RC planes", "1 hr", 60, "design"),
    ("Anatomy &amp; control", "Aircraft parts, control surfaces, stability", "45 min", 45, "design"),
    ("Electronics &amp; power", "Motor, ESC, servos, LiPo battery, radio", "1 hr 15 min", 75, "design"),
    ("Materials &amp; design", "Build materials and sizing a trainer aircraft", "1 hr", 60, "design"),
    ("Fabrication I", "Mark and cut parts", "1 hr 30 min", 90, "build"),
]
DAY2 = [
    ("Fabrication II", "Assemble the airframe", "2 hr 30 min", 150, "build"),
    ("Electronics integration", "Fit motor, ESC, servos and linkages; bind the radio", "1 hr 30 min", 90, "build"),
    ("Pre-flight checks", "Centre of gravity, control directions, battery checks", "30 min", 30, "fly"),
    ("Flight demo &amp; closing", "Supervised flight, Q&amp;A, certificates", "1 hr 30 min", 90, "fly"),
]
GETS = [
    ("calculator", "Design and calculate their own trainer"),
    ("wind", "Aerodynamics"),
    ("radio", "Avionics"),
    ("battery-charging", "Power systems"),
    ("users", "Hands-on team build, all tools provided"),
    ("plane-takeoff", "Live flight demo on campus"),
    ("brain-circuit", "AI in aviation"),
    ("award", "Certificate for every participant"),
]
OUTCOMES = [
    "Explain how an aeroplane flies: lift, weight, thrust, drag and the control surfaces",
    "Identify each electronic part and how they connect",
    "Cut and assemble a foam-board airframe from a scaled build plan",
    "Watch their team's aircraft fly, and try the controls on a trainer link under supervision",
    "Explain how AI makes aircraft smarter, and where AI-powered drones already help people",
]

workshop = f"""{page_hero("The Workshop", "Two days from theory to take-off", "Students learn how aeroplanes fly, build a real RC aircraft in teams, and watch it fly on their own campus.",
    [("Duration", "2 days"), ("Teams", "4–5 students"), ("Ratio", "1 : 12"), ("Every student", "Certificate")], "The Workshop")}

<section class="section section--white" aria-labelledby="outcomes-title">
  <div class="container split split--top">
    <div>
      {section_head("Learning outcomes", "By the end, every student can…", hid="outcomes-title")}
      <ol class="outcomes">
        {"".join(f'<li data-reveal><span class="oc-n">{i}</span><span>{o}</span></li>' for i, o in enumerate(OUTCOMES, 1))}
      </ol>
    </div>
    <div class="card card--tint" data-reveal>
      <h3>Linked to the curriculum</h3>
      <p>The workshop maps to four subjects students already study.</p>
      <ul class="subject-grid">
        <li>{icon("atom")}<span>Physics</span></li>
        <li>{icon("sigma")}<span>Mathematics</span></li>
        <li>{icon("pencil-ruler")}<span>Design &amp; technology</span></li>
        <li>{icon("brain-circuit")}<span>Computer science (AI)</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="forces-title">
  <div class="container">
    {section_head("A taste of Module 01", "Four forces, one aeroplane", "Tap each force to see what it does. Students learn these first, then feel them at work on flight day.", hid="forces-title")}
    <div data-reveal>{forces_diagram()}</div>
  </div>
</section>

<section class="section section--white" id="schedule" aria-labelledby="schedule-title">
  <div class="container">
    {section_head("2-day schedule", "The full programme", "Day 1 builds understanding and starts fabrication. Day 2 finishes the build and ends with a flight demo.", hid="schedule-title")}
    <ul class="phase-legend" aria-label="Stages">
      <li><span class="tl-dot tl-dot--design"></span>Design</li>
      <li><span class="tl-dot tl-dot--build"></span>Build</li>
      <li><span class="tl-dot tl-dot--fly"></span>Fly</li>
    </ul>
    <div class="tl-grid">
      {timeline("Day 1", "5½ hours", DAY1)}
      {timeline("Day 2", "6 hours", DAY2)}
    </div>
    <div class="callout callout--orange mt-2" data-reveal>
      {badge("clock", "badge--solid")}
      <div>
        <h3>Short on time? Choose the 1-day version</h3>
        <p>Theory, a live build demo and a flight demo, without student fabrication.</p>
      </div>
      <a class="btn btn--outline" href="{CONTACT}?package=1day">Ask about 1-day</a>
    </div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="wiring-title">
  <div class="glow" aria-hidden="true" style="right:-25%;top:-10%"></div>
  <div class="container">
    {section_head("Module 03 · Electronics &amp; power", "How the parts connect", "A quick look at the parts inside. Students learn how each one works, and fit them all on Day 2.", hid="wiring-title")}
    <div data-reveal>{wiring_diagram()}</div>
  </div>
</section>

<section class="section section--blueprint" id="aircraft" aria-labelledby="aircraft-title">
  <div class="container">
    {section_head("The aircraft", "A real trainer, built by students", "Each team builds a foam-board trainer from a scaled build plan.", hid="aircraft-title")}
    <div class="split">
      <div data-reveal>{blueprint()}</div>
      <div class="pillars">
        <article class="pillar" data-reveal>{badge("layers")}<div><h3>A foam-board airframe</h3><p>Cut and assembled by each team from a scaled build plan.</p></div></article>
        <article class="pillar" data-reveal>{badge("cpu")}<div><h3>Real RC electronics</h3><p>A motor, servos, a battery and a radio, the same kind of kit RC pilots fly with.</p></div></article>
        <article class="pillar" data-reveal>{badge("users")}<div><h3>Built in teams</h3><p>Teams of 4–5 build their aircraft over two days, with all tools provided.</p></div></article>
        <article class="pillar" data-reveal>{badge("plane-takeoff")}<div><h3>Flown on your campus</h3><p>Our pilots fly it in a supervised demo on your ground.</p></div></article>
      </div>
    </div>
  </div>
</section>

<section class="section section--white" aria-labelledby="gets-title">
  <div class="container">
    {section_head("What students get", "Skills they can see, touch and fly", hid="gets-title")}
    <ul class="gets">
      {"".join(f'<li data-reveal>{badge(i)}<span>{t}</span></li>' for i, t in GETS)}
    </ul>
  </div>
</section>

{cta_band("Give your students a real build", "Pick the 2-day build workshop or the 1-day version. We will plan it around your calendar.")}
"""

COURSE_LD = {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "WingBound RC aircraft and AI workshop",
    "description": "A hands-on aeromodelling workshop run on school and college campuses. Students learn the forces of flight, electronics and design, build a foam-board RC trainer in teams, and watch it fly.",
    "provider": {"@type": "EducationalOrganization", "name": "WingBound", "url": SITE_URL + "/"},
    "educationalLevel": "Class 8 through engineering and diploma",
    "teaches": [html.unescape(o) for o in OUTCOMES],
    "inLanguage": "en-IN",
    "hasCourseInstance": [
        {"@type": "CourseInstance", "courseMode": "Onsite", "name": "2-day build workshop", "location": {"@type": "Place", "name": "Your campus, Andhra Pradesh"}},
        {"@type": "CourseInstance", "courseMode": "Onsite", "name": "1-day workshop", "location": {"@type": "Place", "name": "Your campus, Andhra Pradesh"}},
    ],
}

# ===========================================================================
# AI & AVIATION
# ===========================================================================
BETTER = [
    ("scale", "Self-levelling", "The plane returns to level flight when the pilot lets go of the sticks."),
    ("sliders-horizontal", "Auto-tuning", "The flight controller adjusts its own settings for smoother control."),
    ("house", "Return to home", "With GPS, the aircraft can fly itself back if the radio signal is lost."),
    ("scan-eye", "Obstacle detection", "A camera and AI model spot obstacles in the flight path."),
    ("chart-line", "Predicting failures", "Patterns in flight logs warn of a weak battery or failing motor early."),
    ("drafting-compass", "Smarter design", "Simulation tests many wing and tail shapes before anything is built."),
]
HELP = [
    ("sprout", "Agriculture", "Spotting crop stress and spraying only where it is needed."),
    ("life-buoy", "Search &amp; rescue", "Searching large areas quickly after floods and disasters."),
    ("heart-pulse", "Medical delivery", "Carrying vaccines and medicines to hard-to-reach health centres."),
    ("building-2", "Infrastructure inspection", "Checking bridges, power lines and towers without risky climbs."),
    ("trees", "Environment &amp; wildlife", "Counting animals and mapping forests and coastlines."),
    ("plane", "Airline safety", "Analysing flight data to find risks before they cause problems."),
]
ai = f"""{page_hero("AI &amp; Aviation", "AI is the co-pilot. You are the pilot.", "Students see how sensors, flight controllers and AI make aircraft smarter, and where drones already help people across India.",
    [("Module", "06"), ("Tools", "Free &amp; open source"), ("Runs in", "ATL or computer lab"), ("Ends with", "A science-fair project")], "AI &amp; Aviation")}

<section class="section section--white" aria-labelledby="sta-title">
  <div class="container split">
    <div>
      {section_head("How a smart aircraft works", "Sense. Think. Act.", "Every smart aircraft runs the same loop, over and over.", hid="sta-title")}
      <ol class="sta-steps">
        <li data-reveal>{badge("radar")}<div><h3>Sense</h3><p>Sensors (gyro, accelerometer, GPS, barometer, camera) measure what the plane is doing.</p></div></li>
        <li data-reveal>{badge("cpu")}<div><h3>Think</h3><p>A flight controller decides how to move the controls.</p></div></li>
        <li data-reveal>{badge("cog")}<div><h3>Act</h3><p>The same servos and ESC that students fit carry out each decision.</p></div></li>
      </ol>
    </div>
    {sta_diagram()}
  </div>
</section>

<section class="section" aria-labelledby="vs-title">
  <div class="container">
    {section_head("Key point", "Autopilot is not the same as AI", hid="vs-title", center=True)}
    <div class="versus" data-reveal>
      <div class="vs-card"><span class="vs-k">Autopilot</span><p>Follows rules <strong>we program</strong>.</p></div>
      <span class="vs-mid" aria-hidden="true">vs</span>
      <div class="vs-card vs-card--ai"><span class="vs-k">AI</span><p>Learns patterns <strong>from data</strong>.</p></div>
    </div>
  </div>
</section>

<section class="section section--white" aria-labelledby="better-title">
  <div class="container">
    {section_head("In the air", "How AI makes RC planes better", hid="better-title")}
    <div class="grid grid-3">
      {"".join(f'<article class="card" data-reveal>{badge(i)}<h3>{t}</h3><p>{d}</p></article>' for i, t, d in BETTER)}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="help-title">
  <div class="container">
    {section_head("On the ground", "Where AI and drones help people", hid="help-title")}
    <div class="grid grid-3">
      {"".join(f'<article class="card card--flat" data-reveal>{badge(i)}<h3>{t}</h3><p>{d}</p></article>' for i, t, d in HELP)}
    </div>
    <article class="feature" data-reveal>
      <div class="feature-copy">
        <span class="label">Close to home</span>
        <h3>Medicine from the Sky, Telangana</h3>
        <p>Telangana's "Medicine from the Sky" project began in Vikarabad in September 2021. The first drone carried vaccines to a health centre.</p>
      </div>
      <ul class="feature-stats">
        <li><span class="big">5 kg</span><span>of vaccines</span></li>
        <li><span class="big">3 km</span><span>to the health centre</span></li>
        <li><span class="big">10 min</span><span>flight time</span></li>
      </ul>
    </article>
  </div>
</section>

<section class="section section--dark" aria-labelledby="copilot-title">
  <div class="glow" aria-hidden="true" style="left:30%;top:-30%"></div>
  <div class="container split">
    <div data-reveal>
      <span class="label">Our message to students</span>
      <p class="quote" id="copilot-title"><span class="silver">AI is the co-pilot.</span><br><span class="orange-text">You are the pilot.</span></p>
      <p>AI can help, but the person flying is always responsible. We teach students to understand the technology and to use it with care.</p>
    </div>
    <div class="showcase">
      <div class="glow" aria-hidden="true"></div>
      <picture>
        <source type="image/webp" srcset="assets/img/plane-760.webp 760w, assets/img/plane-1400.webp 1400w" sizes="(min-width: 960px) 560px, 92vw">
        <img src="assets/img/plane-760.png" width="760" height="419" alt="" loading="lazy">
      </picture>
    </div>
  </div>
</section>

<section class="section section--white" aria-labelledby="path-title">
  <div class="container">
    {section_head("After the workshop", "A student project path", "The workshop is the start. Students can take the next steps in your Atal Tinkering Lab or computer lab.", hid="path-title")}
    <ol class="steps">
      <li data-reveal><h3>Fly the basic plane</h3><p>Start with the trainer built in the workshop.</p></li>
      <li data-reveal><h3>Add a flight controller</h3><p>Fit a controller running open-source ArduPilot or INAV, with GPS.</p></li>
      <li data-reveal><h3>Log flight data</h3><p>Record what the sensors measure on every flight.</p></li>
      <li data-reveal><h3>Train a simple model</h3><p>Find patterns in the data and present the project at a science fair.</p></li>
    </ol>
    <div class="tools" data-reveal>
      <h3>Free tools to start with</h3>
      <ul>
        <li><a href="https://ardupilot.org/" target="_blank" rel="noopener"><strong>ArduPilot</strong><span>Open-source autopilot</span>{icon("arrow-up-right")}</a></li>
        <li><a href="https://ardupilot.org/planner/" target="_blank" rel="noopener"><strong>Mission Planner</strong><span>Ground station for ArduPilot</span>{icon("arrow-up-right")}</a></li>
        <li><a href="https://github.com/iNavFlight/inav" target="_blank" rel="noopener"><strong>INAV</strong><span>Open-source flight controller firmware</span>{icon("arrow-up-right")}</a></li>
        <li><a href="https://teachablemachine.withgoogle.com/" target="_blank" rel="noopener"><strong>Teachable Machine</strong><span>Train a simple model in the browser</span>{icon("arrow-up-right")}</a></li>
      </ul>
    </div>
  </div>
</section>

{cta_band("Bring AI and aviation to your lab", "Start with the workshop. Leave with a project your students can grow in your Atal Tinkering Lab or computer lab.")}
"""

# ===========================================================================
# SAFETY
# ===========================================================================
safety = f"""{page_hero("Safety", "Safety comes first, every time", "Clear rules for flying, batteries, tools and supervision, so principals and parents can say yes with confidence.",
    [("Who flies", "Only our pilots"), ("Altitude", "Below 400 ft"), ("Range", "Line of sight"), ("Under 18", "Signed consent")], "Safety")}

<section class="section section--white" aria-labelledby="line-title">
  <div class="container split">
    <div>
      {section_head("On flight day", "Pilots fly. Students watch from behind the line.", hid="line-title")}
      <div class="prose" data-reveal>
        <p class="lead muted">The flight demo happens on an open ground of at least 100 m × 50 m. Before we confirm a date, we visit to check the ground and look up your campus on the DGCA Digital Sky airspace map.</p>
        <p class="muted">Students who want to try the controls do so on a trainer link. The instructor holds the master radio and can take over at any moment.</p>
      </div>
    </div>
    {field_diagram()}
  </div>
</section>

<section class="section" aria-labelledby="rules-title">
  <div class="container">
    {section_head("Our rules", "Three layers of safety", hid="rules-title")}
    <div class="grid grid-3">
      <article class="card rules" data-reveal>
        {badge("plane")}
        <h3>Flying</h3>
        <ul class="check-list">
          <li>{icon("check")}<span>Only experienced WingBound pilots fly. Students stay behind a marked flight line.</span></li>
          <li>{icon("check")}<span>The aircraft (about 800 g) is flown within line of sight, below 400 ft.</span></li>
          <li>{icon("check")}<span>We check your campus on the DGCA Digital Sky airspace map before confirming a date.</span></li>
          <li>{icon("check")}<span>Students try the controls only through a trainer link the instructor can override.</span></li>
          <li>{icon("check")}<span>No flying over people, buildings or roads.</span></li>
        </ul>
      </article>
      <article class="card rules" data-reveal>
        {badge("battery-charging")}
        <h3>Batteries &amp; tools</h3>
        <ul class="check-list">
          <li>{icon("check")}<span>LiPo batteries are charged only by instructors, in fire-safe bags.</span></li>
          <li>{icon("check")}<span>Propellers are fitted only for the flight demo.</span></li>
          <li>{icon("check")}<span>Safety glasses for cutting.</span></li>
          <li>{icon("check")}<span>A supervised glue station.</span></li>
        </ul>
      </article>
      <article class="card rules" data-reveal>
        {badge("users")}
        <h3>People &amp; paperwork</h3>
        <ul class="check-list">
          <li>{icon("check")}<span>First-aid kit on site.</span></li>
          <li>{icon("check")}<span>A school teacher present throughout.</span></li>
          <li>{icon("check")}<span>Signed parental consent for every student under 18.</span></li>
          <li>{icon("check")}<span>Student photos are shared only with parental consent.</span></li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="section section--white" aria-labelledby="before-title">
  <div class="container">
    {section_head("Before the date", "What we check before anyone flies", hid="before-title")}
    <ol class="steps">
      <li data-reveal><h3>Airspace check</h3><p>We look up your campus on the DGCA Digital Sky airspace map before confirming a date.</p></li>
      <li data-reveal><h3>Site visit</h3><p>We visit to check the hall and the ground.</p></li>
      <li data-reveal><h3>Consent forms</h3><p>The school shares consent forms with parents. Every student under 18 needs one signed.</p></li>
      <li data-reveal><h3>On the day</h3><p>First-aid kit on site, a teacher present, and propellers fitted only for the flight demo.</p></li>
    </ol>
  </div>
</section>

{cta_band("Questions about safety?", "We are happy to walk your principal, staff or parent committee through our safety plan before you book.")}
"""

# ===========================================================================
# SCHOOLS
# ===========================================================================
WE_BRING = [("cpu", "All electronics"), ("layers", "Airframe materials"), ("file-text", "Build plans"), ("wrench", "Tools"),
            ("glasses", "Safety glasses"), ("flame", "Fire-safe battery bags"), ("presentation", "Slides and worksheets"), ("award", "Certificates")]
YOU_PROVIDE = [("armchair", "A hall or lab with tables and power sockets"), ("projector", "A projector"),
               ("land-plot", "An open ground at least 100 m × 50 m"), ("user-check", "One teacher present throughout"),
               ("file-pen-line", "Signed consent forms")]
downloads = ""
if HAS_PROPOSAL or HAS_FLYER:
    downloads = '<div class="btn-row mt-2">' + (
        f'<a class="btn btn--outline" href="{PROPOSAL}" download>{icon("file-text")} Download proposal (PDF)</a>' if HAS_PROPOSAL else "") + (
        f'<a class="btn btn--outline" href="{FLYER}" download>{icon("file-image")} Download flyer (PDF)</a>' if HAS_FLYER else "") + "</div>"

schools = f"""{page_hero("For Schools &amp; Colleges", "Easy to host. Hard to forget.", "We bring every tool and part. You provide a hall, a ground and a teacher. Here is how it works.",
    [("We bring", "Everything"), ("Minimum", "30 students"), ("Invoice to", "The institution"), ("Area", "Andhra Pradesh")], "For Schools &amp; Colleges")}

<section class="section section--white" aria-labelledby="provide-title">
  <div class="container">
    {section_head("Who provides what", "A clear split, agreed up front", hid="provide-title")}
    <div class="provide">
      <article class="provide-col provide-col--us" data-reveal>
        <h3>{icon("package-check")} We bring</h3>
        <ul>{"".join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in WE_BRING)}</ul>
      </article>
      <article class="provide-col" data-reveal>
        <h3>{icon("school")} The school provides</h3>
        <ul>{"".join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in YOU_PROVIDE)}</ul>
      </article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="how-title">
  <div class="container">
    {section_head("How booking works", "Four simple steps", hid="how-title")}
    <ol class="steps">
      <li data-reveal><h3>Choose</h3><p>Choose a package and dates.</p></li>
      <li data-reveal><h3>Site visit</h3><p>We visit to check the hall and ground.</p></li>
      <li data-reveal><h3>Paperwork</h3><p>We send an agreement and invoice. The school shares consent forms with parents.</p></li>
      <li data-reveal><h3>Workshop</h3><p>We run the workshop and share photos and certificates.</p></li>
    </ol>
  </div>
</section>

<section class="section section--white" aria-labelledby="packages-title">
  <div class="container">
    {section_head("Packages", "Pick the format that fits your term", hid="packages-title")}
    <div class="packages">
      <article class="package" data-reveal>
        <header><span class="pkg-k">1 day</span><h3>1-day workshop</h3><p>Theory, a live build demo and a flight demo, without student fabrication.</p></header>
        <ul class="check-list">
          <li>{icon("check")}<span>Theory: how aeroplanes fly, the parts and the electronics</span></li>
          <li>{icon("check")}<span>Live build demo by our team</span></li>
          <li>{icon("check")}<span>Flight demo on your ground</span></li>
          <li>{icon("check")}<span>Certificate for every participant</span></li>
        </ul>
        <p class="price">Contact us for pricing</p>
        <a class="btn btn--outline btn--block" href="{CONTACT}?package=1day">Ask about 1-day</a>
      </article>
      <article class="package package--featured" data-reveal>
        <span class="pill pkg-tag">{icon("star")} Full experience</span>
        <header><span class="pkg-k">2 days</span><h3>2-day build workshop</h3><p>Students build their own team aircraft and watch it fly.</p></header>
        <ul class="check-list">
          <li>{icon("check")}<span>Theory, from flight basics to materials and design</span></li>
          <li>{icon("check")}<span>Team build in groups of 4–5, all tools provided</span></li>
          <li>{icon("check")}<span>Electronics integration and pre-flight checks</span></li>
          <li>{icon("check")}<span>Supervised flight demo, Q&amp;A and certificates</span></li>
        </ul>
        <p class="price">Contact us for pricing</p>
        <a class="btn btn--primary btn--block" href="{CONTACT}?package=2day">Ask about 2-day</a>
      </article>
    </div>
    <ul class="terms" data-reveal>
      <li>{icon("receipt")}<span>We invoice the institution, not students.</span></li>
      <li>{icon("users")}<span>Minimum 30 students.</span></li>
      <li>{icon("wallet")}<span>50% on booking, 50% within 7 days after the workshop.</span></li>
    </ul>
    {downloads}
  </div>
</section>

{cta_band()}
"""

# ===========================================================================
# ABOUT
# ===========================================================================
about = f"""{page_hero("About us", "Four pilots. Ten years. One mission.", "We are a team of four RC aircraft builders and pilots from Visakhapatnam. We want every student to feel what it is like to build something that flies.", None, "About us")}

<section class="section section--white" aria-labelledby="story-title">
  <div class="container split split--top">
    <div class="prose" data-reveal>
      <span class="label">Our story</span>
      <h2 id="story-title">From hobby to classroom</h2>
      <p>For 10 years we have designed, built and flown RC aircraft. Along the way we competed in, and won, multiple competitions organised by Boeing in partnership with IIT Madras, NIT Warangal and Vignan University.</p>
      <p>We started WingBound to share that experience with students. We have run workshops at Vignan's Institute of Information Technology in Visakhapatnam and at Malla Reddy College of Engineering and Technology in Hyderabad.</p>
      <p>Today we bring the full workshop to school and college campuses across Andhra Pradesh.</p>
    </div>
    <ul class="facts" data-reveal>
      <li><span class="facts-k">Based in</span><strong>Visakhapatnam</strong></li>
      <li><span class="facts-k">Team</span><strong>Four builders and pilots</strong></li>
      <li><span class="facts-k">Experience</span><strong>10 years of RC aircraft</strong></li>
      <li><span class="facts-k">We serve</span><strong>Schools and colleges across Andhra Pradesh</strong></li>
    </ul>
  </div>
</section>

{proof_section("about-record-title")}

<section class="section section--white" aria-labelledby="team-title">
  <div class="container">
    {section_head("The team", "Meet the people who fly", hid="team-title")}
    <div class="team">
      <article class="person" data-reveal>
        <div class="avatar" aria-hidden="true">NK</div>
        <h3>Nikhil Kalyan</h3>
        <div class="person-links"><a href="tel:{PHONE_1[1]}" aria-label="Call Nikhil">{icon("phone")}</a><a href="mailto:{PHONE_1[3]}" aria-label="Email Nikhil">{icon("mail")}</a></div>
      </article>
      <article class="person" data-reveal>
        <div class="avatar" aria-hidden="true">TP</div>
        <h3>Thoran Prakash</h3>
        <div class="person-links"><a href="tel:{PHONE_2[1]}" aria-label="Call Thoran">{icon("phone")}</a><a href="mailto:{PHONE_2[3]}" aria-label="Email Thoran">{icon("mail")}</a></div>
      </article>
      <article class="person" data-reveal>
        <div class="avatar" aria-hidden="true">SV</div>
        <h3>Sai Supreeth Varma</h3>
        <div class="person-links"><a href="tel:{PHONE_3[1]}" aria-label="Call Sai">{icon("phone")}</a></div>
      </article>
      <article class="person person--todo" data-reveal>
        <div class="avatar" aria-hidden="true">{icon("user")}</div>
        <h3>[Team member 4]</h3>
        <p class="role">[Name and role to be added]</p>
      </article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="values-title">
  <div class="container">
    {section_head("How we work", "What you can expect from us", hid="values-title")}
    <div class="grid grid-3">
      <article class="card" data-reveal>{badge("hand")}<h3>Hands-on</h3><p>Students learn by cutting, building and wiring, not just by watching slides.</p></article>
      <article class="card" data-reveal>{badge("shield-check")}<h3>Careful</h3><p>Only our pilots fly, and every step follows a clear <a href="safety.html">safety plan</a>.</p></article>
      <article class="card" data-reveal>{badge("handshake")}<h3>Easy to work with</h3><p>We bring everything, agree the plan up front and invoice the institution.</p></article>
    </div>
  </div>
</section>

{cta_band()}
"""

# ===========================================================================
# GALLERY
# ===========================================================================
gallery = f"""{page_hero("Gallery", "From the workshop floor", "Photos from our workshops are on their way.", None, "Gallery")}

<section class="section section--white" aria-labelledby="gallery-title">
  <div class="container">
    <div class="soon" data-reveal>
      <svg class="soon-art" viewBox="0 0 320 160" aria-hidden="true" focusable="false">
        <path d="M10 130 C 80 130, 120 60, 200 60 S 300 30, 310 20" class="soon-trail"/>
        <use href="#rc-plane" x="276" y="2" width="44" height="44" transform="rotate(-20 298 24)" class="soon-plane"/>
      </svg>
      <h2 id="gallery-title">Photos are on their way</h2>
      <p>We are putting together photos from our workshops. Student photos are shared only with parental consent.</p>
      <div class="btn-row center-row">
        <a class="btn btn--primary" href="{CONTACT}">Host a workshop {icon("arrow-right")}</a>
        <a class="btn btn--outline" href="workshop.html">See what happens on the day</a>
      </div>
    </div>
  </div>
</section>

{cta_band()}
"""

# ===========================================================================
# CONTACT
# ===========================================================================
contact = f"""{page_hero("Contact us", "Let's connect", "Schools, colleges, students and parents are all welcome. Tell us what you are interested in and send it to us by email or WhatsApp.", None, "Contact us")}

<section class="section" aria-labelledby="form-title">
  <div class="container contact-grid">
    <div class="card card--form">
      <h2 id="form-title" class="sub-head">Show your interest</h2>
      <p class="muted">Fill in a few details, then choose how to send them. Your email app or WhatsApp opens with the message ready to send.</p>
      <form id="contact-form" class="form" action="mailto:{PHONE_1[3]}" method="post" enctype="text/plain" novalidate data-wa="{WHATSAPP}" data-to="{PHONE_1[3]}" data-cc="{PHONE_2[3]}">
        <div class="form-row">
          <div class="field">
            <label for="name">Your name <span class="req" aria-hidden="true">*</span></label>
            <input id="name" name="name" type="text" autocomplete="name" required aria-describedby="name-err">
            <span class="field-err" id="name-err">Please tell us your name.</span>
          </div>
          <div class="field">
            <label for="who">I am</label>
            <select id="who" name="who">
              <option>An individual / student</option>
              <option>A parent</option>
              <option>From a school</option>
              <option>From a college</option>
              <option>Other</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="organisation">School, college or organisation <span class="opt">(optional)</span></label>
            <input id="organisation" name="organisation" type="text" autocomplete="organization">
          </div>
          <div class="field">
            <label for="city">City <span class="opt">(optional)</span></label>
            <input id="city" name="city" type="text" autocomplete="address-level2">
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="phone">Phone <span class="opt">(optional)</span></label>
            <input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" pattern="[0-9+\\(\\)\\s\\-]{{10,16}}" aria-describedby="phone-err">
            <span class="field-err" id="phone-err">Use 10 to 16 digits, e.g. +91 98765 43210.</span>
          </div>
          <div class="field">
            <label for="email">Email <span class="opt">(optional)</span></label>
            <input id="email" name="email" type="email" autocomplete="email" aria-describedby="email-err">
            <span class="field-err" id="email-err">Please check the email address.</span>
          </div>
        </div>
        <fieldset class="field">
          <legend>Interested in</legend>
          <div class="choice-row" id="interest-group">
            <label class="choice"><input type="radio" name="interest" value="Workshops in general" checked><span>Workshops in general</span></label>
            <label class="choice"><input type="radio" name="interest" value="2-day build workshop" data-key="2day"><span>2-day build workshop</span></label>
            <label class="choice"><input type="radio" name="interest" value="1-day workshop" data-key="1day"><span>1-day workshop</span></label>
            <label class="choice"><input type="radio" name="interest" value="AI and drones"><span>AI and drones</span></label>
            <label class="choice"><input type="radio" name="interest" value="Something else"><span>Something else</span></label>
          </div>
        </fieldset>
        <div class="field">
          <label for="message">Message <span class="req" aria-hidden="true">*</span></label>
          <textarea id="message" name="message" rows="4" required aria-describedby="message-err" placeholder="e.g. We would like a workshop for about 40 students in December."></textarea>
          <span class="field-err" id="message-err">Please add a short message.</span>
        </div>
        <p class="form-small">Nothing is stored on this website. Your message goes straight from your email or WhatsApp to us.</p>
        <div class="send-row">
          <button class="btn btn--whatsapp btn--lg" type="submit" name="via" value="whatsapp">{WA_SVG} Send on WhatsApp</button>
          <button class="btn btn--outline btn--lg" type="submit" name="via" value="email">{icon("mail")} Send by email</button>
        </div>
        <div id="form-status" class="form-status" role="status" aria-live="polite"></div>
      </form>
    </div>

    <div class="contact-side">
      <div class="card">
        <h2 class="sub-head">Or reach us directly</h2>
        <ul class="direct">
          <li><a href="tel:{PHONE_1[1]}">{badge("phone")}<span><strong>Call {PHONE_1[0]}</strong>{PHONE_1[2]}</span></a></li>
          <li><a href="{wa_link()}" target="_blank" rel="noopener"><span class="badge badge--wa">{WA_SVG}</span><span><strong>WhatsApp</strong>{PHONE_1[2]}</span></a></li>
          <li><a href="mailto:{PHONE_1[3]}">{badge("mail")}<span><strong>Email {PHONE_1[0].split()[0]}</strong>{PHONE_1[3]}</span></a></li>
          <li><a href="tel:{PHONE_2[1]}">{badge("phone")}<span><strong>Call {PHONE_2[0]}</strong>{PHONE_2[2]}</span></a></li>
          <li><a href="mailto:{PHONE_2[3]}">{badge("mail")}<span><strong>Email {PHONE_2[0].split()[0]}</strong>{PHONE_2[3]}</span></a></li>
          <li><a href="tel:{PHONE_3[1]}">{badge("phone")}<span><strong>Call {PHONE_3[0]}</strong>{PHONE_3[2]}</span></a></li>
        </ul>
      </div>
      <div class="card">
        <h2 class="sub-head">For schools and colleges</h2>
        <ol class="mini-steps">
          <li><strong>We get in touch</strong> to talk through the package and dates.</li>
          <li><strong>We visit your campus</strong> to check the hall and ground.</li>
          <li><strong>Agreement and invoice</strong>, and you share consent forms with parents.</li>
          <li><strong>Workshop day</strong>, then photos and certificates.</li>
        </ol>
      </div>
      <div class="card card--tint">
        <h2 class="sub-head">{icon("map-pin")} Service area</h2>
        <p class="mt-0">Campuses across Andhra Pradesh. We are based in Visakhapatnam.</p>
      </div>
    </div>
  </div>
</section>
"""

# ===========================================================================
# FAQ
# ===========================================================================
faq_groups = "".join(
    f'<div class="faq-group"><h2 class="sub-head" data-reveal>{g}</h2>{faq_list([q for q, _, _ in items])}</div>' for g, items in FAQS)
faq = f"""{page_hero("FAQ", "Questions, answered", "Short answers for principals, teachers, parents and students. If you have another question, call or WhatsApp us.", None, "FAQ")}

<section class="section" aria-label="Frequently asked questions">
  <div class="container faq-wrap">
    {faq_groups}
  </div>
</section>

{cta_band("Still have a question?", f"Call or WhatsApp Nikhil on {PHONE_1[2]}, or send us a message by email or WhatsApp.")}
"""
FAQ_LD = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": p}}
                   for _, items in FAQS for q, _, p in items],
}

# ===========================================================================
# 404
# ===========================================================================
not_found = f"""<section class="page-hero page-hero--404">
  <div class="glow" aria-hidden="true"></div>
  {sky("page")}
  <div class="container center">
    <span class="label">Error 404</span>
    <h1>Lost in the clouds</h1>
    <p class="page-hero-sub">We could not find that page. Let's get you back on course.</p>
    <div class="btn-row center-row mt-2">
      <a class="btn btn--primary" href="index.html">Back to home {icon("arrow-right")}</a>
      <a class="btn btn--ghost" href="{CONTACT}">{CTA_LABEL}</a>
    </div>
  </div>
</section>
"""

# ===========================================================================
# Write everything
# ===========================================================================
PAGES = [
    ("index.html", "Aeromodelling Workshop for Schools &amp; Colleges | WingBound",
     "WingBound runs hands-on aeromodelling and AI workshops on school and college campuses in Andhra Pradesh. Students design, build and fly a real RC aircraft.",
     home, ORG_LD),
    ("workshop.html", "RC Aircraft Workshop: 2-Day Schedule &amp; Outcomes | WingBound",
     "A 2-day RC aircraft workshop for schools and colleges: flight basics, electronics, a team foam-board build and a live flight demo. A 1-day option is also available.",
     workshop, [COURSE_LD, crumbs("The Workshop", "workshop.html")]),
    ("ai-aviation.html", "Drone and AI Workshop for Students | WingBound",
     "How AI makes aircraft smarter: sense, think, act. A drone and AI workshop for students, with a follow-up project using ArduPilot, INAV and Teachable Machine.",
     ai, crumbs("AI & Aviation", "ai-aviation.html")),
    ("safety.html", "Safety at Our RC Aircraft Workshops | WingBound",
     "How WingBound keeps students safe: only our pilots fly, a marked flight line, DGCA Digital Sky airspace checks, LiPo battery safety and parental consent.",
     safety, crumbs("Safety", "safety.html")),
    ("schools.html", "Host an Aeromodelling Workshop at Your School | WingBound",
     "What WingBound brings, what the school provides, how booking works, and our 1-day and 2-day aeromodelling workshop packages for schools and colleges.",
     schools, crumbs("For Schools & Colleges", "schools.html")),
    ("about.html", "About WingBound | RC Aircraft Pilots from Visakhapatnam",
     "WingBound is a team of four RC aircraft builders and pilots from Visakhapatnam with 10 years of experience and multiple competition wins.",
     about, crumbs("About us", "about.html")),
    ("gallery.html", "Workshop Gallery | WingBound RC Aircraft Workshops",
     "Photos from WingBound's RC aircraft and AI workshops at schools and colleges. Student photos are shared only with parental consent.",
     gallery, crumbs("Gallery", "gallery.html")),
    ("contact.html", "Contact WingBound | Aeromodelling &amp; AI Workshops in Andhra Pradesh",
     "Get in touch with WingBound about RC aircraft and AI workshops in Andhra Pradesh. Schools, colleges, students and parents can reach us by email or WhatsApp.",
     contact, crumbs("Contact us", "contact.html")),
    ("faq.html", "FAQ: Aeromodelling Workshop for Schools | WingBound",
     "Answers on safety, who flies the plane, what schools provide, timings, which classes can join and the AI part of WingBound's RC aircraft workshop.",
     faq, [FAQ_LD, crumbs("FAQ", "faq.html")]),
]

for page, title, desc, body, ld in PAGES:
    write(page, title, desc, body, ld)
write("404.html", "Page not found | WingBound", "This page could not be found.", not_found, None, base=True)

# Old booking URL now points to the contact page
with open(os.path.join(ROOT, "book.html"), "w", encoding="utf-8") as f:
    f.write(f'<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><title>Contact WingBound</title>'
            f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE_URL}/contact.html">'
            f'<meta http-equiv="refresh" content="0; url=contact.html"></head>'
            f'<body><p><a href="contact.html">Continue to the contact page</a></p>'
            f'<script>location.replace("contact.html"+location.search)</script></body></html>\n')

with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for page, *_ in PAGES:
        f.write(f"  <url><loc>{SITE_URL}/{'' if page == 'index.html' else page}</loc></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

if MISSING:
    print("Missing icons, run:  python3 src/fetch_icons.py " + " ".join(sorted(MISSING)))
    sys.exit(1)
print(f"Built {len(PAGES) + 1} pages")
