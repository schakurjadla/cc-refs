"""Composite the nazar artwork onto the blank hoodie photo as a washed screenprint.

The photo is left untouched outside the print. Inside the print, the ink takes the
fabric's shading, fold displacement and knit texture, and the drawcords stay on top.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BASE, ART, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

PX_PER_CM = 16.8          # seam-to-seam chest ~1010 px for ~60 cm
WIDTH_CM, DROP_CM = 30, 8
NECK_Y, CENTER_X = 455, 1000
INK_OPACITY = 0.92

base = np.asarray(Image.open(BASE).convert("RGB")).astype(np.float32) / 255
art = np.asarray(Image.open(ART).convert("RGB")).astype(np.float32) / 255

# 1. Key out the painted checkerboard (neutral squares of ~130 and ~191) into real alpha.
grey = art.mean(-1)
chroma = art.max(-1) - art.min(-1)
off_range = np.clip(np.maximum(0.47 - grey, grey - 0.79), 0, None)
alpha = np.clip(np.maximum((chroma - 0.035) / 0.07, off_range / 0.05), 0, 1)
alpha = ndi.grey_closing(ndi.median_filter(alpha, 3), size=2)
pure_bg = (chroma < 0.03) & (off_range == 0)
_, (iy, ix) = ndi.distance_transform_edt(~pure_bg, return_indices=True)
bg = art[iy, ix]                      # nearest checker colour under each pixel
a3 = alpha[..., None]
ink = np.clip((art - (1 - a3) * bg) / np.maximum(a3, 0.05), 0, 1)

# Crop to the inked area and scale to 30 cm wide.
ys, xs = np.where(alpha > 0.5)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
rgba = np.dstack([ink, alpha])[y0:y1, x0:x1]
w = round(WIDTH_CM * PX_PER_CM)
h = round(rgba.shape[0] * w / rgba.shape[1])
rgba = np.asarray(
    Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").resize((w, h), Image.LANCZOS)
).astype(np.float32) / 255

top = NECK_Y + round(DROP_CM * PX_PER_CM)
left = CENTER_X - w // 2
layer = np.zeros(base.shape[:2] + (4,), np.float32)
layer[top:top + h, left:left + w] = rgba

# 2. Fabric maps from the photo's luminance.
lum = base @ np.array([0.299, 0.587, 0.114], np.float32)
smooth = ndi.gaussian_filter(lum, 2.5)
broad = ndi.gaussian_filter(lum, 60)
shade = np.clip(smooth / np.maximum(broad, 1e-3), 0.6, 1.25)   # folds/creases
knit = lum - ndi.gaussian_filter(lum, 1.5)                       # knit texture

# 3. Displace the print along the fold relief so it bends with the fabric.
relief = ndi.gaussian_filter(lum, 6)
gy, gx = np.gradient(relief)
k = 120.0
yy, xx = np.mgrid[0:base.shape[0], 0:base.shape[1]].astype(np.float32)
layer = np.dstack([
    ndi.map_coordinates(layer[..., c], [yy - gy * k, xx - gx * k], order=1)
    for c in range(4)
])

ink, a = layer[..., :3], layer[..., 3]

# 4. Washed ink: fleece breaks through in the knit valleys, plus fine speckle.
rng = np.random.default_rng(7)
speckle = ndi.gaussian_filter(rng.random(lum.shape).astype(np.float32), 0.8)
breaks = np.clip(-knit * 9, 0, 1) * 0.55 + np.clip((speckle - 0.62) * 6, 0, 1) * 0.35
a = a * INK_OPACITY * (1 - np.clip(breaks, 0, 0.8))

# Ink sits in the fibres: takes the fold shading, the knit texture, and a little
# of the dye underneath (matte, no highlight of its own).
ink = ink * shade[..., None] ** 1.15
ink = ink * (1 - 0.18) + ink * (base / np.maximum(broad[..., None], 1e-3)) * 0.18
ink = np.clip(ink + knit[..., None] * 1.1, 0, 1)

# 5. Drawcords stay on top of the print.
cord = Image.new("L", (base.shape[1], base.shape[0]), 0)
from PIL import ImageDraw
d = ImageDraw.Draw(cord)
for pts, knot in (
    ([(905, 370), (918, 550), (920, 700), (918, 815), (918, 878)], (896, 812, 938, 848)),
    ([(1080, 370), (1072, 550), (1073, 700), (1074, 815), (1072, 878)], (1057, 810, 1101, 848)),
):
    d.line(pts, fill=255, width=34, joint="curve")
    d.ellipse(knot, fill=255)
cord = ndi.gaussian_filter(np.asarray(cord, np.float32) / 255, 1.2)
a = a * (1 - cord)

out = base * (1 - a[..., None]) + ink * a[..., None]
Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(OUT)
print("print box", left, top, w, h)
