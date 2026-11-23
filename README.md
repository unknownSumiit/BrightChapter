# Bright Chapter Realty — real estate agent website for buyers and sellers 50+ (iPhone-first)

Static HTML real estate agent website, mobile-first for iPhone, AdSense-ready, deploys to
**Azure Static Web Apps** from GitHub. Placeholders are in CAPITALS — replace them before publishing.

## What's included
- **Homes for Sale** with filters (max price, bedrooms, home type, single-level, 55+ community, hide sold)
- **Listing pages**: swipeable photo gallery, price and specs, features, home facts, built-in monthly
  payment estimate, "Ask about this home" form, share button
- **Sell Your Home** page with a free home value review request form
- **Mortgage calculator** (taxes, insurance, HOA)
- **5 guides**: selling after 50, downsizing checklist, 55+ communities explained, aging-in-place home features,
  closing costs
- About (agent card), Contact, Privacy Policy (Google ads cookies + US state privacy rights), Terms, Disclaimer,
  **Fair Housing statement** with Equal Housing Opportunity logo, Accessibility statement, 404
- Big tap targets, a sticky header with Call button, Text size (AA) button, dark mode
- sitemap.xml, robots.txt, ads.txt, web manifest, icons

## 1. Fill in your details
Open `tools/build.py` and edit `SETTINGS`: agent name, designations you actually hold, license numbers, brokerage,
state, service area, phone, email, office address and domain. Replace `site/assets/img/agent-placeholder.svg` with
your photo (save as `agent-placeholder.svg`, or change the file name on the About page in build.py).
Most states require the **brokerage name** (and some require license numbers) on every web page — the footer shows both.

## 2. Edit listings
Open `tools/listings.py`. Each home is one `{ ... }` block — copy a block to add a home.
- The 6 included homes are **samples** (`"sample": True`). They show a "Sample" label and banner and are hidden from
  Google. Replace them with real listings you are authorized to advertise, then set `"sample": False`.
- Photos: use Unsplash photo IDs, or save your own photos in `site/assets/img/listings/` and list them as
  `"local:my-photo.jpg"`. Use photos you have the right to publish (usually the listing photos from your MLS listing).
- If you show other brokers' listings (IDX), follow your MLS's display rules for attribution.

## 3. Forms
By default, forms open the visitor's email app with the message filled in. For forms that send directly,
create a free form at Formspree (or similar) and paste its URL into `form_endpoint`.

## 4. Build and deploy
Run `python3 tools/build.py`, then push to GitHub. In Azure: Static Web App (Free) → GitHub →
Build preset **Custom**, App location `site`, Output location blank. Add your domain, then submit
`/sitemap.xml` in Google Search Console. Apply for AdSense once the site is live with real content.

## 5. Google Ads — IMPORTANT for housing ads in the US
Google's **housing ads policy** applies to real estate ads in the United States and Canada. You **cannot** target
or exclude by **age, gender, parental status, marital status or ZIP code**. So you cannot target "50+" with
age settings for this site. Instead:
- Target by **location** (city, radius of at least 1 km) and **interests/topics** such as Real Estate,
  Retirement, Moving & Relocation, Senior Living.
- Reach older audiences through your **message**: ads about downsizing, single-level homes, 55+ communities.
- Devices: **Mobile phones**; optionally Operating system: iOS.
- Ad logos are in `brand/gdn/` (square 1200×1200 and landscape 1200×300).
Policy: https://support.google.com/adspolicy/answer/16701755

Also follow your state's real estate advertising rules and the Fair Housing Act in all ads.
