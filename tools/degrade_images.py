"""Make scan- and photo-like copies of a test fixture's slides.

Usage: python tools/degrade_images.py <fixture> <variant> [<variant> ...]
Variants:
  scan      greyscale photocopy: slight tilt, lower contrast, blur, speckles, JPEG artefacts
  photo     phone photo of a projected slide: perspective, uneven light, colour cast, smaller, JPEG
  occluded  photo, plus glare that wipes out the areas listed in OCCLUSIONS for that fixture
Writes tests/fixtures/<fixture>-<variant>/images/slide-NN.jpg. The output is seeded, so the
same input always gives the same images. Requires Pillow and NumPy.
"""

import sys
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"

# Areas to wipe out in the occluded variant, in the clean slide's pixel coordinates:
# {fixture: {page: [(left, top, right, bottom), ...]}}.
OCCLUSIONS = {
    "model-eval": {
        2: [(785, 306, 935, 364)],    # "7 : 2 : 1" in the split-ratio bullet
        7: [(362, 362, 1208, 438)],   # formula and meaning cells of the precision row
    },
}


def to_array(img):
    return np.asarray(img, dtype=np.float32)


def to_image(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def scan(img, rng):
    grey = img.convert("L").rotate(rng.uniform(-1.8, 1.8), resample=Image.BICUBIC, fillcolor=255)
    arr = 45 + to_array(grey) * 0.72                       # grey paper, faded ink
    arr += rng.normal(0, 7, arr.shape)                     # paper grain
    specks = rng.random(arr.shape) < 0.0015
    arr[specks] = rng.uniform(0, 90, specks.sum())         # dust
    return to_image(arr).filter(ImageFilter.GaussianBlur(0.8))


def perspective_coeffs(src, dst):
    """Coefficients for Image.transform: map each output point in dst back to src."""
    rows = []
    for (x, y), (u, v) in zip(dst, src):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(rows), np.array(src).reshape(8))


def photo(img, rng, boxes=()):
    w, h = img.size
    # Keystone: the projected slide is narrower at the top and slightly skewed.
    j = lambda a, b: rng.uniform(a, b)
    dst = [(w * j(0.07, 0.10), h * j(0.06, 0.09)), (w * j(0.90, 0.93), h * j(0.04, 0.07)),
           (w * j(0.96, 0.98), h * j(0.93, 0.96)), (w * j(0.02, 0.04), h * j(0.91, 0.94))]
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    coeffs = perspective_coeffs(src, dst)
    warped = img.convert("RGB").transform((w, h), Image.PERSPECTIVE, coeffs,
                                          resample=Image.BICUBIC, fillcolor=(58, 56, 52))
    arr = to_array(warped)
    # Uneven light: brighter towards one corner, darker at the edges.
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w * j(0.3, 0.7), h * j(0.3, 0.6)
    dist = np.hypot((xx - cx) / w, (yy - cy) / h)
    light = 1.05 - 0.55 * dist ** 1.5
    arr *= light[..., None]
    arr *= np.array([1.04, 1.0, 0.86])                     # warm colour cast
    if boxes:                                              # glare goes on top of the lighting
        mask = to_array(glare_mask((w, h), boxes).transform((w, h), Image.PERSPECTIVE, coeffs,
                                                            resample=Image.BICUBIC)) / 255
        arr = arr * (1 - mask[..., None]) + np.array([255, 255, 248]) * mask[..., None]
    arr += rng.normal(0, 5, arr.shape)                     # sensor noise
    out = to_image(arr).filter(ImageFilter.GaussianBlur(1.0))
    return out.resize((1024, round(1024 * h / w)), Image.LANCZOS)


def glare_mask(size, boxes):
    """A reflection over each box: fully white on the box, fading out a little beyond it."""
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    for left, top, right, bottom in boxes:
        d.ellipse([left - 40, top - 22, right + 40, bottom + 22], fill=120)
    mask = mask.filter(ImageFilter.GaussianBlur(16))
    d = ImageDraw.Draw(mask)
    for left, top, right, bottom in boxes:
        d.rounded_rectangle([left - 6, top - 3, right + 6, bottom + 3], radius=14, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(3))


def degrade(fixture, variant):
    src_dir = FIXTURES / fixture / "images"
    out_dir = FIXTURES / f"{fixture}-{variant}" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    seed = zlib.crc32(f"{fixture}/{variant}".encode())
    for n, path in enumerate(sorted(src_dir.glob("slide-*.png")), start=1):
        rng = np.random.default_rng([seed, n])
        img = Image.open(path)
        if variant == "scan":
            out, quality = scan(img, rng), 45
        elif variant == "photo":
            out, quality = photo(img, rng), 55
        elif variant == "occluded":
            boxes = OCCLUSIONS.get(fixture, {}).get(n, [])
            out, quality = photo(img, rng, boxes), 55
        else:
            raise SystemExit(f"unknown variant: {variant}")
        target = out_dir / f"slide-{n:02d}.jpg"
        out.save(target, quality=quality)
        print(target)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    for v in sys.argv[2:]:
        degrade(sys.argv[1], v)
