"""最新リリースのバージョンと公開日を示すバッジ (SVG) を生成する。

使い方:
    python scripts/make_release_badge.py --project yaya|satori|kawari \
        --version Tc607-2 --published-at 2026-10-19T08:13:51Z --out badge.svg

- 色は site/assets/tokens.css のライトモードの値 (--color-<project>-main / -sub) を読む。
- 明暗どちらのページに置いても読めるよう、配色は固定 (主色の地に白文字、左端に副色の帯、
  暗い背景でも輪郭が残るよう白の細い内枠)。
- 公開日は日本時間 (JST) の YYYY-MM-DD で書く。
- 各リポジトリの .github/workflows/release-badge.yml が、このスクリプトを ukatech.github.io から取得して使う。
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from xml.sax.saxutils import escape

HEIGHT = 36  # .button の min-height (2.25rem) に合わせる
BAR = 4  # 左端の副色の帯
PAD = 14
VERSION_SIZE = 16
DATE_SIZE = 10
FONT = "'Segoe UI','Helvetica Neue',Arial,'Yu Gothic UI',sans-serif"

JST = timezone(timedelta(hours=9))


def read_colors(tokens_path, project):
    """tokens.css 先頭 (ライトモード) の --color-<project>-main / -sub を返す。"""
    with open(tokens_path, encoding="utf-8") as f:
        css = f.read()
    colors = []
    for role in ("main", "sub"):
        m = re.search(rf"--color-{re.escape(project)}-{role}:\s*(#[0-9a-fA-F]{{6}})", css)
        if not m:
            sys.exit(f"{tokens_path} に --color-{project}-{role} が見つかりません")
        colors.append(m.group(1))
    return colors


def format_date(published_at):
    t = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    return t.astimezone(JST).strftime("%Y-%m-%d")


def build_svg(version, date, main, sub):
    # フォントを測れないので文字数から幅を見積もり、中央寄せで余裕を持たせる
    text_w = max(len(version) * VERSION_SIZE * 0.64, len(date) * DATE_SIZE * 0.62)
    width = int(round(max(text_w + PAD * 2 + BAR, 76)))
    cx = BAR + (width - BAR) / 2
    label = f"最新リリース {version} ({date})"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{HEIGHT}" viewBox="0 0 {width} {HEIGHT}" role="img" aria-label="{escape(label)}">
  <title>{escape(label)}</title>
  <clipPath id="c"><rect width="{width}" height="{HEIGHT}" rx="4"/></clipPath>
  <g clip-path="url(#c)">
    <rect width="{width}" height="{HEIGHT}" fill="{main}"/>
    <rect width="{BAR}" height="{HEIGHT}" fill="{sub}"/>
  </g>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{HEIGHT - 1}" rx="3.5" fill="none" stroke="#ffffff" stroke-opacity="0.4"/>
  <g fill="#ffffff" text-anchor="middle" font-family="{FONT}">
    <text x="{cx:g}" y="17" font-size="{VERSION_SIZE}" font-weight="700">{escape(version)}</text>
    <text x="{cx:g}" y="30" font-size="{DATE_SIZE}" fill-opacity="0.85">{escape(date)}</text>
  </g>
</svg>
"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True, choices=["yaya", "satori", "kawari"])
    ap.add_argument("--version", required=True)
    ap.add_argument("--published-at", required=True, help="ISO 8601 (例: 2026-10-19T08:13:51Z)")
    ap.add_argument("--tokens", default=os.path.join(here, "..", "site", "assets", "tokens.css"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    main_color, sub_color = read_colors(args.tokens, args.project)
    svg = build_svg(args.version, format_date(args.published_at), main_color, sub_color)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
