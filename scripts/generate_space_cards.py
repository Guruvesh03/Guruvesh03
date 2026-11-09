#!/usr/bin/env python3
"""Generate solar-system themed profile cards from live GitHub data.

Writes three self-hosted SVGs (no third-party servers involved):
  assets/mission-control.svg   stats + streaks
  assets/top-languages.svg     languages as planets, sized by real code share
  assets/top-repos.svg         top repositories as mission cards

Usage:
  python scripts/generate_space_cards.py              # live data (uses GITHUB_TOKEN if set)
  python scripts/generate_space_cards.py --placeholder  # write "data incoming" cards
"""
import argparse
import datetime as dt
import html
import json
import math
import os
import random
import textwrap
import urllib.request

USER = os.environ.get("GH_USER", "Guruvesh03")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HIDE_LANGS = set()  # e.g. {"Jupyter Notebook"} to keep a language off the chart

LANG_COLORS = {
    "Python": "#FFD43B", "Java": "#F89820", "JavaScript": "#F7DF1E",
    "TypeScript": "#3B82F6", "HTML": "#F97316", "CSS": "#A78BFA",
    "Jupyter Notebook": "#FB923C", "C++": "#F472B6", "C": "#9CA3AF",
    "Shell": "#86EFAC", "SCSS": "#F472B6", "Go": "#22D3EE", "Rust": "#FDBA74",
    "Kotlin": "#C084FC", "PHP": "#818CF8", "Dockerfile": "#38BDF8",
}
DEFAULT_COLOR = "#93C5FD"
FONT = "'Segoe UI', Arial, sans-serif"


# ---------- data ----------
def gh(url, data=None):
    headers = {"User-Agent": "space-cards", "Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def contributions():
    """Return (total, current_streak, longest_streak) or None without a token."""
    if not TOKEN:
        return None
    query = ('query { user(login: "%s") { contributionsCollection { contributionCalendar '
             '{ totalContributions weeks { contributionDays { date contributionCount } } } } } }' % USER)
    try:
        res = gh("https://api.github.com/graphql", json.dumps({"query": query}).encode())
        cal = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except Exception as exc:  # noqa: BLE001
        print("GraphQL failed:", exc)
        return None
    days = sorted((d["date"], d["contributionCount"])
                  for w in cal["weeks"] for d in w["contributionDays"])
    today = dt.datetime.utcnow().date().isoformat()
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    current = 0
    for date, c in reversed(days):
        if c > 0:
            current += 1
        elif date == today:
            continue  # today not committed yet: do not break the streak
        else:
            break
    return cal["totalContributions"], current, longest


def collect():
    user = gh(f"https://api.github.com/users/{USER}")
    repos, page = [], 1
    while True:
        batch = gh(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"] and r["name"].lower() != USER.lower()]
    langs = {}
    for r in own:
        for k, v in gh(r["languages_url"]).items():
            if k not in HIDE_LANGS:
                langs[k] = langs.get(k, 0) + v
    own.sort(key=lambda r: (r["stargazers_count"], r["pushed_at"]), reverse=True)
    return {
        "followers": user["followers"],
        "public_repos": user["public_repos"],
        "stars": sum(r["stargazers_count"] for r in own),
        "contrib": contributions(),
        "langs": sorted(langs.items(), key=lambda kv: kv[1], reverse=True),
        "repos": own,
        "updated": dt.datetime.utcnow().strftime("%d %b %Y"),
    }


def demo_data():
    return {
        "followers": 12, "public_repos": 18, "stars": 7, "contrib": (342, 5, 21),
        "langs": [("Python", 5200), ("Java", 4100), ("JavaScript", 2300), ("HTML", 1500), ("CSS", 900), ("Jupyter Notebook", 600)],
        "repos": [
            {"name": "DSA-in-Java", "description": "Data structures and algorithms in Java with explanations next to every solution.", "language": "Java", "stargazers_count": 3, "forks_count": 1},
            {"name": "Crop-Predictor", "description": "Crop recommendation app built with Streamlit.", "language": "Python", "stargazers_count": 2, "forks_count": 0},
            {"name": "Summary-Generator", "description": None, "language": "Python", "stargazers_count": 1, "forks_count": 0},
            {"name": "Scholar-Mentor", "description": "Student mentoring platform.", "language": "JavaScript", "stargazers_count": 1, "forks_count": 0},
        ],
        "updated": "demo",
    }


# ---------- svg helpers ----------
def esc(s):
    return html.escape(str(s), quote=True)


def mix(color, target, amount):
    c = color.lstrip("#")
    rgb = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(x + (target - x) * amount) for x in rgb)


def planet_grad(gid, color):
    return (f'<radialGradient id="{gid}" cx="35%" cy="30%" r="75%">'
            f'<stop offset="0" stop-color="{mix(color, 255, .5)}"/>'
            f'<stop offset="0.5" stop-color="{color}"/>'
            f'<stop offset="1" stop-color="{mix(color, 0, .55)}"/></radialGradient>')


def frame(w, h, defs, body, seed=3):
    rnd = random.Random(seed)
    stars = []
    for _ in range(max(25, w * h // 6000)):
        x, y = rnd.randint(8, w - 8), rnd.randint(8, h - 8)
        r = rnd.choice([0.6, 0.8, 1, 1.2])
        stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="0.6"><animate attributeName="opacity" '
                     f'values="0.15;0.9;0.15" dur="{rnd.uniform(2, 5):.1f}s" begin="-{rnd.uniform(0, 4):.1f}s" repeatCount="indefinite"/></circle>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">'
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#020617"/>'
            f'<stop offset="0.6" stop-color="#0F172A"/><stop offset="1" stop-color="#172554"/></linearGradient>{defs}</defs>'
            f'<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>' + "".join(stars) + body + "</svg>")


def title(text, sub):
    return (f'<text x="32" y="44" font-size="22" font-weight="700" fill="#E2E8F0">{esc(text)}</text>'
            f'<text x="32" y="64" font-size="12" fill="#93C5FD">{esc(sub)}</text>')


# ---------- cards ----------
def mission_control(d):
    w, h = 960, 320
    contrib = d["contrib"]
    tiles = [
        (f"{contrib[0]:,}" if contrib else "n/a", "Contributions, last year", "#FBBF24"),
        (f"{contrib[1]} days" if contrib else "n/a", "Current streak", "#F97316"),
        (f"{contrib[2]} days" if contrib else "n/a", "Longest streak", "#F472B6"),
        (str(d["public_repos"]), "Public repositories", "#61DAFB"),
        (str(d["stars"]), "Stars earned", "#FFD43B"),
        (str(d["followers"]), "Followers", "#A78BFA"),
    ]
    defs, body = "", title("Mission Control", f"Live from GitHub  |  updated {d['updated']}")
    tw, th, gap, x0, y0 = 290, 104, 15, 30, 84
    for i, (val, label, color) in enumerate(tiles):
        x = x0 + (i % 3) * (tw + gap)
        y = y0 + (i // 3) * (th + gap)
        cx, cy = x + 46, y + th / 2
        defs += planet_grad(f"t{i}", color)
        dur = 5 + i
        body += (f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="#0F172A" fill-opacity="0.7" stroke="#3B82F6" stroke-opacity="0.35"/>'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="12" fill="none" stroke="#93C5FD" stroke-opacity="0.3" transform="rotate(-20 {cx} {cy})"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="19" fill="url(#t{i})"/>'
                 f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<circle cx="{cx + 30}" cy="{cy}" r="3.5" fill="#fff"/></g>'
                 f'<text x="{x + 92}" y="{y + 54}" font-size="30" font-weight="700" fill="#F1F5F9">{esc(val)}</text>'
                 f'<text x="{x + 92}" y="{y + 78}" font-size="13" fill="#94A3B8">{esc(label)}</text>')
    return frame(w, h, defs, body, seed=11)


def top_languages(d):
    w, h = 960, 340
    langs = d["langs"][:6]
    body = title("Top Languages", "Planet size = share of code across my public repositories")
    if not langs:
        return placeholder("Top Languages", w, h, "No language data yet")
    total = sum(v for _, v in langs)
    big = langs[0][1]
    defs, n = "", len(langs)
    for i, (name, size) in enumerate(langs):
        color = LANG_COLORS.get(name, DEFAULT_COLOR)
        defs += planet_grad(f"l{i}", color)
        cx = w / (n + 1) * (i + 1)
        r = 14 + 34 * math.sqrt(size / big)
        cy = 180
        body += f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="{4 + i * 0.7:.1f}s" begin="-{i}s" repeatCount="indefinite"/>'
        rx, ry = r * 1.55, r * 0.34
        if i == 0:
            body += f'<g transform="rotate(-18 {cx:.1f} {cy})"><ellipse cx="{cx:.1f}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{color}" stroke-opacity="0.45" stroke-width="3"/></g>'
        body += f'<circle cx="{cx:.1f}" cy="{cy}" r="{r:.1f}" fill="url(#l{i})"/>'
        if i == 0:
            body += (f'<g transform="rotate(-18 {cx:.1f} {cy})"><path d="M {cx - rx:.1f} {cy} A {rx:.1f} {ry:.1f} 0 0 0 {cx + rx:.1f} {cy}" '
                     f'fill="none" stroke="{color}" stroke-opacity="0.9" stroke-width="3"/></g>')
        body += '</g>'
        body += (f'<text x="{cx:.1f}" y="285" text-anchor="middle" font-size="15" font-weight="700" fill="#F1F5F9">{esc(name)}</text>'
                 f'<text x="{cx:.1f}" y="305" text-anchor="middle" font-size="13" fill="#94A3B8">{size / total * 100:.1f}%</text>')
    return frame(w, h, defs, body, seed=5)


def wrap(text, width=56, lines=2):
    parts = textwrap.wrap(text, width)
    if len(parts) > lines:
        parts = parts[:lines]
        parts[-1] = parts[-1][: width - 3].rstrip() + "..."
    return parts


def top_repos(d):
    repos = d["repos"][:6]
    if not repos:
        return placeholder("Top Repositories", 960, 200, "No public repositories yet")
    cw, ch, gx, gy, x0, y0 = 435, 108, 30, 14, 30, 82
    rows = math.ceil(len(repos) / 2)
    w, h = 960, y0 + rows * (ch + gy) + 14
    defs, body = "", title("Top Repositories", "Ranked by stars, then by latest push")
    for i, r in enumerate(repos):
        x = x0 + (i % 2) * (cw + gx)
        y = y0 + (i // 2) * (ch + gy)
        lang = r.get("language")
        color = LANG_COLORS.get(lang, DEFAULT_COLOR)
        defs += planet_grad(f"r{i}", color)
        name = r["name"] if len(r["name"]) <= 30 else r["name"][:27] + "..."
        desc = wrap(r.get("description") or "No description provided")
        body += (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="#0F172A" fill-opacity="0.7" stroke="#3B82F6" stroke-opacity="0.35"/>'
                 f'<circle cx="{x + 38}" cy="{y + 44}" r="20" fill="url(#r{i})"/>'
                 f'<text x="{x + 74}" y="{y + 32}" font-size="16" font-weight="700" fill="#E2E8F0">{esc(name)}</text>')
        for j, line in enumerate(desc):
            body += f'<text x="{x + 74}" y="{y + 54 + j * 16}" font-size="12" fill="#94A3B8">{esc(line)}</text>'
        sc, fc = r["stargazers_count"], r["forks_count"]
        meta = f'{sc} star{"" if sc == 1 else "s"}   {fc} fork{"" if fc == 1 else "s"}'
        body += (f'<circle cx="{x + 80}" cy="{y + 92}" r="5" fill="{color}"/>'
                 f'<text x="{x + 92}" y="{y + 96}" font-size="12" fill="#CBD5E1">{esc(lang or "n/a")}</text>'
                 f'<text x="{x + cw - 16}" y="{y + 96}" text-anchor="end" font-size="12" fill="#CBD5E1">{esc(meta)}</text>')
    return frame(w, h, defs, body, seed=9)


def placeholder(name, w=960, h=200, msg=None):
    msg = msg or 'Mission data incoming. Run the "Space cards" workflow once from the Actions tab.'
    body = (f'<text x="{w / 2}" y="{h / 2 - 6}" text-anchor="middle" font-size="22" font-weight="700" fill="#E2E8F0">{esc(name)}</text>'
            f'<text x="{w / 2}" y="{h / 2 + 20}" text-anchor="middle" font-size="13" fill="#93C5FD">{esc(msg)}</text>')
    return frame(w, h, "", body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--placeholder", action="store_true")
    ap.add_argument("--demo", action="store_true", help="sample data, for layout testing only")
    ap.add_argument("--out", default="assets")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.placeholder:
        files = {"mission-control.svg": placeholder("Mission Control", 960, 200),
                 "top-languages.svg": placeholder("Top Languages", 960, 200),
                 "top-repos.svg": placeholder("Top Repositories", 960, 200)}
    else:
        d = demo_data() if a.demo else collect()
        files = {"mission-control.svg": mission_control(d),
                 "top-languages.svg": top_languages(d),
                 "top-repos.svg": top_repos(d)}
    for name, svg in files.items():
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote", os.path.join(a.out, name))


if __name__ == "__main__":
    main()
