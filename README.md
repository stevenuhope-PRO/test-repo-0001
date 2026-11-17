# finchby.ai website prototypes

Two home page prototypes for Finchby, an SEO agency for the AI search era.

| Version | Direction | Preview | Elementor import |
|---|---|---|---|
| V2 | Light, editorial, trust-led (cream, forest green, goldfinch yellow, serif headings) | `v2/index.html` | `elementor/finchby-v2-home.json` |
| V3 | Light, conversion-led (white, blue accent, 10 services, plan comparison table, industries section) | `v3/index.html` | `elementor/finchby-v3-home.json` |

Open either `index.html` in a browser to preview. Each is one self-contained file.

## Before launch: placeholders to replace

- **Pricing** ($2,500 audit, $3,500/month Growth) is sample pricing.
- **hello@finchby.ai** is an assumed address.
- **V3 hero report** and **V2 hero AI answer** are labeled illustrations, not real data.
- No testimonials, client logos or results are included. Add real ones when you have them.
- Privacy and Terms links in the footer need real pages.

## Import into WordPress + Elementor

1. Install the **Hello Elementor** theme, **Elementor** and **Yoast SEO**.
2. Pages → Add New → Edit with Elementor.
3. Folder icon (Add Template) → upload arrow → import `elementor/finchby-v2-home.json` or `-v3-`, then Insert.
4. Page Settings → Page Layout → **Elementor Canvas** (the template carries its own header and footer).
5. Settings → Reading → set the page as the static home page.

The import uses one full-width container per section, each holding an HTML widget, so it looks identical to the prototype. Fonts and CSS travel in the first container. To make a section editable with native widgets, rebuild it container by container using the same section order; class names (`fb-*` for V2, `f3-*` for V3) can be pasted into each widget's Advanced → CSS Classes to reuse the styling.

Swap the contact `<form>` for the Elementor **Form** widget (Pro) or your forms plugin. Swap the FAQ for the **Yoast FAQ block** or Elementor Accordion with FAQ schema enabled, so FAQPage structured data is generated for you.

Regenerate the templates after editing a prototype:

```bash
python3 tools/build_elementor.py v2 v3
```

## Yoast SEO settings

The prototypes follow Yoast's checks: one H1 per page, focus keyphrase in the title, H1 area, first paragraph and meta description, descriptive H2/H3 hierarchy, and labeled images/illustrations. The `<title>`, meta description, canonical and Open Graph tags in the HTML are for preview only; in WordPress, Yoast outputs them from the values below.

**Site-wide (Yoast → Settings):** Site representation = Organization, name "Finchby", upload logo. Title separator `|`. Yoast then generates Organization, WebSite and WebPage schema automatically.

| Page | Slug | Focus keyphrase | SEO title | Meta description |
|---|---|---|---|---|
| Home | `/` | AI SEO agency | AI SEO Agency \| SEO for the AI Search Era \| Finchby | Finchby is an AI SEO agency. We get your brand found in Google, AI Overviews, ChatGPT, Perplexity and Gemini with technical SEO, content and GEO. |
| AI Search Visibility Audit | `/ai-search-visibility-audit/` | AI search visibility audit | AI Search Visibility Audit \| Finchby | See how ChatGPT, Gemini, Perplexity and AI Overviews describe your brand, who they cite instead, and what to fix first. |
| Generative Engine Optimization | `/generative-engine-optimization/` | generative engine optimization services | Generative Engine Optimization (GEO) Services \| Finchby | GEO services that get your brand mentioned and cited by AI assistants. Prompt research, answer-ready content and citation building. |
| Technical SEO | `/technical-seo/` | technical SEO services | Technical SEO Services \| Finchby | Technical SEO audits, Core Web Vitals, crawl and index fixes, AI crawler access and safe site migrations. |
| Content Strategy | `/seo-content-strategy/` | SEO content strategy | SEO Content Strategy & Creation \| Finchby | Topical authority maps and expert-led content that earn rankings in search and citations in AI answers. |
| Digital PR & Link Building | `/digital-pr-link-building/` | digital PR and link building | Digital PR & Link Building \| Finchby | Earned coverage, quality backlinks and brand mentions in the sources search engines and AI models trust. |
| Local SEO | `/local-seo/` | local SEO services | Local SEO Services \| Finchby | Google Business Profile, reviews, citations and location pages that win local searches and AI recommendations. |
| E-commerce SEO | `/ecommerce-seo/` | e-commerce SEO services | E-commerce SEO Services \| Finchby | Product and category SEO, product schema and merchant feeds built for search and AI shopping. |
| Schema & Entity Optimization | `/schema-entity-optimization/` | schema markup services | Schema & Entity Optimization \| Finchby | Structured data and knowledge graph work that help search engines and AI understand your brand. |
| Pricing | `/pricing/` | SEO pricing | SEO & GEO Pricing \| Finchby | Transparent SEO and GEO plans, from a one-time audit to a full monthly program. |
| Contact | `/contact/` | free AI visibility audit | Get a Free AI Visibility Audit \| Finchby | Send us your website and get a free snapshot of how search engines and AI assistants see your brand. |

Suggested structure: each service on the home page links to its own service page (parent `/services/`), plus a `/blog/` for topical content. Enable Yoast breadcrumbs for service pages.
