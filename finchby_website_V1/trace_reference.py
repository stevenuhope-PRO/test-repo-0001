#!/usr/bin/env python3
"""Cuts the finch out of the reference photo and measures its wings and tail for
make_art.py.

Run:  pip install opencv-python-headless numpy
      python3 trace_reference.py PHOTO.png [OUT_DIR]

Writes OUT_DIR/finch-cutout.png (the bird on a transparent background) and
prints the UPPER, LOWER and TAIL feather-length lists to paste into make_art.py.
The crop box, the belly patch and the logo mapping below are set for the
554 x 554 house-finch photo the logo was drawn from; adjust them for another photo.
"""
import sys, pathlib
import cv2, numpy as np

F = 4                                   # work at 4x the photo's size
BOX = (135, 95, 335, 345)               # bird's bounding box in the photo (x0, y0, x1, y1)
BELLY = [(195, 201), (217, 204), (247, 205), (270, 220), (275, 228), (260, 231),
         (230, 231), (210, 235), (195, 230), (191, 220)]   # smooth, untextured belly, forced in
to_logo = lambda x, y: (3.7 * x - 475, 3.7 * y - 282)       # photo px -> logo units
to_photo = lambda x, y: ((x + 475) / 3.7, (y + 282) / 3.7)
ROOTS = {"UPPER": ((330, 418), -115, 2), "LOWER": ((300, 560), 28, 125), "TAIL": ((520, 525), -42, 68)}

def largest(mask):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
    return lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])

def cut_out(img):
    """The bird is sharp and the background is blurred, so local sharpness seeds
    GrabCut: very sharp = surely bird, somewhat sharp = probably bird."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    sharp = cv2.GaussianBlur(np.abs(cv2.Laplacian(g, cv2.CV_32F, ksize=3)), (0, 0), 2.0)
    roi = np.zeros(g.shape, bool); roi[BOX[1]:BOX[3], BOX[0]:BOX[2]] = True
    sure = cv2.erode(largest((sharp > 140) & roi).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2) > 0
    prob = cv2.dilate(largest((sharp > 45) & roi).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2) > 0
    seed = np.full(g.shape, cv2.GC_BGD, np.uint8); seed[prob] = cv2.GC_PR_FGD; seed[sure] = cv2.GC_FGD
    seed = cv2.resize(seed, None, fx=F, fy=F, interpolation=cv2.INTER_NEAREST)
    cv2.fillPoly(seed, [(np.array(BELLY) * F).astype(np.int32)], cv2.GC_FGD)
    big = cv2.resize(img, None, fx=F, fy=F, interpolation=cv2.INTER_CUBIC)
    cv2.grabCut(big, seed, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
    bird = largest((seed == cv2.GC_FGD) | (seed == cv2.GC_PR_FGD))
    n, lab, st, _ = cv2.connectedComponentsWithStats((~bird).astype(np.uint8))   # fill small holes
    for k in range(1, n):
        x, y, _, _, area = st[k]
        if area < 4000 and x > 0 and y > 0:
            bird[lab == k] = True
    return big, bird

def profile(bird, root, a0, a1):
    """Distance from root to the bird's outer edge every 1 degree, smoothed and
    kept every 3 degrees: the feather lengths of one fan."""
    ux, uy = (c * F for c in to_photo(*root)); H, W = bird.shape; out = []
    for a in range(a0, a1 + 1):
        dx, dy, last = np.cos(np.radians(a)), np.sin(np.radians(a)), 0
        for r in range(1400):
            x, y = int(ux + dx * r), int(uy + dy * r)
            if not (0 <= x < W and 0 <= y < H): break
            if bird[y, x]: last = r
        out.append(last / F * 3.7)
    sm = [np.mean(out[max(0, i - 2):i + 3]) for i in range(len(out))]
    keep = list(range(0, len(sm), 3)) + ([len(sm) - 1] if (len(sm) - 1) % 3 else [])
    return [(a0 + i, round(float(sm[i]))) for i in keep]

if __name__ == "__main__":
    img = cv2.imread(sys.argv[1]); out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else ".")
    big, bird = cut_out(img)
    rgba = cv2.cvtColor(big, cv2.COLOR_BGR2BGRA); rgba[:, :, 3] = bird * 255
    cv2.imwrite(str(out / "finch-cutout.png"), rgba[BOX[1]*F:BOX[3]*F, BOX[0]*F:BOX[2]*F])
    for name, (root, a0, a1) in ROOTS.items():
        print(f"{name} = {profile(bird, root, a0, a1)}")
