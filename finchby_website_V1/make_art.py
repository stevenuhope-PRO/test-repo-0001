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
  <!-- 1. wisdom: an owl perched on a branch that grows in from the shield's edge -->
  <g clip-path="url(#sh)">
  <g transform="translate(153 242) scale(.95)" fill="#fff" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round">
    <!-- tail, hanging behind the branch -->
    <path d="M-3.2 18 L-2.4 29.2 C-1 30.4 1 30.4 2.4 29.2 L3.2 18 Z"/>
    <!-- branch: tapering, slightly bowed, with bark, a knot, a broken stub and a leafy twig -->
    <path d="M-52 18.2 C-38 17.8 -22 19.2 -8 18.8 C6 18.4 18 17.4 29 15.8 C33.4 15.2 36.6 15.1 38.4 15.7 C37.8 17.1 35 18.2 30.6 19.2 C18.6 22 6.4 25 -8 26.2 C-22 27.4 -37 27.8 -52 29.4 Z"/>
    <path d="M-27 27.2 C-30 29.4 -32.4 32.4 -33.6 36 C-35.4 35.6 -36.6 34.6 -37 33.4 C-35 30.6 -33 28.8 -31.4 27.6 Z"/>
    <path d="M-35.2 35.8 C-36.4 34.9 -36.8 34.2 -37 33.4" fill="none" stroke-width=".8"/>
    <path d="M14 18 C19 14.2 24 10.4 30.2 6.6 C31 7 31.2 7.7 30.8 8.2 C25.6 11.8 21.4 15.6 18.4 17.7 Z"/>
    <path d="M30.4 7.4 C32 3.1 36 .9 40.4 1.1 C39.2 5.1 35.2 7.9 30.4 7.4 Z M31.2 6.6 L38.4 2.3" stroke-width="1.1"/>
    <path d="M23.4 12.3 C21.8 8.3 23 4.3 26.2 2.1 C27.8 5.9 26.8 10.1 23.4 12.3 Z M23.7 11.3 L25.8 3.7" stroke-width="1.1"/>
    <path d="M-50 21.4 C-44 21 -40 21.6 -34 21.3 M-49 25.4 C-43 25.2 -39 25.6 -32 25.1 M-14 23.6 C-10 23.4 -7 23.2 -3 22.8 M10 22 C15 21.2 19 20.4 24 19.4 M14 19.4 C17 19 20 18.5 22 18.1" fill="none" stroke-width=".7"/>
    <path d="M-30 22.4 l1.6 1.2 M-11 20.6 l1.4 1.1 M20 18.8 l1.2 1" fill="none" stroke-width=".6"/>
    <ellipse cx="-21" cy="23.4" rx="2.4" ry="1.4" stroke-width=".9"/><ellipse cx="-21" cy="23.4" rx="1" ry=".55" fill="{INK}" stroke="none"/>
    <!-- head and body in one rounded silhouette, as an owl has no visible neck -->
    <path d="M0 -25.5 C6 -25.5 10.6 -24.4 12.8 -21 C14.4 -17.6 14.2 -13 13.4 -9.6 C15.2 -4 15.6 3 14 9.4 C12.6 15 9 19.4 4.6 21.4 L-4.6 21.4 C-9 19.4 -12.6 15 -14 9.4 C-15.6 3 -15.2 -4 -13.4 -9.6 C-14.2 -13 -14.4 -17.6 -12.8 -21 C-10.6 -24.4 -6 -25.5 0 -25.5 Z"/>
    <!-- face: feathering fans out from each eye instead of a closed disc outline -->
    <path d="M-10.6 -18.6 L-12.2 -20 M-11.6 -15.4 L-13.4 -15.8 M-11.2 -12 L-12.9 -11.4 M-9.4 -9.2 L-10.6 -7.9 M10.6 -18.6 L12.2 -20 M11.6 -15.4 L13.4 -15.8 M11.2 -12 L12.9 -11.4 M9.4 -9.2 L10.6 -7.9" fill="none" stroke-width=".8"/>
    <path d="M-1.2 -15.8 C-3 -18.6 -6.6 -19.8 -10.2 -18.8 M1.2 -15.8 C3 -18.6 6.6 -19.8 10.2 -18.8" fill="none" stroke-width=".8"/>
    <circle cx="-5.4" cy="-14" r="3.7" stroke-width="1.2"/><circle cx="5.4" cy="-14" r="3.7" stroke-width="1.2"/>
    <circle cx="-5.2" cy="-13.8" r="2.2" fill="{INK}" stroke="none"/><circle cx="5.2" cy="-13.8" r="2.2" fill="{INK}" stroke="none"/>
    <circle cx="-4.4" cy="-14.7" r=".65" stroke="none"/><circle cx="6" cy="-14.7" r=".65" stroke="none"/>
    <path d="M-1.5 -11.6 C-1.6 -9.2 -.7 -7.4 0 -6.4 C.7 -7.4 1.6 -9.2 1.5 -11.6 C.6 -12.2 -.6 -12.2 -1.5 -11.6 Z" fill="{INK}" stroke-width=".8"/>
    <!-- breast: small barred feathers -->
    <path d="M-5 -1 q1.3 1.5 2.6 0 M2.4 -1 q1.3 1.5 2.6 0 M-1.3 2.8 q1.3 1.5 2.6 0 M-6 6.6 q1.3 1.5 2.6 0 M3.4 6.6 q1.3 1.5 2.6 0 M-2.3 10.4 q1.3 1.5 2.6 0 M-.3 10.4 q1.3 1.5 2.6 0 M-5 14.2 q1.3 1.5 2.6 0 M2.4 14.2 q1.3 1.5 2.6 0" fill="none" stroke-width=".85"/>
    <!-- folded wings, primaries crossing towards the tail -->
    <path d="M-13.6 -6 C-9 -5.6 -7.4 0 -7.2 7 C-7 13 -6 18 -2.6 25 C-7 23.6 -11.4 19.6 -13.6 13.4 C-15.4 7 -15.4 -1 -13.6 -6 Z"/>
    <path d="M13.6 -6 C9 -5.6 7.4 0 7.2 7 C7 13 6 18 2.6 25 C7 23.6 11.4 19.6 13.6 13.4 C15.4 7 15.4 -1 13.6 -6 Z"/>
    <path d="M-13.8 2 C-11.8 1 -9.6 1.4 -8 3 M-14 8 C-11.8 7 -9.4 7.6 -7.6 9.4 M-12.4 13 C-10.4 15.4 -7.6 19.6 -4.8 23.2 M-10.6 11.4 C-9 14.6 -7 18.6 -4.4 22 M13.8 2 C11.8 1 9.6 1.4 8 3 M14 8 C11.8 7 9.4 7.6 7.6 9.4 M12.4 13 C10.4 15.4 7.6 19.6 4.8 23.2 M10.6 11.4 C9 14.6 7 18.6 4.4 22" fill="none" stroke-width=".8"/>
    <!-- feathered feet, talons curled over the front of the branch -->
    <path d="M-8 18.4 C-8.6 21 -7.8 23.4 -6.2 23.6 C-5.2 23.7 -4.6 23 -4.4 22.4 C-4 23.3 -3.2 23.7 -2.4 23.4 C-1.4 22.8 -1.2 20.6 -2 18.4 Z M8 18.4 C8.6 21 7.8 23.4 6.2 23.6 C5.2 23.7 4.6 23 4.4 22.4 C4 23.3 3.2 23.7 2.4 23.4 C1.4 22.8 1.2 20.6 2 18.4 Z" stroke-width="1"/>
    <path d="M-7 23 C-7.4 24.8 -6.8 26.2 -5.4 27 C-5.9 25.8 -5.9 24.6 -5.4 23.5 Z M-3.2 23.2 C-3.5 24.8 -3 26 -1.8 26.7 C-2.2 25.6 -2.2 24.5 -1.8 23.4 Z M7 23 C7.4 24.8 6.8 26.2 5.4 27 C5.9 25.8 5.9 24.6 5.4 23.5 Z M3.2 23.2 C3.5 24.8 3 26 1.8 26.7 C2.2 25.6 2.2 24.5 1.8 23.4 Z" fill="{INK}" stroke-width=".6"/>
  </g>
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
