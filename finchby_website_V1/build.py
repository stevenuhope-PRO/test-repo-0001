#!/usr/bin/env python3
"""Builds the Finchby static prototype.  Run:  python3 build.py

To reveal a service on the site, change its status below from SOON to NOW
and re-run.  The same wording feeds the Services page and the structured data.
"""
import json, pathlib, html

ROOT = pathlib.Path(__file__).parent
SITE = "https://finchby.ai"
EMAIL = "hello@finchby.ai"          # placeholder: set up this mailbox or change it
TAGLINE = "Be the business AI recommends."
UPDATED = "November 17, 2026"
NOW, SOON = "now", "soon"

# ---------------------------------------------------------------- services
SERVICES = [
  ("1", "Measure", "Find out what AI says about you today, and why, before changing anything.", [
    (NOW, "AI Visibility Baseline",
     "We ask ChatGPT, Google, Gemini, Perplexity and Copilot the questions your customers ask, several times each. You see how often you're named, where you rank, which facts are wrong and which competitors show up instead."),
    (NOW, "Source Tracing",
     "AI rarely quotes your own website. We find the list sites, directories and review platforms it actually pulls from for your trade and city, and show where you stand on each one."),
    (NOW, "Site Readiness Audit",
     "A technical check of whether search engines and AI crawlers can reach and understand your website. You get a clear verdict (Ready, Needs Work or Blocked) and the reason."),
    (NOW, "Action Plan",
     "A prioritized plan in plain English. Every task has an owner, a time estimate and a cost, with milestones at 30, 60 and 90 days."),
  ]),
  ("2", "Fix the facts", "Make every source say the same true things about your business.", [
    (NOW, "Master Record",
     "One agreed source of truth for your name, address, phone, hours, founding year and credentials. Every listing gets checked against it, field by field."),
    (NOW, "Core Profiles",
     "We claim and complete the profiles AI reads first: Google Business Profile, Bing Places, Apple Business, Yelp, Facebook and the top directory in your industry."),
    (NOW, "Directory and List-Site Fixes",
     "We get you onto the &ldquo;best of&rdquo; lists AI quotes, correct the entries that are wrong, and tell you which paid placements aren't worth it."),
    (NOW, "Duplicate and Legacy Cleanup",
     "Old domains, former owners, extra phone numbers and conflicting founding dates confuse AI. We reconcile them, or work around the ones you can't change."),
  ]),
  ("3", "Upgrade your website", "A site that answers buyers' questions and explains itself to machines.", [
    (NOW, "Website Cleanup and Care",
     "We remove leftover pages, broken links, oversized images and security gaps. We work in WordPress, Elementor and Yoast SEO, alongside your developer if you have one."),
    (NOW, "Technical Setup and Schema",
     "Page titles, descriptions, headings and structured data that tell machines what you do and where, plus the right AI-crawler settings at your host and firewall."),
    (NOW, "Answer Pages",
     "The pages buyers and AI look for and rarely find: pricing and terms, credentials, services, service areas and FAQs, each answering the question in the first two sentences."),
    (SOON, "New Website Builds",
     "Complete new websites, built AI-ready from the first page."),
  ]),
  ("4", "Build your reputation", "AI repeats what customers and third parties say. Give it something accurate to repeat.", [
    (NOW, "Review Program",
     "A simple routine for asking every customer for a review and replying to each one. We never buy, filter or gate reviews."),
    (NOW, "AI Answer Corrections",
     "When AI repeats an outdated or unfair claim about you, we trace it to the source, publish the real facts and respond where the claim was made."),
    (SOON, "Local PR and Mentions",
     "Earned mentions in local media, trade associations and partner websites."),
  ]),
  ("5", "Advertise", "Paid placement, once your foundations are solid.", [
    (SOON, "Google Ads and Local Services Ads",
     "Search campaigns set up to be eligible for Google's AI answers, plus pay-per-lead local listings."),
    (SOON, "ChatGPT Ads Pilot",
     "A 60-day test with a fixed budget and a clear go or no-go decision from the numbers."),
    (SOON, "Maps Ads",
     "Small, targeted placements on Apple Maps and similar platforms where the data supports it."),
  ]),
  ("6", "Track and advise", "Proof every month, and advice you can act on.", [
    (NOW, "Monthly Answer Check",
     "We re-run the same questions on every engine, multiple times, and compare with your baseline. AI answers vary from one run to the next, so a single check proves nothing."),
    (NOW, "Reporting",
     "AI citations from Bing, question searches from Google, AI-assistant traffic in Google Analytics, and what customers say when you ask how they found you."),
    (NOW, "Ongoing Advisory",
     "A monthly retainer for owners who want the work watched, adjusted and explained as AI platforms change."),
    (SOON, "Team AI Training",
     "Practical sessions on using AI tools well inside a small business."),
    (SOON, "AI Agent Readiness",
     "Getting your business ready to be quoted, booked and bought from by AI assistants acting for a customer."),
  ]),
]

PAGES = {
  "index.html":    ("Home",         "AI Visibility for Local Businesses | Finchby",
                    "Finchby helps local businesses get found, described accurately and recommended by ChatGPT, Google AI, Gemini, Perplexity and Copilot."),
  "services.html": ("Services",     "AI Visibility Services for Local Businesses | Finchby",
                    "Finchby services: AI visibility baseline, source tracing, listings and profiles, website upgrades, reviews, and monthly tracking. See what's available now."),
  "approach.html": ("How it works", "How AI Visibility Works | Finchby",
                    "How Finchby gets local businesses into AI answers: measure, fix the facts, upgrade the website, track monthly. Plus what we tell clients not to buy."),
  "about.html":    ("About",        "About Finchby | AI Visibility Consultancy",
                    "Finchby is an independent AI visibility consultancy for local businesses, run by founder Steven Hope. Evidence first, no hype, no lock-in."),
  "contact.html":  ("Contact",      "Book a Free Intro Call | Finchby",
                    "Book a free 30-minute call with Finchby to talk about how your business shows up in ChatGPT, Google AI and other AI answers."),
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{schema(fn)}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Finchby, home">
      <img src="assets/img/finch.svg" alt="" width="30" height="40">
      <span>Finchby</span>
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
        if f in ("index.html", "contact.html"):
            continue
        cur = ' aria-current="page"' if f == fn else ""
        out.append(f'<a href="{f}"{cur}>{label}</a>')
    out.append('<a class="btn" href="contact.html">Book a call</a>')
    return "\n      ".join(out)

def schema(fn):
    if fn != "index.html":
        return ""
    offers = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": html.unescape(n), "description": html.unescape(d)}}
              for _, _, _, items in SERVICES for st, n, d in items if st == NOW]
    data = {
      "@context": "https://schema.org", "@type": "ProfessionalService",
      "@id": SITE + "/#organization", "name": "Finchby", "url": SITE + "/",
      "logo": SITE + "/assets/img/finch.svg", "email": EMAIL,
      "description": "AI visibility consultancy for local businesses.",
      "slogan": TAGLINE,
      "founder": {"@type": "Person", "name": "Steven Hope"},
      "areaServed": {"@type": "Country", "name": "United States"},
      "knowsAbout": ["AI visibility", "Generative engine optimization", "Answer engine optimization", "Local SEO", "WordPress", "Structured data"],
      "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": offers},
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=1) + "\n</script>"

CTA = """
<section>
  <div class="wrap">
    <div class="cta">
      <h2>Find out what AI says about your business</h2>
      <p>Book a free 30-minute call. We'll talk through your business and your customers, and tell you honestly whether we can help.</p>
      <div class="actions" style="justify-content:center"><a class="btn" href="contact.html">Book a free intro call</a></div>
    </div>
  </div>
</section>
"""

FOOT = f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div class="foot-brand">
        <img src="assets/img/crest.svg" alt="The Finchby crest" width="74" height="101">
        <p><strong>Finchby</strong><br>{TAGLINE}<br><span class="small">AI visibility and website consulting for local businesses.</span></p>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="services.html">Services</a></li>
          <li><a href="approach.html">How it works</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="contact.html">Book a free intro call</a></li>
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
            badge = ('<span class="status">Available now</span>' if st == NOW
                     else '<span class="status soon">Coming soon</span>')
            cls = "svc" if st == NOW else "svc is-soon"
            rows.append(f'<div class="{cls}">{badge}<h3>{n}</h3><p>{d}</p></div>')
        out.append(f"""<div class="svc-group">
  <header><span class="num">{num}</span><h2>{name}</h2><p>{blurb}</p></header>
  <div class="svc-list">
    {chr(10).join(rows)}
  </div>
</div>""")
    return "\n".join(out)

BODY = {}

BODY["index.html"] = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">AI visibility for local businesses</p>
      <h1>{TAGLINE}</h1>
      <p class="lede">Your customers now ask ChatGPT and Google's AI who to call. Finchby makes sure your business is in the answer, with the right facts and a link that brings them to you.</p>
      <div class="actions">
        <a class="btn" href="contact.html">Book a free intro call</a>
        <a class="btn ghost" href="approach.html">See how it works</a>
      </div>
    </div>
    <div class="answer" role="img" aria-label="Illustration of an AI assistant recommending three local businesses, with yours listed first">
      <p class="q">Who's the best kitchen remodeler near me?</p>
      <div class="a-label"><span class="dot"></span>AI assistant</div>
      <ol>
        <li class="you"><strong>Your Company</strong><span>Highly rated locally, clear pricing, 5 to 7 day turnaround.</span></li>
        <li><strong>Competitor A</strong><span>Well reviewed, larger showroom.</span></li>
        <li><strong>Competitor B</strong><span>Good for budget projects.</span></li>
      </ol>
      <p class="src">Sources: Google Business Profile, Yelp, a local &ldquo;best of&rdquo; list, your website</p>
    </div>
  </div>
</section>

<div class="engines">
  <div class="wrap">
    <span>We measure and improve how you appear in</span>
    <span class="chip">ChatGPT</span><span class="chip">Google AI</span><span class="chip">Gemini</span><span class="chip">Perplexity</span><span class="chip">Copilot</span><span class="chip">Siri</span>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">The shift</p>
      <h2>Search changed. Most local businesses haven't noticed yet.</h2>
    </div>
    <div class="grid-3">
      <div class="card"><h3>Buyers ask AI first</h3><p>Instead of ten blue links, people get three or four names from an assistant. If you're not one of them, you're not considered.</p></div>
      <div class="card"><h3>AI reads other people's pages</h3><p>Answers are built from directories, &ldquo;best of&rdquo; lists, maps and reviews more than from your own website. Whatever those sources say, right or wrong, gets repeated.</p></div>
      <div class="card"><h3>The fix is practical</h3><p>Consistent facts everywhere, complete profiles, a website that states prices and terms clearly, and a steady flow of real reviews. No tricks required.</p></div>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">How it works</p>
      <h2>Four steps, in the order that works</h2>
    </div>
    <div class="grid-4">
      <div class="card"><span class="num">1</span><h3>Measure</h3><p>We test what each AI engine says about you today and trace where it gets its information.</p></div>
      <div class="card"><span class="num">2</span><h3>Fix the facts</h3><p>One master record of your business, then every profile and directory brought in line with it.</p></div>
      <div class="card"><span class="num">3</span><h3>Upgrade your site</h3><p>Clean up, add the technical labels machines read, and publish the pages buyers ask about.</p></div>
      <div class="card"><span class="num">4</span><h3>Track monthly</h3><p>We re-run the same tests every month so you can see what moved.</p></div>
    </div>
    <div class="actions"><a class="btn ghost" href="approach.html">More on our approach</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Services</p>
      <h2>Everything you need to show up in AI answers</h2>
      <p class="sub">Start with a baseline, or hand us the whole program.</p>
    </div>
    <div class="grid-3">
      <a class="card" href="services.html"><h3>AI Visibility Baseline</h3><p>How often you're named, where you rank, and what AI gets wrong about you.</p></a>
      <a class="card" href="services.html"><h3>Source Tracing</h3><p>The exact lists, directories and review sites AI quotes for your trade and city.</p></a>
      <a class="card" href="services.html"><h3>Profiles and Listings</h3><p>Google, Bing, Apple, Yelp and industry directories: claimed, completed and consistent.</p></a>
      <a class="card" href="services.html"><h3>Website Upgrades</h3><p>Cleanup, schema, and the pricing, service and FAQ pages that AI can cite.</p></a>
      <a class="card" href="services.html"><h3>Reviews and Reputation</h3><p>An honest review routine, and corrections when AI repeats something untrue.</p></a>
      <a class="card" href="services.html"><h3>Monthly Tracking</h3><p>The same questions, re-tested every month, with a plain report of what changed.</p></a>
    </div>
    <div class="actions"><a class="btn ghost" href="services.html">See all services</a></div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="case">
      <div>
        <p class="eyebrow">Client story</p>
        <h2>A respected fabricator that AI couldn't see</h2>
        <p>A long-established stone fabricator in Central Texas had strong reviews and industry credentials, yet almost never came up when people asked AI for the best in the city.</p>
        <p>The problem wasn't the quality of the business. Two websites and two phone numbers were in circulation, three different founding years were quoted online, and the list sites AI relied on had the details wrong. No page stated prices, terms or credentials.</p>
        <p>We're fixing it in order: one master record, the core profiles, the cited list sites, then the website, with a monthly re-test against the baseline.</p>
        <p class="small">Shared with the client's name withheld. Engagement in progress.</p>
      </div>
      <div>
        <div class="stat"><b>1 of 13</b><span>AI answers to general &ldquo;who's best?&rdquo; questions named the business at baseline.</span></div>
        <div class="stat"><b>4</b><span>third-party list sites supplied most of what the AI engines said.</span></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid-2">
      <div>
        <p class="eyebrow">Why Finchby</p>
        <h2>Consulting you can check</h2>
        <p class="sub">The name is a nod to old-school professional firms: do careful work, explain it clearly, and let results earn the next client. That's how we operate.</p>
      </div>
      <ul class="checks">
        <li><strong>Evidence first.</strong> Every engagement starts with a recorded baseline and is judged against it.</li>
        <li><strong>No ranking guarantees.</strong> Nobody controls what AI says. We improve your odds and show you the numbers.</li>
        <li><strong>We tell you what not to buy.</strong> Every plan lists the tools, badges and placements to skip.</li>
        <li><strong>You own everything.</strong> Profiles, logins and pages stay in your company's name.</li>
        <li><strong>Plain English.</strong> Plans are written for owners, not engineers.</li>
      </ul>
    </div>
  </div>
</section>
""" + CTA

BODY["services.html"] = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1>What we do</h1>
    <p class="lede">Finchby helps local businesses show up accurately in AI answers through measurement, listings and profile work, website upgrades, reputation building and monthly tracking. The steps run in order because each one builds on the last.</p>
    <p class="legend"><span><span class="status" style="margin:0">Available now</span></span><span><span class="status soon" style="margin:0">Coming soon</span> &nbsp;launching once proven with clients</span></p>
  </div>
</section>
<section style="padding-top:8px">
  <div class="wrap">
    %%SERVICES%%
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Ways to work with us</p>
      <h2>Three ways to start</h2>
    </div>
    <div class="grid-3">
      <div class="card"><span class="num">A</span><h3>Baseline Assessment</h3><p>A one-time project: AI Visibility Baseline, Source Tracing, Site Readiness Audit and a written Action Plan. Yours to run with or without us.</p></div>
      <div class="card"><span class="num">B</span><h3>90-Day Program</h3><p>We carry out the plan with you and your web developer, with milestones at 30, 60 and 90 days and a fresh AI re-test at each.</p></div>
      <div class="card"><span class="num">C</span><h3>Ongoing Advisory</h3><p>A monthly retainer: the answer check, reporting, drafted review replies and pages, and advice as AI platforms change.</p></div>
    </div>
    <p class="small" style="margin-top:1.6rem">Pricing depends on the size of your business and the state of your listings and website. You get a written quote after a free intro call.</p>
  </div>
</section>
""" + CTA

BODY["approach.html"] = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">How it works</p>
    <h1>A clear process, in the right order</h1>
    <p class="lede">We measure what AI says about your business, fix the sources it reads, upgrade your website, and re-test every month. Order matters: advertising a business whose facts don't match just sends buyers to a contradiction.</p>
  </div>
</section>
<section style="padding-top:24px">
  <div class="wrap">
    <div class="grid-3">
      <div class="card"><span class="num">1</span><h3>Measure</h3><p>We put real customer questions to each AI engine, several times, and record the answers: whether you're named, what's said, which sources are cited and which competitors appear. That's your baseline.</p></div>
      <div class="card"><span class="num">2</span><h3>Agree the facts</h3><p>One short meeting settles the basics: your exact name, address, phone, hours, founding year, credentials and terms. That becomes your master record.</p></div>
      <div class="card"><span class="num">3</span><h3>Fix the sources</h3><p>We claim and complete your core profiles, then correct or join the directories and list sites AI cites. Everything is checked against the master record.</p></div>
      <div class="card"><span class="num">4</span><h3>Upgrade the website</h3><p>We clear the clutter, add the labels machines read, and write the missing pages. Each one answers its question in the first two sentences, with real prices, lead times and dates.</p></div>
      <div class="card"><span class="num">5</span><h3>Build reputation</h3><p>A routine for asking every customer for a review and replying to each. If AI repeats an unfair claim, we publish the real facts and respond at the source.</p></div>
      <div class="card"><span class="num">6</span><h3>Track monthly</h3><p>We re-run the same questions and compare with the baseline, alongside data from Google, Bing and your own enquiry form. The plan adjusts based on the numbers.</p></div>
    </div>
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="grid-2">
      <div>
        <p class="eyebrow">What makes us different</p>
        <h2>We tell you what not to buy</h2>
        <p class="sub">Every Finchby plan includes a list of things not to spend time or money on. Good advice includes what to leave alone.</p>
        <p>The list changes as AI platforms change, and we update it based on evidence. Right now it usually includes the items here.</p>
      </div>
      <ul class="checks no">
        <li><strong>Paid &ldquo;best of&rdquo; badges</strong> on sites that just copy their data from Google and Yelp.</li>
        <li><strong>Buying, filtering or rewarding reviews.</strong> It risks your profile being suspended.</li>
        <li><strong>Trendy technical files</strong> that no major AI engine currently reads.</li>
        <li><strong>Daily tracking subscriptions</strong> before a monthly check shows a gap worth watching.</li>
        <li><strong>Ads before your foundations are consistent.</strong></li>
        <li><strong>Content hidden in tabs, scripts or PDFs,</strong> where AI crawlers can't read it.</li>
      </ul>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">FAQ</p>
      <h2>Common questions</h2>
    </div>
    <div class="faq">
      <div><h3>Can you guarantee ChatGPT will recommend my business?</h3>
      <p>No, and nobody honestly can. The same question gives different businesses from one run to the next. What we can do is raise how often you appear and make sure the facts are right. We measure both.</p></div>
      <div><h3>How is this different from SEO?</h3>
      <p>It includes SEO, but the weight is elsewhere. AI engines lean heavily on third-party sources like maps data, reviews, directories and list sites, so much of the work happens off your website.</p></div>
      <div><h3>How long until I see results?</h3>
      <p>Corrected listings and profiles can be picked up by AI within weeks. New website pages and a body of reviews take longer. We plan in 90-day blocks and check monthly.</p></div>
      <div><h3>Do I need a new website?</h3>
      <p>Rarely. Most sites need a cleanup, proper labelling and a handful of new pages. We work in WordPress with Elementor and Yoast SEO, alongside your developer if you have one.</p></div>
      <div><h3>Who does the work?</h3>
      <p>Finchby's founder, using AI research tools that he directs and checks. Some tasks, like gathering facts, photos and reviews, need the owner. The plan says exactly which.</p></div>
      <div><h3>What kinds of businesses do you work with?</h3>
      <p>Established local businesses whose customers ask &ldquo;who should I call?&rdquo;: trades, contractors, fabricators, showrooms and professional practices.</p></div>
    </div>
  </div>
</section>
""" + CTA

BODY["about.html"] = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>Modern work, old-fashioned standards</h1>
    <p class="lede">Finchby is an independent AI visibility consultancy for local businesses. It's run personally by its founder and works with a small number of clients at a time.</p>
  </div>
</section>
<section style="padding-top:24px">
  <div class="wrap">
    <div class="grid-2">
      <div>
        <h2>Why Finchby exists</h2>
        <p>Founder Steven Hope started Finchby after helping a business owner work out why his long-established company was missing from AI answers. The fix turned out to be mostly careful, unglamorous work that few people were offering to do properly.</p>
        <p>AI platforms change every month. Steven tests each new model and tool as it's released, and brings into client work only what proves itself in real results.</p>
        <p>The name is deliberate. It's meant to sound like a firm that's been around for a century, because that's the standard we hold ourselves to: do the work carefully, explain it clearly, and earn the next client through results.</p>
      </div>
      <div>
        <h2>What we stand for</h2>
        <ul class="checks">
          <li><strong>Evidence first.</strong> A baseline before any advice.</li>
          <li><strong>Honesty.</strong> Including what not to buy and what can't be promised.</li>
          <li><strong>Order.</strong> Foundations before advertising.</li>
          <li><strong>Ownership.</strong> You keep every account, record and page.</li>
          <li><strong>Discretion.</strong> We don't name clients without permission.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="soft">
  <div class="wrap">
    <div class="grid-2" style="align-items:center">
      <div class="center"><img src="assets/img/crest.svg" alt="The Finchby crest: a shield in three parts showing an owl, a wing and an anchor, framed by laurel branches, with a finch in flight above, and the name Finchby on the scroll" width="300" height="409" style="width:300px"></div>
      <div>
        <p class="eyebrow">The crest</p>
        <h2>Where the finch comes from</h2>
        <p>The finch is small, quick and precise, which is how we like to work. It's our logo, and it sits at the top of the crest.</p>
        <p>The shield is divided into three parts, one for each value we work by. The owl stands for <strong>wisdom</strong>, the wing for <strong>agility</strong> as AI changes, and the anchor for <strong>integrity</strong>: advice you can trust to hold steady.</p>
        <p>The rest borrows from the founder's Scottish family heritage. The chevron comes from the arms of Hope, and the three buckles come from Leslie. The laurel branches are the long-standing mark of work judged on merit.</p>
        <p class="small">The crest is a company emblem inspired by those family arms, not an official grant of arms.</p>
      </div>
    </div>
  </div>
</section>
""" + CTA

BODY["contact.html"] = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Book a free intro call</h1>
    <p class="lede">Tell us a little about your business and we'll set up a 30-minute call. You can also email <a href="mailto:{EMAIL}">{EMAIL}</a>. We reply within two business days.</p>
  </div>
</section>
<section style="padding-top:24px">
  <div class="wrap">
    <div class="grid-2">
      <form class="form-card" action="mailto:{EMAIL}" method="post" enctype="text/plain">
        <div><label for="name">Your name</label><input id="name" name="Name" autocomplete="name" required></div>
        <div><label for="biz">Business name and website</label><input id="biz" name="Business" autocomplete="organization"></div>
        <div><label for="email">Email</label><input id="email" name="Email" type="email" autocomplete="email" required></div>
        <div><label for="tel">Phone (optional)</label><input id="tel" name="Phone" type="tel" autocomplete="tel"></div>
        <div><label for="msg">What would you like help with?</label><textarea id="msg" name="Message" rows="4"></textarea></div>
        <div><label for="src">How did you hear about us?</label>
          <select id="src" name="Source">
            <option value="">Please choose</option>
            <option>Referral</option>
            <option>ChatGPT</option>
            <option>Google search or Google AI</option>
            <option>Perplexity, Copilot, Claude or Gemini</option>
            <option>Siri or another voice assistant</option>
            <option>Other</option>
          </select></div>
        <button class="btn" type="submit">Send message</button>
      </form>
      <div>
        <h2>What happens next</h2>
        <ul class="checks">
          <li><strong>A 30-minute call.</strong> Free, about your business and your customers.</li>
          <li><strong>An honest read.</strong> Whether we can help, and what we'd look at first.</li>
          <li><strong>A written quote.</strong> Scope, price and timeline before any work starts.</li>
        </ul>
        <p class="small" style="margin-top:1.6rem">We take on a limited number of clients so each one gets the founder's direct attention.</p>
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
