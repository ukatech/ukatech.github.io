# Ukagaka Tech Team デザインシステム

ukatech.shillest.net で使う見た目の決まりごと。値の実体は `site/assets/tokens.css`、部品は `site/assets/style.css` にある。

## 方針

- シンプルに。装飾より情報の読みやすさを優先する。
- 色はプロジェクトの識別にだけ使い、それ以外は無彩色(生成りの背景と墨色の文字)で組む。
- ライト/ダークの両方に対応する(`prefers-color-scheme`)。
- ビルド不要の素の HTML/CSS。外部フォントや JS ライブラリに依存しない。

## 色

### ベース

| トークン | ライト | ダーク | 用途 |
|---|---|---|---|
| `--color-bg` | `#fafaf8` | `#151619` | ページ背景 |
| `--color-surface` | `#ffffff` | `#1d1f23` | カード |
| `--color-ink` | `#1c1d21` | `#e8e8e4` | 本文 |
| `--color-ink-muted` | `#5e616b` | `#a3a6ae` | 補足文 |
| `--color-line` | `#e3e3df` | `#2f3238` | 罫線・枠 |
| `--color-focus` | `#2f6fd6` | `#7aa7f0` | キーボードフォーカス |

### プロジェクト

ゴースト「SHIORIES」(整備班)のキャラクターの配色から取っている。主色(main)と副色(sub)の 2 色を組で使う。

| プロジェクト | main | sub | 由来 |
|---|---|---|---|
| YAYA | くすんだ赤 `#9b3f3a` | 黒 `#1c1d21` | 文 |
| 里々 | 緑 `#2f6b3f` | 黄土 `#b48e3e` | 里々 |
| 華和梨 | 黒 `#1c1d21` | 赤 `#c4262e` | 華和梨 |

- ダークモードでは黒が背景に沈むため、黒の役割を白寄り(`#e8e8e4`)に反転させる。他の色も明度を上げる。
- `-on` トークンは主色の上に載せる文字色(主ボタンの文字)。
- 部品側では `.project--yaya` などのクラスが `--accent-main` / `--accent-sub` / `--accent-on` を設定し、カードの中はこの 3 つだけを参照する。プロジェクトを増やすときはトークンを 3 つ足し、同じ形のクラスを 1 つ足す。

## 文字

- 本文: `--font-sans`(OS の日本語ゴシック)。外部フォントは読み込まない。
- 英字のタグラインや org 名: `--font-mono`。
- サイズは `--text-xs` から `--text-2xl` まで。見出し(`--text-2xl`)は画面幅に応じて `clamp()` で伸縮する。
- 行間は本文 1.8、見出し 1.35。

## 余白と形

- 余白は 4px グリッドの `--space-1`〜`--space-8`。
- 角丸はボタン `--radius-sm`(4px)、カード `--radius-md`(8px)。
- 影は使わず、1px の罫線(`--border`)で面を区切る。
- 本文幅は `--content-width`(60rem)。左右の余白 `--gutter` はスマートフォンで 16px、40rem 以上で 32px。

## 部品

| 部品 | クラス | 説明 |
|---|---|---|
| ヘッダー | `.site-header`, `.brand` | ロゴマークとチーム名 |
| ヒーロー | `.hero` | キッカー(`ukatech`)、見出し、リード文 |
| セクション | `.section`, `.section__title` | 下罫線付きの小見出しで区切る |
| プロジェクトカード | `.project-card` + `.project--*` | 上端に主色の太帯(6px)と副色の細線(2px)。名前、タグライン(主色)、説明、リンク |
| 小カード | `.project-card--compact` + `.project-grid--2` | SHIORI 以外のプロジェクト用。色帯とプロジェクト色を使わない無彩色のカードを 2 列で並べる |
| ボタン | `.button`, `.button--primary` | 主ボタンは主色で塗る。通常ボタンは枠線のみで、ホバー時に枠が主色になる |
| ボタン注記 | `.button__note` | ボタン内に小さく添える補足。チーム外のサイト(里々wiki など)であることを示すのに使う |
| org カード | `.org-card` | リンク全体がカード。org 名(等幅)と一言説明。`.org-card__title` を先頭に置くと、名前(太字)+ URL(等幅・小)+ 説明の形になる(提携欄) |
| メンバー一覧 | `.member-list`, `.member`, `.member-list__more` | 丸いアバター(24px)+ ID のピルを折り返して並べる。中身はデプロイ時に `scripts/build_members.py` が生成する |
| フッター | `.site-footer` | |

## ロゴマーク

`site/assets/favicon.svg`。伺かのバルーン(吹き出し)の中に、YAYA・里々・華和梨の主色の点を 3 つ並べたもの。favicon とヘッダーで共用し、SVG 内の `prefers-color-scheme` でダークモードの色に切り替わる。
