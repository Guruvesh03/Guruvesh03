#!/usr/bin/env python3
"""Builds the hand-designed (non data-driven) SVGs: terminal, neon circuit, marquee.
Edit the text blocks below, run `python scripts/build_visuals.py`, commit the assets.
"""
import os

OUT = "assets"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Courier New', monospace"
SANS = "'Segoe UI', Arial, sans-serif"
G, W, C, Y, M, DIM = "#4ADE80", "#E5E7EB", "#22D3EE", "#FBBF24", "#F472B6", "#6B7280"


def save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# =====================================================================
# STYLE 2: TERMINAL (typewriter effect, loops every cycle)
# =====================================================================
def terminal(name, title, lines, height, fs=15, lh=25, cw=9.0):
    """lines: list of (kind, [(text, color), ...]) where kind is 'cmd' or 'out'."""
    W_, TOP, X0 = 960, 44, 28
    BODY = "#0D1117"
    t, plan = 0.7, []
    for kind, segs in lines:
        n = sum(len(s) for s, _ in segs)
        dur = max(0.2, n * (0.05 if kind == "cmd" else 0.014))
        plan.append((t, dur, n))
        t += dur + (0.45 if kind == "cmd" else 0.12)
    T = round(t + 7, 2)  # hold the finished screen for 7s, then loop
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {height}" width="{W_}" height="{height}" font-family="{MONO}">',
         f'<rect width="{W_}" height="{height}" rx="14" fill="{BODY}" stroke="#30363D"/>',
         f'<path d="M0 14a14 14 0 0 1 14-14h{W_ - 28}a14 14 0 0 1 14 14v{TOP - 14}H0z" fill="#161B22"/>',
         '<circle cx="26" cy="22" r="6.5" fill="#FF5F56"/><circle cx="48" cy="22" r="6.5" fill="#FFBD2E"/><circle cx="70" cy="22" r="6.5" fill="#27C93F"/>',
         f'<text x="{W_ / 2}" y="27" text-anchor="middle" font-size="13" fill="{DIM}">{esc(title)}</text>']
    for i, ((kind, segs), (t0, dur, n)) in enumerate(zip(lines, plan)):
        y = TOP + 34 + i * lh
        spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in segs)
        o.append(f'<text x="{X0}" y="{y}" font-size="{fs}" xml:space="preserve">{spans}</text>')
        # cover rect: hides the not-yet-typed part, slides right step by step
        xs = [X0 + k * cw for k in range(n + 1)]
        xs[-1] = 2000
        kt = [0, t0 / T] + [(t0 + dur * k / n) / T for k in range(1, n + 1)] + [1]
        vals = [X0, X0] + xs[1:] + [2000]
        kt = kt[: len(vals)]
        kt[-1] = 1
        o.append(f'<rect x="2000" y="{y - lh + 7}" width="1000" height="{lh}" fill="{BODY}">'
                 f'<animate attributeName="x" calcMode="discrete" dur="{T}s" repeatCount="indefinite" '
                 f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(f"{v:.1f}" for v in vals)}"/></rect>')
    # blinking cursor after the last line
    ly = TOP + 34 + (len(lines) - 1) * lh
    last_n = plan[-1][2]
    o.append(f'<rect x="{X0 + last_n * cw + 3}" y="{ly - 14}" width="9" height="18" fill="{G}" opacity="0">'
             f'<animate attributeName="opacity" calcMode="discrete" dur="{T}s" repeatCount="indefinite" '
             f'keyTimes="0;{(plan[-1][0] + plan[-1][1]) / T:.4f};{(plan[-1][0] + plan[-1][1] + 0.5) / T:.4f};1" values="0;1;0;0"/>'
             f'<animate attributeName="fill" values="{G};{G}" dur="1s" repeatCount="indefinite"/></rect>')
    o.append("</svg>")
    save(name, "\n".join(o))


def P(cmd):  # prompt + command
    return ("cmd", [("guruvesh@dev", G), (":", W), ("~", C), ("$ ", W), (cmd, W)])


def K(key, val, kc=Y, vc=W, pad=11):
    return ("out", [(key.ljust(pad), kc), (": ", DIM), (val, vc)])


def build_terminals():
    about = [
        P("whoami"),
        ("out", [("Guruvesh Bachhav", W), (" - Computer Engineering student, SPPU (graduating 2027)", DIM)]),
        P("cat focus.txt"),
        K("primary", "Python backend (APIs, SQL / PostgreSQL) + React"),
        K("secondary", "Java for DSA and OOP"),
        K("long-term", "AI / ML engineering"),
        P("cat status.txt"),
        K("internship", "Data Science / AI-ML @ Supratech AI Solutions (Jan-Feb 2026)"),
        K("dsa", "~120 problems solved in Java"),
        K("targeting", "SDE / Python backend roles, Pune and Bangalore"),
        P("echo $MOTTO"),
        ("out", [("First understand how it works. Then optimize it.", G)]),
    ]
    terminal("terminal-about.svg", "guruvesh@dev: ~", about, height=44 + 34 + 12 * 25 + 22)

    log = [
        P("git log --graph --oneline"),
        ("out", [("* ", M), ("2027      ", Y), ("(next) ", C), ("graduate and land the first SDE / backend role", W)]),
        ("out", [("* ", M), ("Nov 2026  ", Y), ("(HEAD -> main) ", G), ("rebuilt my profile, DSA in Java ongoing", W)]),
        ("out", [("* ", M), ("Oct 2026  ", Y), ("chose Python backend + React + PostgreSQL as my main direction", W)]),
        ("out", [("* ", M), ("Jan-Feb 26 ", Y), ("Data Science / AI-ML intern, Supratech AI Solutions and Innovations", W)]),
        ("out", [("* ", M), ("          ", Y), ("shipped Crop Predictor, Summary Generator, Scholar Mentor", DIM)]),
        ("out", [("* ", M), ("Earlier   ", Y), ("B.E. Computer Engineering, PVG's COE and SSDIOM, Nashik (SPPU)", W)]),
    ]
    terminal("terminal-journey.svg", "guruvesh@dev: ~/journey", log, height=44 + 34 + 7 * 25 + 22)


# =====================================================================
# STYLE 3: NEON CIRCUIT
# =====================================================================
NEON_BG = "#070B1A"
GRID = ('<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" '
        'stroke="#22D3EE" stroke-opacity="0.07"/></pattern>')
GLOW = ('<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def neon_frame(w, h, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}">'
            f'<defs>{GRID}{GLOW}{defs}</defs><rect width="{w}" height="{h}" rx="16" fill="{NEON_BG}"/>'
            f'<rect width="{w}" height="{h}" rx="16" fill="url(#grid)"/>{body}</svg>')


def pipeline():
    w, h = 960, 360
    b = ['<text x="32" y="44" font-size="22" font-weight="700" fill="#E2E8F0">How I build</text>',
         '<text x="32" y="64" font-size="12" fill="#67E8F9">Life of a request in a typical full-stack project</text>']

    def node(cx, cy, title, sub, color, dashed=False, nw=190, nh=86):
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        return (f'<g filter="url(#glow)"><rect x="{cx - nw / 2}" y="{cy - nh / 2}" width="{nw}" height="{nh}" rx="14" fill="#0B1226" '
                f'stroke="{color}" stroke-width="2"{dash}/></g>'
                f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-size="18" font-weight="700" fill="{color}">{title}</text>'
                f'<text x="{cx}" y="{cy + 18}" text-anchor="middle" font-size="12" fill="#CBD5E1">{sub}</text>')

    def link(x1, x2, y, color, label, ly, rev=False, dur=2.4):
        d = f"M{x2} {y} H{x1}" if rev else f"M{x1} {y} H{x2}"
        s = f'<path d="{d}" stroke="{color}" stroke-opacity="0.45" stroke-width="2" fill="none"/>'
        for k in range(3):
            s += (f'<circle r="4" fill="{color}" filter="url(#glow)"><animateMotion path="{d}" dur="{dur}s" '
                  f'begin="-{k * dur / 3:.2f}s" repeatCount="indefinite"/></circle>')
        s += f'<text x="{(x1 + x2) / 2}" y="{ly}" text-anchor="middle" font-size="11" fill="{color}">{label}</text>'
        return s

    cy = 160
    xs = [150, 480, 810]
    b.append(link(xs[0] + 95, xs[1] - 95, cy - 14, "#22D3EE", "HTTP request", cy - 24))
    b.append(link(xs[0] + 95, xs[1] - 95, cy + 14, "#F472B6", "JSON response", cy + 34, rev=True, dur=2.8))
    b.append(link(xs[1] + 95, xs[2] - 95, cy - 14, "#22D3EE", "SQL query", cy - 24, dur=2.2))
    b.append(link(xs[1] + 95, xs[2] - 95, cy + 14, "#F472B6", "rows", cy + 34, rev=True, dur=2.6))
    b.append(node(xs[0], cy, "React UI", "JavaScript · HTML · CSS", "#22D3EE"))
    b.append(node(xs[1], cy, "Python API", "Python · REST", "#FBBF24"))
    b.append(node(xs[2], cy, "Database", "SQL · MySQL · MongoDB", "#A3E635"))
    # AI/ML branch
    d = f"M{xs[1]} {cy + 43} V{cy + 100}"
    b.append(f'<path d="{d}" stroke="#A78BFA" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="5 5" fill="none"/>')
    b.append(f'<circle r="4" fill="#A78BFA" filter="url(#glow)"><animateMotion path="{d}" dur="1.8s" repeatCount="indefinite"/></circle>')
    b.append(node(xs[1], cy + 135, "AI / ML service", "where I want to go next", "#A78BFA", dashed=True, nh=60))
    b.append('<text x="928" y="338" text-anchor="end" font-size="11" fill="#64748B">solid = used so far   dashed = next up</text>')
    save("pipeline.svg", neon_frame(w, h, "", "".join(b)))


def marquee():
    w, h = 960, 188
    rows = [
        ("SKILLS", 30, ["Python", "Java", "JavaScript", "React", "HTML5", "CSS3", "SQL", "MySQL", "MongoDB", "Streamlit", "Git", "GitHub", "OOP", "DSA"], 1, 46),
        ("LEARNING NOW", 104, ["Python backend", "PostgreSQL", "REST APIs", "Computer Networks", "System Design", "AI / ML"], -1, 40),
    ]
    colors = ["#22D3EE", "#F472B6", "#A3E635", "#FBBF24", "#A78BFA"]
    defs = ('<linearGradient id="fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#000"/><stop offset="0.08" stop-color="#fff"/>'
            '<stop offset="0.92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="m"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>')
    body = ['<g mask="url(#m)">']
    for label, y, items, direction, speed in rows:
        body.append(f'<text x="32" y="{y - 8}" font-size="11" letter-spacing="2" fill="#64748B">{label}</text>')
        chips, x, k = [], 0, 0
        while x < 1000:
            for it in items:
                cw_ = len(it) * 8.4 + 44
                col = colors[k % 5]
                chips.append(f'<g transform="translate({x:.1f},{y})"><rect width="{cw_:.1f}" height="38" rx="19" fill="#0B1226" stroke="{col}" stroke-width="1.5"/>'
                             f'<circle cx="18" cy="19" r="4" fill="{col}"/><text x="30" y="24" font-size="14" font-weight="600" fill="#E2E8F0">{it}</text></g>')
                x += cw_ + 14
                k += 1
        total = x
        frm, to = (0, -total) if direction > 0 else (-total, 0)
        body.append(f'<g><animateTransform attributeName="transform" type="translate" from="{frm} 0" to="{to} 0" dur="{total / speed:.1f}s" repeatCount="indefinite"/>')
        body.append("".join(chips))
        body.append(f'<g transform="translate({total:.1f},0)">' + "".join(chips) + "</g></g>")
    body.append("</g>")
    save("marquee.svg", neon_frame(w, h, defs, "".join(body)))


def dsa_progress():
    topics = [
        ("Arrays", 1), ("Strings", 1), ("Patterns", 1), ("Bit Manipulation", 1), ("2D Arrays", 1), ("Sorting", 1), ("Recursion", 0.5),
        ("Searching", 0), ("Linked Lists", 0), ("Stacks & Queues", 0), ("Trees", 0), ("Graphs", 0), ("Dynamic Programming", 0),
    ]
    w, h = 960, 380
    b = ['<text x="32" y="44" font-size="22" font-weight="700" fill="#E2E8F0">DSA Progress</text>',
         '<text x="32" y="64" font-size="12" fill="#67E8F9">Solved in Java  |  github.com/Guruvesh03/DSA-in-Java</text>',
         '<text x="928" y="46" text-anchor="end" font-size="30" font-weight="700" fill="#FBBF24" filter="url(#glow)">~120</text>',
         '<text x="928" y="64" text-anchor="end" font-size="12" fill="#94A3B8">problems solved</text>']
    T = 6.0
    for i, (name, frac) in enumerate(topics):
        col, row = i // 7, i % 7
        x, y = 32 + col * 464, 96 + row * 40
        track_x, track_w = x + 170, 190
        color = "#A3E635" if frac == 1 else "#FBBF24" if frac else "#475569"
        status = "done" if frac == 1 else "in progress" if frac else "planned"
        b.append(f'<text x="{x}" y="{y + 14}" font-size="14" fill="#E2E8F0">{esc(name)}</text>')
        b.append(f'<rect x="{track_x}" y="{y + 3}" width="{track_w}" height="14" rx="7" fill="#0B1226" stroke="#1E293B"/>')
        if frac:
            tw = track_w * frac
            d0 = 0.3 + i * 0.25
            b.append(f'<g filter="url(#glow)"><rect x="{track_x}" y="{y + 3}" width="{tw:.1f}" height="14" rx="7" fill="{color}">'
                     f'<animate attributeName="width" values="0;0;{tw:.1f}" keyTimes="0;{d0 / T:.3f};{(d0 + 1.2) / T:.3f}" dur="{T}s" fill="freeze"/>'
                     + (f'<animate attributeName="opacity" values="1;0.55;1" dur="1.6s" begin="{d0 + 1.2:.1f}s" repeatCount="indefinite"/>' if frac < 1 else "")
                     + '</rect></g>')
        b.append(f'<text x="{track_x + track_w + 12}" y="{y + 15}" font-size="12" fill="{color}">{status}</text>')
    save("dsa-progress.svg", neon_frame(w, h, "", "".join(b)))


def open_to_work():
    w, h = 960, 64
    per = 2 * (w - 6 - 52) + 2 * 3.1416 * 26
    body = (f'<rect x="3" y="3" width="{w - 6}" height="{h - 6}" rx="29" fill="#0B1226" stroke="#14532D" stroke-width="1.5"/>'
            f'<g filter="url(#glow)"><rect x="3" y="3" width="{w - 6}" height="{h - 6}" rx="29" fill="none" stroke="#4ADE80" stroke-width="2.5" '
            f'stroke-dasharray="150 {per - 150:.0f}"><animate attributeName="stroke-dashoffset" from="0" to="-{per:.0f}" dur="6s" repeatCount="indefinite"/></rect></g>'
            f'<circle cx="46" cy="32" r="7" fill="#4ADE80" filter="url(#glow)"><animate attributeName="r" values="5;9;5" dur="1.6s" repeatCount="indefinite"/></circle>'
            f'<text x="72" y="38" font-size="16" font-weight="700" fill="#4ADE80" letter-spacing="2">OPEN TO WORK</text>'
            f'<text x="236" y="38" font-size="15" fill="#E2E8F0">SDE / Python backend roles   |   Pune · Bangalore   |   Graduating 2027</text>')
    save("open-to-work.svg", neon_frame(w, h, "", body))


if __name__ == "__main__":
    build_terminals()
    pipeline()
    marquee()
    dsa_progress()
    open_to_work()
