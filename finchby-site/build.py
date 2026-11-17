#!/usr/bin/env python3
"""Builds the Finchby static prototype.  Run:  python3 build.py

Edit the SERVICES list below to reveal a service on the site: change its
status from SOON to NOW and re-run.  The same wording is used on the
Services page and in the structured data.
"""
import json, pathlib, html

ROOT = pathlib.Path(__file__).parent
SITE = "https://finchby.ai"
EMAIL = "enquiries@finchby.ai"      # placeholder: set up this mailbox or change it
UPDATED = "November 17, 2026"
NOW, SOON = "now", "soon"

# ---------------------------------------------------------------- services
SERVICES = [
  ("I", "Assessment", "Establishing what the engines say today, and why, before anything is changed.", [
    (NOW, "AI Visibility Baseline",
     "We put the questions your customers actually ask to ChatGPT, Google, Gemini, Perplexity and Copilot, several times each, and record whether you are named, in what position, with which facts, and beside which competitors."),
    (NOW, "Cited-Source Tracing",
     "AI engines seldom quote a company's own website. We identify the list sites, directories and review sources they do quote for your trade and town, and where you stand on each."),
    (NOW, "Website Readiness Audit",
     "A technical examination of whether search engines and AI crawlers can reach and understand your site, returned with a plain verdict: Ready, Needs Work or Blocked, and the reason."),
    (NOW, "The Action Plan",
     "A written plan in order of effect, with every task assigned to a named person, an estimate of time and cost, and milestones at thirty, sixty and ninety days."),
  ]),
  ("II", "Identity &amp; Listings", "One set of facts about your business, repeated everywhere a machine might look.", [
    (NOW, "The Master Record",
     "A single agreed record of your name, address, telephone, hours, founding year and credentials. Every listing is checked against it, field by field."),
    (NOW, "Core Profiles",
     "Claiming and completing the profiles the engines read first: Google Business Profile, Bing Places, Apple Business, Yelp, Facebook and the leading directory in your trade."),
    (NOW, "List-Site and Directory Corrections",
     "Getting you on to the third-party lists the engines cite, correcting wrong entries, and advising plainly which paid placements are not worth the money."),
    (NOW, "Legacy and Duplicate Site Remediation",
     "Old domains, former owners, second telephone numbers and conflicting founding dates confuse the engines. We reconcile them, or work around those that cannot be changed."),
  ]),
  ("III", "The Website", "A site that answers the buyer's question in plain words, and labels itself properly for machines.", [
    (NOW, "Website Clean-Up and Care",
     "Removing leftover pages, broken links, oversized images and exposed logins. We work in WordPress, Elementor and Yoast SEO."),
    (NOW, "Machine-Readable Labelling",
     "Page titles, descriptions, headings and structured data that state what the business is, where it is and what each page covers, with crawler access correctly set at the host and firewall."),
    (NOW, "Answer Pages",
     "The pages buyers and engines look for and seldom find: prices and terms, credentials, a trade page, materials or services, service areas, and questions answered in the first two sentences."),
    (SOON, "New Website Builds",
     "Complete new sites for established firms, built to the same standard from the first page."),
  ]),
  ("IV", "Reputation", "The engines repeat what customers and third parties say. We see that there is something accurate to repeat.", [
    (NOW, "Review Program",
     "A simple, honest routine for asking every customer for a review and answering each one. Reviews are never bought, filtered or gated."),
    (NOW, "Correcting the Record",
     "Where an AI answer repeats an outdated or unfair claim, we trace it to its source, publish the true terms, and reply where the claim was made."),
    (SOON, "Local Press and Community Mentions",
     "Earned mentions in local publications, trade associations and partner websites."),
  ]),
  ("V", "Advertising", "Paid placement, begun only once the foundations agree with one another.", [
    (SOON, "Google Ads and Local Services Ads",
     "Search campaigns configured for eligibility in Google's AI answers, and pay-per-lead local service listings."),
    (SOON, "ChatGPT Advertising Pilot",
     "A measured sixty-day trial with a fixed budget and a decision at the end, taken from the figures."),
    (SOON, "Maps Advertising",
     "Modest placements on Apple Maps and similar surfaces, where the numbers support them."),
  ]),
  ("VI", "Measurement &amp; Counsel", "Evidence each month, and advice you can act upon.", [
    (NOW, "The Monthly Answer Check",
     "The same questions, put again to each engine and repeated, so that movement is measured and not guessed. One answer on one day proves nothing."),
    (NOW, "Standing Reports",
     "AI citations from Bing Webmaster Tools, question queries from Google Search Console, an AI-assistant channel in Google Analytics, and a tally of what customers say when asked how they found you."),
    (NOW, "Retained Counsel",
     "A standing arrangement for owners who wish to have the work watched, adjusted and explained as the engines change."),
    (SOON, "Owner and Staff Instruction",
     "Practical sessions on using AI tools well within a small firm."),
    (SOON, "Readiness for AI Agents",
     "Preparing a business to be quoted, booked and bought from by AI assistants acting for a customer."),
  ]),
]

PAGES = {
  "index.html":    ("Home",     "AI Visibility &amp; Website Consultancy | Finchby",
                    "Finchby is a consultancy that helps established local businesses be found, described correctly and recommended by ChatGPT, Google and other AI engines."),
  "services.html": ("Services", "Services: AI Visibility, Listings &amp; Websites | Finchby",
                    "The Finchby schedule of services: AI visibility assessment, identity and listings, website improvement, reputation, advertising, and monthly measurement."),
  "approach.html": ("Approach", "Our Approach to AI Visibility | Finchby",
                    "How Finchby works: establish the facts, set the foundations in order, improve the website, and measure every month. Includes what we advise against."),
  "about.html":    ("About",    "About the Firm | Finchby",
                    "Finchby is an independent consultancy in AI visibility and website improvement, conducted by its principal. The firm, its arms and its principles."),
  "contact.html":  ("Contact",  "Contact | Finchby",
                    "Write to Finchby to arrange an introductory conversation about your firm's visibility in AI answers and search."),
}

# ---------------------------------------------------------------- chrome
def head(fn):
    _, title, desc = PAGES[fn]
    url = SITE + "/" + ("" if fn == "index.html" else fn)
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Finchby">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<link rel="icon" href="assets/img/finch.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{schema(fn)}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Finchby, home">
      <img src="assets/img/finch.svg" alt="" width="58" height="32">
      <span><span class="brand-name">Finchby</span><span class="brand-sub">AI VISIBILITY COUNSEL</span></span>
    </a>
    <nav class="nav" aria-label="Primary">
      {nav(fn)}
    </nav>
  </div>
</header>
<main>
"""

def nav(fn):
    out = []
    for f, (label, _, _) in PAGES.items():
        if f == "index.html":
            continue
        cur = ' aria-current="page"' if f == fn else ""
        out.append(f'<a href="{f}"{cur}>{label}</a>')
    return "\n      ".join(out)

def schema(fn):
    if fn != "index.html":
        return ""
    offers = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": html.unescape(n), "description": d}}
              for _, _, _, items in SERVICES for st, n, d in items if st == NOW]
    data = {
      "@context": "https://schema.org", "@type": "ProfessionalService",
      "@id": SITE + "/#organization", "name": "Finchby", "url": SITE + "/",
      "logo": SITE + "/assets/img/finch.svg", "email": EMAIL,
      "description": "Consultancy in AI visibility and website improvement for established local businesses.",
      "slogan": "Fide et Opera",
      "areaServed": {"@type": "Country", "name": "United States"},
      "knowsAbout": ["AI visibility", "Generative engine optimization", "Local SEO", "WordPress", "Structured data"],
      "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Schedule of Services", "itemListElement": offers},
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=1) + "\n</script>"

FOOT = f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div class="foot-brand">
        <img src="assets/img/crest.svg" alt="The Finchby arms" width="64" height="80">
        <p><strong>Finchby</strong><br>Counsel in AI visibility and website improvement for established local businesses.<br><em>Fide et Opera</em> &mdash; by trust and by work.</p>
      </div>
      <div>
        <h2>The Firm</h2>
        <ul>
          <li><a href="services.html">Services</a></li>
          <li><a href="approach.html">Approach</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Correspondence</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>finchby.ai</li>
        </ul>
      </div>
    </div>
    <div class="colophon"><span>&copy; 2026 Finchby. All rights reserved.</span><span>Last updated {UPDATED}</span></div>
  </div>
</footer>
</body>
</html>
"""

# ---------------------------------------------------------------- bodies
def services_html():
    out = []
    for num, name, blurb, items in SERVICES:
        rows = []
        for st, n, d in items:
            badge = ('<span class="status">Offered at present</span>' if st == NOW
                     else '<span class="status soon">In preparation</span>')
            cls = "svc" if st == NOW else "svc is-soon"
            rows.append(f'<div class="{cls}"><h3>{n} {badge}</h3><p>{d}</p></div>')
        out.append(f"""<div class="svc-group">
  <header><span class="numeral">{num}</span><h2>{name}</h2><p>{blurb}</p></header>
  <div>
    {chr(10).join(rows)}
  </div>
</div>""")
    return "\n".join(out)

BODY = {}

BODY["index.html"] = """
<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">Counsel in AI Visibility &amp; Websites</p>
      <h1>When a customer asks the machine whom to call, your firm should be in the answer.</h1>
      <p class="lede">Finchby helps established local businesses be found, described correctly and recommended by ChatGPT, Google, Siri, Copilot and Perplexity. We work from evidence, put the foundations in order first, and report what changed each month.</p>
      <div class="actions">
        <a class="btn" href="contact.html">Arrange a conversation</a>
        <a class="btn ghost" href="services.html">Schedule of services</a>
      </div>
    </div>
    <div class="hero-crest"><img src="assets/img/crest.svg" alt="The Finchby arms: a chevron between two roundels and a finch in flight" width="220" height="275"></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p class="eyebrow">The matter in brief</p>
    <div class="grid-3">
      <div><h3>Buyers now ask an assistant</h3><p>People put the question to ChatGPT or Google's AI and receive three or four names. A firm that is not among them is not considered.</p></div>
      <div><h3>The engines read other people's pages</h3><p>Their answers are assembled from directories, list sites, maps and reviews, more than from your own website. Whatever those sources say, right or wrong, is repeated.</p></div>
      <div><h3>Most of the remedy is orderly work</h3><p>One consistent set of facts, complete profiles, a website that states its prices and terms plainly, and a steady flow of honest reviews.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">What we do</p>
    <h2>Six lines of work, taken in order</h2>
    <div class="grid-3">
      <div class="card"><span class="numeral">I</span><h3>Assessment</h3><p>What the engines say about you today, which sources they draw upon, and whether your website can be read by them.</p></div>
      <div class="card"><span class="numeral">II</span><h3>Identity &amp; Listings</h3><p>One master record of your business, and every profile and directory brought into agreement with it.</p></div>
      <div class="card"><span class="numeral">III</span><h3>The Website</h3><p>Clean-up, proper labelling for machines, and the pages buyers look for: prices, terms, credentials, answers.</p></div>
      <div class="card"><span class="numeral">IV</span><h3>Reputation</h3><p>An honest review routine, and the correction of outdated claims that AI answers repeat.</p></div>
      <div class="card"><span class="numeral">V</span><h3>Advertising</h3><p>Paid placement on Google and ChatGPT, begun only when the foundations are sound. In preparation.</p></div>
      <div class="card"><span class="numeral">VI</span><h3>Measurement &amp; Counsel</h3><p>A monthly check of what each engine says, standing reports, and advice as the field changes.</p></div>
    </div>
    <div class="actions"><a class="btn ghost" href="services.html">Read the full schedule</a></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="grid-2">
      <div>
        <p class="eyebrow">From a current engagement</p>
        <h2>A stone fabricator in Central Texas</h2>
        <p>An established family-run fabricator with strong reviews and long-standing trade credentials was nonetheless absent from nearly every AI answer to the question &ldquo;who are the best in the city?&rdquo;</p>
        <p>Our assessment found the cause was not the quality of the firm. Two websites and two telephone numbers were in circulation, three different founding years were quoted, and the list sites the engines relied upon carried wrong details. No page stated the firm's prices, terms or credentials.</p>
        <p>The engagement set these right in order: one master record, the core profiles, the cited list sites, the website, and a monthly check against the original baseline. The work continues.</p>
        <p class="updated">Described with the client's identity withheld.</p>
      </div>
      <div>
        <p class="eyebrow">How we conduct ourselves</p>
        <ul class="plain">
          <li><strong>Evidence before opinion.</strong> Every engagement begins with a recorded baseline, and is judged against it.</li>
          <li><strong>No promised rankings.</strong> Nobody controls what an AI engine says. We improve the odds and show the figures.</li>
          <li><strong>We say what not to buy.</strong> Each plan lists the tools, badges and placements we advise against.</li>
          <li><strong>Your accounts remain yours.</strong> Profiles are held in the company's name, never in ours.</li>
          <li><strong>Plain language.</strong> Plans are written to be read and acted upon by an owner, not an engineer.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <blockquote>The engines repeat whatever they read. Our work is to see that what they read about your firm is true, consistent and easy to find.</blockquote>
    <div class="actions"><a class="btn" href="contact.html">Arrange a conversation</a></div>
  </div>
</section>
"""

BODY["services.html"] = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Schedule of Services</p>
    <h1>Services</h1>
    <p class="lede">Finchby offers AI visibility assessment, listings and identity work, website improvement, reputation work and monthly measurement for established local businesses. Services are taken in the order below, since each depends upon the one before.</p>
    <p class="legend"><span><span class="status">Offered at present</span> &nbsp;available now</span><span><span class="status soon">In preparation</span> &nbsp;to be offered as the capability is proven</span></p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    %%SERVICES%%
  </div>
</section>
<section class="band">
  <div class="wrap">
    <p class="eyebrow">Forms of engagement</p>
    <h2>Three ways of working with the firm</h2>
    <div class="grid-3">
      <div class="card"><span class="numeral">I</span><h3>The Baseline Assessment</h3><p>A fixed piece of work: the AI Visibility Baseline, Cited-Source Tracing, the Website Readiness Audit and a written Action Plan. Yours to carry out with or without us.</p></div>
      <div class="card"><span class="numeral">II</span><h3>The Ninety-Day Program</h3><p>We carry out the plan beside you and your web developer, with milestones at thirty, sixty and ninety days and a fresh answer check at each.</p></div>
      <div class="card"><span class="numeral">III</span><h3>Retained Counsel</h3><p>A continuing monthly arrangement: the answer check, standing reports, drafted review replies and pages, and advice as the engines change.</p></div>
    </div>
    <p style="margin-top:1.6rem">Fees are quoted in writing after an introductory conversation, and depend upon the size of the business and the state of its listings and website.</p>
    <div class="actions"><a class="btn" href="contact.html">Arrange a conversation</a></div>
  </div>
</section>
"""

BODY["approach.html"] = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Method</p>
    <h1>Our approach</h1>
    <p class="lede">We establish what the AI engines say about a business today, correct the sources they read, improve the website, and measure the result every month. The order matters: advertising a business whose facts disagree only sends buyers to a contradiction.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="grid-2">
      <div class="card"><span class="numeral">First</span><h3>Establish the facts</h3><p>We put real buyers' questions to each engine, several times, and record the answers: whether the firm is named, what is said, which sources are cited and which competitors appear. That record is the baseline for everything after.</p></div>
      <div class="card"><span class="numeral">Second</span><h3>Agree one identity</h3><p>A short meeting with the owner settles the facts: the true name, address, telephone, hours, founding year, credentials and terms. These become the master record.</p></div>
      <div class="card"><span class="numeral">Third</span><h3>Correct the sources</h3><p>Core profiles are claimed and completed; the directories and list sites the engines cite are corrected or joined. Every entry is checked against the master record.</p></div>
      <div class="card"><span class="numeral">Fourth</span><h3>Improve the website</h3><p>Clutter is removed, pages are labelled for machines, and the missing pages are written, each answering its question in the first two sentences and stating real prices, lead times and dates.</p></div>
      <div class="card"><span class="numeral">Fifth</span><h3>Build the reputation</h3><p>A routine for asking each customer for a review, and for answering every one. Where an engine repeats an unfair claim, the true position is published and the claim answered at its source.</p></div>
      <div class="card"><span class="numeral">Sixth</span><h3>Measure, monthly</h3><p>The same questions are put again and compared with the baseline, alongside the reports from Google, Bing and the firm's own enquiry form. The plan is adjusted from the figures.</p></div>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="grid-2">
      <div>
        <p class="eyebrow">A point of difference</p>
        <h2>What we advise against</h2>
        <p>Every Finchby plan carries a list of things not to spend time or money on. A consultant's advice is worth more when it includes what to leave alone.</p>
        <p>The list changes as the engines change, and we revise it with evidence. At present it commonly includes the items opposite.</p>
      </div>
      <div>
        <ul class="plain">
          <li><strong>Paid &ldquo;best of&rdquo; badges and placements</strong> on sites that merely copy their data from Google and Yelp.</li>
          <li><strong>Buying, filtering or rewarding reviews.</strong> It risks suspension of the profile and is not honest.</li>
          <li><strong>Fashionable technical files</strong> that no major engine presently reads.</li>
          <li><strong>Daily tracking subscriptions</strong> before a monthly check has shown a gap worth watching.</li>
          <li><strong>Advertising before the foundations agree.</strong></li>
          <li><strong>Text hidden in tabs, scripts or PDFs,</strong> where AI crawlers cannot read it.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap narrow faq">
    <p class="eyebrow">Questions commonly asked</p>
    <h2>Plain answers</h2>
    <h3>Can you guarantee that ChatGPT will recommend my business?</h3>
    <p>No, and no one honestly can. The same question returns the same businesses only some of the time. What can be done is to raise the share of answers in which you appear and to see that the facts given are correct. We measure both.</p>
    <h3>How does this differ from ordinary search engine optimization?</h3>
    <p>It includes it, but the weight falls elsewhere. AI engines draw heavily on third-party sources: maps data, reviews, directories and list sites. Much of the work therefore lies off your own website.</p>
    <h3>How long before there is a result?</h3>
    <p>Corrected listings and profiles can be read by the engines within weeks. New website pages and a body of reviews take longer. We plan in ninety-day terms and check monthly.</p>
    <h3>Do you need to rebuild my website?</h3>
    <p>Seldom. Most sites need cleaning, labelling and a handful of new pages. We work in WordPress with Elementor and Yoast SEO, and alongside your existing developer where there is one.</p>
    <h3>Who does the work?</h3>
    <p>The principal, assisted by AI research tools that he directs and checks. Some tasks, such as collecting facts, photographs and reviews, necessarily fall to the owner; the plan says which.</p>
    <h3>What kinds of business do you take on?</h3>
    <p>Established local firms whose customers ask &ldquo;who should I call?&rdquo;: trades, fabricators, contractors, showrooms and professional practices.</p>
  </div>
</section>
"""

BODY["about.html"] = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">The Firm</p>
    <h1>About Finchby</h1>
    <p class="lede">Finchby is an independent consultancy in AI visibility and website improvement, serving established local businesses. It is conducted personally by its principal, and takes on a small number of clients at a time.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="grid-2">
      <div>
        <h2>A traditional practice in a new field</h2>
        <p>The field is new and changes monthly; the manner of practice need not be. Finchby is run as a professional firm of the older kind: the work is done carefully, explained plainly, and judged by its results.</p>
        <p>We do not make loud promises. We record where a client stands, do the work in order, and show the figures afterwards. Clients are gained by performance and kept by trust.</p>
        <h2 style="margin-top:1.4em">The principal</h2>
        <p>Steven Hope founded Finchby after advising a business owner on why his long-established firm was missing from AI answers, and finding that the remedy was mostly orderly, unglamorous work that few were offering to do properly.</p>
        <p>He studies each new AI model and platform as it is released, and brings into the practice only what has proved itself in a client's figures.</p>
      </div>
      <div>
        <h2>Principles</h2>
        <ul class="plain">
          <li><strong>Evidence first.</strong> A baseline before any advice.</li>
          <li><strong>Candour.</strong> Including what not to buy, and what cannot be promised.</li>
          <li><strong>Order.</strong> Foundations before advertising.</li>
          <li><strong>Stewardship.</strong> The client owns every account, record and page.</li>
          <li><strong>Discretion.</strong> Clients are not named without their leave.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="grid-2" style="align-items:center">
      <div style="text-align:center"><img src="assets/img/crest.svg" alt="The Finchby arms" width="240" height="300" style="width:240px"></div>
      <div>
        <p class="eyebrow">The house device</p>
        <h2>The arms and the finch</h2>
        <p>The finch is a small, quick and exact bird, and stands for the manner in which the firm works. It appears in flight as the firm's mark and in the base of the shield.</p>
        <p>The chevron and roundels are drawn from the arms of Hope, and the firm's regard for tenacity from the Leslie motto, <em>Grip Fast</em>; both are Scottish families of the principal's descent.</p>
        <p>The motto, <em>Fide et Opera</em>, means &ldquo;by trust and by work.&rdquo;</p>
        <p class="updated">The device is a house mark adopted by the firm, and not a grant of arms.</p>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap narrow" style="text-align:center">
    <h2>An introductory conversation costs nothing</h2>
    <p>Tell us about the business and the customers you wish to reach, and we shall say candidly whether we can help.</p>
    <div class="actions" style="justify-content:center"><a class="btn" href="contact.html">Arrange a conversation</a></div>
  </div>
</section>
"""

BODY["contact.html"] = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Correspondence</p>
    <h1>Contact</h1>
    <p class="lede">To arrange an introductory conversation, write to <a href="mailto:{EMAIL}">{EMAIL}</a> or use the form below. Enquiries are answered personally, ordinarily within two working days.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="grid-2">
      <form action="mailto:{EMAIL}" method="post" enctype="text/plain">
        <div><label for="name">Your name</label><input id="name" name="Name" autocomplete="name" required></div>
        <div><label for="biz">Business and website</label><input id="biz" name="Business" autocomplete="organization"></div>
        <div><label for="email">Email</label><input id="email" name="Email" type="email" autocomplete="email" required></div>
        <div><label for="tel">Telephone (optional)</label><input id="tel" name="Telephone" type="tel" autocomplete="tel"></div>
        <div><label for="msg">How may we help?</label><textarea id="msg" name="Message" rows="5"></textarea></div>
        <div><label for="src">How did you hear of us?</label>
          <select id="src" name="Source">
            <option value="">Please choose</option>
            <option>A recommendation</option>
            <option>ChatGPT</option>
            <option>Google search or Google AI</option>
            <option>Perplexity, Copilot, Claude or Gemini</option>
            <option>Siri or another voice assistant</option>
            <option>Other</option>
          </select></div>
        <button class="btn" type="submit">Send enquiry</button>
      </form>
      <div>
        <h2>What follows</h2>
        <ul class="plain">
          <li><strong>A conversation.</strong> Half an hour, without charge, about the business and its customers.</li>
          <li><strong>A candid view.</strong> Whether we can help, and what we would look at first.</li>
          <li><strong>A written proposal.</strong> Scope, fee and timetable, before any work begins.</li>
        </ul>
        <p style="margin-top:1.4rem">Finchby takes on a limited number of clients so that each receives the principal's own attention.</p>
      </div>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- build
def main():
    for fn in PAGES:
        body = BODY[fn].replace("%%SERVICES%%", services_html())
        (ROOT / fn).write_text(head(fn) + body + FOOT, encoding="utf-8")
    urls = "\n".join(f"  <url><loc>{SITE}/{'' if f == 'index.html' else f}</loc></url>" for f in PAGES)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    (ROOT / "robots.txt").write_text(f"# All crawlers welcome, AI engines included.\nUser-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", ", ".join(PAGES))

if __name__ == "__main__":
    main()
