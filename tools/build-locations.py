#!/usr/bin/env python3
"""
Generate the /locations/ hub and one landing page per city.

Each city carries its own copy — distinct intros, local market angles, and
neighbourhood lists — so the pages read as genuinely different documents
rather than a template with the city name swapped in. Thin, near-duplicate
location pages are the single most common way a local-SEO play backfires.

Run from the repo root:  python3 tools/build-locations.py

To add a city: append an entry to CITIES, create the folder, re-run.
"""

import os
from string import Template

from relativize import relativize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.topreno.co"

CITIES = [
    {
        "slug": "ottawa",
        "name": "Ottawa",
        "region": "Eastern Ontario",
        "sub": "Kanata · Orléans · Barrhaven · Nepean",
        "blurb": "The most competitive trades market in eastern Ontario — and a bilingual one most competitors ignore.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in Ottawa. Local SEO, Google Maps ranking, and lead generation across Kanata, Orléans, and Barrhaven.",
        "lead": "A million-plus people, century homes and brand-new subdivisions in the same city, and winters that turn a dead furnace into an emergency. Ottawa rewards contractors who show up in the right places.",
        "intro1": "Ottawa is the most competitive trades market in eastern Ontario, and also the most rewarding one. The housing stock runs from century homes in the Glebe to subdivisions in Barrhaven finished last year, which means the work ranges from delicate retrofits to straight-ahead replacements — and the marketing for each looks nothing alike.",
        "intro2": "It is also a market where the top three Google Maps results take the overwhelming share of emergency calls. If you are not in that pack in Kanata, Orléans, or Nepean, you are leaning on referrals alone. We build listings and campaigns around the specific suburbs your trucks actually cover — and where it matters, in both English and French.",
        "notes": [
            ("A bilingual search market", "Roughly one in six Ottawa residents speaks French at home. Pages and ads that acknowledge that reach a segment most of your competitors leave completely untouched."),
            ("Federal-town seasonality", "Public service pay cycles and spring transfer season create predictable spikes in home sales and renovation spend. We plan budget around those peaks instead of spreading it flat across the year."),
            ("Suburb-by-suburb competition", "Ranking in Kanata is a different fight than ranking in Vanier. We build separate landing pages and Maps geography rather than one generic push at &ldquo;Ottawa&rdquo;."),
        ],
        "hoods": ["Kanata", "Orléans", "Barrhaven", "Nepean", "Stittsville", "Gloucester", "Westboro", "The Glebe", "Riverside South", "Manotick"],
        "nearby": ["Gatineau", "Carleton Place", "Kemptville", "Rockland", "Arnprior"],
    },
    {
        "slug": "kingston",
        "name": "Kingston",
        "region": "Eastern Ontario",
        "sub": "Amherstview · Napanee · Gananoque",
        "blurb": "A small market that punishes generic marketing and rewards a strong reputation faster than any big city.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in Kingston, Ontario. Review generation, local SEO, and websites serving Amherstview and Napanee.",
        "lead": "About 130,000 people between the 401 and the lake. Word travels fast here — which cuts both ways, and makes reputation the highest-leverage thing you can invest in.",
        "intro1": "Kingston is a small market that punishes generic marketing. With roughly 130,000 people, a couple of bad reviews will follow you around for years, and a strong reputation compounds faster than it ever would in a larger city. Ad spend matters far less here than what people find when they look you up.",
        "intro2": "The housing stock is unusually split, too: limestone heritage homes downtown that need careful, expensive work, and a large student rental market around Queen&rsquo;s where landlords buy on price and turnaround speed. Those are two completely different customers, and marketing to both with one message wastes money on each.",
        "notes": [
            ("Reputation is the whole game", "In a market this size, review volume and recency matter more than budget. We build review generation into your job-completion workflow so it happens without anyone having to remember to ask."),
            ("Two customers, two messages", "Heritage homeowners and student-rental landlords search differently and buy differently. We separate the campaigns so neither message gets diluted trying to serve both."),
            ("Landlord and property-manager work", "Recurring maintenance across a rental portfolio is far steadier than one-off calls. We help you identify and pitch the property managers who actually hold those contracts."),
        ],
        "hoods": ["Downtown", "Williamsville", "Reddendale", "Westbrook", "Kingscourt", "Barriefield", "Sydenham"],
        "nearby": ["Amherstview", "Napanee", "Gananoque", "Odessa", "Bath"],
    },
    {
        "slug": "london",
        "name": "London",
        "region": "Southwestern Ontario",
        "sub": "Byron · Masonville · St. Thomas",
        "blurb": "Big enough for real ad budgets, fragmented enough that nobody owns it yet.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in London, Ontario. Targeted local SEO and lead generation across Byron, Masonville, and St. Thomas.",
        "lead": "Roughly 420,000 people across a wide, low-density footprint. Drive time is a real cost here, and the winners dominate a few neighbourhoods rather than chasing the whole city.",
        "intro1": "London is big enough to support serious ad budgets and fragmented enough that no single contractor owns it. The city sprawls, which makes drive time a genuine line item — the contractors who do best concentrate on a handful of neighbourhoods instead of spreading themselves across every postal code.",
        "intro2": "Add Western University and Fanshawe, a substantial rental market, and steady suburban growth to the north and northwest, and you get a market where targeting precision beats budget size almost every time.",
        "notes": [
            ("Drive time is margin", "Ranking city-wide sounds good until your crew spends ninety minutes a day in transit. We concentrate spend where the jobs are actually profitable after travel."),
            ("North-end growth", "Masonville, Hyde Park, and Sunningdale keep adding homes, and new builds age into replacement work on a schedule you can forecast years ahead."),
            ("A real commercial layer", "Property management, healthcare, and institutional buildings support service contracts that hold up through a slow residential quarter."),
        ],
        "hoods": ["Byron", "Masonville", "Hyde Park", "Oakridge", "Westmount", "Old North", "White Oaks", "Sunningdale"],
        "nearby": ["St. Thomas", "Strathroy", "Ingersoll", "Dorchester", "Komoka"],
    },
    {
        "slug": "kitchener",
        "name": "Kitchener",
        "region": "Waterloo Region",
        "sub": "Waterloo · Cambridge · Guelph",
        "blurb": "One of the fastest-growing regions in Canada, with a research-heavy buyer who compares before calling.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in Kitchener–Waterloo. Websites, local SEO, and lead generation across Waterloo, Cambridge, and Guelph.",
        "lead": "New subdivisions keep coming online across Kitchener, Cambridge, and Guelph — and every one of them becomes replacement and service work on a schedule you can plan around.",
        "intro1": "Waterloo Region is one of the fastest-growing areas in Canada, and it shows in the trades. Housing keeps going up across Kitchener, Cambridge, and Guelph, and each new subdivision turns into service and replacement work on a predictable timeline. Getting established early in those pockets costs a fraction of fighting your way in later.",
        "intro2": "It is also a tech-heavy region, which genuinely changes buyer behaviour. Homeowners here research thoroughly, compare online, read reviews closely, and increasingly expect to book without picking up the phone. A contractor with online scheduling and a fast, clear website converts noticeably better here than one running a call-only funnel.",
        "notes": [
            ("A research-heavy buyer", "Waterloo Region homeowners compare more before they call. Detailed service pages, a transparent process, and visible reviews do the selling before the phone ever rings."),
            ("New-build replacement cycles", "Subdivisions built ten to fifteen years ago are hitting their first replacement wave now. We target those specific pockets rather than the region as a whole."),
            ("Three cities, one region", "Kitchener, Waterloo, and Cambridge are separate search markets that people casually merge into one. We treat them separately so you rank in all three."),
        ],
        "hoods": ["Downtown Kitchener", "Doon", "Forest Heights", "Stanley Park", "Uptown Waterloo", "Hespeler", "Preston", "Galt"],
        "nearby": ["Cambridge", "Guelph", "Elmira", "New Hamburg", "Ayr"],
    },
    {
        "slug": "barrie",
        "name": "Barrie",
        "region": "Simcoe County",
        "sub": "Innisfil · Orillia · Wasaga Beach",
        "blurb": "A commuter city running on two clocks — year-round residential and a hard seasonal cottage surge.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in Barrie, Ontario. Seasonal campaign planning and local SEO across Innisfil, Orillia, and Wasaga Beach.",
        "lead": "Year-round residential work in a fast-growing commuter city, plus a cottage-country surge that runs from May to Thanksgiving. Plan for only one and you leave money on the table in the other.",
        "intro1": "Barrie runs on two clocks. There is the steady residential market of a fast-growing commuter city, and there is the cottage-country surge that starts in May and does not let up until Thanksgiving. Contractors who build their year around only one of those consistently give up revenue in the other.",
        "intro2": "The commuter dynamic shapes everything else. A large share of Barrie and Innisfil homeowners work in the GTA, which means they are searching in the evening, booking on a phone, and rarely free for a mid-day quote. If your intake process assumes a nine-to-five customer, you are losing jobs you already paid to generate.",
        "notes": [
            ("Two seasons, two budgets", "Cottage-country demand around Wasaga, Innisfil, and Muskoka spikes hard and then stops cold. We shift spend into that window instead of running flat all year."),
            ("Evening, mobile intake", "GTA commuters search after 7pm. Click-to-call, mobile booking, and after-hours response capture the work a nine-to-five office never sees."),
            ("Fast residential growth", "Barrie and Innisfil keep adding housing. Establishing yourself in a new subdivision early is dramatically cheaper than buying your way in once competitors arrive."),
        ],
        "hoods": ["Ardagh", "Painswick", "Holly", "Allandale", "East End", "South Barrie"],
        "nearby": ["Innisfil", "Orillia", "Wasaga Beach", "Angus", "Alcona", "Midhurst"],
    },
    {
        "slug": "peterborough",
        "name": "Peterborough",
        "region": "Kawartha Lakes",
        "sub": "Kawartha Lakes · Lindsay · Cobourg",
        "blurb": "An older, established market with steady replacement work — sold on trust rather than urgency.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in Peterborough and the Kawarthas. Local SEO and lead generation across Lindsay and Cobourg.",
        "lead": "A lot of homes here are well past the point where the original furnace, roof, or plumbing was ever going to last. That is steady replacement work — but it is sold very differently than in a young market.",
        "intro1": "Peterborough and the Kawarthas make up an older, established market with a housing stock to match. A great many homes are well past the point where the original furnace, roof, or plumbing was ever going to hold up. That is dependable replacement work, and it is not going anywhere.",
        "intro2": "The customer, though, is different. This market skews older, often retired, and frequently paying from savings rather than financing. People take longer to decide, they call more than they click, and they weigh trust heavily. Marketing that leads with manufactured urgency and discount pressure tends to bounce straight off.",
        "notes": [
            ("Trust over urgency", "Clear pricing, real credentials, and visible local history matter far more here than countdown timers and limited-time offers."),
            ("Seasonal cottage demand", "Kawartha waterfront properties generate spring open-up and fall close-down work that is easy to systematize into recurring contracts."),
            ("Phone-first customers", "A meaningful share of this market still calls rather than filling in a form. We make the number impossible to miss and keep the Maps listing accurate."),
        ],
        "hoods": ["East City", "Downtown", "Monaghan", "Otonabee", "Northcrest", "Bridgenorth"],
        "nearby": ["Lindsay", "Cobourg", "Lakefield", "Ennismore", "Havelock", "Kawartha Lakes"],
    },
    {
        "slug": "cornwall",
        "name": "Cornwall",
        "region": "Stormont, Dundas &amp; Glengarry",
        "sub": "Long Sault · Ingleside · Morrisburg",
        "blurb": "A market where being genuinely local is an advantage you cannot buy — and a bilingual opening most ignore.",
        "meta_desc": "Marketing for HVAC, roofing, and plumbing contractors in Cornwall, Ontario. Bilingual local SEO and lead generation across SDG counties and Long Sault.",
        "lead": "About 47,000 people in the city plus the surrounding SDG counties — and a customer base that notices whether you are actually from here or dialing in from Ottawa.",
        "intro1": "Cornwall is the kind of market where being genuinely local is a competitive advantage you cannot buy. Customers here can tell the difference between a contractor with roots in the community and an out-of-town company running ads into the area, and they act on that difference.",
        "intro2": "It is also strongly bilingual, sitting close to the Quebec border, and a meaningful share of homeowners search and read in French. Most competing contractors do not bother serving them properly. That is an opening, and it is a cheap one to take.",
        "notes": [
            ("Bilingual is an edge, not a checkbox", "French-language pages and ads reach a large share of this market that competitors serve poorly or not at all — usually at a lower cost per lead."),
            ("Local really means local", "Cornwall customers can spot an Ottawa company running ads into the area. We lean hard into your actual roots here rather than hiding them behind generic copy."),
            ("A wide rural service area", "SDG counties spread your jobs out considerably. We target the townships that are worth the drive and skip the ones that quietly lose you money."),
        ],
        "hoods": ["Le Village", "Riverdale", "Downtown", "Cornwall Centre", "Guindon Park"],
        "nearby": ["Long Sault", "Ingleside", "Alexandria", "Morrisburg", "Winchester"],
    },
]

# --- Shared chrome ---------------------------------------------------------

HEAD = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>$title</title>
<meta name="description" content="$meta_desc">
<link rel="canonical" href="$canonical">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">

<meta property="og:type" content="website">
<meta property="og:site_name" content="TOP Reno">
<meta property="og:locale" content="en_CA">
<meta property="og:title" content="$og_title">
<meta property="og:description" content="$meta_desc">
<meta property="og:url" content="$canonical">
<meta property="og:image" content="$site/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="$site/assets/img/og-image.png">

<meta name="theme-color" content="#0D0E10">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/main.js" defer></script>

<script type="application/ld+json">
$jsonld
</script>
</head>
<body>

<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="TOP Reno — home">
      <svg class="logo-mark" viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false">
        <path d="M4.5 14.5 L16 4 L27.5 14.5" stroke="#FF5A1F" stroke-width="4.5" stroke-linecap="square"/>
        <path d="M4.5 27 L16 16.5 L27.5 27" stroke="currentColor" stroke-width="4.5" stroke-linecap="square"/>
      </svg>
      <span class="logo-text">Top<span>&nbsp;Reno</span></span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>

    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/services/">Services</a></li>
        <li><a href="/locations/" aria-current="page">Locations</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
      <div class="nav-cta"><a class="btn btn-primary" href="/contact/">Get in touch</a></div>
      <a class="nav-phone" href="tel:+16137079210">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M14.5 11.3v2a1.3 1.3 0 0 1-1.5 1.3 13 13 0 0 1-5.6-2 12.8 12.8 0 0 1-4-4 13 13 0 0 1-2-5.6A1.3 1.3 0 0 1 2.7 1.5h2a1.3 1.3 0 0 1 1.3 1.2c.1.6.2 1.3.5 1.9a1.3 1.3 0 0 1-.3 1.4l-.9.8a10.7 10.7 0 0 0 4 4l.8-.9a1.3 1.3 0 0 1 1.4-.3c.6.3 1.2.4 1.9.5a1.3 1.3 0 0 1 1.1 1.2Z" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        613 707 9210
      </a>
    </nav>
  </div>
</header>
<div class="stripe stripe-thin" aria-hidden="true"></div>
"""

FOOT = """
<footer class="site-footer">
  <div class="stripe" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="logo" href="/" aria-label="TOP Reno — home">
          <svg class="logo-mark" viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false">
            <path d="M4.5 14.5 L16 4 L27.5 14.5" stroke="#FF5A1F" stroke-width="4.5" stroke-linecap="square"/>
            <path d="M4.5 27 L16 16.5 L27.5 27" stroke="currentColor" stroke-width="4.5" stroke-linecap="square"/>
          </svg>
          <span class="logo-text">Top<span>&nbsp;Reno</span></span>
        </a>
        <p>Marketing, web, and operations support built for Ontario&rsquo;s HVAC, roofing, and plumbing contractors.</p>
      </div>

      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/services/">Services</a></li>
          <li><a href="/locations/">Locations</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Get in touch</h4>
        <ul>
          <li><a href="tel:+16137079210">613 707 9210</a></li>
          <li><a href="mailto:jared@topreno.co">jared@topreno.co</a></li>
          <li><a href="/contact/">Book a discovery call</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> TOP Reno. All rights reserved.</span>
      <div class="footer-social">
        <a href="https://www.facebook.com/share/9Qxds2Kxn3eTgKLA/" target="_blank" rel="noopener noreferrer" aria-label="TOP Reno on Facebook">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1Z"/></svg>
        </a>
        <a href="mailto:jared@topreno.co" aria-label="Email TOP Reno">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="1.5" stroke="currentColor" stroke-width="1.7"/><path d="m3 6 9 7 9-7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

ARROW = ('<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
         '<path d="M1 7h12M7 1l6 6-6 6" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

TICK = ('<svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
        '<path d="M13.5 4.5 6.2 11.8 2.5 8.1" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

CITY_BODY = Template("""
<main id="main">

  <section class="page-hero grid-bg">
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol>
          <li><a href="/">Home</a></li>
          <li><a href="/locations/">Locations</a></li>
          <li><span aria-current="page">$name</span></li>
        </ol>
      </nav>
      <p class="eyebrow reveal">$region</p>
      <h1 class="reveal">HVAC, roofing &amp; plumbing marketing in $name</h1>
      <p class="lead reveal reveal-1">$lead</p>
      <div class="btn-row reveal reveal-2">
        <a class="btn btn-primary" href="/contact/">Book a free discovery call $arrow</a>
        <a class="btn btn-ghost" href="tel:+16137079210">Call 613 707 9210</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap wrap-narrow">
      <p class="eyebrow reveal">The $name market</p>
      <h2 class="reveal">What we see in $name.</h2>
      <p class="lead reveal reveal-1">$intro1</p>
      <p class="reveal reveal-2">$intro2</p>
    </div>
  </section>

  <section class="section dark grid-bg" style="padding-top:0;padding-bottom:var(--section)">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow reveal">Local angles</p>
        <h2 class="reveal">Three things that move the needle here.</h2>
      </div>
      <div class="card-grid cols-3">
        $notes
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head-split">
        <div>
          <p class="eyebrow reveal">Coverage</p>
          <h2 class="reveal">Where we target in and around $name.</h2>
        </div>
        <p class="lead reveal reveal-1">Local search is won neighbourhood by neighbourhood. These are the areas we build campaigns and Maps geography around.</p>
      </div>

      <div class="card-grid cols-2 reveal">
        <div class="card">
          <span class="card-num">In the city</span>
          <h3>$name neighbourhoods</h3>
          <ul class="card-list">
            $hoods
          </ul>
        </div>
        <div class="card">
          <span class="card-num">Surrounding</span>
          <h3>Nearby communities</h3>
          <ul class="card-list">
            $nearby
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section steel">
    <div class="wrap">
      <div class="head-split">
        <div>
          <p class="eyebrow reveal">What we do</p>
          <h2 class="reveal">Services for $name contractors.</h2>
        </div>
        <p class="lead reveal reveal-1">The same three levers we pull everywhere, tuned to what actually works in this market.</p>
      </div>

      <div class="card-grid cols-3">
        <article class="card card-dark reveal">
          <span class="card-num">01 / Brand</span>
          <h3>Brand</h3>
          <p>Websites, logo and identity work, and competitive research so $name homeowners see your business as positively as you do.</p>
        </article>
        <article class="card card-dark reveal reveal-1">
          <span class="card-num">02 / Growth</span>
          <h3>Growth</h3>
          <p>Quote-ready lead generation, paid advertising, and local search ranking that puts you in the $name Maps pack.</p>
        </article>
        <article class="card card-dark reveal reveal-2">
          <span class="card-num">03 / Operations</span>
          <h3>Operations</h3>
          <p>Workflow automation, documented processes, and reporting that shows you cost per booked job — not vanity metrics.</p>
        </article>
      </div>

      <div class="btn-row reveal">
        <a class="btn btn-ghost" href="/services/">Full service breakdown $arrow</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow reveal">Other areas</p>
        <h2 class="reveal">We work across Ontario.</h2>
      </div>
      <div class="loc-grid reveal">
        $others
      </div>
    </div>
  </section>

  <section class="section cta-band">
    <div class="wrap">
      <p class="eyebrow reveal" style="justify-content:center">Let&rsquo;s talk</p>
      <h2 class="reveal">Ready to own the $name market?</h2>
      <p class="lead reveal reveal-1">Book a free discovery call. We&rsquo;ll look at your local competition and tell you honestly where the biggest opportunity is.</p>
      <div class="btn-row reveal reveal-2">
        <a class="btn btn-primary" href="/contact/">Get in touch $arrow</a>
        <a class="btn btn-ghost" href="tel:+16137079210">Call 613 707 9210</a>
      </div>
    </div>
  </section>

</main>
""")

HUB_BODY = Template("""
<main id="main">

  <section class="page-hero grid-bg">
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol>
          <li><a href="/">Home</a></li>
          <li><span aria-current="page">Locations</span></li>
        </ol>
      </nav>
      <p class="eyebrow reveal">Service areas</p>
      <h1 class="reveal">Marketing for trade contractors across Ontario.</h1>
      <p class="lead reveal reveal-1">Local search is won city by city, and every market has its own quirks. Pick yours below &mdash; or call us and we&rsquo;ll tell you what we already know about your competition.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head-split">
        <div>
          <p class="eyebrow reveal">Where we work</p>
          <h2 class="reveal">Seven markets we know well.</h2>
        </div>
        <p class="lead reveal reveal-1">We work with contractors anywhere in Ontario. These are the areas where we have the deepest local knowledge of the competition, the housing stock, and the search behaviour.</p>
      </div>

      <div class="card-grid cols-2">
        $cards
      </div>
    </div>
  </section>

  <section class="section steel">
    <div class="wrap wrap-narrow">
      <p class="eyebrow reveal">Not on the list?</p>
      <h2 class="reveal">We still probably cover you.</h2>
      <p class="lead reveal reveal-1">Everything we do is remote-friendly, so your location is rarely the deciding factor. We work with HVAC, roofing, and plumbing contractors throughout Ontario &mdash; including Windsor, Sudbury, Thunder Bay, Belleville, Brockville, Sarnia, and the GTA.</p>
      <div class="btn-row reveal reveal-2">
        <a class="btn btn-primary" href="/contact/">Ask about your area $arrow</a>
      </div>
    </div>
  </section>

  <section class="section cta-band">
    <div class="wrap">
      <p class="eyebrow reveal" style="justify-content:center">Let&rsquo;s talk</p>
      <h2 class="reveal">Ready to be the contractor they call first?</h2>
      <p class="lead reveal reveal-1">Book a free discovery call. No pitch deck, no pressure &mdash; just a straight conversation about where the opportunity is in your market.</p>
      <div class="btn-row reveal reveal-2">
        <a class="btn btn-primary" href="/contact/">Get in touch $arrow</a>
        <a class="btn btn-ghost" href="tel:+16137079210">Call 613 707 9210</a>
      </div>
    </div>
  </section>

</main>
""")


def esc_json(text):
    """Strip HTML entities back to plain characters for use inside JSON-LD."""
    return (text.replace("&rsquo;", "’")
                .replace("&ldquo;", "“")
                .replace("&rdquo;", "”")
                .replace("&mdash;", "—")
                .replace("&ndash;", "–")
                .replace("&amp;", "&")
                .replace('"', '\\"'))


def loc_tile(city):
    return f"""<a class="loc" href="/locations/{city['slug']}/">
          <span class="loc-name">{city['name']} <svg width="16" height="16" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M7 1l6 6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          <p class="loc-sub">{city['sub']}</p>
        </a>"""


def build_city(city, all_cities):
    canonical = f"{SITE}/locations/{city['slug']}/"
    # City first: leads with the local keyword and keeps the tag under the
    # ~65-char point where Google starts truncating.
    title = f"{city['name']} HVAC, Roofing &amp; Plumbing Marketing | TOP Reno"
    og_title = f"{city['name']} HVAC, Roofing & Plumbing Marketing"

    jsonld = f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Locations", "item": "{SITE}/locations/" }},
        {{ "@type": "ListItem", "position": 3, "name": "{city['name']}", "item": "{canonical}" }}
      ]
    }},
    {{
      "@type": "ProfessionalService",
      "name": "TOP Reno — {city['name']}",
      "description": "{esc_json(city['meta_desc'])}",
      "url": "{canonical}",
      "email": "jared@topreno.co",
      "telephone": "+1-613-707-9210",
      "image": "{SITE}/assets/img/og-image.png",
      "parentOrganization": {{ "@type": "Organization", "name": "TOP Reno", "url": "{SITE}/" }},
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "{city['name']}",
        "addressRegion": "ON",
        "addressCountry": "CA"
      }},
      "areaServed": [
{chr(10).join('        {{ "@type": "City", "name": "{}" }}{}'.format(esc_json(p), "," if i < len(city["hoods"] + city["nearby"]) - 1 else "") for i, p in enumerate(city["hoods"] + city["nearby"]))}
      ],
      "sameAs": ["https://www.facebook.com/share/9Qxds2Kxn3eTgKLA/"]
    }}
  ]
}}"""

    notes = "\n".join(
        f"""<article class="card card-dark reveal{f' reveal-{i}' if i else ''}">
          <span class="card-num">{i + 1:02d}</span>
          <h3>{heading}</h3>
          <p>{body}</p>
        </article>"""
        for i, (heading, body) in enumerate(city["notes"])
    )

    hoods = "\n            ".join(f"<li>{TICK} {h}</li>" for h in city["hoods"])
    nearby = "\n            ".join(f"<li>{TICK} {n}</li>" for n in city["nearby"])
    others = "\n        ".join(
        loc_tile(c) for c in all_cities if c["slug"] != city["slug"]
    )

    head = Template(HEAD).substitute(
        title=title, meta_desc=city["meta_desc"], canonical=canonical,
        og_title=og_title, site=SITE, jsonld=jsonld,
    )
    body = CITY_BODY.substitute(
        name=city["name"], region=city["region"], lead=city["lead"],
        intro1=city["intro1"], intro2=city["intro2"],
        notes=notes, hoods=hoods, nearby=nearby, others=others, arrow=ARROW,
    )

    path = os.path.join(ROOT, "locations", city["slug"], "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(relativize(head + body + FOOT, depth=2))  # locations/<city>/
    print("wrote", os.path.relpath(path, ROOT))


def build_hub(all_cities):
    canonical = f"{SITE}/locations/"
    meta_desc = ("TOP Reno serves HVAC, roofing, and plumbing contractors across "
                 "Ontario — Ottawa, Kingston, London, Kitchener, Barrie, "
                 "Peterborough, and Cornwall.")

    items = "\n".join(
        f"""        {{ "@type": "ListItem", "position": {i + 1}, "name": "{c['name']}", "item": "{SITE}/locations/{c['slug']}/" }}{"," if i < len(all_cities) - 1 else ""}"""
        for i, c in enumerate(all_cities)
    )

    jsonld = f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Locations", "item": "{canonical}" }}
      ]
    }},
    {{
      "@type": "ItemList",
      "name": "TOP Reno service areas",
      "itemListElement": [
{items}
      ]
    }}
  ]
}}"""

    cards = "\n".join(
        f"""<article class="card reveal{f' reveal-{i % 3}' if i % 3 else ''}">
          <span class="card-num">{c['region']}</span>
          <h3>{c['name']}</h3>
          <p>{c['blurb']}</p>
          <ul class="card-list">
            <li>{TICK} {c['sub'].replace(' · ', '</li><li>' + TICK + ' ')}</li>
          </ul>
          <p style="margin-top:1.25rem">
            <a class="arrow-link" href="/locations/{c['slug']}/">{c['name']} marketing {ARROW}</a>
          </p>
        </article>"""
        for i, c in enumerate(all_cities)
    )

    head = Template(HEAD).substitute(
        title="Service Areas &mdash; Ontario Trade Contractor Marketing | TOP Reno",
        meta_desc=meta_desc, canonical=canonical,
        og_title="Service Areas — Ontario Trade Contractor Marketing",
        site=SITE, jsonld=jsonld,
    )
    body = HUB_BODY.substitute(cards=cards, arrow=ARROW)

    path = os.path.join(ROOT, "locations", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(relativize(head + body + FOOT, depth=1))  # locations/
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    build_hub(CITIES)
    for c in CITIES:
        build_city(c, CITIES)
    print(f"\n{len(CITIES)} city pages + hub generated.")
