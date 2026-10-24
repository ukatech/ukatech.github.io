# Ukagaka Tech Team デザインシステム

ukatech.shillest.net で使う見た目の決まりごと。値の実体は `site/assets/tokens.css`、部品は `site/assets/style.css` にある。

yaya-shiori.github.io (YAYA-shiori/YAYA-shiori.github.io) も、公開中の `https://ukatech.shillest.net/assets/` の CSS とロゴを直接読み込んでいる。クラス名を変えたり消したりするときは、あちらのページも合わせて直すこと。

## 方針

- シンプルに。装飾より情報の読みやすさを優先する。
- 色はプロジェクトの識別にだけ使い、それ以外は無彩色(生成りの背景と墨色の文字)で組む。
- ライト/ダークの両方に対応する。既定は OS の設定に追従(`prefers-color-scheme`)し、ヘッダーの「自動 / ライト / ダーク」で固定もできる。固定は `<html data-theme="light|dark">` で表し、選択は `assets/theme.js` が localStorage(`ukatech-theme`)に保存する。`data-theme` を付けないページは OS 追従のまま。暗色の値は `tokens.css` の `@media` 内と `[data-theme="dark"]` の 2 か所に同じものを置くので、変えるときは両方を直す。
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

ドキュメント欄の 2 枚は、キャラクターではなく SHIORI と被らない色を割り当てている。

| ドキュメント | main | sub |
|---|---|---|
| UKADOC 仕様書 | 紺 `#1f4e8c` | 淡い金 `#bfa968` |
| SSP ヘルプ | 紫 `#6a4c93` | 灰 `#8a8d96` |

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
| ヒーロー | `.hero` | 見出し、リード文。縦の余白は詰めてある。`.hero__kicker`(見出し上の小さな文字)は、このページでは使わず、yaya-shiori.github.io が使う |
| セクション | `.section`, `.section__title` | 下罫線付きの小見出しで区切る |
| プロジェクトカード | `.project-card` + `.project--*` | 上端に主色の太帯(6px)と副色の細線(2px)。名前、タグライン(主色)、説明、リンク |
| 小カード | `.project-card--compact` + `.project-grid--2` | SHIORI 以外のプロジェクト用。2 列で並べる。基本は色帯なしの無彩色で、ドキュメント欄の 2 枚だけ `.project--ukadoc-spec` / `.project--ukadoc-ssp` と `.project-card__stripe` で色帯を付ける |
| ボタン | `.button`, `.button--primary`, `.button--emphasis` | 主ボタンは主色で塗る。通常ボタンは枠線のみで、ホバー時に枠が主色になる。`.button--emphasis` は太枠(`--emphasis-width`)で、色は `.project--*` の主色、無彩色のカードでは黒(ダークでは白寄り)。カードの先頭(左上)に置く。SHIORI は最新リリース(塗り)→ドキュメント(太枠)、色帯付きのドキュメント欄は仕様書/ヘルプ、それ以外は開発者向けでない入口(最新リリース・ドキュメント・サイトなど。GitHub リポジトリは通常ボタン)を太枠にする |
| ボタン注記 | `.button__note` | ボタン内に小さく添える補足。チーム外のサイト(里々wiki など)であることを示すのに使う |
| トピック案内 | `.topic-guide`, `.topic` | カード群の下に置く補足の枠。サービスごとの条件を 2 列で並べ、GitHub のトピック名は `.topic` のピル(等幅・リンク)で示す |
| org カード | `.org-card` | リンク全体がカード。org 名(等幅)と一言説明。`.org-card__title` を先頭に置くと、名前(太字)+ URL(等幅・小)+ 説明の形になる(提携欄) |
| メンバー一覧 | `.member-list`, `.member`, `.member-list__more` | 丸いアバター(24px)+ ID のピルを折り返して並べる。中身はデプロイ時に `scripts/build_members.py` が生成する |
| バナー | `.banner-list`, `.banner-item`, `.snippet` | バナー画像と、貼り付け用 HTML (クリックで全選択される) を縦に並べる |
| フッター | `.site-footer` | |

## リンク用バナー

`site/assets/banner/ukatech_200x40.png` と `ukatech_88x31.png`。2000 年代のバナー風に、ダークモードの色で描いている。

- 暗色の地に 2px おきの走査線、1px の黒枠と明暗のベベル。
- 左にロゴマーク(ドットで描き直したもの)、右にチーム名(Tahoma 太字・アンチエイリアスなし)、YAYA・里々・華和梨の 3 色の帯、URL。
- `scripts/make_banners.py` で生成する。Tahoma を使うので Windows で実行し、生成した PNG をコミットする。

## ロゴマーク

`site/assets/favicon.svg`。伺かのバルーン(吹き出し)の中に、YAYA・里々・華和梨の主色の点を 3 つ並べたもの。favicon.svg は SVG 内の `prefers-color-scheme` でダークモードの色に切り替わる(タブのアイコンは手動切替に追従できず、OS 設定のまま)。ヘッダーのロゴは同じ形のインライン SVG で、色をトークン(`--color-*-main` など)から取るので手動切替にも追従する。
