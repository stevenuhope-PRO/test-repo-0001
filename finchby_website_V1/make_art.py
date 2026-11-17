#!/usr/bin/env python3
"""Draws the Finchby logo (assets/img/finch.svg) and crest (assets/img/crest.svg).
Run:  python3 make_art.py      Colors and proportions are set at the top."""
import math, pathlib

INK, TINT = "#14261f", "#dfe8e2"
OUT = pathlib.Path(__file__).parent / "assets" / "img"

# ------------------------------------------------------------------ finch
# Feather lengths of each wing and the tail, measured from the reference photo of
# a house finch in flight by trace_reference.py: (angle clockwise from pointing
# right, length) from the wing's root, in logo units.
UPPER = [(-115, 253), (-112, 261), (-109, 270), (-106, 270), (-103, 277), (-100, 286), (-97, 282), (-94, 285), (-91, 283), (-88, 266), (-85, 268), (-82, 268), (-79, 253), (-76, 250), (-73, 246), (-70, 238), (-67, 236), (-64, 226), (-61, 212), (-58, 216), (-55, 218), (-52, 216), (-49, 208), (-46, 206), (-43, 207), (-40, 202), (-37, 201), (-34, 196), (-31, 196), (-28, 197), (-25, 193), (-22, 191), (-19, 192), (-16, 189), (-13, 184), (-10, 186), (-7, 187), (-4, 184), (-1, 182), (2, 183)]
LOWER = [(28, 199), (31, 202), (34, 206), (37, 206), (40, 209), (43, 216), (46, 220), (49, 220), (52, 226), (55, 233), (58, 236), (61, 239), (64, 245), (67, 249), (70, 258), (73, 265), (76, 270), (79, 281), (82, 286), (85, 294), (88, 307), (91, 313), (94, 328), (97, 339), (100, 356), (103, 373), (106, 387), (109, 391), (112, 399), (115, 401), (118, 396), (121, 350), (124, 236), (125, 182)]
TAIL  = [(-42, 122), (-39, 129), (-36, 136), (-33, 137), (-30, 135), (-27, 139), (-24, 144), (-21, 144), (-18, 142), (-15, 142), (-12, 147), (-9, 154), (-6, 154), (-3, 153), (0, 150), (3, 147), (6, 156), (9, 164), (12, 162), (15, 159), (18, 161), (21, 148), (24, 154), (27, 177), (30, 183), (33, 186), (36, 194), (39, 199), (42, 204), (45, 196), (48, 180), (51, 191), (54, 205), (57, 208), (60, 206), (63, 203), (66, 174), (68, 159)]

def length(profile, a):
    """Feather length at angle a, interpolated from a measured profile."""
    for (a0, l0), (a1, l1) in zip(profile, profile[1:]):
        if a0 <= a <= a1:
            return l0 + (l1 - l0) * (a - a0) / (a1 - a0)
    return profile[0][1] if a < profile[0][0] else profile[-1][1]

def feather(L, w, ang, side=1):
    """One flight feather pointing along +x: a straight leading vane, a sharp tip
    set toward the leading side, and the trailing vane cut back at an angle, as
    on a real primary. side flips which edge leads."""
    y = lambda v: v * side
    return (f'<path d="M0 {y(-.4*w):.1f} L{L-1.2*w:.1f} {y(-w):.1f} Q{L-.3*w:.1f} {y(-.85*w):.1f} {L:.1f} {y(-.3*w):.1f} '
            f'L{L-2.2*w:.1f} {y(w):.1f} L0 {y(.4*w):.1f} Z" transform="rotate({ang:.1f})"/>')

def wing(root, profile, a0, a1, n, side=1, gap=.92, fingers=0, solid=.78):
    """n feathers fanned from root between angles a0 and a1. Each feather is
    slightly narrower than its share of the fan, so the tips stand apart in a
    jagged edge; the first `fingers` feathers (the outer primaries) are narrower
    still and spread like fingers. The inner part of the fan is filled solid."""
    out, pts, da = [], ["0 0"], (a1 - a0) / (n - 1)
    for i in range(n):
        a = a0 + i * da; L = length(profile, a)
        g = gap - (.22 * (1 - i / fingers) if i < fingers else 0)
        out.append(feather(L, .5 * g * L * math.radians(abs(da)), a, side))
        pts.append(f"{L*solid*math.cos(math.radians(a)):.1f} {L*solid*math.sin(math.radians(a)):.1f}")
    out.append(f'<path d="M{" L".join(pts)} Z"/>')
    return f'<g transform="translate({root[0]} {root[1]})">' + "".join(out) + "</g>"

def head(eye="#fff"):
    """Head and body in profile, from the photo: a long flat crown, the forehead
    running straight into a stout conical seed-cracker's beak, and a long
    sloping throat. A heavy brow ridge cuts across the top of the eye and slants
    down toward the beak, for an eagle's level, focused stare."""
    return f"""<path d="M104 477 C112 465 124 453 140 446 C143 440 148 435 158 432 C190 427 228 427 258 424 C284 420 310 410 345 410 C420 418 490 470 540 505 L545 545 C500 572 430 585 360 582 C320 580 285 578 262 574 C240 560 215 540 192 523 C172 510 155 501 140 496 C128 492 114 488 104 477 Z"/>
    <path d="M141 471 C131 473 120 475 110 477" fill="none" stroke="{eye}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M155 457 L194 447 C195 459 187 467 175 467 C164 467 157 463 155 457 Z" fill="{eye}"/>
    <circle cx="176" cy="457" r="6.6"/>
    <path d="M150 455 L199 442 L199 448 L152 461 Z"/>
    <circle cx="173.6" cy="458.6" r="1.5" fill="{eye}"/>"""

def finch(eye="#fff"):
    """House finch in flight, heading left, after the reference photo: upper wing
    raised, lower wing swept down and forward, tail fanned behind."""
    upper = wing((330, 418), UPPER, -111, -2, 16, fingers=5)
    lower = wing((300, 560), LOWER, 119, 34, 17, side=-1, fingers=5)
    tail  = wing((520, 525), TAIL, -38, 64, 12, gap=.95, solid=.7)
    forearm = '<path d="M330 420 L264 448 C262 390 252 300 242 224 L240 186 Z"/>'
    return f"""{upper}
    {lower}
    {tail}
    {forearm}
    {head(eye)}"""

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
