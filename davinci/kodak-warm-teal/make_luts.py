#!/usr/bin/env python3
"""Generate the "Kodak Warm Teal" creative LUTs for DaVinci Resolve.

All LUTs are Rec.709 (gamma 2.4) in -> Rec.709 (gamma 2.4) out, 33x33x33 .cube.
They are meant to sit AFTER a CST OUT node (or directly on Rec.709 footage).

Each look component is its own LUT so it can live in its own node and be
dialled in with that node's Key Output Gain:

  KWT_1_Hue.cube      greens -> teal, blues -> cyan, skin protected
  KWT_2_Split.cube    teal shadows / warm highlights (luma-preserving)
  KWT_3_Print.cube    Kodak-print style contrast, density, highlight rolloff
  KWT_Full.cube       all three combined (single-node version)

Run:  python3 make_luts.py            -> writes the .cube files next to this script
"""
import os

import numpy as np

SIZE = 33
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

LUMA = np.array([0.2126, 0.7152, 0.0722])


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def luma(rgb):
    return rgb @ LUMA


# ---------------------------------------------------------------- HSV helpers
def rgb_to_hsv(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1)
    mn = rgb.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    nz = d > 1e-8
    rc = nz & (mx == r)
    gc = nz & (mx == g) & ~rc
    bc = nz & ~rc & ~gc
    h[rc] = ((g - b)[rc] / d[rc]) % 6.0
    h[gc] = (b - r)[gc] / d[gc] + 2.0
    h[bc] = (r - g)[bc] / d[bc] + 4.0
    h = h * 60.0
    s = np.where(mx > 1e-8, d / np.maximum(mx, 1e-8), 0.0)
    return np.stack([h, s, mx], -1)


def hsv_to_rgb(hsv):
    h, s, v = hsv[..., 0] % 360.0, hsv[..., 1], hsv[..., 2]
    c = v * s
    hp = h / 60.0
    x = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(h)
    sectors = [
        (0, 1, np.stack([c, x, z], -1)),
        (1, 2, np.stack([x, c, z], -1)),
        (2, 3, np.stack([z, c, x], -1)),
        (3, 4, np.stack([z, x, c], -1)),
        (4, 5, np.stack([x, z, c], -1)),
        (5, 6, np.stack([c, z, x], -1)),
    ]
    out = np.zeros(h.shape + (3,))
    for lo, hi, val in sectors:
        m = (hp >= lo) & (hp < hi)
        out[m] = val[m]
    return out + (v - c)[..., None]


def hue_window(h, center, width):
    """Smooth 0..1 weight around a hue (degrees), falling to 0 at +-width."""
    d = np.abs((h - center + 180.0) % 360.0 - 180.0)
    return 1.0 - smoothstep(0.0, width, d)


# ---------------------------------------------------------------- components
def hue_component(rgb):
    """Greens -> teal, blues -> cyan, skin tones kept clean and warm."""
    hsv = rgb_to_hsv(np.clip(rgb, 0.0, 1.0))
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # only act on colours that actually have some saturation
    sat_gate = smoothstep(0.04, 0.25, s)

    w_green = hue_window(h, 115.0, 55.0) * sat_gate
    w_blue = hue_window(h, 220.0, 40.0) * sat_gate
    w_skin = hue_window(h, 28.0, 22.0) * sat_gate

    h = h + w_green * 38.0          # 115 deg -> ~153 deg (teal-green)
    h = h - w_blue * 18.0           # push blues toward cyan/teal
    h = h + w_skin * (27.0 - h) * 0.25  # pull skin toward clean orange (30 deg)

    s = s * (1.0 - 0.22 * w_green)  # tame foliage
    s = s * (1.0 + 0.03 * w_skin)   # a touch richer skin
    s = s * (1.0 + 0.08 * w_blue)   # slightly richer teal skies

    return hsv_to_rgb(np.stack([h, np.clip(s, 0, 1), v], -1))


def split_component(rgb):
    """Teal shadows, warm highlights; luminance preserved."""
    y = luma(rgb)
    w_sh = (1.0 - smoothstep(0.05, 0.55, y)) * smoothstep(0.0, 0.08, y)
    w_hi = smoothstep(0.45, 0.95, y) * (1.0 - 0.5 * smoothstep(0.95, 1.0, y))

    teal = np.array([-1.0, 0.25, 0.75])
    warm = np.array([1.0, 0.35, -0.95])
    teal = teal - (teal @ LUMA)   # zero-luma tint directions
    warm = warm - (warm @ LUMA)

    out = rgb + (0.040 * w_sh)[..., None] * teal + (0.038 * w_hi)[..., None] * warm
    return out


def _sigmoid_curve(x, pivot, contrast, black, white):
    """Filmic S-curve on 0..1 code values, normalised to hit black/white."""
    def f(t):
        return 1.0 / (1.0 + np.exp(-contrast * (t - pivot)))
    lo, hi = f(0.0), f(1.0)
    return black + (white - black) * (f(x) - lo) / (hi - lo)


def print_component(rgb):
    """Kodak-print flavour: S-curve with soft toe/shoulder, subtle channel
    crossover (cool toe, warm shoulder), subtractive density on saturated
    colours and highlight desaturation."""
    x = np.clip(rgb, 0.0, 1.0)
    # per-channel curves: red a bit longer in the shoulder, blue a bit lifted in the toe
    r = _sigmoid_curve(x[..., 0], 0.44, 4.8, 0.012, 0.985)
    g = _sigmoid_curve(x[..., 1], 0.45, 4.9, 0.014, 0.975)
    b = _sigmoid_curve(x[..., 2], 0.455, 4.7, 0.026, 0.965)
    out = np.stack([r, g, b], -1)

    # blend back a little of the linear response so mids aren't crushed
    out = 0.7 * out + 0.3 * (0.012 + 0.97 * x)

    # subtractive density: saturated colours get darker & richer
    y = luma(out)
    chroma = out.max(-1) - out.min(-1)
    out = y[..., None] + (out - y[..., None]) * 0.92
    out = out * (1.0 - 0.14 * chroma)[..., None]

    # highlight desaturation (print rolloff)
    y = luma(out)
    hd = smoothstep(0.78, 1.0, y) * 0.55
    out = out + (y[..., None] - out) * hd[..., None]
    return out


def full_look(rgb):
    return print_component(split_component(hue_component(rgb)))


COMPONENTS = {
    "KWT_1_Hue": ("Kodak Warm Teal - 1 Hue (green>teal, skin protect)", hue_component),
    "KWT_2_Split": ("Kodak Warm Teal - 2 Split (teal shadows / warm highs)", split_component),
    "KWT_3_Print": ("Kodak Warm Teal - 3 Print (Kodak-style contrast & density)", print_component),
    "KWT_Full": ("Kodak Warm Teal - Full look (Rec709 in/out)", full_look),
}


# ---------------------------------------------------------------- .cube I/O
def identity_grid(n=SIZE):
    r = np.linspace(0.0, 1.0, n)
    # .cube order: red changes fastest, then green, then blue
    b, g, rr = np.meshgrid(r, r, r, indexing="ij")
    return np.stack([rr, g, b], -1).reshape(-1, 3)


def write_cube(path, title, fn, n=SIZE):
    grid = identity_grid(n)
    out = np.clip(fn(grid), 0.0, 1.0)
    with open(path, "w", newline="\n") as fh:
        fh.write(f'TITLE "{title}"\n')
        fh.write("# Rec.709 gamma 2.4 in -> Rec.709 gamma 2.4 out\n")
        fh.write(f"LUT_3D_SIZE {n}\n")
        fh.write("DOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
        for r, g, b in out:
            fh.write(f"{r:.6f} {g:.6f} {b:.6f}\n")


def main():
    for name, (title, fn) in COMPONENTS.items():
        path = os.path.join(OUT_DIR, f"{name}.cube")
        write_cube(path, title, fn)
        print("wrote", path)


if __name__ == "__main__":
    main()
