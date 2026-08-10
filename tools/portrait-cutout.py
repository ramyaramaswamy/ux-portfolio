"""Knock the studio background out of the portrait.

Flood fill inward from the border rather than a global threshold, so light things
*inside* the subject — teeth, the pearl bracelet, highlights on the watch — stay
opaque instead of being punched into holes.
"""
from PIL import Image, ImageFilter
import numpy as np

SRC = "/Users/ramyaramaswamy/src/portfolio/Home page/1_Ramya_Portrait.png"
DST = "/Users/ramyaramaswamy/src/portfolio/Home page/1_Ramya_Portrait_cutout.png"

# Luminance alone cannot separate subject from background here: her lit skin reaches
# 255 while the background bottoms out at 214, so the ranges fully overlap. What works
# is connectivity plus a strict barrier — at T=200 the fill found a path through a
# forehead highlight and ate half her face. Measured sweep:
#     T=200 -> 23.5% of the face lost      T=220 -> 0.4% of background left unfilled
#     T=210 -> clean                       T=224 -> 5.0% left unfilled
#     T=215 -> clean                       T=232 -> 23.9% left unfilled
# 210-215 is the only window where both are zero. Sitting at 215.
T = 215
T_FRINGE = 195   # local-only cleanup of the brightest edge pixels
FRINGE_PX = 3    # how far that cleanup may reach — short, so it cannot leak
FEATHER = 1.0    # px of blur on the alpha edge, to kill the staircase

im = Image.open(SRC).convert("RGBA")
rgb = np.asarray(im)[:, :, :3].astype(np.float32)
L = rgb.mean(axis=2)
H, W = L.shape

light = L >= T

# Seed from every light pixel on the four borders. Her trousers run off the
# bottom edge, so seeding from *light* border pixels only keeps the fill out
# of the subject.
seed = np.zeros_like(light)
seed[0, :] = light[0, :]
seed[H - 1, :] = light[H - 1, :]
seed[:, 0] = light[:, 0]
seed[:, W - 1] = light[:, W - 1]

# Directional sweeps. Far faster than 1px dilation: each sweep carries the fill
# the whole way across a row or column, so this converges in a handful of passes.
cur = seed.copy()
passes = 0
while True:
    before = int(cur.sum())
    for j in range(1, W):
        cur[:, j] |= cur[:, j - 1] & light[:, j]
    for j in range(W - 2, -1, -1):
        cur[:, j] |= cur[:, j + 1] & light[:, j]
    for i in range(1, H):
        cur[i, :] |= cur[i - 1, :] & light[i, :]
    for i in range(H - 2, -1, -1):
        cur[i, :] |= cur[i + 1, :] & light[i, :]
    passes += 1
    if int(cur.sum()) == before:
        break

bg = cur

# Bounded fringe cleanup: push the background a few px into the brightest edge
# pixels so no light halo survives. Range-limited, so it cannot run into her face
# the way an unbounded fill at this threshold would.
fringe = L >= T_FRINGE
for _ in range(FRINGE_PX):
    grow = np.zeros_like(bg)
    grow[1:, :] |= bg[:-1, :]
    grow[:-1, :] |= bg[1:, :]
    grow[:, 1:] |= bg[:, :-1]
    grow[:, :-1] |= bg[:, 1:]
    bg |= grow & fringe

alpha = np.where(bg, 0, 255).astype(np.uint8)
alpha_img = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(FEATHER))

out = im.copy()
out.putalpha(alpha_img)
out.save(DST)

# ── diagnostics ────────────────────────────────────────────────────────────
a = np.asarray(alpha_img)
print(f"converged in {passes} passes")
print(f"transparent: {100 * (a < 8).mean():.1f}%   opaque: {100 * (a > 247).mean():.1f}%")

# Interior light regions that survived == holes we successfully avoided.
kept_light = light & ~bg
print(f"light pixels kept as subject (teeth, pearls, highlights): {int(kept_light.sum())}")

# Any dark speck left stranded out in the background would show as a floating dot.
edge = np.zeros_like(bg)
edge[:60, :] = True; edge[-60:, :] = True; edge[:, :60] = True; edge[:, -60:] = True
print(f"opaque pixels in the outer 60px frame: {int((a > 128)[edge].sum())}")

ys, xs = np.where(a > 128)
print(f"subject bounds  rows {ys.min()}-{ys.max()}  cols {xs.min()}-{xs.max()}  (image {H}x{W})")

# The check that actually matters: is her face still solid?
print(f"face-box transparency (must be ~0): {100 * (a[250:600, 780:1030] < 128).mean():.2f}%")
print(f"background strip left opaque (must be ~0): {100 * (a[:, 0:250] > 128).mean():.2f}%")

# Proof-on-magenta, so transparency can't hide against a white preview.
chk = Image.new("RGB", out.size, (255, 0, 170))
chk.paste(out, (0, 0), out)
chk.resize((out.width // 3, out.height // 3)).save(
    "/Users/ramyaramaswamy/src/portfolio/tools/verify-cutout.png")
print("wrote", DST)
