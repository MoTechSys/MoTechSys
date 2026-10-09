"""Builds the live cards from real GitHub data. Runs daily in GitHub Actions.

Outputs (dark + light):
  assets/live-stats-*.svg   languages · contributions · repos/stars · streak
  assets/live-grid-*.svg    the real contribution grid with a verification scan

Data:
  - GraphQL API when GH_TOKEN is set (exact contribution calendar, both accounts)
  - fallback: REST API + public contributions page (no token needed)
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.request

from svgtext import text_path as T
from svgtext import width as W
from theme import LANG_COLORS, THEMES

USERS = [u.strip() for u in os.environ.get("PROFILE_USERS", "MoTechSys,moain2026").split(",") if u.strip()]
PRIMARY = USERS[0]
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def _get(url, data=None):
    headers = {"User-Agent": "profile-readme-builder", "Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    return json.loads(_get("https://api.github.com/graphql", body))


Q = """query($login:String!){ user(login:$login){
  contributionsCollection{ contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } }
  repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){ totalCount nodes{ stargazerCount
    languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } } } } }"""


def fetch_user(login):
    days, langs, repos, stars = {}, {}, 0, 0
    if TOKEN:
        try:
            d = gql(Q, {"login": login})["data"]["user"]
            for wk in d["contributionsCollection"]["contributionCalendar"]["weeks"]:
                for day in wk["contributionDays"]:
                    days[day["date"]] = day["contributionCount"]
            repos = d["repositories"]["totalCount"]
            for n in d["repositories"]["nodes"]:
                stars += n["stargazerCount"]
                for e in n["languages"]["edges"]:
                    langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
            return days, langs, repos, stars
        except Exception as exc:  # fall through to public endpoints
            print(f"  graphql failed for {login}: {exc}")
    # public fallback
    html = _get(f"https://github.com/users/{login}/contributions")
    ids = dict(re.findall(r'data-date="([\d-]+)" id="([^"]+)"', html))
    tips = dict(re.findall(r'for="([^"]+)"[^>]*>(\d+|No) contribution', html))
    for date, cid in ids.items():
        v = tips.get(cid, "No")
        days[date] = 0 if v == "No" else int(v)
    page = 1
    while True:
        arr = json.loads(_get(f"https://api.github.com/users/{login}/repos?per_page=100&page={page}"))
        if not arr:
            break
        for r in arr:
            if r.get("fork"):
                continue
            repos += 1
            stars += r.get("stargazers_count", 0)
            try:
                for k, v in json.loads(_get(r["languages_url"])).items():
                    langs[k] = langs.get(k, 0) + v
            except Exception:
                if r.get("language"):
                    langs[r["language"]] = langs.get(r["language"], 0) + 1
        page += 1
    return days, langs, repos, stars


def collect():
    days, langs, repos, stars = {}, {}, 0, 0
    for u in USERS:
        try:
            d, l, r, s = fetch_user(u)
        except Exception as exc:
            print(f"  skip {u}: {exc}")
            continue
        for k, v in d.items():
            days[k] = days.get(k, 0) + v
        for k, v in l.items():
            langs[k] = langs.get(k, 0) + v
        repos += r
        stars += s
    return days, langs, repos, stars


def streaks(days):
    today = dt.date.today()
    cur = 0
    d = today
    if days.get(d.isoformat(), 0) == 0:
        d -= dt.timedelta(days=1)  # today not over yet
    while days.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    best = run = 0
    for k in sorted(days):
        run = run + 1 if days[k] > 0 else 0
        best = max(best, run)
    return cur, best


def svg(w, h, body, title):
    title = title.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{title}"><title>{title}</title><style>{REDUCED}</style>{body}</svg>')


def card(c, x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>'


def stats_svg(c, data):
    days, langs, repos, stars, cur, best, total = data
    w, h = 900, 168
    b = []
    cw = (w - 24) / 3
    # ── languages
    x0 = 0
    b.append(card(c, x0 + .5, .5, cw - 1, h - 1))
    b.append(T("LANGUAGES", x0 + 20, 32, family="mono", weight=700, size=11, tracking=1.6, fill=c["mute"]))
    tot = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    rest = tot - sum(v for _, v in top)
    segs = top + ([("Other", rest)] if rest / tot > .01 else [])
    bx, bw = x0 + 20, cw - 40
    b.append(f'<clipPath id="lb"><rect x="{bx}" y="48" width="{bw}" height="8" rx="4"/></clipPath><g clip-path="url(#lb)">')
    xx = bx
    for i, (k, v) in enumerate(segs):
        sw = bw * v / tot
        col = LANG_COLORS.get(k, c["gold"] if k == "Other" else c["mute"])
        b.append(f'<rect x="{xx:.1f}" y="48" width="0" height="8" fill="{col}"><animate attributeName="width" from="0" to="{sw + .5:.1f}" begin="{.15 * i:.2f}s" dur=".8s" fill="freeze"/></rect>')
        xx += sw
    b.append('</g>')
    # legend 2 columns
    for i, (k, v) in enumerate(segs[:6]):
        lx = bx + (i % 2) * (bw / 2)
        ly = 82 + (i // 2) * 24
        col = LANG_COLORS.get(k, c["gold"] if k == "Other" else c["mute"])
        b.append(f'<rect x="{lx}" y="{ly - 9}" width="8" height="8" rx="2" fill="{col}"/>')
        b.append(T(k, lx + 14, ly, family="mono", size=11, fill=c["soft"]))
        b.append(T(f"{100 * v / tot:.0f}%", lx + bw / 2 - 12, ly, family="mono", size=11, fill=c["dim"], anchor="end"))

    # ── contributions
    x1 = cw + 12
    b.append(card(c, x1 + .5, .5, cw - 1, h - 1))
    b.append(T("CONTRIBUTIONS · 12 MO", x1 + 20, 32, family="mono", weight=700, size=11, tracking=1.6, fill=c["mute"]))
    b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin=".3s" dur=".8s" fill="freeze"/>'
             f'{T(f"{total:,}", x1 + 20, 92, family="mono", weight=700, size=42, fill=c["gold"])}</g>')
    # sparkline of last 26 weeks
    keys = sorted(days)[-182:]
    weeks = [sum(days[k] for k in keys[i:i + 7]) for i in range(0, len(keys), 7)]
    mx = max(weeks) or 1
    sx, sy, sw_, sh = x1 + 20, 108, cw - 40, 28
    pts = [(sx + i * sw_ / max(len(weeks) - 1, 1), sy + sh - sh * v / mx) for i, v in enumerate(weeks)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    L = sum(((pts[i][0] - pts[i - 1][0]) ** 2 + (pts[i][1] - pts[i - 1][1]) ** 2) ** .5 for i in range(1, len(pts))) + 1
    b.append(f'<path d="{d} L{sx + sw_:.1f} {sy + sh} L{sx} {sy + sh}Z" fill="{c["mint"]}" opacity=".08"/>')
    b.append(f'<path d="{d}" fill="none" stroke="{c["mint"]}" stroke-width="1.6" stroke-linejoin="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}">'
             f'<animate attributeName="stroke-dashoffset" from="{L:.0f}" to="0" begin=".4s" dur="1.8s" fill="freeze"/></path>')
    b.append(T("last 26 weeks", x1 + 20, 156, family="mono", size=10, fill=c["dim"]))
    b.append(T(f"{'+'.join(USERS)}", x1 + cw - 20, 156, family="mono", size=10, fill=c["dim"], anchor="end"))

    # ── repos / streak
    x2 = 2 * (cw + 12)
    b.append(card(c, x2 + .5, .5, cw - 1, h - 1))
    b.append(T("SHIPPING", x2 + 20, 32, family="mono", weight=700, size=11, tracking=1.6, fill=c["mute"]))
    active = sum(1 for k in sorted(days)[-365:] if days[k] > 0)
    rows = [("public repos", f"{repos}"), ("active days", f"{active}"), ("longest streak", f"{best} d"), ("languages", f"{len(langs)}")]
    if cur >= 3:
        rows[2] = ("current streak", f"{cur} d")
    for i, (k, v) in enumerate(rows):
        y = 62 + i * 24
        b.append(T(k, x2 + 20, y, family="mono", size=12, fill=c["soft"]))
        b.append(f'<line x1="{x2 + 20 + W(k, "mono", 400, 12) + 8:.1f}" y1="{y - 4}" x2="{x2 + cw - 28 - W(v, "mono", 700, 13):.1f}" y2="{y - 4}" stroke="{c["line"]}" stroke-dasharray="2 4"/>')
        b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{.3 + .15 * i:.2f}s" dur=".6s" fill="freeze"/>'
                 f'{T(v, x2 + cw - 20, y, family="mono", weight=700, size=13, fill=c["mint"] if i in (1, 2) else c["text"], anchor="end")}</g>')
    upd = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    b.append(T(f"updated {upd}", x2 + 20, 156, family="mono", size=10, fill=c["dim"]))
    return svg(w, h, "".join(b), f"Live stats: {total} contributions, {repos} repos, longest streak {best} days")


def grid_svg(c, days):
    w = 900
    keys = sorted(days)[-371:]
    # align to weeks starting Sunday
    first = dt.date.fromisoformat(keys[0])
    pad = (first.weekday() + 1) % 7
    cells = [None] * pad + [(k, days[k]) for k in keys]
    nweeks = (len(cells) + 6) // 7
    gap = 3
    size = (w - 40 - gap * (nweeks - 1)) / nweeks
    h = int(40 + 7 * size + 6 * gap + 34)
    vals = sorted(v for _, v in [x for x in cells if x] if v > 0)

    def level(v):
        if v == 0:
            return 0
        if not vals:
            return 1
        q = [vals[int(len(vals) * f)] for f in (.25, .5, .75)]
        return 1 + sum(v > t for t in q)

    b = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>']
    b.append(T("CONTRIBUTION GRID", 20, 26, family="mono", weight=700, size=11, tracking=1.6, fill=c["mute"]))
    dur = 10
    b.append(f'<defs><linearGradient id="bm" x1="0" x2="1"><stop offset="0" stop-color="{c["gold"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{c["gold"]}" stop-opacity=".55"/></linearGradient></defs>')
    gx0, gy0 = 20, 40
    for i, cell in enumerate(cells):
        if cell is None:
            continue
        col, row = divmod(i, 7)
        x = gx0 + col * (size + gap)
        y = gy0 + row * (size + gap)
        lv = level(cell[1])
        fill = c["cells"][lv]
        if lv > 0:
            # the scan "verifies" each active cell as it passes: brief gold flash
            t = (x - gx0) / (w - 40) * .8 + .05
            b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" rx="2" fill="{fill}">'
                     f'<animate attributeName="fill" values="{fill};{fill};{c["gold"]};{fill};{fill}" keyTimes="0;{t:.3f};{t + .02:.3f};{t + .07:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
        else:
            b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" rx="2" fill="{fill}"/>')
    gh = 7 * size + 6 * gap
    b.append(f'<g><rect x="0" y="{gy0 - 4}" width="70" height="{gh + 8:.1f}" fill="url(#bm)" opacity=".5"/>'
             f'<rect x="68" y="{gy0 - 6}" width="2.5" height="{gh + 12:.1f}" fill="{c["gold"]}"/>'
             f'<animateTransform attributeName="transform" type="translate" values="{gx0 - 72};{gx0 - 72};{w - 70};{w - 70}" keyTimes="0;.05;.85;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.83;.86;1" dur="{dur}s" repeatCount="indefinite"/></g>')
    # legend
    ly = h - 14
    lx = w - 20 - 5 * 14 - 34
    b.append(T("less", lx - 8, ly, family="mono", size=10, fill=c["dim"], anchor="end"))
    for i in range(5):
        b.append(f'<rect x="{lx + i * 14}" y="{ly - 9}" width="10" height="10" rx="2" fill="{c["cells"][i]}"/>')
    b.append(T("more", lx + 5 * 14 + 4, ly, family="mono", size=10, fill=c["dim"]))
    first_m = dt.date.fromisoformat(keys[0]).strftime("%b %Y")
    last_m = dt.date.fromisoformat(keys[-1]).strftime("%b %Y")
    b.append(T(f"{first_m} — {last_m}", 20, ly, family="mono", size=10, fill=c["dim"]))
    return svg(w, h, "".join(b), "Contribution grid of the last 12 months")


def main():
    os.makedirs(OUT, exist_ok=True)
    days, langs, repos, stars = collect()
    if not days:
        raise SystemExit("no contribution data")
    cur, best = streaks(days)
    keys = sorted(days)[-365:]
    total = sum(days[k] for k in keys)
    data = (days, langs, repos, stars, cur, best, total)
    print(f"  users={USERS} total={total} repos={repos} stars={stars} streak={cur}/{best} langs={len(langs)}")
    for theme, c in THEMES.items():
        for name, content in (("live-stats", stats_svg(c, data)), ("live-grid", grid_svg(c, days))):
            p = os.path.join(OUT, f"{name}-{theme}.svg")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(content)
            print(f"  {name}-{theme}.svg  {len(content) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
