# WingBound website

Static HTML/CSS/JS, with no build step. Upload this folder to any static host (Netlify, Vercel, GitHub Pages, cPanel).

To preview it locally:

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765

## Before launch

1. **Contact form** (`book.html`): there's no form service. The form writes a message and opens the visitor's email app (to Nikhil, cc Thoran) or WhatsApp (+91 8332032455). There's nothing to set up.
2. **Domain**: the site is temporarily hosted at https://thoranprakash.github.io/wingbound-site/. When the domain is ready, replace `https://thoranprakash.github.io/wingbound-site` with it in every `.html` file, `sitemap.xml` and `robots.txt`. It appears in the canonical, Open Graph and schema tags. In the repo's **Settings → Pages → Custom domain**, add the domain too.
3. **Downloads**: add `downloads/wingbound-proposal.pdf` and `downloads/wingbound-flyer.pdf`. Every page links to the proposal.
4. **Photos**: replace each dashed "Photo placeholder" box with an `<img>` that has alt text. Use only photos with parental consent.
   - `workshop.html`: the foam-board trainer
   - `safety.html`: flight-line photo
   - `about.html`: team photo and four portraits
   - `gallery.html`: nine shots
5. **Team**: add names and roles for team members 3 and 4 in `about.html`.
6. **Hero plane image**: the plane carries Hangar 9 "Extra" markings. Confirm you have the rights to use it, or swap in a photo of your own aircraft at `assets/img/plane-760.*` and `plane-1100.webp`.
7. **Pricing**: the packages say "Contact us for pricing". To show fees, edit `schools.html`.

## Files

- `index.html`: home
- `workshop.html`: the workshop
- `ai-aviation.html`: AI & aviation
- `safety.html`: safety
- `schools.html`: for schools and colleges
- `about.html`: about us
- `gallery.html`: gallery
- `book.html`: contact / show-interest form (email or WhatsApp)
- `faq.html`: FAQ
- `assets/css/styles.css`: all styles; brand colours are tokens at the top
- `assets/js/main.js`: mobile menu, contact form, flying-plane animations, icons
- `assets/img/`: logo, plane (PNG and WebP), favicons, social share image

The header and footer are repeated in each page. If you change a nav link or contact detail, update all nine files.
