"""ukagaka-developer のソーシャルプレビュー画像 (1280x640 PNG) を生成する。

使い方:
    python scripts/make_social_preview.py --out social-preview.png

- 色は site/assets/tokens.css のライトモードの値を読む (地・罫線・文字と、YAYA・里々・華和梨の主色)。
- 吹き出しのロゴマークは site/assets/favicon.svg と同じ形。
- Consolas / Yu Gothic を使うので Windows で実行する。
- GitHub のリポジトリ設定 (Settings > Social preview) には手でアップロードする。
"""

import argparse
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
S = 2  # 作画の倍率。最後に縮めてアンチエイリアスにする
MARGIN = 88

FONTS = r"C:\Windows\Fonts"
MONO = os.path.join(FONTS, "consola.ttf")
MONO_BOLD = os.path.join(FONTS, "consolab.ttf")
GOTHIC_BOLD = os.path.join(FONTS, "YuGothB.ttc")
GOTHIC_MEDIUM = os.path.join(FONTS, "YuGothM.ttc")


def read_token(css, name):
    m = re.search(rf"--color-{re.escape(name)}:\s*(#[0-9a-fA-F]{{6}})", css)
    if not m:
        sys.exit(f"tokens.css に --color-{name} が見つかりません")
    return m.group(1)


def mix(a, b, t):
    """色 a から b へ t (0..1) だけ寄せる。"""
    ca = [int(a[i : i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i : i + 2], 16) for i in (1, 3, 5)]
    return tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))


def bubble_points(scale, ox, oy, step=24):
    """favicon.svg の吹き出し (viewBox 32) を、折れ線に直して返す。"""
    pts = []

    def arc(cx, cy, r, a0, a1):
        import math

        for i in range(step + 1):
            a = math.radians(a0 + (a1 - a0) * i / step)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    # M6 4 h20 a4 4 0 0 1 4 4 v11 a4 4 0 0 1 -4 4 H14 l-6 5 v-5 H6 a4 4 0 0 1 -4 -4 V8 a4 4 0 0 1 4 -4 z
    pts.append((6, 4))
    pts.append((26, 4))
    arc(26, 8, 4, -90, 0)
    pts.append((30, 19))
    arc(26, 19, 4, 0, 90)
    pts.append((14, 23))
    pts.append((8, 28))
    pts.append((8, 23))
    pts.append((6, 23))
    arc(6, 19, 4, 90, 180)
    pts.append((2, 8))
    arc(6, 8, 4, 180, 270)
    return [(ox + x * scale, oy + y * scale) for x, y in pts]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tokens", default=os.path.join(here, "..", "site", "assets", "tokens.css"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.tokens, encoding="utf-8") as f:
        css = f.read()
    bg = read_token(css, "bg")
    surface = read_token(css, "surface")
    ink = read_token(css, "ink")
    muted = read_token(css, "ink-muted")
    line = read_token(css, "line")
    yaya = read_token(css, "yaya-main")
    satori = read_token(css, "satori-main")
    kawari = read_token(css, "kawari-main")

    def px(v):
        return int(round(v * S))

    img = Image.new("RGB", (px(W), px(H)), bg)

    # ---- 薄いグリッド: 右ほど濃く、左 (文字の側) は消える ----
    grid = Image.new("RGB", img.size, bg)
    gd = ImageDraw.Draw(grid)
    step = 40
    for x in range(0, W + 1, step):
        gd.line([(px(x), 0), (px(x), px(H))], fill=line, width=S)
    for y in range(0, H + 1, step):
        gd.line([(0, px(y)), (px(W), px(y))], fill=line, width=S)
    mask = Image.linear_gradient("L").rotate(90).resize(img.size)  # 左 0 → 右 255
    mask = mask.point(lambda v: int(max(0, v - 70) * 255 / 185))
    img.paste(grid, (0, 0), mask)

    d = ImageDraw.Draw(img)

    def font(path, size, index=0):
        return ImageFont.truetype(path, px(size), index=index)

    # ---- 吹き出しのロゴマーク ----
    scale = 8.6
    bw, bh = 28 * scale, 26 * scale  # 輪郭の外接 (stroke 込みの余白を見る)
    ox = 1280 - MARGIN - 30 * scale  # 右端 (viewBox x=30) を余白に合わせる
    oy = (H - 28 * scale) / 2 - 18  # 縦の中心よりやや上
    pts = [(px(x), px(y)) for x, y in bubble_points(scale, ox, oy)]
    d.polygon(pts, fill=surface)
    d.line(pts + [pts[0], pts[1]], fill=ink, width=px(2.0 * scale), joint="curve")
    r = 2.25 * scale
    for cx, color in ((10, yaya), (16, satori), (22, kawari)):
        x, y = ox + cx * scale, oy + 13.5 * scale
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=color)

    # 吹き出しの四隅に、図面の位置合わせ印 (+)
    tick = 9
    pad = 34
    left, right = ox + 2 * scale - pad, ox + 30 * scale + pad
    top, bottom = oy + 4 * scale - pad, oy + 28 * scale + pad
    tick_color = mix(bg, muted, 0.55)
    for cx, cy in ((left, top), (right, top), (left, bottom), (right, bottom)):
        d.line([(px(cx - tick), px(cy)), (px(cx + tick), px(cy))], fill=tick_color, width=S)
        d.line([(px(cx), px(cy - tick)), (px(cx), px(cy + tick))], fill=tick_color, width=S)

    # ---- 左: 文字 ----
    d.text((px(MARGIN), px(100)), "Ukagaka Tech Team", font=font(MONO, 32), fill=muted, anchor="ls")

    # 3 色の短い罫 (カードの色帯に倣う)
    seg, gap, y0 = 64, 4, 130
    for i, color in enumerate((yaya, satori, kawari)):
        x = MARGIN + i * (seg + gap)
        d.rectangle([px(x), px(y0), px(x + seg), px(y0 + 7)], fill=color)

    d.text((px(MARGIN - 3), px(274)), "ukagaka-developer", font=font(MONO_BOLD, 84), fill=ink, anchor="ls")
    d.text((px(MARGIN), px(364)), "AI と作る伺かゴースト", font=font(GOTHIC_BOLD, 54), fill=ink, anchor="ls")
    d.text(
        (px(MARGIN), px(420)),
        "AI skill for Ukagaka ghost development",
        font=font(MONO, 32),
        fill=muted,
        anchor="ls",
    )

    # ---- 下段 ----
    d.text(
        (px(MARGIN), px(560)),
        "github.com/ukatech/ukagaka-developer",
        font=font(MONO, 28),
        fill=muted,
        anchor="ls",
    )

    # 隠し味: さくらスクリプトの断片 (右寄せ)。仮名は Consolas に無いので字体を切り替える
    faint = mix(bg, muted, 0.7)
    mono, gothic = font(MONO, 30), font(GOTHIC_MEDIUM, 30)

    def draw_mixed_right(x, y, text):
        runs = []
        for ch in text:
            f = mono if ord(ch) < 0x80 else gothic
            if runs and runs[-1][0] is f:
                runs[-1][1] += ch
            else:
                runs.append([f, ch])
        x -= sum(f.getlength(t) for f, t in runs)
        for f, t in runs:
            d.text((x, y), t, font=f, fill=faint, anchor="ls")
            x += f.getlength(t)

    draw_mixed_right(px(W - MARGIN), px(100), "\\0\\s[0]Hello.\\e")
    draw_mixed_right(px(W - MARGIN), px(560), "\\0\\s[5]えんい～\\e")

    img = img.resize((W, H), Image.LANCZOS)
    img.save(args.out, optimize=True)


if __name__ == "__main__":
    main()
