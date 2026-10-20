"""所属メンバー一覧を GitHub API から取得し、HTML のマーカー間に差し込む。

使い方: python scripts/build_members.py <index.html>

- 両 org の公開メンバーを合わせて(重複は除いて)アイコン + ID で並べる。
- org のメンバーを読めるトークンがあれば全メンバー数も取得し、
  非公開メンバーを「ほか n 人 (非公開)」として人数だけ書く。
- トークンは org ごとに ORG_MEMBERS_TOKEN_<ORG>(英大文字、- は _)、
  なければ ORG_MEMBERS_TOKEN、それもなければ GITHUB_TOKEN を使う。
  GITHUB_TOKEN では公開メンバーしか取れないので、非公開の人数は出ない。
"""

import html
import json
import os
import sys
import urllib.request

ORGS = ["ukatech", "YAYA-shiori"]
START = "<!-- members:start -->"
END = "<!-- members:end -->"


def token_for(org):
    key = "ORG_MEMBERS_TOKEN_" + org.upper().replace("-", "_")
    return os.environ.get(key) or os.environ.get("ORG_MEMBERS_TOKEN") or ""


def fetch_all(path, token):
    """ページングをたどって配列を全部返す。"""
    items = []
    page = 1
    while True:
        req = urllib.request.Request(
            f"https://api.github.com{path}?per_page=100&page={page}",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "ukatech-site-build",
            },
        )
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as res:
            chunk = json.load(res)
        items.extend(chunk)
        if len(chunk) < 100:
            return items
        page += 1


def collect():
    public = {}
    everyone = set()
    for org in ORGS:
        token = token_for(org) or os.environ.get("GITHUB_TOKEN", "")
        for m in fetch_all(f"/orgs/{org}/public_members", token):
            public[m["login"]] = m["avatar_url"]

        # 権限のないトークンでは /members も公開メンバーしか返さない(エラーにはならない)
        org_token = token_for(org)
        if org_token:
            members = fetch_all(f"/orgs/{org}/members", org_token)
            everyone.update(m["login"] for m in members)
            print(f"{org}: {len(members)} members", file=sys.stderr)
        else:
            print(f"{org}: no org token, public members only", file=sys.stderr)

    hidden = len(everyone - set(public))
    print(f"public {len(public)}, hidden {hidden}", file=sys.stderr)
    return public, hidden


def render(public, hidden):
    lines = ['<ul class="member-list">']
    for login in sorted(public, key=str.lower):
        avatar = public[login]
        avatar += ("&" if "?" in avatar else "?") + "s=64"
        lines.append(
            f'  <li><a class="member" href="https://github.com/{html.escape(login)}">'
            f'<img class="member__avatar" src="{html.escape(avatar)}" alt="" width="24" height="24" loading="lazy">'
            f"{html.escape(login)}</a></li>"
        )
    lines.append("</ul>")
    if hidden:
        lines.append(f'<p class="member-list__more">ほか {hidden} 人 (非公開)</p>')
    return "\n".join(lines)


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        text = f.read()
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    text = head + START + "\n" + render(*collect()) + "\n" + END + tail
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


if __name__ == "__main__":
    main()
