#!/usr/bin/env python3
"""Draws the Finchby logo (assets/img/finch.svg) and crest (assets/img/crest.svg).
Run:  python3 make_art.py      Colors and proportions are set at the top."""
import math, pathlib

INK, TINT = "#14261f", "#dfe8e2"
OUT = pathlib.Path(__file__).parent / "assets" / "img"

# ------------------------------------------------------------------ finch
def fan(root, feathers, n, overlap=1.25, solid=.9):
    """A wing or tail: round-tipped feathers fanned from a root point, giving a
    scalloped edge. feathers = [(angle clockwise from pointing right, length), ...]
    measured from the reference pose; they are interpolated to n feathers."""
    fs = []
    for i in range(n):
        f = i / (n - 1) * (len(feathers) - 1)
        k = min(int(f), len(feathers) - 2); u = f - k
        fs.append((feathers[k][0] * (1-u) + feathers[k+1][0] * u, feathers[k][1] * (1-u) + feathers[k+1][1] * u))
    out, pts = [], ["0 0"]
    for i, (ang, L) in enumerate(fs):
        step = max(abs(fs[min(i+1, n-1)][0] - ang), abs(ang - fs[max(i-1, 0)][0]))   # local spacing
        w = L * math.sin(math.radians(step / 2)) * overlap
        out.append(f'<path d="M0 {-w*.3:.1f} L{L-w:.1f} {-w:.1f} A{w:.1f} {w:.1f} 0 0 1 {L-w:.1f} {w:.1f} L0 {w*.3:.1f} Z" transform="rotate({ang:.1f})"/>')
        r = L * solid
        pts.append(f"{r*math.cos(math.radians(ang)):.1f} {r*math.sin(math.radians(ang)):.1f}")
    out.append(f'<path d="M{" L".join(pts)} Z"/>')
    return f'<g transform="translate({root[0]} {root[1]})">' + "".join(out) + "</g>"

def finch(eye="#fff"):
    """House finch in flight, heading left and looking slightly down: upper wing
    raised in a broad fan, lower wing swept down and forward, tail fanned behind."""
    upper = fan((300, 412), [(-103, 275), (-92, 305), (-82, 315), (-66, 302), (-50, 284), (-30, 272), (-11, 262), (12, 240)], 15)
    lower = fan((290, 548), [(114, 414), (109, 430), (103, 426), (98, 396), (93, 358), (85, 333), (75, 312), (65, 288), (54, 267), (42, 249), (28, 238), (13, 231)], 17)
    tail  = fan((540, 512), [(-31, 158), (-8, 180), (10, 191), (26, 203), (39, 228), (54, 236)], 8, 1.15)
    return f"""{upper}
    {lower}
    {tail}
    <ellipse cx="388" cy="492" rx="196" ry="80" transform="rotate(8 388 492)"/>
    <circle cx="196" cy="466" r="57"/>
    <path d="M150 432 L102 484 L158 506 Z"/>
    <circle cx="174" cy="450" r="9" fill="{eye}"/>"""

LOGO = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="70 70 690 920" role="img" aria-labelledby="t">
  <title id="t">Finchby — a finch in flight, wings spread</title>
  <g fill="{INK}">
  {finch()}
  </g>
</svg>
"""

# ------------------------------------------------------------------ crest
def laurel():
    cx, cy, r = 200, 300, 138
    pt = lambda th: (cx + r * math.cos(math.radians(th)), cy + r * math.sin(math.radians(th)))
    leaf = "M0 0 C7 -6 17 -6 25 0 C17 6 7 6 0 0 Z"
    angs = [104 + i * 9.6 for i in range(13)]
    (x0, y0), (x1, y1) = pt(98), pt(angs[-1] + 6)
    parts = [f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke-width="2"/>']
    for i, th in enumerate(angs):
        x, y = pt(th)
        for off in (-34, 34):
            parts.append(f'<path d="{leaf}" transform="translate({x:.1f} {y:.1f}) rotate({th+90+off:.1f}) scale({1-.025*i:.2f})"/>')
    parts.append(f'<path d="{leaf}" transform="translate({x1:.1f} {y1:.1f}) rotate({angs[-1]+96:.1f}) scale(.7)"/>')
    return "\n      ".join(parts)

SHIELD = "M110 210 H290 V300 C290 360 250 400 200 425 C150 400 110 360 110 300 Z"

def wreath(x0=158, x1=242, y0=194, y1=208, n=6):
    """The torse: a roll of two colours of silk twisted together, shown side-on
    as n curved twists alternating white and ink, with rounded ends."""
    w, r = (x1 - x0) / n, (y1 - y0) / 2
    edge = lambda x: f"{x+3:.1f} {y0} Q{x+7:.1f} {y0+r:.1f} {x-3:.1f} {y1}"   # one twist boundary, top to bottom
    roll = f"M{x0+r} {y0} H{x1-r} A{r} {r} 0 0 1 {x1-r} {y1} H{x0+r} A{r} {r} 0 0 1 {x0+r} {y0} Z"
    parts = [f'<clipPath id="wr"><path d="{roll}"/></clipPath>', f'<path d="{roll}" fill="#fff"/>', '<g clip-path="url(#wr)">']
    for i in range(n):
        a, b = x0 + i * w, x0 + (i + 1) * w
        fill = INK if i % 2 else "#fff"
        if i == 0: a -= 10          # end twists run past the rounded ends, which clip them
        if i == n - 1: b += 10
        parts.append(f'<path d="M{edge(a)} L{b-3:.1f} {y1} Q{b+7:.1f} {y0+r:.1f} {b+3:.1f} {y0} Z" fill="{fill}" stroke-width="1.2"/>')
    parts += ["</g>", f'<path d="{roll}" fill="none"/>']
    return "\n    ".join(parts)

CREST = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 84 320 430" role="img" aria-labelledby="ct">
  <title id="ct">Finchby crest: a shield in three parts showing an owl, a wing and an anchor, divided by a chevron with three buckles, framed by laurel, with a finch in flight above and the motto Grip Fast</title>
  <defs>
    <!-- engraver's hatching: horizontal lines = blue, dots = gold -->
    <pattern id="az" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0 2.5 H5" stroke="{INK}" stroke-width=".8"/></pattern>
    <pattern id="or" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#fff"/><circle cx="1.5" cy="1.5" r=".7" fill="{INK}"/><circle cx="4.5" cy="4.5" r=".7" fill="{INK}"/></pattern>
    <clipPath id="sh"><path d="{SHIELD}"/></clipPath>
    <g id="laurel" fill="{TINT}" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round">
      {laurel()}
    </g>
    <g id="buckle" fill="none" stroke="{INK}"><circle r="7" stroke-width="2.4" fill="#fff"/><path d="M-7 0 H5" stroke-width="2"/></g>
  </defs>

  <use href="#laurel"/>
  <use href="#laurel" transform="translate(400 0) scale(-1 1)"/>
  <path d="M188 436 L212 444 M212 436 L188 444" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>

  <!-- crest: the finch -->
  <g transform="translate(152 88) scale(.115)" fill="{INK}">
  {finch()}
  </g>
  <!-- wreath -->
  <g stroke="{INK}" stroke-width="1.6" stroke-linejoin="round">
    {wreath()}
  </g>

  <!-- shield: three fields -->
  <path d="{SHIELD}" fill="#fff"/>
  <g clip-path="url(#sh)">
    <rect x="100" y="200" width="200" height="240" fill="url(#az)"/>
    <path d="M200 208 V262" stroke="{INK}" stroke-width="5"/>
    <path d="M200 208 V262" stroke="#fff" stroke-width="2"/>
    <path d="M200 258 L300 338 V374 L200 294 L100 374 V338 Z" fill="url(#or)" stroke="{INK}" stroke-width="2"/>
  </g>
  <!-- 1. wisdom: an owl, perched on a branch -->
  <g transform="translate(153 242) scale(.95)" fill="#fff" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">
    <path d="M-26 25 C-12 20.5 8 19.5 26 14" fill="none" stroke-width="2.4"/>
    <path d="M0 -19 C4 -19 8 -20 11.5 -23.5 C13 -19.5 13.5 -14 12.6 -9 C14.8 -3 15 4 13.4 10 C11.8 15.6 7.4 20.4 0 21 C-7.4 20.4 -11.8 15.6 -13.4 10 C-15 4 -14.8 -3 -12.6 -9 C-13.5 -14 -13 -19.5 -11.5 -23.5 C-8 -20 -4 -19 0 -19 Z"/>
    <path d="M-10.5 -15.5 C-7 -17 -3 -16 0 -12.5 C3 -16 7 -17 10.5 -15.5" fill="none" stroke-width="1.1"/>
    <circle cx="-5" cy="-11.5" r="2" fill="{INK}" stroke="none"/><circle cx="5" cy="-11.5" r="2" fill="{INK}" stroke="none"/>
    <path d="M-1.3 -9.5 L0 -5.8 L1.3 -9.5 Z" fill="{INK}" stroke-width=".8"/>
    <path d="M-12.5 -2 C-10 5 -8.5 12 -5 19 M12.5 -2 C10 5 8.5 12 5 19" fill="none" stroke-width="1.2"/>
    <path d="M-4 20 V22.6 M-1.5 20.6 V22.3 M1.5 20.6 V22 M4 20 V21.6" fill="none" stroke-width="1.1"/>
  </g>
  <path d="{SHIELD}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>

  <!-- 2. agility: a wing -->
  <g transform="translate(247 246) scale(1.05)" fill="#fff" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round">
    <path d="M-21 9 C-15 -8 3 -17 23 -15 C17 -11 13 -9 10 -6 C15 -6 18 -6 20 -5 C14 -2 10 0 7 2 C11 3 13 3 15 4 C9 7 4 9 -1 10 C-8 13 -15 12 -21 9 Z"/>
    <path d="M-14 6 C-8 -4 2 -9 12 -10 M-9 8 C-3 2 4 -2 11 -3" fill="none" stroke-width="1.1"/>
  </g>
  <!-- 3. integrity: an anchor -->
  <g transform="translate(200 367)" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M0 -15 V21 M-9 -8 H9 M-17 5 C-15 16 -7 21 0 21 C7 21 15 16 17 5 M-22 10 L-17 2 L-11 8 M22 10 L17 2 L11 8" stroke="{INK}" stroke-width="7"/>
    <circle cy="-20" r="5" stroke="{INK}" stroke-width="7"/>
    <path d="M0 -15 V21 M-9 -8 H9 M-17 5 C-15 16 -7 21 0 21 C7 21 15 16 17 5 M-22 10 L-17 2 L-11 8 M22 10 L17 2 L11 8" stroke="#fff" stroke-width="3.4"/>
    <circle cy="-20" r="5" stroke="#fff" stroke-width="3.4"/>
  </g>

  <!-- three buckles on the chevron, after Leslie -->
  <use href="#buckle" x="200" y="278"/>
  <use href="#buckle" transform="translate(156 314) rotate(-39)"/>
  <use href="#buckle" transform="translate(244 314) rotate(39)"/>

  <!-- motto scroll -->
  <g stroke="{INK}" stroke-width="2" stroke-linejoin="round">
    <path d="M92 462 L64 450 L74 470 L62 486 L92 492 Z M308 462 L336 450 L326 470 L338 486 L308 492 Z" fill="{TINT}"/>
    <path d="M92 462 L104 474 L104 502 L92 492 Z M308 462 L296 474 L296 502 L308 492 Z" fill="{INK}"/>
    <path d="M104 452 C160 470 240 470 296 452 L296 484 C240 502 160 502 104 484 Z" fill="#fff"/>
  </g>
  <path id="mp" d="M112 478 C164 494 236 494 288 478" fill="none"/>
  <text font-family="Georgia, 'Times New Roman', serif" font-size="17" letter-spacing="5" fill="{INK}" text-anchor="middle">
    <textPath href="#mp" startOffset="50%">GRIP FAST</textPath>
  </text>
</svg>
"""

if __name__ == "__main__":
    (OUT / "finch.svg").write_text(LOGO)
    (OUT / "crest.svg").write_text(CREST)
    print("drew finch.svg and crest.svg")
