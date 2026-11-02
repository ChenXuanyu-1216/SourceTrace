"""Render the ml-basics test slides as PNG images.

Usage: python tools/make_sample_slides.py
Requires Pillow (pip install pillow). Writes to tests/fixtures/ml-basics/images/.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "ml-basics" / "images"
W, H = 1280, 720
MARGIN = 70
BG = "#ffffff"
ACCENT = "#1f4e79"
TEXT = "#222222"
MUTED = "#555555"
FONT_DIR = Path("C:/Windows/Fonts")


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default(size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def new_slide(title, number):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 110], fill=ACCENT)
    d.text((MARGIN, 55), title, font=font(48, bold=True), fill="white", anchor="lm")
    d.text((W - MARGIN, H - 35), str(number), font=font(22), fill=MUTED, anchor="rm")
    return img, d


def bullets(d, items, top, left=MARGIN, width=W - 2 * MARGIN, size=30):
    fnt = font(size)
    y = top
    for item in items:
        indent = 40 if item.startswith("- ") else 0
        text = item[2:] if indent else item
        d.text((left + indent, y), "•" if not indent else "–", font=fnt, fill=ACCENT)
        for line in wrap(d, text, fnt, width - indent - 35):
            d.text((left + indent + 35, y), line, font=fnt, fill=TEXT)
            y += size + 12
        y += 14
    return y


def box(d, xy, label, fill="#dbe8f5"):
    d.rounded_rectangle(xy, radius=14, fill=fill, outline=ACCENT, width=3)
    cx, cy = (xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2
    d.text((cx, cy), label, font=font(26, bold=True), fill=ACCENT, anchor="mm")


def slide_01():
    img, d = new_slide("Machine Learning: Overview", 1)
    bullets(d, [
        "Machine learning lets computers learn patterns from data "
        "instead of following hand-written rules.",
        "There are three main learning paradigms:",
    ], top=150)
    # Diagram: one parent box with three children.
    box(d, (490, 360, 790, 440), "Machine Learning")
    children = ["Supervised", "Unsupervised", "Reinforcement"]
    for i, label in enumerate(children):
        x0 = 130 + i * 360
        box(d, (x0, 540, x0 + 300, 620), label, fill="#eef4fa")
        d.line([(640, 440), (x0 + 150, 540)], fill=ACCENT, width=3)
    return img


def slide_02():
    img, d = new_slide("Supervised Learning", 2)
    bullets(d, [
        "Supervised learning uses labeled data for training: "
        "each input comes with the correct output.",
        "Two typical tasks:",
        "- Classification: predict a discrete category (e.g. spam / not spam).",
        "- Regression: predict a continuous value (e.g. house price).",
    ], top=150)
    return img


def slide_03():
    img, d = new_slide("Unsupervised Learning", 3)
    bullets(d, [
        "Unsupervised learning discovers patterns in unlabeled data.",
        "Two typical tasks:",
        "- Clustering: group similar data points (e.g. k-means).",
        "- Dimensionality reduction: compress features while keeping "
        "the structure of the data (e.g. PCA).",
    ], top=150)
    return img


def slide_04():
    img, d = new_slide("Reinforcement Learning & Comparison", 4)
    y = bullets(d, [
        "In reinforcement learning, an agent learns by interacting "
        "with an environment and receiving rewards.",
    ], top=150)
    # Comparison table.
    rows = [
        ("Paradigm", "Training data", "Feedback"),
        ("Supervised", "Labeled", "Correct answers"),
        ("Unsupervised", "Unlabeled", "None"),
        ("Reinforcement", "Interaction", "Rewards"),
    ]
    cols = [MARGIN, MARGIN + 380, MARGIN + 760, W - MARGIN]
    top, row_h = y + 20, 70
    for r, row in enumerate(rows):
        y0 = top + r * row_h
        fill = ACCENT if r == 0 else ("#eef4fa" if r % 2 else BG)
        d.rectangle([cols[0], y0, cols[-1], y0 + row_h], fill=fill, outline="#9db5cc")
        for c, cell in enumerate(row):
            d.text((cols[c] + 20, y0 + row_h / 2), cell,
                   font=font(28, bold=r == 0), fill="white" if r == 0 else TEXT, anchor="lm")
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for n, make in enumerate([slide_01, slide_02, slide_03, slide_04], start=1):
        path = OUT_DIR / f"slide-{n:02d}.png"
        make().save(path)
        print(path)


if __name__ == "__main__":
    main()
