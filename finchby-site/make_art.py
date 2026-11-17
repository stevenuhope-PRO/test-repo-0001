#!/usr/bin/env python3
"""Draws the Finchby logo (assets/img/finch.svg) and crest (assets/img/crest.svg).
Run:  python3 make_art.py      Colors and proportions are set at the top."""
import math, pathlib

INK, TINT = "#14261f", "#dfe8e2"
OUT = pathlib.Path(__file__).parent / "assets" / "img"

# ------------------------------------------------------------------ finch
def feather(length, width, deg):
    """A round-tipped feather from the origin, rotated deg degrees."""
    L, w = length, width
    return (f'<path d="M0 0 C{L*.35:.1f} {-w:.1f} {L*.92:.1f} {-w:.1f} {L:.1f} 0 C{L*.92:.1f} {w:.1f} {L*.35:.1f} {w:.1f} 0 0 Z" '
            f'transform="rotate({deg:.1f})"/>')

def fan(root, feathers, width, solid=.86):
    """A wing or tail: round-tipped feathers fanned from a root point.
    feathers = [(angle in degrees clockwise from pointing right, length), ...]"""
    out, pts = [], ["0 0"]
    for ang, length in feathers:
        out.append(feather(length, width, ang))
        r = length * solid
        pts.append(f"{r*math.cos(math.radians(ang)):.1f} {r*math.sin(math.radians(ang)):.1f}")
    out.append(f'<path d="M{" L".join(pts)} Z"/>')
    return f'<g transform="translate({root[0]} {root[1]})">' + "".join(out) + "</g>"

def spread(a0, a1, l0, lmid, l1, n):
    """n feathers from angle a0 to a1, lengths easing l0 -> lmid -> l1."""
    res = []
    for i in range(n):
        f = i / (n - 1)
        length = (1-f)**2 * l0 + 2*f*(1-f) * lmid + f**2 * l1
        res.append((a0 + (a1 - a0) * f, length))
    return res

def finch(eye="#fff"):
    """Finch flying left: upper wing raised in a broad fan, lower wing swept down
    and forward, tail fanned behind. Pose modelled on a house finch in flight."""
    upper = fan((216, 200), spread(-114, -6, 74, 98, 48, 13), 6)
    lower = fan((210, 228), spread(124, 14, 108, 80, 38, 13), 6)
    tail  = fan((262, 216), spread(-28, 56, 46, 54, 48, 7), 8, .9)
    return f"""{upper}
    {lower}
    {tail}
    <ellipse cx="222" cy="215" rx="50" ry="19.5" transform="rotate(5 222 215)"/>
    <circle cx="176" cy="209" r="14.5"/>
    <path d="M161.5 205 L151.5 218 L167.5 221 Z"/>
    <circle cx="169.5" cy="207" r="2.2" fill="{eye}"/>"""

LOGO = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="136 104 190 236" role="img" aria-labelledby="t">
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

CREST = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 84 320 430" role="img" aria-labelledby="ct">
  <title id="ct">Finchby crest: a shield in three parts showing an owl, a wing and a torch, divided by a chevron with three buckles, framed by laurel, with a finch in flight above and the motto Grip Fast</title>
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
  <g transform="translate(106 66) scale(.42)" fill="{INK}">
  {finch()}
  </g>
  <!-- wreath -->
  <g stroke="{INK}" stroke-width="1.6" stroke-linejoin="round">
    <path d="M158 194 H242 V208 H158 Z" fill="#fff"/>
    <path d="M158 208 L166 194 H180 L172 208 Z M186 208 L194 194 H208 L200 208 Z M214 208 L222 194 H236 L228 208 Z" fill="{INK}"/>
  </g>

  <!-- shield: three fields -->
  <path d="{SHIELD}" fill="#fff"/>
  <g clip-path="url(#sh)">
    <rect x="100" y="200" width="200" height="240" fill="url(#az)"/>
    <path d="M200 208 V262" stroke="{INK}" stroke-width="5"/>
    <path d="M200 208 V262" stroke="#fff" stroke-width="2"/>
    <path d="M200 258 L300 338 V374 L200 294 L100 374 V338 Z" fill="url(#or)" stroke="{INK}" stroke-width="2"/>
  </g>
  <path d="{SHIELD}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>

  <!-- 1. wisdom: an owl, perched -->
  <g transform="translate(153 242) scale(.95)" fill="#fff" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">
    <path d="M-4 20 H4 V27 H-4 Z"/>
    <path d="M0 -22 C9 -22 13 -15 13 -7 C13 -1 12 3 13 9 C14 16 8 21 0 21 C-8 21 -14 16 -13 9 C-12 3 -13 -1 -13 -7 C-13 -15 -9 -22 0 -22 Z"/>
    <path d="M0 -15 C-3 -18 -9 -17 -10 -12 C-11 -7 -6 -3 0 -3 C6 -3 11 -7 10 -12 C9 -17 3 -18 0 -15 Z" stroke-width="1.2"/>
    <circle cx="-4.8" cy="-11" r="2" fill="{INK}" stroke="none"/><circle cx="4.8" cy="-11" r="2" fill="{INK}" stroke="none"/>
    <path d="M-1.6 -8 L0 -4.5 L1.6 -8 Z" fill="{INK}" stroke-width=".8"/>
    <path d="M-12.5 -2 C-10 6 -8 12 -5 18 M12.5 -2 C10 6 8 12 5 18 M-3 3 L0 5.5 L3 3 M-3 9 L0 11.5 L3 9" fill="none" stroke-width="1.2"/>
    <path d="M-19 21 H19" fill="none" stroke-width="2.6"/>
    <path d="M-6 19 V23 M-3 19 V23 M3 19 V23 M6 19 V23" fill="none" stroke-width="1.3"/>
  </g>
  <!-- 2. agility: a wing -->
  <g transform="translate(247 246) scale(1.05)" fill="#fff" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round">
    <path d="M-21 9 C-15 -8 3 -17 23 -15 C17 -11 13 -9 10 -6 C15 -6 18 -6 20 -5 C14 -2 10 0 7 2 C11 3 13 3 15 4 C9 7 4 9 -1 10 C-8 13 -15 12 -21 9 Z"/>
    <path d="M-14 6 C-8 -4 2 -9 12 -10 M-9 8 C-3 2 4 -2 11 -3" fill="none" stroke-width="1.1"/>
  </g>
  <!-- 3. integrity: a torch -->
  <g transform="translate(200 368)" fill="#fff" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-5 2 L-2.5 24 H2.5 L5 2 Z"/>
    <path d="M-3.6 9 H3.6 M-3 15 H3" fill="none" stroke-width="1.1"/>
    <path d="M-10 -4 H10 L7 3 H-7 Z"/>
    <path d="M0 -27 C2 -21 9 -17 8 -10 C7.5 -6.5 4.5 -4 0 -4 C-4.5 -4 -7.5 -6.5 -8 -10 C-8.5 -14 -5 -16 -4 -20 C-2 -18 -1 -17 -1 -15 C1 -18 1 -23 0 -27 Z"/>
    <path d="M0 -13 C2 -11 3 -9 2 -7 C1.5 -5.5 -1.5 -5.5 -2 -7 C-2.5 -9 -1 -11 0 -13 Z" fill="{INK}" stroke="none"/>
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
