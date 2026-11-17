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
    <circle cx="177" cy="206" r="14.5"/>
    <path d="M167 196 L152 205 L168 212 Z"/>
    <circle cx="172" cy="202" r="2.2" fill="{eye}"/>"""

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
  <title id="ct">Finchby crest: a shield in three parts showing an owl, a wing and a pair of scales, divided by a chevron with three buckles, framed by laurel, with a finch in flight above and the motto Grip Fast</title>
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

  <!-- 1. wisdom: an owl -->
  <g transform="translate(153 245)" fill="#fff" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">
    <path d="M-15 -17 L-8 -12 C-3 -14 3 -14 8 -12 L15 -17 C17 -8 17 2 14 10 C11 17 5 20 0 20 C-5 20 -11 17 -14 10 C-17 2 -17 -8 -15 -17 Z"/>
    <circle cx="-6.5" cy="-3" r="5.6"/><circle cx="6.5" cy="-3" r="5.6"/>
    <circle cx="-6.5" cy="-3" r="2.1" fill="{INK}" stroke="none"/><circle cx="6.5" cy="-3" r="2.1" fill="{INK}" stroke="none"/>
    <path d="M-2.2 2 L0 6.5 L2.2 2 Z" fill="{INK}" stroke-width="1"/>
    <path d="M-6 11 Q-3 14 0 11 Q3 14 6 11" fill="none" stroke-width="1.2"/>
  </g>
  <!-- 2. agility: a wing -->
  <g transform="translate(247 246) scale(1.05)" fill="#fff" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round">
    <path d="M-21 9 C-15 -8 3 -17 23 -15 C17 -11 13 -9 10 -6 C15 -6 18 -6 20 -5 C14 -2 10 0 7 2 C11 3 13 3 15 4 C9 7 4 9 -1 10 C-8 13 -15 12 -21 9 Z"/>
    <path d="M-14 6 C-8 -4 2 -9 12 -10 M-9 8 C-3 2 4 -2 11 -3" fill="none" stroke-width="1.1"/>
  </g>
  <!-- 3. integrity: the scales -->
  <g transform="translate(200 366)" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-10 21 H10 L6 16 H-6 Z"/>
    <path d="M0 16 V-20 M-22 -14 H22" fill="none" stroke-width="2.4"/>
    <circle cx="0" cy="-21" r="3"/>
    <path d="M-22 -14 L-30 4 M-22 -14 L-14 4 M22 -14 L14 4 M22 -14 L30 4" fill="none" stroke-width="1.2"/>
    <path d="M-32 4 H-12 C-13 11 -17 14 -22 14 C-27 14 -31 11 -32 4 Z M12 4 H32 C31 11 27 14 22 14 C17 14 13 11 12 4 Z"/>
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
