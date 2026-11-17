# Finchby — building the prototype in WordPress, Elementor and Yoast SEO

The prototype in `finchby-site/` is plain HTML and CSS. Every section is a simple row of columns,
so each maps directly to an Elementor container. No JavaScript is used, and all text is in plain HTML
(the same standing rule as in the Victory plan).

## 0. Two ways to go live

- **Quick (today):** publish `finchby-site/` as it is on Cloudflare Pages (Cloudflare dashboard →
  Workers & Pages → Create → Pages → upload the folder or connect this repository, build output
  directory `finchby-site`), then add `finchby.ai` as the custom domain. Free, and the domain is
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
| Paper | `#FAF8F3` | page background |
| Paper 2 | `#F2EFE7` | alternate bands, footer |
| Card | `#FFFEFB` | cards, form fields |
| Ink | `#1C1C1A` | headings, buttons, logo |
| Text | `#3A3936` | body |
| Muted | `#6F6D67` | eyebrows, captions |
| Rule | `#D8D3C7` | 1px borders |
| Accent | `#4A5A50` | links |

| Global font | Family | Settings |
|---|---|---|
| Primary (headings) | Cormorant Garamond | 500; H1 56px, H2 37px, H3 22px (600) |
| Text | EB Garamond | 400, 19px, line height 1.65 |
| Eyebrow / buttons / menu | Cormorant Garamond | 600, uppercase, letter spacing 2–3px |

Layout: content width 1080px. Buttons: square corners, Ink background, 13px × 28px padding.
The whole of `assets/css/style.css` can also be pasted into Site Settings → Custom CSS (Pro) as a
shortcut, with the class names added under each widget's Advanced → CSS Classes.

## 3. Pages and Yoast fields

| Page | Slug | Yoast SEO title | Focus keyphrase |
|---|---|---|---|
| Home | `/` | AI Visibility & Website Consultancy \| Finchby | AI visibility consultancy |
| Services | `/services/` | Services: AI Visibility, Listings & Websites \| Finchby | AI visibility services |
| Approach | `/approach/` | Our Approach to AI Visibility \| Finchby | AI visibility approach |
| About | `/about/` | About the Firm \| Finchby | Finchby |
| Contact | `/contact/` | Contact \| Finchby | contact Finchby |

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
| Hero | Container, 2 columns (75/25): Heading H1, Text, 2 Buttons / Image (crest) |
| "The matter in brief", cards | Container with 3 child containers; cards get Card background + 1px Rule border |
| Services list | Per group: container 25/75; left Heading H2 + Text; right repeated Heading H3 + Text. Status badge = small inline `<span class="status">` in the heading text |
| Principles lists | Icon List without icons, or Text Editor with list |
| Quote | Blockquote or Text Editor |
| Contact form | Form widget; keep the "How did you hear of us?" select and its AI options |
| Footer | Theme Builder footer, 3 columns |

To reveal a service later: in WordPress, change its badge text from "In preparation" to
"Offered at present" (and remove the `soon` class). In the static version, edit `build.py`.

## 5. Before going live — decisions for you

- **Email:** the site uses `enquiries@finchby.ai` as a placeholder. Create it (Cloudflare Email
  Routing can forward it to your own mailbox free of charge) or change `EMAIL` in `build.py`.
- **Your name** appears on the About page as principal. Remove it if you prefer.
- **The case study** is anonymized ("a stone fabricator in Central Texas"). Ask the client before
  naming him, and before quoting any figures.
- **Motto** *Fide et Opera* ("by trust and by work") and the arms are proposals; the arms are stated
  on the site to be a house mark, not a grant of arms.
- **Fees** are not shown.
- **Photographs:** none are used. Soft greyscale photographs can be added to the hero and About page.
- The static contact form opens the visitor's email program; replace it with the Elementor form in
  WordPress (or a form service) for a proper submission.
