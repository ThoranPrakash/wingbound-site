# WingBound website

A static site (HTML, CSS and a little JavaScript), hosted free on GitHub Pages:
https://thoranprakash.github.io/wingbound-site/

## Editing content

All page text lives in one file: `src/build.py`. Edit it, then rebuild:

```bash
python3 src/build.py
```

This rewrites every `.html` page, `sitemap.xml` and `robots.txt`. It needs only Python 3 (no packages).
Commit and push, and GitHub Pages republishes within about a minute.

Don't edit the `.html` files directly: the next build will overwrite them.

### Adding social proof

Near the top of `src/build.py` are three lists. Only add real content you have permission to publish:

```python
NUMBERS = [("500+", "students taught")]
COMPETITIONS = [("Event name", "Organised by …", "2023", "1st place")]
QUOTES = [("Quote text", "Name", "Role", "Institution")]
```

While a list is empty, the site shows a dashed "To add" box in its place. To hide those boxes on the live site, set `SHOW_EMPTY_SLOTS = False`.

### Adding icons

Icons are [Lucide](https://lucide.dev/icons) line icons, inlined into the pages. To use a new one:

```bash
python3 src/fetch_icons.py icon-name
```

Then use `icon("icon-name")` in `src/build.py`.

### Styles and scripts

- `assets/css/styles.css`: all styles. Brand colours are tokens at the top.
- `assets/js/main.js`: mobile menu, audience tabs, forces and wiring diagrams, scroll reveals, contact form.

The build adds a version tag to these file links, so visitors always get the latest version after a change.

## Previewing locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765

## Before launch

1. **Social proof**: fill `NUMBERS`, `COMPETITIONS` and `QUOTES` (see above), or set `SHOW_EMPTY_SLOTS = False`.
2. **Team**: add the name of team member 4, and roles for everyone if you want them (search `Team member 4` in `src/build.py`).
3. **Downloads**: put `wingbound-proposal.pdf` and `wingbound-flyer.pdf` in `downloads/` and rebuild. Download buttons appear automatically once the files exist.
4. **Photos**: the gallery shows a "Photos are on their way" panel. Use only photos with parental consent.
5. **Hero plane image**: the plane carries Hangar 9 "Extra" markings. Confirm you have the rights to use it, or use a photo of your own aircraft. The cleaned, AI-upscaled master (2346 px, transparent) is `src/plane-master.png`. The site uses `assets/img/plane-760.webp`, `plane-1400.webp` and `plane-760.png`, exported from it. A replacement needs the same three files with a transparent background.
6. **Domain**: when it's ready, change `SITE_URL` in `src/build.py`, rebuild, and add the domain under the repo's **Settings → Pages → Custom domain**.

## Contact form

The form stores nothing. It writes a message and opens WhatsApp (+91 62818 43302) or the visitor's email app (to Nikhil, copied to Thoran). There's no form service to set up.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `workshop.html` | The Workshop: outcomes, forces of flight, schedule, electronics, aircraft blueprint |
| `ai-aviation.html` | AI & Aviation |
| `safety.html` | Safety, with the flight-day layout |
| `schools.html` | For Schools & Colleges: who provides what, booking, packages |
| `about.html` | About us and the team |
| `gallery.html` | Gallery (photos coming soon) |
| `contact.html` | Contact / show interest |
| `faq.html` | FAQ, grouped by topic |
| `404.html` | Page not found |
| `book.html` | Redirects old links to `contact.html` |

## Credits

- Fonts: Lato and Michroma (SIL Open Font Licence), self-hosted in `assets/fonts/`.
- Icons: Lucide (ISC licence).
