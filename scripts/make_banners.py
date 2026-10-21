"""リンク用バナー (200x40, 88x31) を生成する。

使い方: python scripts/make_banners.py [出力先ディレクトリ]
既定の出力先は site/assets/banner/。

- 2000 年代のバナー風に、暗色の地・ベベル枠・アンチエイリアスなしの文字で描く。
- 色は tokens.css のダークモードの値に合わせている。
- Tahoma を使うので Windows で実行する (要 Pillow)。生成した PNG はリポジトリに入れる。
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")

# tokens.css (ダークモード) に合わせた色
BG = (0x1d, 0x1f, 0x23)
SCANLINE = (0x24, 0x26, 0x2c)
INK = (0xe8, 0xe8, 0xe4)
MUTED = (0xa3, 0xa6, 0xae)
EDGE = (0x00, 0x00, 0x00)
LIGHT = (0x5e, 0x61, 0x6b)
SHADOW = (0x0d, 0x0e, 0x10)
YAYA = (0xd0, 0x73, 0x6b)
SATORI = (0x6f, 0xb0, 0x7f)
KAWARI = (0xe8, 0xe8, 0xe4)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def base(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # アンチエイリアスなし
    for y in range(2, h - 2, 2):
        d.line([(2, y), (w - 3, y)], fill=SCANLINE)
    # 外枠 + ベベル (左上が明るく、右下が暗い)
    d.rectangle([0, 0, w - 1, h - 1], outline=EDGE)
    d.line([(1, 1), (w - 2, 1)], fill=LIGHT)
    d.line([(1, 1), (1, h - 2)], fill=LIGHT)
    d.line([(1, h - 2), (w - 2, h - 2)], fill=SHADOW)
    d.line([(w - 2, 1), (w - 2, h - 2)], fill=SHADOW)
    return img, d


def balloon(d, x, y, w, h, dot):
    """ロゴマーク (吹き出し + 3 色の点)。favicon.svg をドットで描き直したもの。"""
    body = h - max(3, h // 5)
    d.rounded_rectangle([x, y, x + w - 1, y + body - 1], radius=max(2, w // 7), fill=BG, outline=INK)
    tx = x + w // 4
    d.polygon([(tx, y + body - 1), (tx + h // 4, y + body - 1), (tx, y + h - 1)], fill=INK)
    cy = y + (body - dot) // 2
    gap = (w - dot * 3) // 4
    for i, c in enumerate((YAYA, SATORI, KAWARI)):
        cx = x + gap + i * (dot + gap)
        d.rectangle([cx, cy, cx + dot - 1, cy + dot - 1], fill=c)


def stripe(d, x, y, w, h):
    """3 色の帯。"""
    seg = w // 3
    for i, c in enumerate((YAYA, SATORI, KAWARI)):
        x0 = x + i * seg
        x1 = x + w - 1 if i == 2 else x0 + seg - 1
        d.rectangle([x0, y, x1, y + h - 1], fill=c)


def banner_200x40():
    img, d = base(200, 40)
    balloon(d, 7, 7, 28, 27, 4)
    d.text((42, 6), "UKAGAKA TECH TEAM", font=font("tahomabd.ttf", 11), fill=INK)
    stripe(d, 42, 20, 150, 2)
    d.text((42, 24), "ukatech.shillest.net", font=font("tahoma.ttf", 10), fill=MUTED)
    return img


def banner_88x31():
    img, d = base(88, 31)
    balloon(d, 5, 6, 20, 20, 3)
    d.text((30, 3), "ukatech", font=font("tahomabd.ttf", 11), fill=INK)
    stripe(d, 30, 16, 48, 2)
    d.text((30, 18), "Tech Team", font=font("tahoma.ttf", 9), fill=MUTED)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join("site", "assets", "banner")
    os.makedirs(out, exist_ok=True)
    for name, img in (("ukatech_200x40.png", banner_200x40()), ("ukatech_88x31.png", banner_88x31())):
        img.save(os.path.join(out, name), optimize=True)
        print(os.path.join(out, name))


if __name__ == "__main__":
    main()
