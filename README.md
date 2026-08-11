# TOP Reno — topreno.co

Static marketing site for **TOP Reno** — marketing, web, and operations support for
Ontario's HVAC, roofing, and plumbing contractors.

No build step, no framework, no dependencies. Plain HTML, CSS, and vanilla JS that
can be hosted free on GitHub Pages, Cloudflare Pages, Netlify, or any static host.

---

## Contact form

Submissions go to **Formspree** endpoint `https://formspree.io/f/xaewonon`, which
delivers to **jared@topreno.co**. The endpoint appears in exactly one place —
the `action` on the form in [`contact/index.html`](contact/index.html).

The form posts by `fetch` and shows an inline success message; it never navigates
away. If the request fails, it surfaces an error pointing the visitor at the phone
number and email instead of failing silently.

**Send one real test submission after deploying.** Formspree requires you to
confirm the first submission from a new domain before it starts delivering, so
until you do that once, live inquiries won't reach your inbox.

The free tier covers 50 submissions/month per account. If TOP Reno and CDWK Labs
share a Formspree account, they share that allowance.

---

## Structure

```
/                       Home
/about/                 About
/services/              Services — Brand, Growth, Operations
/contact/               Contact + inquiry form
/locations/             Service-area hub
/locations/ottawa/      ─┐
/locations/kingston/     │
/locations/london/       │ One landing page per city,
/locations/kitchener/    │ each with its own copy
/locations/barrie/       │
/locations/peterborough/ │
/locations/cornwall/    ─┘
404.html                Not-found page
assets/css/style.css    All styles
assets/js/main.js       Nav, scroll reveal, form handling
assets/img/             Logo, favicons, social share image
tools/                  Optional generators (see below)
```

Asset paths and internal links are **relative**, so the same files work at a
domain root, at a subdirectory, and from the filesystem. `tools/relativize.py`
enforces this and is safe to re-run at any time.

---

## Hosting

**Deployed:** <https://jchad086.github.io/topreno/>
Repo `jchad086/topreno`, GitHub Pages serving `main` at `/`.

That URL is a **live staging copy**. The custom domain is deliberately not set
yet, because attaching it would make GitHub redirect this URL to
`www.topreno.co` — which still points at Duda — leaving nothing to preview.
Check the staging copy first, then cut over.

### Cutting over to www.topreno.co

1. **Point DNS at GitHub Pages** (at whoever hosts topreno.co's DNS):

   | Type  | Name  | Value |
   |-------|-------|-------|
   | CNAME | `www` | `jchad086.github.io` |
   | A     | `@`   | `185.199.108.153` |
   | A     | `@`   | `185.199.109.153` |
   | A     | `@`   | `185.199.110.153` |
   | A     | `@`   | `185.199.111.153` |

   The four `A` records make the bare `topreno.co` resolve to the `www` version.
   Removing the existing Duda records is what takes the old site down.

2. **Attach the domain** — Settings → Pages → Custom domain → `www.topreno.co`,
   or:

   ```bash
   gh api -X PUT repos/jchad086/topreno/pages -f cname=www.topreno.co
   ```

   This writes a `CNAME` file into the repo automatically.

3. **Wait for the certificate**, then tick **Enforce HTTPS**. Usually minutes,
   occasionally up to an hour.

4. **Send one test submission** through the contact form (see above).

5. **Only then cancel Duda.** Keep it running until the new site resolves and
   the form delivers — DNS changes are not instant and lowering TTL beforehand
   makes the switch faster to undo if something is wrong.

### Running locally

```bash
python3 -m http.server 8765
```

Then open <http://localhost:8765>. Any static file server works — asset paths are
relative, so the site also runs correctly from a subdirectory.

---

## SEO

Already in place:

- Unique `<title>` (≤65 chars) and meta description (≤160 chars) on every page
- One `<h1>` per page, semantic heading order, landmark elements
- Canonical URLs, Open Graph, and Twitter card tags
- **JSON-LD structured data** — `ProfessionalService` with `areaServed`,
  `WebSite`, `FAQPage` on the homepage, `BreadcrumbList` on every inner page,
  `ItemList` on the locations hub, and a per-city `ProfessionalService`
- `sitemap.xml` and `robots.txt`
- Location pages carry genuinely distinct copy rather than a swapped city name —
  near-duplicate location pages are the usual reason this tactic backfires
- Fast by default: no framework, no render-blocking JS, one stylesheet

**After launch:**

1. Submit `https://www.topreno.co/sitemap.xml` in
   [Google Search Console](https://search.google.com/search-console).
2. Update `<lastmod>` dates in `sitemap.xml` when content changes materially.
3. Claim and complete a **Google Business Profile** — for local trades-adjacent
   search this moves the needle more than anything on the site itself.
4. Consider adding client case studies with real numbers. Nothing converts
   contractors like proof from another contractor.

---

## Accessibility

Text colour meets **WCAG 2.1 AA** contrast (4.5:1 normal, 3:1 large) on every
page, verified at 1440px and 375px with all scroll-reveals forced visible and
all FAQ accordions expanded. Focus rings clear the 3:1 non-text minimum against
the surface behind them.

Colour is handled through three inherited roles rather than per-component
values, so a component doesn't need to know which background it landed on:

| Role | Light surfaces | Dark surfaces |
|------|----------------|---------------|
| `--accent-text` | `--orange-ink` `#C2410C` | `--orange` `#FF5A1F` |
| `--lead-text` | `--steel-2` | `--smoke-2` |
| `--muted-text` | `--muted` `#5E6672` | `--smoke` |

Dark sections re-point all three in one rule (search `Every dark surface` in
`style.css`). **If you add a section with a dark background, add its class to
that selector** — otherwise it inherits the light-surface defaults, which are
near-black and will vanish.

Brand orange `#FF5A1F` is only 3.1:1 on light backgrounds, so it is used there
for fills, borders, and decorative icons — never for text. Primary buttons use
dark text on orange (6.2:1); white on orange would be 3.1:1 and fail.

---

## Optional generators

Both are conveniences, not part of a build. The generated output is committed,
so the site works without ever running them. They need `python3`; the image
script also needs Pillow (`pip3 install Pillow`).

```bash
python3 tools/build-locations.py   # regenerates /locations/ and all city pages
python3 tools/make-images.py       # regenerates favicons + og-image.png
```

**To add a city:** append an entry to `CITIES` in `tools/build-locations.py`
(with its own intro copy and local angles), re-run it, then add the new URL to
`sitemap.xml`.

If you'd rather not touch Python, edit the generated HTML directly — just be
aware that re-running the generator would overwrite those edits.

---

## Editing content

Because there's no templating, the header and footer markup are duplicated in
each page. If you change navigation or footer links, update them everywhere —
`grep -rl "footer-col" .` lists every affected file.

Common edits:

| What | Where |
|------|-------|
| Phone number | search `613 707 9210` and `tel:+16137079210` |
| Email | search `jared@topreno.co` |
| Facebook link | search `facebook.com/share` |
| Colours, type, spacing | `assets/css/style.css` (`:root` custom properties) |
| Business hours | `contact/index.html` (also in its JSON-LD block) |

---

## Known content to revisit

The four homepage statistics (62% / 78% / 86% / 32%) were carried over from the
previous Duda site. They're unsourced there and unsourced here. Either cite them
or replace them with your own client results — unattributed statistics are a soft
spot on a page whose whole argument is about building trust.

---

## Browser support

Modern evergreen browsers. Uses CSS custom properties, `clamp()`, grid, and
`IntersectionObserver`. The scroll-reveal animation degrades gracefully — if
`IntersectionObserver` is unavailable or the visitor has *reduce motion* enabled,
all content renders immediately instead of animating.
