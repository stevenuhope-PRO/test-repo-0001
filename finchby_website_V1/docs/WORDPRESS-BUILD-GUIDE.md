# Finchby — building the prototype in WordPress, Elementor and Yoast SEO

The prototype in `finchby_website_V1/` is plain HTML and CSS. Every section is a simple row of columns,
so each maps directly to an Elementor container. No JavaScript is used, and all text is in plain HTML
(the same standing rule as in the Victory plan).

## 0. Two ways to go live

- **Quick (today):** publish `finchby_website_V1/` as it is on Cloudflare Pages (Cloudflare dashboard →
  Workers & Pages → Create → Pages → upload the folder or connect this repository, build output
  directory `finchby_website_V1`), then add `finchby.ai` as the custom domain. Free, and the domain is
  already at Cloudflare.
- **WordPress (the plan):** Cloudflare does not host WordPress. Buy WordPress hosting, install
  WordPress, and point the Cloudflare DNS records for `finchby.ai` at the host. Then follow below.

In Cloudflare → Security → Settings, keep AI crawlers on **Allow** (never Block).

## 1. Set-up

1. Theme: **Hello Elementor**. Plugins: **Elementor** (Pro is needed for the header/footer Theme
   Builder and the Form widget; otherwise use the free "Header Footer & Blocks" and WPForms Lite),
   **Yoast SEO**.
2. Settings → Permalinks → Post name. Settings → Reading → static home page.
3. Media → upload `assets/img/finch.svg` and `crest.svg` (SVG upload needs the "Safe SVG" plugin,
   or export PNGs).

## 2. Elementor Site Settings (global style)

| Global colour | Hex | Use |
|---|---|---|
| Background | `#FFFFFF` | page background |
| Soft | `#F5F7F5` | alternate bands, footer |
| Tint | `#E9F2ED` | badges, number tiles, call-to-action band |
| Ink | `#14261F` | headings, logo |
| Text | `#43524C` | body |
| Muted | `#6C7A74` | captions |
| Line | `#E2E8E4` | 1px borders |
| Brand | `#1D5C45` | buttons, links, eyebrows (hover `#154634`) |

| Global font | Family | Settings |
|---|---|---|
| Primary (headings) | Inter | 650/600; H1 58px, H2 38px, H3 18px; letter spacing -0.02em |
| Text | Inter | 400, 17px, line height 1.65 |
| Eyebrow | Inter | 600, 13px, uppercase, letter spacing 1.2px, Brand colour |

Layout: content width 1120px. Buttons: fully rounded (999px), Brand background, 13px x 24px padding.
Cards: white, 1px Line border, 14px radius, 26px padding.
The whole of `assets/css/style.css` can also be pasted into Site Settings -> Custom CSS (Pro) as a
shortcut, with the class names added under each widget's Advanced -> CSS Classes.

## 3. Pages and Yoast fields

| Page | Slug | Yoast SEO title | Focus keyphrase |
|---|---|---|---|
| Home | `/` | AI Visibility for Local Businesses \| Finchby | AI visibility for local businesses |
| Services | `/services/` | AI Visibility Services for Local Businesses \| Finchby | AI visibility services |
| How it works | `/approach/` | How AI Visibility Works \| Finchby | how AI visibility works |
| About | `/about/` | About Finchby \| AI Visibility Consultancy | AI visibility consultancy |
| Contact | `/contact/` | Book a Free Intro Call \| Finchby | Finchby contact |

Meta descriptions: copy from the `<meta name="description">` of each HTML file (all under 160
characters). Each page has exactly one H1.

Yoast → Settings → Site representation: Organization, name Finchby, logo the finch.
Yoast outputs Organization schema itself; the richer `ProfessionalService` block in `index.html`
can be added to the home page with an Elementor HTML widget. Add address and telephone to it once
you decide what to publish. Set a social share image (Yoast → Social) — one is not yet made.
Yoast generates `sitemap_index.xml` and manages `robots.txt`; the two static files are only for the
Cloudflare Pages route. No `llms.txt` is included, in keeping with your own advice.

## 4. Section → Elementor map

| Prototype block | Elementor |
|---|---|
| Header | Theme Builder header: container (row) → Image (finch) + Heading + Nav Menu |
| Hero | Container, 2 columns (55/45): Heading H1, Text, 2 Buttons / HTML widget holding the "AI answer" card (copy the `<div class="answer">` block) |
| Engine strip | Container (row, centred) of Text widgets styled as pills |
| Card rows | Container with 3 child containers; cards get Card background + 1px Rule border |
| Services list | Per group: container 25/75; left Heading H2 + Text; right repeated Heading H3 + Text. Status badge = small inline `<span class="status">` in the heading text |
| Check lists | Icon List with a check icon |
| Client story | Container with shadow, 2 columns; stats are Heading + Text on Tint background |
| Contact form | Form widget; keep the "How did you hear of us?" select and its AI options |
| Footer | Theme Builder footer, 3 columns |

To reveal a service later: in WordPress, change its badge text from "Coming soon" to
"Available now" (and remove the `soon` class). In the static version, edit `build.py`.

## 5. Before going live — decisions for you

- **Email:** the site uses `hello@finchby.ai` as a placeholder. Create it (Cloudflare Email
  Routing can forward it to your own mailbox free of charge) or change `EMAIL` in `build.py`.
- **Your name** appears on the About page as principal. Remove it if you prefer.
- **The case study** is anonymized ("a stone fabricator in Central Texas"). Ask the client before
  naming him, and before quoting any figures.
- **Tagline:** "Be the business AI recommends." is set once as `TAGLINE` in `build.py`.
- **Crest:** uses the Leslie motto *Grip Fast*; the site says it is a company emblem, not a grant of arms.
- **Client story figures** ("1 of 13", "4 list sites") come from your Victory baseline; get the
  client's agreement before publishing them.
- **Fees** are not shown.
- **Photographs:** none are used. A founder photo on the About page would add trust.
- The static contact form opens the visitor's email program; replace it with the Elementor form in
  WordPress (or a form service) for a proper submission.
