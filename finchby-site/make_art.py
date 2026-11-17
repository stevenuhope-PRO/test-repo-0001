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

def wing(side, scale=1.0, n=11):
    """Fanned wing. side=-1 upper, +1 lower. Angles are measured from the direction of flight."""
    a0, a1 = 52, 150
    out, fan = [], ["0 0"]
    for i in range(n):
        f = i / (n - 1)
        ang = a0 + (a1 - a0) * f
        length = (60 + 14 * math.sin(math.pi * min(f * 2.2, 1)) - 26 * f ** 1.6) * scale          # long primaries in front, short secondaries behind
        out.append(feather(length, 6.2, side * ang))
        r = length * .8
        fan.append(f"{r*math.cos(math.radians(ang)):.1f} {side*r*math.sin(math.radians(ang)):.1f}")
    out.append(f'<path d="M{" L".join(fan)} Z"/>')      # solid inner wing
    return "\n      ".join(out)

def finch(eye="#fff"):
    tail = "".join(feather(L, 7, 180 + d) for d, L in [(-24, 36), (-12, 35), (0, 30), (12, 35), (24, 36)])
    return f"""<g transform="rotate(-24)">
    <g transform="translate(6 -7)">
      {wing(-1)}
    </g>
    <g transform="translate(6 7)">
      {wing(1, .9)}
    </g>
    <g transform="translate(-22 0)">{tail}</g>
    <ellipse cx="2" cy="0" rx="31" ry="13.5"/>
    <circle cx="31" cy="0" r="11.5"/>
    <path d="M39 -7 L51 0 L39 7 Z"/>
    <circle cx="34" cy="-4.5" r="1.9" fill="{eye}"/>
  </g>"""

LOGO = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="-68 -80 140 140" role="img" aria-labelledby="t">
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
  <title id="ct">Finchby crest: a shield in three parts showing an open book, a wing and an arrow in a target, divided by a chevron with three buckles, framed by laurel, with a finch in flight above and the motto Grip Fast</title>
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
  <g transform="translate(198 158) scale(.8)" fill="{INK}">
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

  <!-- 1. intelligent: an open book -->
  <g transform="translate(153 246)" fill="#fff" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round">
    <path d="M0 -9 C-7 -15 -15 -15 -22 -11 V13 C-15 9 -7 9 0 14 C7 9 15 9 22 13 V-11 C15 -15 7 -15 0 -9 Z"/>
    <path d="M0 -9 V14 M-17 -6 C-12 -8 -8 -8 -4 -5 M-17 0 C-12 -2 -8 -2 -4 1 M-17 6 C-12 4 -8 4 -4 7 M17 -6 C12 -8 8 -8 4 -5 M17 0 C12 -2 8 -2 4 1 M17 6 C12 4 8 4 4 7" fill="none" stroke-width="1.2"/>
  </g>
  <!-- 2. agile: a wing -->
  <g transform="translate(247 246) scale(1.05)" fill="#fff" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round">
    <path d="M-21 9 C-15 -8 3 -17 23 -15 C17 -11 13 -9 10 -6 C15 -6 18 -6 20 -5 C14 -2 10 0 7 2 C11 3 13 3 15 4 C9 7 4 9 -1 10 C-8 13 -15 12 -21 9 Z"/>
    <path d="M-14 6 C-8 -4 2 -9 12 -10 M-9 8 C-3 2 4 -2 11 -3" fill="none" stroke-width="1.1"/>
  </g>
  <!-- 3. focused: an arrow in the target (the roundel of Hope) -->
  <g transform="translate(200 368)" stroke="{INK}">
    <circle r="17" fill="#fff" stroke-width="2"/><circle r="11" fill="none" stroke-width="1.6"/><circle r="5" fill="{INK}"/>
    <path d="M0 0 L24 -24" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M17 -24 L24 -24 L24 -17 M21 -28 L28 -28 L28 -21" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
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
