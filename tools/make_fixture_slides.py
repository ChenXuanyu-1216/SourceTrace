"""Render the test-fixture slides as PNG images.

Usage: python tools/make_fixture_slides.py [ml-basics | model-eval | all]
Requires Pillow (pip install pillow) and the Windows fonts Arial and Microsoft YaHei.
Writes to tests/fixtures/<deck>/images/.
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
W, H = 1280, 720
MARGIN = 70
BG = "#ffffff"
ACCENT = "#1f4e79"
TEXT = "#222222"
MUTED = "#555555"
LIGHT = "#eef4fa"
FONT_DIR = Path("C:/Windows/Fonts")
LATIN_FONTS = ("arial.ttf", "arialbd.ttf")
CJK_FONTS = ("msyh.ttc", "msyhbd.ttc")
fonts = LATIN_FONTS  # set per deck in main()

# One CJK character, or a run of non-space non-CJK characters, or whitespace.
CJK = "\u2e80-\u9fff\u3000-\u303f\uff00-\uffef"
TOKEN = re.compile(rf"\s+|[{CJK}]|[^\s{CJK}]+")
# Chinese punctuation that must not start a line.
NO_BREAK_BEFORE = set("，。、；：！？）》」』")


def font(size, bold=False):
    try:
        return ImageFont.truetype(str(FONT_DIR / fonts[bold]), size)
    except OSError:
        return ImageFont.load_default(size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for tok in TOKEN.findall(text):
        trial = line + (" " if tok.isspace() else tok)
        if (line and not tok.isspace() and tok not in NO_BREAK_BEFORE
                and draw.textlength(trial.rstrip(), font=fnt) > width):
            lines.append(line.rstrip())
            line = tok
        else:
            line = trial
    lines.append(line.rstrip())
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


def box(d, xy, label, fill="#dbe8f5", size=26):
    d.rounded_rectangle(xy, radius=14, fill=fill, outline=ACCENT, width=3)
    cx, cy = (xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2
    d.text((cx, cy), label, font=font(size, bold=True), fill=ACCENT, anchor="mm")


def arrow(d, start, end):
    d.line([start, end], fill=ACCENT, width=4)
    x, y = end
    d.polygon([(x, y), (x - 18, y - 10), (x - 18, y + 10)], fill=ACCENT)


def table(d, rows, cols, top, row_h=70, size=28):
    for r, row in enumerate(rows):
        y0 = top + r * row_h
        fill = ACCENT if r == 0 else (LIGHT if r % 2 else BG)
        d.rectangle([cols[0], y0, cols[-1], y0 + row_h], fill=fill, outline="#9db5cc")
        for c, cell in enumerate(row):
            d.text((cols[c] + 20, y0 + row_h / 2), cell,
                   font=font(size, bold=r == 0), fill="white" if r == 0 else TEXT, anchor="lm")


# --- ml-basics (English) ---------------------------------------------------

def ml_01():
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
        box(d, (x0, 540, x0 + 300, 620), label, fill=LIGHT)
        d.line([(640, 440), (x0 + 150, 540)], fill=ACCENT, width=3)
    return img


def ml_02():
    img, d = new_slide("Supervised Learning", 2)
    bullets(d, [
        "Supervised learning uses labeled data for training: "
        "each input comes with the correct output.",
        "Two typical tasks:",
        "- Classification: predict a discrete category (e.g. spam / not spam).",
        "- Regression: predict a continuous value (e.g. house price).",
    ], top=150)
    return img


def ml_03():
    img, d = new_slide("Unsupervised Learning", 3)
    bullets(d, [
        "Unsupervised learning discovers patterns in unlabeled data.",
        "Two typical tasks:",
        "- Clustering: group similar data points (e.g. k-means).",
        "- Dimensionality reduction: compress features while keeping "
        "the structure of the data (e.g. PCA).",
    ], top=150)
    return img


def ml_04():
    img, d = new_slide("Reinforcement Learning & Comparison", 4)
    y = bullets(d, [
        "In reinforcement learning, an agent learns by interacting "
        "with an environment and receiving rewards.",
    ], top=150)
    table(d, [
        ("Paradigm", "Training data", "Feedback"),
        ("Supervised", "Labeled", "Correct answers"),
        ("Unsupervised", "Unlabeled", "None"),
        ("Reinforcement", "Interaction", "Rewards"),
    ], cols=[MARGIN, MARGIN + 380, MARGIN + 760, W - MARGIN], top=y + 20)
    return img


# --- model-eval (Chinese) --------------------------------------------------

def me_01():
    img, d = new_slide("模型评估与泛化：课程概览", 1)
    bullets(d, [
        "模型评估的目标：衡量模型在未见过的数据上的表现（泛化能力）。",
        "本讲内容：",
        "- 数据集划分",
        "- 过拟合与欠拟合、偏差-方差权衡",
        "- 正则化",
        "- 交叉验证",
        "- 分类评价指标",
    ], top=150)
    return img


def me_02():
    img, d = new_slide("数据集划分", 2)
    bullets(d, [
        "训练集（Training set）：用于拟合模型参数。",
        "验证集（Validation set）：用于选择超参数和模型。",
        "测试集（Test set）：仅在最后用于评估泛化性能，不可用于调参。",
        "本课程推荐的划分比例：训练集 : 验证集 : 测试集 = 7 : 2 : 1。",
    ], top=150)
    return img


def me_03():
    img, d = new_slide("过拟合与欠拟合", 3)
    bullets(d, [
        "过拟合（Overfitting）：训练误差低，但测试误差高。",
        "欠拟合（Underfitting）：训练误差和测试误差都较高。",
        "过拟合通常由模型过于复杂或训练数据过少导致。",
    ], top=150)
    return img


def me_04():
    img, d = new_slide("偏差-方差权衡", 4)
    # Diagram: each failure mode points to its source of error.
    for y, left, right in ((170, "欠拟合", "高偏差（模型过于简单）"),
                           (330, "过拟合", "高方差（对训练数据过于敏感）")):
        box(d, (130, y, 430, y + 100), left, size=32)
        box(d, (620, y, 1150, y + 100), right, fill=LIGHT)
        arrow(d, (430, y + 50), (615, y + 50))
    bullets(d, ["模型复杂度增加时，偏差降低、方差升高；需要在两者之间取得平衡。"], top=530)
    return img


def me_05():
    img, d = new_slide("正则化（Regularization）", 5)
    bullets(d, [
        "在损失函数中加入惩罚项，用于降低过拟合。",
        "- L1 正则化：惩罚权重绝对值之和，倾向于产生稀疏解（部分权重为 0）。",
        "- L2 正则化：惩罚权重平方和，使权重整体变小，但一般不产生稀疏解。",
    ], top=150)
    return img


def me_06():
    img, d = new_slide("交叉验证（Cross-validation）", 6)
    bullets(d, [
        "k 折交叉验证：将训练数据分成 k 份，轮流用其中 1 份做验证、"
        "其余 k−1 份做训练，最后取 k 次结果的平均。",
        "常用 k = 5 或 10。",
        "适用于数据量较少、单独划分验证集代价较高的情况。",
    ], top=150)
    return img


def me_07():
    img, d = new_slide("分类评价指标", 7)
    d.text((MARGIN, 155), "TP：真正例　FP：假正例　FN：假反例　TN：真反例",
           font=font(24), fill=MUTED, anchor="lm")
    table(d, [
        ("指标", "公式", "含义"),
        ("准确率 (Accuracy)", "(TP+TN) / 全部样本", "预测正确的比例"),
        ("精确率 (Precision)", "TP / (TP+FP)", "预测为正的样本中，真正为正的比例"),
        ("召回率 (Recall)", "TP / (TP+FN)", "真正为正的样本中，被预测为正的比例"),
        ("F1 分数", "2PR / (P+R)", "精确率与召回率的调和平均"),
    ], cols=[MARGIN, MARGIN + 290, MARGIN + 560, W - MARGIN], top=200, row_h=80, size=24)
    return img


def me_08():
    img, d = new_slide("小结与注意事项", 8)
    bullets(d, [
        "在类别不平衡的数据上，准确率可能具有误导性，应结合精确率和召回率一起判断。",
        "测试集只能在最终评估时使用一次。",
        "课后作业：在 Iris 数据集上比较 L1 与 L2 正则化的效果。",
    ], top=150)
    return img


DECKS = {
    "ml-basics": (LATIN_FONTS, [ml_01, ml_02, ml_03, ml_04]),
    "model-eval": (CJK_FONTS, [me_01, me_02, me_03, me_04, me_05, me_06, me_07, me_08]),
}


def main(argv):
    global fonts
    names = list(DECKS) if not argv or argv[0] == "all" else argv
    for name in names:
        fonts, slides = DECKS[name]
        out_dir = FIXTURES / name / "images"
        out_dir.mkdir(parents=True, exist_ok=True)
        for n, make in enumerate(slides, start=1):
            path = out_dir / f"slide-{n:02d}.png"
            make().save(path)
            print(path)


if __name__ == "__main__":
    main(sys.argv[1:])
