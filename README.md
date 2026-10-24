# ukatech.github.io

Ukagaka Tech Team のサイト <https://ukatech.shillest.net/> のソース。

- `site/` 以下が公開される。`main` への push と毎週月曜 09:00 (JST) に `.github/workflows/pages.yml` が GitHub Pages にデプロイする。
- `/kawari-docs/`、`/satori-docs/`、`/ukadoc-spec/`、`/ukadoc-ssp/`、`/jsstp-lib/`、`/metainfo-standard/` は各リポジトリのプロジェクトページで、このリポジトリには含まれない。同じパスのファイルを `site/` に置かないこと。
- 色・文字・部品の決まりは [DESIGN.md](DESIGN.md) を参照。

## 所属メンバー一覧

デプロイ時に `scripts/build_members.py` が ukatech と YAYA-shiori の公開メンバーを取得し、`site/index.html` の `<!-- members:start -->` から `<!-- members:end -->` までを置き換える(リポジトリ内のファイルは書き換えない)。

非公開メンバーの人数を出すには、org のメンバーを読めるトークンを Actions の secret に登録する。

- `ORG_MEMBERS_TOKEN`: 両 org に共通で使うトークン
- `ORG_MEMBERS_TOKEN_UKATECH` / `ORG_MEMBERS_TOKEN_YAYA_SHIORI`: org ごとのトークン(fine-grained PAT は 1 つの org しか対象にできないため)。あればこちらが優先される

どれも未登録なら公開メンバーだけを表示し、人数の行は出さない。

ローカルで確かめるとき:

```sh
cp -r site _site
ORG_MEMBERS_TOKEN=$(gh auth token) python scripts/build_members.py _site/index.html
```
