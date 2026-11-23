#!/usr/bin/env python3
"""
Builds the Bright Chapter Realty website into the ../site folder.

1. Edit SETTINGS below (agent, brokerage, license, contact details, AdSense ID).
2. Edit your homes in tools/listings.py.
3. Run:  python3 tools/build.py
4. Commit and push to GitHub. Azure Static Web Apps publishes the /site folder.
Python 3.8+ only, no extra packages.
"""
import html, json, os, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from listings import LISTINGS          # noqa: E402
from content_guides import GUIDES      # noqa: E402

# ---------------------------------------------------------------------------
# SETTINGS — replace every "YOUR ..." value before publishing
# ---------------------------------------------------------------------------
SETTINGS = {
    "site_name": "Bright Chapter Realty",
    "tagline": "Real estate help for your next chapter",
    "site_url": "https://www.yourdomain.com",          # no trailing slash
    "agent_name": "YOUR NAME",
    "agent_title": "REALTOR® | Seniors Real Estate Specialist®",   # only list designations you actually hold
    "brokerage": "YOUR BROKERAGE NAME",
    "license": "YOUR LICENSE NUMBER",                   # agent license number
    "brokerage_license": "YOUR BROKERAGE LICENSE NUMBER",
    "service_area": "Your City and surrounding communities",
    "state": "YOUR STATE",
    "phone": "(555) 555-0100",                          # 555-01xx numbers are reserved for examples
    "email": "hello@yourdomain.com",
    "office_address": "YOUR OFFICE ADDRESS, City, ST 00000",
    "form_endpoint": "",        # optional: Formspree or similar URL. Empty = forms open the visitor's email app
    "adsense_client": "",       # e.g. "ca-pub-1234567890123456"
    "updated": date(2026, 11, 24),
}
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
S = SETTINGS
E = html.escape
U = S["updated"]
UPDATED_HUMAN = f"{U:%B} {U.day}, {U.year}"
UPDATED_ISO = U.isoformat()
PAGES = []

NAV = [("Home", "index.html", "home"), ("Homes for Sale", "listings/index.html", "listings"),
       ("Sell Your Home", "sell.html", "sell"), ("Guides", "guides/index.html", "guides"),
       ("About", "about.html", "about"), ("Contact", "contact.html", "contact")]

ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>'
ICON_SHARE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>'
EHO_ICON = ('<svg class="eho" viewBox="0 0 40 40" role="img" aria-label="Equal Housing Opportunity">'
            '<path d="M20 4 3 16h4v19h26V16h4z" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M13 21h14M13 27h14" stroke="currentColor" stroke-width="3.2"/></svg>')
HERO_PHOTO = "1564013799919-ab600027ffc6"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def canonical_for(path):
    if path == "index.html":
        return S["site_url"] + "/"
    if path.endswith("/index.html"):
        return S["site_url"] + "/" + path[: -len("index.html")]
    return S["site_url"] + "/" + path


def prefix(path):
    return "../" * path.count("/")


def money(n):
    return "${:,.0f}".format(n)


def baths(n):
    return ("%g" % n)


def photo_url(ph, p, w, h):
    if ph.startswith("local:"):
        return p + "assets/img/listings/" + ph[6:]
    return f"https://images.unsplash.com/photo-{ph}?auto=format&fit=crop&w={w}&h={h}&q=70"


def photo_abs(ph, w=1200, h=630):
    if ph.startswith("local:"):
        return S["site_url"] + "/assets/img/listings/" + ph[6:]
    return photo_url(ph, "", w, h)


def img(ph, p, alt, w, h, sizes, eager=False, cls=""):
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    if ph.startswith("local:"):
        src = photo_url(ph, p, w, h)
        return f'<img class="{cls}" src="{src}" alt="{E(alt)}" {loading} decoding="async" width="{w}" height="{h}" onerror="this.remove()">'
    srcset = ", ".join(f"{photo_url(ph, p, ww, round(ww * h / w))} {ww}w" for ww in (480, 800, 1200, 1600))
    return (f'<img class="{cls}" src="{photo_url(ph, p, w, h)}" srcset="{srcset}" sizes="{sizes}" alt="{E(alt)}" '
            f'{loading} decoding="async" width="{w}" height="{h}" onerror="this.remove()">')


def status_badge(l):
    cls = {"For Sale": "s-sale", "Pending": "s-pending", "Sold": "s-sold", "Coming Soon": "s-soon"}.get(l["status"], "s-sale")
    sample = '<span class="badge s-sample">Sample</span>' if l.get("sample") else ""
    return f'<span class="badge {cls}">{E(l["status"])}</span>{sample}'


def listing_card(l, p):
    tags = []
    if l["single_level"]:
        tags.append("Single-level")
    if l["community_55"]:
        tags.append("55+ community")
    tag_html = "".join(f'<span class="chip">{t}</span>' for t in tags)
    data = (f'data-price="{l["price"]}" data-beds="{l["beds"]}" data-type="{E(l["type"])}" '
            f'data-single="{1 if l["single_level"] else 0}" data-55="{1 if l["community_55"] else 0}" '
            f'data-status="{E(l["status"])}"')
    return (f'<a class="lcard" href="{p}listings/{l["slug"]}.html" {data}>'
            f'<div class="lphoto">{img(l["photos"][0], p, l["title"], 800, 560, "(max-width: 700px) 100vw, 420px")}'
            f'<div class="badges">{status_badge(l)}</div></div>'
            f'<div class="lbody"><p class="price">{money(l["price"])}</p>'
            f'<p class="specs"><strong>{l["beds"]}</strong> bd · <strong>{baths(l["baths"])}</strong> ba · <strong>{l["sqft"]:,}</strong> sq ft</p>'
            f'<h3>{E(l["title"])}</h3><p class="addr">{E(l["street"])}, {E(l["city"])}, {E(l["state"])}</p>'
            f'<div class="chips">{tag_html}</div></div></a>')


def guide_card(g, p):
    return (f'<a class="gcard" href="{p}guides/{g["slug"]}.html"><span class="tag">Guide</span>'
            f'<h3>{E(g["title"])}</h3><p>{E(g["desc"])}</p><span class="more">Read the guide · {g["minutes"]} min</span></a>')


def breadcrumbs(items, p):
    lis = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            lis.append(f'<li><a href="{p}{href}">{E(label)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{E(label)}</li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def agent_ld():
    return {"@type": "RealEstateAgent", "name": S["site_name"], "url": S["site_url"] + "/",
            "telephone": S["phone"], "email": S["email"], "areaServed": S["service_area"]}


def cta_box(p, heading="Have a question about buying or selling?", text=None):
    text = text or "Call or email for a friendly, no-pressure conversation. We will answer your questions and explain your options in plain English."
    tel = "tel:" + "".join(c for c in S["phone"] if c.isdigit() or c == "+")
    return (f'<section class="cta-box no-print"><h2>{E(heading)}</h2><p>{E(text)}</p>'
            f'<div class="cta-actions"><a class="btn btn-primary" href="{tel}">{ICON_PHONE} Call {E(S["phone"])}</a>'
            f'<a class="btn btn-ghost" href="{p}contact.html">{ICON_MAIL} Send a message</a></div></section>')


def contact_form(p, kind="contact", listing=None):
    endpoint = S["form_endpoint"]
    action = f' action="{E(endpoint)}" method="POST"' if endpoint else ' action="#"'
    subject = {"contact": "Website message", "valuation": "Home value request", "showing": "Showing request"}[kind]
    if listing:
        subject += f' – {listing["street"]}'
    extra = ""
    if kind == "valuation":
        extra = ('<div class="field"><label for="f-addr">Property address</label><input id="f-addr" name="address" autocomplete="street-address" required></div>'
                 '<div class="field"><label for="f-time">When are you thinking of selling?</label><select id="f-time" name="timeline">'
                 '<option>Just exploring</option><option>Within 3 months</option><option>3 to 6 months</option><option>6 to 12 months</option><option>More than a year</option></select></div>')
    msg_default = ""
    if kind == "showing" and listing:
        msg_default = f"I would like more information about {listing['street']}."
    return f"""
<form class="lead-form" data-form data-email="{E(S['email'])}" data-subject="{E(subject)}"{action}>
  <input type="hidden" name="_subject" value="{E(subject)}">
  <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
  <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  {extra}
  <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="4">{E(msg_default)}</textarea></div>
  <label class="consent"><input type="checkbox" name="consent" required> <span>I agree that {E(S['site_name'])} may contact me by phone or email about my request. I can opt out at any time. See our <a href="{p}privacy-policy.html">Privacy Policy</a>.</span></label>
  <button type="submit" class="btn btn-primary btn-block">Send</button>
  <p class="form-note" hidden></p>
</form>"""


def head_ads():
    if S["adsense_client"]:
        return ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
                + E(S["adsense_client"]) + '" crossorigin="anonymous"></script>')
    return "<!-- AdSense code goes here -->"


def layout(path, title, description, body, active=None, jsonld=None, noindex=False, og_image=None, og_type="website"):
    p = prefix(path)
    full_title = title if title == S["site_name"] else f"{title} | {S['site_name']}"
    canonical = canonical_for(path)
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{p}{h}"{cur if k == active else ""}>{E(l)}</a></li>' for l, h, k in NAV)
    lds = jsonld if isinstance(jsonld, list) else ([jsonld] if jsonld else [])
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in lds)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    og = f'<meta property="og:image" content="{E(og_image)}">' if og_image else ""
    tel = "tel:" + "".join(c for c in S["phone"] if c.isdigit() or c == "+")
    page = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{E(S['site_name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{E(canonical)}">
{og}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121820" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-title" content="{E(S['site_name'])}">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="stylesheet" href="{p}assets/css/style.css">
<script>try{{var s=localStorage.getItem("bcr-text-size");if(s==="1")document.documentElement.classList.add("text-lg");if(s==="2")document.documentElement.classList.add("text-xl");}}catch(e){{}}</script>
{head_ads()}
{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{p}index.html"><picture><source srcset="{p}assets/img/logo-white.svg" media="(prefers-color-scheme: dark)"><img src="{p}assets/img/logo.svg" alt="{E(S['site_name'])}" width="401" height="100"></picture></a>
    <div class="header-actions">
      <button type="button" class="text-size-btn" aria-label="Change text size"><span aria-hidden="true">A<span class="big">A</span></span></button>
      <a class="call-btn" href="{tel}" aria-label="Call {E(S['phone'])}">{ICON_PHONE}<span>Call</span></a>
      <button type="button" class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
    </div>
    <nav class="site-nav" id="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
<div class="container">
{body}
</div>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h2>{E(S['site_name'])}</h2>
        <p>{E(S['agent_name'])}, {E(S['agent_title'])}<br>License #{E(S['license'])}</p>
        <p>Brokered by {E(S['brokerage'])}<br>Brokerage license #{E(S['brokerage_license'])}<br>{E(S['office_address'])}</p>
        <p><a href="{tel}">{E(S['phone'])}</a> · <a href="mailto:{E(S['email'])}">{E(S['email'])}</a></p>
      </div>
      <div>
        <h2>Explore</h2>
        <ul><li><a href="{p}listings/index.html">Homes for sale</a></li><li><a href="{p}sell.html">Sell your home</a></li>
        <li><a href="{p}mortgage-calculator.html">Mortgage calculator</a></li><li><a href="{p}guides/index.html">Guides for buyers and sellers</a></li></ul>
      </div>
      <div>
        <h2>Information</h2>
        <ul><li><a href="{p}about.html">About</a></li><li><a href="{p}contact.html">Contact</a></li>
        <li><a href="{p}privacy-policy.html">Privacy Policy</a></li><li><a href="{p}terms-of-use.html">Terms of Use</a></li>
        <li><a href="{p}disclaimer.html">Disclaimer</a></li><li><a href="{p}fair-housing.html">Fair Housing</a></li>
        <li><a href="{p}accessibility.html">Accessibility</a></li></ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="eho-line">{EHO_ICON}<span>Equal Housing Opportunity. We are committed to the letter and spirit of the federal Fair Housing Act.</span></p>
      <p>Listing information is deemed reliable but not guaranteed and should be independently verified. &copy; {U.year} {E(S['site_name'])}.</p>
    </div>
  </div>
</footer>
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
"""
    dest = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(page)


# ---------------------------------------------------------------------------
# Listings
# ---------------------------------------------------------------------------
def build_listing_pages():
    for l in LISTINGS:
        path = f"listings/{l['slug']}.html"
        p = prefix(path)
        alt = l["title"]
        gallery = "".join(
            f'<figure class="g-item">{img(ph, p, f"{alt}, photo {i + 1}", 1200, 800, "(max-width: 900px) 100vw, 860px", eager=(i == 0))}</figure>'
            for i, ph in enumerate(l["photos"]))
        facts = [("Price", money(l["price"])), ("Bedrooms", str(l["beds"])), ("Bathrooms", baths(l["baths"])),
                 ("Living area", f'{l["sqft"]:,} sq ft'), ("Home type", l["type"]), ("Year built", str(l["year"])),
                 ("Lot", l["lot"]), ("Parking", l["garage"]),
                 ("HOA", f'{money(l["hoa"])}/month' if l["hoa"] else "None"),
                 ("Single-level living", "Yes" if l["single_level"] else "No"),
                 ("55+ community", "Yes" if l["community_55"] else "No")]
        if l.get("mls"):
            facts.append(("MLS #", l["mls"]))
        facts_html = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in facts)
        desc = "".join(f"<p>{E(x)}</p>" for x in l["description"])
        feats = "".join(f"<li>{E(x)}</li>" for x in l["features"])
        sample_banner = ('<div class="sample-banner" role="note"><strong>Sample listing.</strong> This page demonstrates the layout of the website. '
                         'It is not a real property for sale.</div>') if l.get("sample") else ""
        others = [o for o in LISTINGS if o["slug"] != l["slug"] and o["status"] != "Sold"][:3]
        map_q = "+".join(f'{l["city"]} {l["state"]}'.split())
        body = f"""
{breadcrumbs([("Home", "index.html"), ("Homes for Sale", "listings/index.html"), (l["title"], None)], p)}
{sample_banner}
<div class="listing-layout">
<article class="listing">
  <div class="gallery" data-gallery>{gallery}</div>
  <p class="gallery-hint no-print">Swipe or scroll to see {len(l["photos"])} photos</p>
  <div class="listing-head">
    <div class="badges inline">{status_badge(l)}</div>
    <p class="price big">{money(l["price"])}</p>
    <p class="specs big"><strong>{l["beds"]}</strong> bedrooms · <strong>{baths(l["baths"])}</strong> baths · <strong>{l["sqft"]:,}</strong> sq ft</p>
    <h1>{E(l["title"])}</h1>
    <p class="addr">{E(l["street"])}, {E(l["city"])}, {E(l["state"])} {E(l["zip"])}</p>
    <div class="action-row no-print">
      <a class="btn btn-primary" href="#ask">Ask about this home</a>
      <button type="button" class="btn btn-ghost" data-share="{E(l['title'])}">{ICON_SHARE} Share</button>
    </div>
  </div>
  <p class="lead">{E(l["summary"])}</p>
  <h2>About this home</h2>
  {desc}
  <h2>Features</h2>
  <ul class="features">{feats}</ul>
  <h2>Home facts</h2>
  <dl class="facts">{facts_html}</dl>
  <h2>Estimated monthly payment</h2>
  <div class="mini-calc" data-calc data-price="{l['price']}" data-hoa="{l['hoa']}">
    <div class="calc-grid">
      <label>Down payment (%)<input type="number" inputmode="decimal" name="down" value="20" min="0" max="100" step="1"></label>
      <label>Interest rate (%)<input type="number" inputmode="decimal" name="rate" value="6.5" min="0" max="20" step="0.125"></label>
      <label>Loan term (years)<select name="term"><option selected>30</option><option>20</option><option>15</option></select></label>
    </div>
    <p class="calc-out" aria-live="polite">Principal and interest: <strong data-out>—</strong></p>
    <p class="small">An estimate only. Does not include property taxes or insurance. Use the full <a href="{p}mortgage-calculator.html">mortgage calculator</a> or ask a lender for an exact quote.</p>
  </div>
  <p><a href="https://www.google.com/maps/search/?api=1&amp;query={E(map_q)}" rel="noopener" target="_blank">See the area on Google Maps</a></p>
  <p class="small">Information is deemed reliable but not guaranteed. Square footage, lot size, HOA fees and other details should be verified independently. Listing courtesy of {E(S["brokerage"])}.</p>
</article>
<aside class="listing-side" id="ask">
  <div class="side-box">
    <h2>Ask about this home</h2>
    <p class="agent-line"><strong>{E(S["agent_name"])}</strong><br>{E(S["brokerage"])}</p>
    {contact_form(p, "showing", l)}
  </div>
</aside>
</div>
<section class="more-listings no-print"><h2>More homes for sale</h2><div class="lgrid">{"".join(listing_card(o, p) for o in others)}</div></section>
"""
        ld = None
        if not l.get("sample"):
            ld = {"@context": "https://schema.org", "@type": "RealEstateListing", "name": l["title"],
                  "url": canonical_for(path), "datePosted": UPDATED_ISO, "image": [photo_abs(x) for x in l["photos"]],
                  "offers": {"@type": "Offer", "price": l["price"], "priceCurrency": "USD"}}
        layout(path, f'{l["title"]} – {l["city"]}, {l["state"]}',
               f'{l["beds"]} bed, {baths(l["baths"])} bath, {l["sqft"]:,} sq ft {l["type"].lower()} for {money(l["price"])}. {l["summary"]}',
               body, active="listings", jsonld=ld, noindex=bool(l.get("sample")), og_image=photo_abs(l["photos"][0]))
        if not l.get("sample"):
            PAGES.append((path, "0.8"))


def build_listings_index():
    path = "listings/index.html"
    p = prefix(path)
    order = {"Coming Soon": 1, "For Sale": 0, "Pending": 2, "Sold": 3}
    ls = sorted(LISTINGS, key=lambda x: (order.get(x["status"], 4), x["price"]))
    types = sorted({l["type"] for l in LISTINGS})
    type_opts = "".join(f"<option>{E(t)}</option>" for t in types)
    body = f"""
{breadcrumbs([("Home", "index.html"), ("Homes for Sale", None)], p)}
<h1>Homes for Sale</h1>
<p class="lead">Browse homes in {E(S["service_area"])}. Use the filters to find single-level homes, homes in 55+ communities, and homes within your budget.</p>
<form class="filters no-print" data-filters onsubmit="return false">
  <label>Max price<select name="price"><option value="">Any</option><option value="250000">$250,000</option><option value="300000">$300,000</option><option value="350000">$350,000</option><option value="400000">$400,000</option><option value="500000">$500,000</option></select></label>
  <label>Bedrooms<select name="beds"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option></select></label>
  <label>Home type<select name="type"><option value="">Any</option>{type_opts}</select></label>
  <label class="check"><input type="checkbox" name="single"> Single-level</label>
  <label class="check"><input type="checkbox" name="c55"> 55+ community</label>
  <label class="check"><input type="checkbox" name="active" checked> Hide sold</label>
</form>
<p class="results-count" aria-live="polite" data-count></p>
<div class="lgrid" data-listings>{"".join(listing_card(l, p) for l in ls)}</div>
<p class="no-results" hidden>No homes match those filters. Try widening your search, or <a href="{p}contact.html">tell us what you are looking for</a>.</p>
{cta_box(p, "Don’t see the right home?", "Not every home is listed online. Tell us what you are looking for, and we will let you know when something comes up.")}
"""
    layout(path, "Homes for Sale", f"Homes for sale in {S['service_area']}: single-level homes, condos, townhomes and homes in 55+ communities.",
           body, active="listings")
    PAGES.append((path, "0.9"))


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def build_home():
    path, p = "index.html", ""
    featured = [l for l in LISTINGS if l["status"] in ("For Sale", "Coming Soon")][:3]
    hero = img(HERO_PHOTO, p, "A welcoming home with a front lawn", 1600, 900, "100vw", eager=True)
    body = f"""
<section class="hero">
  <div class="hero-img">{hero}</div>
  <div class="hero-text">
    <p class="eyebrow">{E(S["service_area"])}</p>
    <h1>Real estate help for your next chapter</h1>
    <p>Downsizing, moving closer to family, or finding a single-level home? Get patient, honest guidance from someone who listens.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="listings/index.html">See homes for sale</a><a class="btn btn-light" href="sell.html">What’s my home worth?</a></div>
  </div>
</section>

<section class="quick-links" aria-label="Popular searches">
  <a href="listings/index.html#single">🏡 <span>Single-level homes</span></a>
  <a href="listings/index.html#c55">🌳 <span>55+ communities</span></a>
  <a href="listings/index.html#condo">🏢 <span>Condos &amp; townhomes</span></a>
  <a href="sell.html">💬 <span>Selling a family home</span></a>
</section>

<section aria-labelledby="feat-h">
  <div class="section-head"><h2 id="feat-h">Featured homes</h2><a href="listings/index.html">All homes →</a></div>
  <div class="lgrid">{"".join(listing_card(l, p) for l in featured)}</div>
</section>

<section class="why" aria-labelledby="why-h">
  <h2 id="why-h">Why work with us</h2>
  <div class="why-grid">
    <div><h3>Patient, no-pressure help</h3><p>We take time to explain every step, answer every question, and never rush your decisions.</p></div>
    <div><h3>Downsizing experience</h3><p>We help you sell the family home and find a right-sized next home, and can connect you with trusted movers and estate sale professionals.</p></div>
    <div><h3>Local knowledge</h3><p>We know the neighborhoods, the 55+ communities, and where to find single-level homes near shops and doctors.</p></div>
    <div><h3>Clear communication</h3><p>Phone calls, emails, or a visit at your kitchen table. Whatever is easiest for you.</p></div>
  </div>
</section>

<section aria-labelledby="g-h">
  <div class="section-head"><h2 id="g-h">Guides for buyers and sellers</h2><a href="guides/index.html">All guides →</a></div>
  <div class="ggrid">{"".join(guide_card(g, p) for g in GUIDES[:4])}</div>
</section>

<section class="tools-strip" aria-label="Tools">
  <a href="mortgage-calculator.html"><strong>Mortgage calculator</strong><span>Estimate a monthly payment</span></a>
  <a href="guides/downsizing-checklist.html"><strong>Downsizing checklist</strong><span>A step-by-step moving plan</span></a>
  <a href="sell.html"><strong>Free home value review</strong><span>Find out what your home could sell for</span></a>
</section>

{cta_box(p)}
"""
    ld = {"@context": "https://schema.org", **agent_ld()}
    layout(path, S["site_name"], f"Real estate help for homebuyers and sellers 50+ in {S['service_area']}: single-level homes, condos, 55+ communities, downsizing and selling the family home.",
           body, active="home", jsonld=ld, og_image=photo_abs(HERO_PHOTO))
    PAGES.append((path, "1.0"))


def build_sell():
    path, p = "sell.html", ""
    body = f"""
{breadcrumbs([("Home", "index.html"), ("Sell Your Home", None)], p)}
<div class="two-col">
<div class="prose">
<h1>Sell Your Home with Confidence</h1>
<p class="lead">Selling a home you have lived in for years is a big step. We make it simpler, with clear advice, careful pricing, and help with every detail from decluttering to closing day.</p>
<h2>How we help</h2>
<ul>
  <li><strong>A free, no-obligation home value review</strong> based on recent sales near you.</li>
  <li><strong>A clear plan and timeline</strong> that fits your next move, whether you buy first or sell first.</li>
  <li><strong>Help getting ready</strong>, including referrals to trusted handymen, cleaners, movers, senior move managers, and estate sale companies.</li>
  <li><strong>Professional marketing</strong> with quality photos and a detailed listing.</li>
  <li><strong>Careful negotiation</strong> and regular updates, by phone or email, whichever you prefer.</li>
  <li><strong>Support through closing</strong>, so you always know what comes next.</li>
</ul>
<h2>Thinking about downsizing?</h2>
<p>Read our <a href="guides/selling-your-home-after-50.html">step-by-step guide to selling your home after 50</a> and the <a href="guides/downsizing-checklist.html">downsizing checklist</a>.</p>
<p class="small">A home value review is an opinion of market value from a real estate licensee, not an appraisal. We will never share your information with other companies.</p>
</div>
<aside class="side-box" id="value">
  <h2>Request a free home value review</h2>
  <p>Tell us a little about your home and we will be in touch, usually within one business day.</p>
  {contact_form(p, "valuation")}
</aside>
</div>
"""
    layout(path, "Sell Your Home", f"Selling your home in {S['service_area']}? Get a free home value review and patient, step-by-step help from listing to closing.",
           body, active="sell")
    PAGES.append((path, "0.9"))


def build_calculator():
    path, p = "mortgage-calculator.html", ""
    body = f"""
{breadcrumbs([("Home", "index.html"), ("Mortgage Calculator", None)], p)}
<div class="readable">
<h1>Mortgage Calculator</h1>
<p class="lead">Estimate your monthly payment, including property taxes, insurance, and HOA fees.</p>
<div class="calculator" data-full-calc>
  <div class="calc-grid">
    <label>Home price ($)<input type="number" inputmode="decimal" name="price" value="350000" min="0" step="1000"></label>
    <label>Down payment (%)<input type="number" inputmode="decimal" name="down" value="20" min="0" max="100" step="1"></label>
    <label>Interest rate (%)<input type="number" inputmode="decimal" name="rate" value="6.5" min="0" max="20" step="0.125"></label>
    <label>Loan term (years)<select name="term"><option selected>30</option><option>20</option><option>15</option></select></label>
    <label>Property tax ($ per year)<input type="number" inputmode="decimal" name="tax" value="4200" min="0" step="100"></label>
    <label>Home insurance ($ per year)<input type="number" inputmode="decimal" name="ins" value="1800" min="0" step="100"></label>
    <label>HOA ($ per month)<input type="number" inputmode="decimal" name="hoa" value="0" min="0" step="10"></label>
  </div>
  <div class="calc-results" aria-live="polite">
    <div><span>Loan amount</span><strong data-o="loan">—</strong></div>
    <div><span>Principal &amp; interest</span><strong data-o="pi">—</strong></div>
    <div><span>Taxes, insurance &amp; HOA</span><strong data-o="extra">—</strong></div>
    <div class="total"><span>Estimated monthly total</span><strong data-o="total">—</strong></div>
  </div>
</div>
<p class="small">This calculator gives estimates for information only. It is not a loan offer or a guarantee of terms. Actual rates, taxes, insurance, and fees vary. Speak with a licensed mortgage lender for a quote.</p>
<h2>Paying cash?</h2>
<p>Many buyers who are downsizing use proceeds from selling their current home to buy with cash or a smaller mortgage. Even with cash, budget for property taxes, insurance, HOA fees, and closing costs. Read <a href="guides/understanding-closing-costs.html">Understanding Closing Costs</a>.</p>
</div>
"""
    layout(path, "Mortgage Calculator", "Free mortgage calculator: estimate your monthly payment with taxes, insurance and HOA fees.", body)
    PAGES.append((path, "0.6"))


# ---------------------------------------------------------------------------
# Guides
# ---------------------------------------------------------------------------
def build_guides():
    for g in GUIDES:
        path = f"guides/{g['slug']}.html"
        p = prefix(path)
        others = "".join(guide_card(o, p) for o in GUIDES if o["slug"] != g["slug"])
        body = f"""
<article class="prose readable">
{breadcrumbs([("Home", "index.html"), ("Guides", "guides/index.html"), (g["title"], None)], p)}
<h1>{E(g["title"])}</h1>
<p class="meta">By {E(S["agent_name"])} · Updated {UPDATED_HUMAN} · {g["minutes"]} min read</p>
{g["body"].replace("{p}", p)}
</article>
{cta_box(p)}
<section class="no-print"><h2>More guides</h2><div class="ggrid">{others}</div></section>
"""
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
              "datePublished": UPDATED_ISO, "dateModified": UPDATED_ISO,
              "author": {"@type": "Person", "name": S["agent_name"]}, "publisher": agent_ld(),
              "mainEntityOfPage": canonical_for(path)}
        layout(path, g["title"], g["desc"], body, active="guides", jsonld=ld, og_type="article")
        PAGES.append((path, "0.7"))
    path = "guides/index.html"
    p = prefix(path)
    body = f"""
{breadcrumbs([("Home", "index.html"), ("Guides", None)], p)}
<div class="readable"><h1>Guides for Buyers and Sellers</h1>
<p class="lead">Plain-English guides to selling a long-time home, downsizing, 55+ communities, closing costs, and finding a home that is easy to live in for years to come.</p></div>
<div class="ggrid">{"".join(guide_card(g, p) for g in GUIDES)}</div>
"""
    layout(path, "Guides for Buyers and Sellers", "Real estate guides for homebuyers and sellers 50+: downsizing, selling the family home, 55+ communities and closing costs.", body, active="guides")
    PAGES.append((path, "0.7"))


# ---------------------------------------------------------------------------
# About, contact and policy pages
# ---------------------------------------------------------------------------
def info_page(path, title, desc, inner, active=None, updated=True, priority="0.4"):
    p = prefix(path)
    upd = f'<p class="meta">Last updated: {UPDATED_HUMAN}</p>' if updated else ""
    body = f'<article class="prose readable">{breadcrumbs([("Home", "index.html"), (title, None)], p)}<h1>{E(title)}</h1>{upd}{inner}</article>'
    layout(path, title, desc, body, active=active)
    PAGES.append((path, priority))


def build_info():
    name = E(S["site_name"])
    mail = f'<a href="mailto:{E(S["email"])}">{E(S["email"])}</a>'
    tel = "tel:" + "".join(c for c in S["phone"] if c.isdigit() or c == "+")
    phone = f'<a href="{tel}">{E(S["phone"])}</a>'

    info_page("about.html", "About", f"Meet {S['agent_name']} of {S['site_name']}, helping buyers and sellers 50+ in {S['service_area']}.", f"""
<div class="agent-card"><img src="assets/img/agent-placeholder.svg" alt="Photo of {E(S['agent_name'])}" width="160" height="160">
<div><p class="agent-name">{E(S['agent_name'])}</p><p>{E(S['agent_title'])}<br>License #{E(S['license'])}<br>{E(S['brokerage'])}</p><p>{phone} · {mail}</p></div></div>
<p class="lead">{name} helps homeowners and homebuyers in {E(S['service_area'])} through life’s next chapter, whether that means downsizing, moving closer to family, or finding a home that is easier to live in.</p>
<h2>My approach</h2>
<p><em>Replace this section with your own story: how long you have been in real estate, why you enjoy working with clients who are downsizing or relocating, and what clients can expect when they work with you.</em></p>
<ul>
  <li>Patient explanations and no-pressure advice</li>
  <li>Regular updates by phone, email, or in person</li>
  <li>A network of trusted local professionals: lenders, inspectors, movers, estate sale companies, and senior move managers</li>
</ul>
<h2>Licensing</h2>
<p>{E(S['agent_name'])} is a licensed real estate salesperson in {E(S['state'])}, license #{E(S['license'])}, brokered by {E(S['brokerage'])}, license #{E(S['brokerage_license'])}, {E(S['office_address'])}.</p>
<h2>Advertising</h2>
<p>This website may display advertising from Google and other partners to help cover its costs. Advertisers do not influence our listings or guides. See our <a href="privacy-policy.html">Privacy Policy</a>.</p>
""", active="about", updated=False, priority="0.6")

    info_page("contact.html", "Contact", f"Contact {S['site_name']} by phone, email or message about buying or selling a home in {S['service_area']}.", f"""
<p class="lead">Questions about a home, selling, or your next move? We would love to hear from you. There is never any obligation.</p>
<div class="contact-methods">
  <a class="btn btn-primary" href="{tel}">{ICON_PHONE} Call {E(S['phone'])}</a>
  <a class="btn btn-ghost" href="mailto:{E(S['email'])}">{ICON_MAIL} Email {E(S['email'])}</a>
</div>
<p>Office: {E(S['office_address'])}</p>
<h2>Send a message</h2>
{contact_form("", "contact")}
<p class="small">Please do not send sensitive financial information, such as bank account numbers, by email or through this form.</p>
""", active="contact", updated=False, priority="0.6")

    info_page("privacy-policy.html", "Privacy Policy", f"How {S['site_name']} collects, uses and protects your information, including cookies and Google advertising.", f"""
<p>This Privacy Policy explains how {name} (“we,” “us”) collects, uses, and protects information when you visit {E(S['site_url'])}.</p>
<h2>Information we collect</h2>
<ul>
  <li><strong>Information you give us:</strong> When you contact us or request a home value review, we collect your name, email address, phone number (optional), property address (if provided), and your message.</li>
  <li><strong>Information collected automatically:</strong> Our hosting provider and advertising partners may collect your IP address, browser type, device information, pages visited, and the date and time of your visit.</li>
  <li><strong>Settings stored on your device:</strong> If you use the Text size button, your choice is saved in your browser’s local storage on your device only.</li>
</ul>
<h2>How we use information</h2>
<ul>
  <li>To respond to your questions and provide real estate services you request</li>
  <li>To send you information you ask for, such as homes that match your search</li>
  <li>To operate, secure, and improve this website</li>
  <li>To display advertising</li>
  <li>To comply with legal obligations</li>
</ul>
<h2>How we share information</h2>
<p>We do not sell your personal information. We share it only as needed to provide the services you request (for example, with our brokerage, a lender, or a title company you choose to work with), with service providers that help us operate this website, or when required by law. We do not share your phone number with other companies for their marketing.</p>
<h2>Phone and email contact</h2>
<p>If you give us your phone number or email, we will contact you only about your request. You can ask us to stop at any time by replying “STOP” or emailing {mail}.</p>
<h2>Cookies and advertising</h2>
<ul>
  <li>Third-party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites.</li>
  <li>Google’s use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet.</li>
  <li>You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com/" rel="noopener">Google Ads Settings</a>, or opt out of third-party vendors’ cookies at <a href="https://www.aboutads.info/choices/" rel="noopener">www.aboutads.info</a>.</li>
  <li>See <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites or apps that use its services</a>.</li>
</ul>
<h2>Your privacy rights</h2>
<p>Depending on where you live, including California, Colorado, Connecticut, Virginia, Texas, and other states with consumer privacy laws, you may have the right to access, correct, delete, or obtain a copy of your personal information, and to opt out of targeted advertising or the sale or sharing of personal information. To make a request, email {mail}. We will not discriminate against you for exercising your rights. Your browser’s Global Privacy Control signal will be honored where required by law.</p>
<h2>Data security and retention</h2>
<p>We use reasonable safeguards to protect your information and keep it only as long as needed for the purposes above or as required by law and real estate record-keeping rules.</p>
<h2>Children</h2>
<p>This website is not directed to children under 13, and we do not knowingly collect their information.</p>
<h2>Changes</h2>
<p>We may update this policy. The date at the top shows when it last changed.</p>
<h2>Contact</h2>
<p>{E(S['site_name'])}, {E(S['office_address'])} · {mail} · {phone}</p>
""", priority="0.3")

    info_page("terms-of-use.html", "Terms of Use", f"Terms of use for the {S['site_name']} website.", f"""
<p>By using this website, you agree to these Terms of Use.</p>
<h2>Information only</h2>
<p>Content on this website, including listings, guides, and calculators, is provided for general information. It is not legal, tax, financial, or investment advice. Consult qualified professionals before making decisions.</p>
<h2>Listings</h2>
<p>Listing information is provided for consumers’ personal, non-commercial use and may not be used for any purpose other than identifying properties consumers may be interested in purchasing. Information is deemed reliable but is not guaranteed. Prices, availability, and details may change without notice.</p>
<h2>No agency relationship</h2>
<p>Using this website or contacting us does not by itself create an agency or client relationship. Any such relationship is established only by a written agreement as required by {E(S['state'])} law.</p>
<h2>Intellectual property</h2>
<p>Text, design, and logos on this website belong to {name} or its licensors. Listing photos may be owned by third parties. Do not copy or republish content without permission.</p>
<h2>Acceptable use</h2>
<p>Do not misuse this website, attempt to access it without authorization, scrape content in bulk, or submit false information.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, {name} is not liable for any damages arising from your use of this website or reliance on its content.</p>
<h2>Changes</h2>
<p>We may update these terms at any time by posting a new version on this page.</p>
""", priority="0.3")

    info_page("disclaimer.html", "Disclaimer", f"Disclaimer for listings, guides and calculators on {S['site_name']}.", f"""
<h2>Listings</h2>
<p>Listing information, including prices, square footage, lot size, HOA fees, school information, and features, is deemed reliable but not guaranteed and should be independently verified. Properties may be sold, withdrawn, or changed without notice. Photos may be representative.</p>
<p>Listings marked <strong>“Sample”</strong> are demonstrations of this website’s layout and are not real properties for sale.</p>
<h2>Guides and calculators</h2>
<p>Our guides and the mortgage calculator provide general information and estimates only. They are not legal, tax, financial, or lending advice and are not an offer to lend. Consult a licensed mortgage lender, tax professional, or attorney about your situation.</p>
<h2>Home value reviews</h2>
<p>A home value review or comparative market analysis is an opinion of value by a real estate licensee. It is not an appraisal.</p>
<h2>External links</h2>
<p>We are not responsible for the content of websites we link to.</p>
<h2>Advertising</h2>
<p>Advertisements on this website are provided by third parties. We do not endorse advertised products or services.</p>
""", priority="0.3")

    info_page("fair-housing.html", "Fair Housing Statement", f"{S['site_name']} is committed to fair housing and equal opportunity.", f"""
<p class="eho-line">{EHO_ICON}<span><strong>Equal Housing Opportunity</strong></span></p>
<p>{name} is committed to compliance with all federal, state, and local fair housing laws. We do not discriminate against any person because of race, color, religion, sex (including sexual orientation and gender identity), handicap or disability, familial status, or national origin, or any other class protected by state or local law.</p>
<p>We will not say, write, or do anything that limits a person’s housing choices based on a protected characteristic. We serve every client with the same level of professionalism and care.</p>
<h2>Housing for older persons</h2>
<p>Some communities shown on this website may be “housing for older persons” (such as 55+ communities) that meet the requirements of the federal Housing for Older Persons Act. Those communities set their own age eligibility rules. Homes in other communities are available to all qualified buyers regardless of age or familial status.</p>
<h2>Learn more or report discrimination</h2>
<p>If you believe you have experienced housing discrimination, contact the U.S. Department of Housing and Urban Development (HUD) at <a href="https://www.hud.gov/fairhousing" rel="noopener">hud.gov/fairhousing</a> or call 1-800-669-9777.</p>
""", priority="0.4")

    info_page("accessibility.html", "Accessibility Statement", f"Our commitment to making {S['site_name']} accessible to everyone.", f"""
<p>We want everyone to be able to use this website, including people with low vision, hearing loss, limited mobility, or other disabilities.</p>
<h2>What we do</h2>
<ul>
  <li>Large, readable text with strong color contrast, and a <strong>Text size</strong> button (“AA” at the top of every page)</li>
  <li>Descriptive text for images and clear headings for screen readers</li>
  <li>Pages that work with keyboard navigation and with your device’s zoom and accessibility settings</li>
  <li>Large, easy-to-tap buttons on phones</li>
</ul>
<p>We aim to follow the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA.</p>
<h2>Need help?</h2>
<p>If you have trouble using any part of this website, call {phone} or email {mail}, and we will gladly provide the information another way.</p>
""", priority="0.3")


def build_404():
    body = """
<div class="readable"><h1>Page not found</h1>
<p class="lead">Sorry, we could not find that page. It may have moved, or the home may no longer be listed.</p>
<p><a class="btn btn-primary" href="/listings/index.html">See homes for sale</a> <a class="btn btn-ghost" href="/index.html">Go to the home page</a></p></div>
"""
    layout("404.html", "Page not found", "This page could not be found.", body, noindex=True)
    f = os.path.join(OUT, "404.html")
    t = open(f, encoding="utf-8").read()
    import re
    t = re.sub(r'(href|src|srcset)="(?!/|https?:|mailto:|tel:|#)([^"]+)"', r'\1="/\2"', t)
    open(f, "w", encoding="utf-8").write(t)


def build_support():
    urls = "".join(f"  <url><loc>{E(canonical_for(pth))}</loc><lastmod>{UPDATED_ISO}</lastmod><priority>{pri}</priority></url>\n" for pth, pri in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {S['site_url']}/sitemap.xml\n")
    pub = S["adsense_client"].replace("ca-", "") if S["adsense_client"] else "pub-0000000000000000"
    note = "" if S["adsense_client"] else "# Replace pub-0000000000000000 with your AdSense publisher ID once approved.\n"
    open(os.path.join(OUT, "ads.txt"), "w").write(f"{note}google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    man = {"name": S["site_name"], "short_name": S["site_name"], "start_url": "/", "display": "browser",
           "background_color": "#ffffff", "theme_color": "#1b4d5c",
           "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    json.dump(man, open(os.path.join(OUT, "site.webmanifest"), "w"), indent=2)


def main():
    build_home()
    build_listings_index()
    build_listing_pages()
    build_sell()
    build_calculator()
    build_guides()
    build_info()
    build_404()
    build_support()
    samples = sum(1 for l in LISTINGS if l.get("sample"))
    print(f"Built site into {OUT}: {len(LISTINGS)} listings ({samples} marked as samples), {len(GUIDES)} guides, {len(PAGES)} pages in sitemap.")
    if samples:
        print("Reminder: sample listings are hidden from Google. Replace them with real listings (sample=False) before advertising.")


if __name__ == "__main__":
    main()
