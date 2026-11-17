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

# "Finchby" set in Grenze Gotisch (SIL Open Font License), converted to outlines so the
# crest needs no font when used as an image. Width 113.6 units at size 40, baseline at y=0.
NAME_W = 113.64
NAME = "M10.80 -24.12L18.92 -24.12L18.40 -17.12L16.24 -17.12L15.80 -21.52L10.68 -22.00L10.80 -24.12Z M7.40 -2.36L10.84 -1.76L10.08 -0.28Q9.68 -0.24 8.86 -0.12Q8.04 -0.00 7.20 0.10Q6.36 0.20 5.74 0.28Q5.12 0.36 5.04 0.36Q4.92 0.36 4.60 0.08Q4.28 -0.20 3.98 -0.52Q3.68 -0.84 3.68 -0.96L3.68 -21.72L1.20 -22.32L1.20 -23.88Q1.68 -23.96 2.44 -24.06Q3.20 -24.16 4.00 -24.26Q4.80 -24.36 5.40 -24.42Q6.00 -24.48 6.12 -24.48Q6.24 -24.48 6.56 -24.20Q6.88 -23.92 7.14 -23.58Q7.40 -23.24 7.40 -23.12L7.40 -2.36Z M9.80 -12.60L15.96 -12.92L15.64 -9.96L9.80 -10.48L9.80 -12.60Z M10.68 -24.12L11.68 -24.12L11.68 -4.04Q11.68 -3.80 11.48 -3.18Q11.28 -2.56 10.84 -1.76L9.60 -1.76L9.60 -20.68Q9.60 -21.12 9.94 -22.08Q10.28 -23.04 10.68 -24.12Z M23.88 0.36Q23.76 0.36 23.36 0.04Q22.96 -0.28 22.62 -0.64Q22.28 -1.00 22.28 -1.12L22.28 -15.72L20.88 -16.16L20.88 -17.64Q20.88 -17.64 21.34 -17.74Q21.80 -17.84 22.44 -17.96Q23.08 -18.08 23.62 -18.18Q24.16 -18.28 24.28 -18.28Q24.44 -18.28 24.82 -17.98Q25.20 -17.68 25.54 -17.32Q25.88 -16.96 25.88 -16.76L25.88 -2.16L27.28 -1.76L27.28 -0.28Q27.28 -0.28 26.82 -0.18Q26.36 -0.08 25.72 0.04Q25.08 0.16 24.54 0.26Q24.00 0.36 23.88 0.36Z M21.88 -24.44Q21.88 -24.52 22.22 -24.78Q22.56 -25.04 23.00 -25.36Q23.44 -25.68 23.80 -25.90Q24.16 -26.12 24.24 -26.12Q24.40 -26.12 24.76 -25.84Q25.12 -25.56 25.50 -25.16Q25.88 -24.76 26.16 -24.40Q26.44 -24.04 26.40 -23.84L26.24 -23.04Q26.20 -22.92 25.88 -22.66Q25.56 -22.40 25.14 -22.10Q24.72 -21.80 24.36 -21.58Q24.00 -21.36 23.88 -21.36Q23.72 -21.36 23.36 -21.66Q23.00 -21.96 22.64 -22.36Q22.28 -22.76 22.02 -23.12Q21.76 -23.48 21.76 -23.60L21.88 -24.44Z M32.76 0.36Q32.64 0.36 32.32 0.08Q32.00 -0.20 31.70 -0.52Q31.40 -0.84 31.40 -0.96L31.40 -15.56L30.00 -16.16L30.00 -17.64Q30.00 -17.64 30.50 -17.74Q31.00 -17.84 31.68 -17.94Q32.36 -18.04 32.94 -18.14Q33.52 -18.24 33.64 -18.24Q33.76 -18.24 34.08 -17.98Q34.40 -17.72 34.66 -17.40Q34.92 -17.08 34.92 -16.96L34.92 -15.44Q35.44 -15.84 36.10 -16.32Q36.76 -16.80 37.40 -17.24Q38.04 -17.68 38.50 -17.98Q38.96 -18.28 39.04 -18.28Q40.84 -18.28 42.12 -17.68Q43.40 -17.08 44.10 -15.60Q44.80 -14.12 44.80 -11.52L44.80 -2.36L46.20 -1.76L46.20 -0.28Q46.20 -0.28 45.70 -0.18Q45.20 -0.08 44.50 0.04Q43.80 0.16 43.24 0.26Q42.68 0.36 42.56 0.36Q42.44 0.36 42.10 0.08Q41.76 -0.20 41.46 -0.52Q41.16 -0.84 41.16 -0.96L41.16 -11.52Q41.16 -13.44 40.70 -14.22Q40.24 -15.00 39.68 -15.14Q39.12 -15.28 38.84 -15.28Q38.60 -15.28 37.98 -15.04Q37.36 -14.80 36.58 -14.46Q35.80 -14.12 35.04 -13.76L35.04 -2.36L36.40 -1.76L36.40 -0.28Q36.40 -0.28 35.90 -0.18Q35.40 -0.08 34.72 0.04Q34.04 0.16 33.46 0.26Q32.88 0.36 32.76 0.36Z M54.84 0.36Q53.48 0.36 52.16 -0.54Q50.84 -1.44 49.98 -3.32Q49.12 -5.20 49.12 -8.12Q49.12 -10.12 49.40 -11.84Q49.68 -13.56 50.08 -14.32Q50.40 -14.80 51.20 -15.46Q52.00 -16.12 52.94 -16.78Q53.88 -17.44 54.70 -17.86Q55.52 -18.28 55.88 -18.28Q56.80 -18.28 58.00 -18.06Q59.20 -17.84 60.28 -17.52L60.16 -12.40L57.72 -12.40L57.16 -15.16Q56.76 -15.36 56.02 -15.58Q55.28 -15.80 54.68 -15.80Q54.52 -15.80 54.38 -15.76Q54.24 -15.72 54.12 -15.64Q53.76 -15.36 53.50 -14.36Q53.24 -13.36 53.10 -11.88Q52.96 -10.40 52.96 -8.64Q52.96 -6.40 53.44 -5.06Q53.92 -3.72 54.58 -3.14Q55.24 -2.56 55.76 -2.56L60.28 -2.56L60.28 -0.88Q59.56 -0.64 58.72 -0.42Q57.88 -0.20 57.08 -0.02Q56.28 0.16 55.68 0.26Q55.08 0.36 54.84 0.36Z M62.72 -23.72L62.72 -25.20Q62.72 -25.20 63.06 -25.26Q63.40 -25.32 63.90 -25.42Q64.40 -25.52 64.92 -25.62Q65.44 -25.72 65.84 -25.78Q66.24 -25.84 66.36 -25.84Q66.48 -25.84 66.82 -25.56Q67.16 -25.28 67.46 -24.98Q67.76 -24.68 67.76 -24.52L67.56 -15.48L67.76 -15.44Q68.28 -15.84 68.94 -16.32Q69.60 -16.80 70.22 -17.24Q70.84 -17.68 71.28 -17.98Q71.72 -18.28 71.76 -18.28Q73.60 -18.28 74.88 -17.68Q76.16 -17.08 76.84 -15.60Q77.52 -14.12 77.52 -11.52L77.52 -1.12Q77.52 0.08 77.08 1.42Q76.64 2.76 75.82 3.88Q75.00 5.00 73.80 5.56L72.64 4.60Q73.20 3.68 73.46 2.74Q73.72 1.80 73.80 0.86Q73.88 -0.08 73.88 -0.96L73.88 -11.52Q73.88 -13.44 73.42 -14.22Q72.96 -15.00 72.42 -15.14Q71.88 -15.28 71.56 -15.28Q71.40 -15.28 70.60 -14.96Q69.80 -14.64 68.96 -14.28Q68.12 -13.92 67.76 -13.76L67.76 -2.36L69.12 -1.76L69.12 -0.28Q69.12 -0.28 68.62 -0.18Q68.12 -0.08 67.42 0.04Q66.72 0.16 66.14 0.26Q65.56 0.36 65.44 0.36Q65.32 0.36 65.00 0.08Q64.68 -0.20 64.40 -0.52Q64.12 -0.84 64.12 -0.96L64.12 -23.16L62.72 -23.72Z M89.68 -18.28Q90.84 -18.28 91.94 -17.78Q93.04 -17.28 93.94 -16.24Q94.84 -15.20 95.38 -13.60Q95.92 -12.00 95.92 -9.80Q95.92 -7.72 95.66 -6.08Q95.40 -4.44 94.96 -3.60Q94.64 -3.16 93.84 -2.50Q93.04 -1.84 92.10 -1.18Q91.16 -0.52 90.34 -0.08Q89.52 0.36 89.16 0.36Q88.96 0.36 88.06 0.28Q87.16 0.20 86.00 0.06Q84.84 -0.08 83.78 -0.22Q82.72 -0.36 82.16 -0.48L82.16 -23.16L80.76 -23.72L80.76 -25.20Q81.08 -25.28 81.64 -25.38Q82.20 -25.48 82.80 -25.58Q83.40 -25.68 83.84 -25.76Q84.28 -25.84 84.40 -25.84Q84.52 -25.84 84.86 -25.56Q85.20 -25.28 85.50 -24.98Q85.80 -24.68 85.80 -24.52L85.60 -15.56L85.80 -15.52Q86.48 -16.04 87.34 -16.68Q88.20 -17.32 88.88 -17.80Q89.56 -18.28 89.68 -18.28Z M89.44 -15.32Q89.32 -15.32 88.66 -15.04Q88.00 -14.76 87.20 -14.40Q86.40 -14.04 85.80 -13.72L85.80 -2.72Q86.44 -2.52 87.42 -2.32Q88.40 -2.12 89.30 -2.02Q90.20 -1.92 90.56 -1.96Q91.04 -2.04 91.38 -2.68Q91.72 -3.32 91.90 -4.90Q92.08 -6.48 92.08 -9.28Q92.08 -11.48 91.58 -12.80Q91.08 -14.12 90.46 -14.72Q89.84 -15.32 89.44 -15.32Z M103.80 7.24Q103.68 7.24 103.46 6.90Q103.24 6.56 103.08 6.16Q102.92 5.76 102.92 5.64L104.80 -0.04Q104.52 -0.00 104.20 0.06Q103.88 0.12 103.76 0.12Q103.68 0.12 103.42 -0.04Q103.16 -0.20 103.16 -0.20L98.92 -15.72L97.36 -16.16L97.36 -17.80Q97.36 -17.80 97.82 -17.88Q98.28 -17.96 98.92 -18.04Q99.56 -18.12 100.10 -18.20Q100.64 -18.28 100.76 -18.28Q100.88 -18.28 101.26 -18.06Q101.64 -17.84 101.98 -17.56Q102.32 -17.28 102.36 -17.08L104.68 -7.68L105.60 -3.40L106.00 -3.40L109.36 -15.80L106.96 -16.08L106.96 -18.00Q106.96 -18.00 107.40 -18.02Q107.84 -18.04 108.48 -18.10Q109.12 -18.16 109.80 -18.20Q110.48 -18.24 110.98 -18.26Q111.48 -18.28 111.56 -18.28Q111.68 -18.28 111.96 -18.02Q112.24 -17.76 112.50 -17.42Q112.76 -17.08 112.72 -16.88L107.40 -0.00L106.24 4.56L107.80 5.28L107.80 6.76Q107.80 6.76 107.24 6.84Q106.68 6.92 105.92 7.00Q105.16 7.08 104.54 7.16Q103.92 7.24 103.80 7.24Z"

SHIELD = "M110 210 H290 V300 C290 360 250 400 200 425 C150 400 110 360 110 300 Z"

def wreath(x0=154, x1=246, base=208.5, thick=17, n=7):
    """The torse: a roll of cloth in two colours twisted together, resting on the
    shield. It is thickest in the middle and narrows towards the ends, as it would
    curling round out of sight; each twist is slanted and puffed, white twists shaded
    with a few engraved lines and ink twists given a highlight along the fold."""
    cx, hw = (x0 + x1) / 2, (x1 - x0) / 2
    T = lambda x: thick * (1 - .42 * ((x - cx) / hw) ** 2)          # thickness along the roll
    pt = lambda x, v: (x, base - T(x) * (1 - v) / 2)                 # v = -1 top edge, +1 bottom edge
    w = (x1 - x0) / n
    def seam(x, v):                                                  # seams slant and bow like a twisted cord
        k = .3 * T(x)
        return pt(x - k * v + .18 * T(x) * (1 - v * v), v)
    f = lambda q: f"{q[0]:.1f} {q[1]:.1f}"
    parts = []
    for i in range(n):
        a, b = x0 + i * w, x0 + (i + 1) * w
        c = (a + b) / 2
        vs = [-1 + 2 * j / 6 for j in range(7)]
        if i == 0:   left = [pt(a + 2 - 4 * math.cos(math.asin(v * .97)), v) for v in vs]          # rounded end
        else:        left = [seam(a, v) for v in vs]
        if i == n - 1: right = [pt(b - 2 + 4 * math.cos(math.asin(v * .97)), v) for v in vs]
        else:          right = [seam(b, v) for v in vs]
        tl, tr, br, bl = left[0], right[0], right[-1], left[-1]
        topc = pt(c + .2 * T(c), -1.25); botc = pt(c - .2 * T(c), 1.12)                    # puff above and below
        d = (f"M{f(tl)} Q{f(topc)} {f(tr)} L" + " L".join(f(q) for q in right[1:]) +
             f" Q{f(botc)} {f(bl)} L" + " L".join(f(q) for q in reversed(left[:-1])) + " Z")
        ink = i % 2
        parts.append(f'<path d="{d}" fill="{INK if ink else "#fff"}"/>')
        if ink:   # highlight along the fold of a dark twist
            hl = [seam(c - .12 * w, v) for v in (-.7, -.15, .4)]
            parts.append(f'<path d="M{f(hl[0])} Q{f(hl[1])} {f(hl[2])}" fill="none" stroke="#fff" stroke-width="1.1" stroke-linecap="round"/>')
        else:     # engraved shading on the lower, shadowed side of a light twist
            for off, v0 in ((.3, -.55), (.4, -.75)):
                sh = [seam(c + off * w, v) for v in (v0, .1, .8)]
                parts.append(f'<path d="M{f(sh[0])} Q{f(sh[1])} {f(sh[2])}" fill="none" stroke="{INK}" stroke-width=".7" stroke-linecap="round"/>')
    return "\n    ".join(parts)

CREST = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 84 320 474" role="img" aria-labelledby="ct">
  <title id="ct">Finchby crest: a shield in three parts showing an owl, a wing and an anchor, divided by a chevron with three buckles, framed by laurel, with a finch in flight above, the motto Grip Fast and the name Finchby</title>
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
  <g transform="translate(158.4 91.6) scale(.1)" fill="{INK}">
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

  <!-- the name -->
  <path transform="translate({200 - NAME_W / 2:.1f} 543)" fill="{INK}" d="{NAME}"/>
</svg>
"""

if __name__ == "__main__":
    (OUT / "finch.svg").write_text(LOGO)
    (OUT / "crest.svg").write_text(CREST)
    print("drew finch.svg and crest.svg")
