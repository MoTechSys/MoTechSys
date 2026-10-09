"""Builds the hand-designed animated SVGs (header, roles, basira, stack, footer).

Run:  python scripts/build_static.py
Output: assets/<name>-dark.svg and assets/<name>-light.svg
All text is converted to outlines (see svgtext.py) so it renders identically
inside GitHub's image proxy, which blocks web fonts.
"""
from __future__ import annotations

import os
import re

from svgtext import text_path as T
from svgtext import width as W
from theme import THEMES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def svg(w, h, body, title, css=""):
    title = _esc(title)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f'<style>{css}{REDUCED}</style>{body}</svg>')


def check(x, y, s, color, sw=2.2):
    """A checkmark drawn as a stroke (the fonts have no ✓ glyph)."""
    return (f'<path d="M{x} {y + s * .55} L{x + s * .38} {y + s * .9} L{x + s} {y + s * .1}" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def write(name, theme, content):
    path = os.path.join(OUT, f"{name}-{theme}.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  {name}-{theme}.svg  {len(content) / 1024:.1f} KB")


# ─────────────────────────────────────────────── HEADER ──
def header(c, theme):
    w, h = 900, 310
    dur = 9  # seconds per verification cycle
    quote = "وَمَا أُوتِيتُم مِّنَ الْعِلْمِ إِلَّا قَلِيلًا"
    qsize = 25
    qw = W(quote, "ar", 500, qsize)
    q_right = w - 62
    q_left = q_right - qw
    q_base = 252

    # Background
    b = [f'''<defs>
<radialGradient id="ga" cx="88%" cy="0%" r="60%"><stop offset="0" stop-color="{c['mint']}" stop-opacity="{.13 if theme == 'dark' else .10}"/><stop offset="1" stop-color="{c['mint']}" stop-opacity="0"/></radialGradient>
<radialGradient id="gb" cx="0%" cy="100%" r="55%"><stop offset="0" stop-color="{c['gold']}" stop-opacity="{.12 if theme == 'dark' else .10}"/><stop offset="1" stop-color="{c['gold']}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{c['grid']}" stroke-width="1"/></pattern>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity="1"/><stop offset=".65" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="gm"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
<clipPath id="frame"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16"/></clipPath>
<clipPath id="reveal"><rect x="{q_right + 4}" y="200" width="0" height="80">
  <animate attributeName="x" values="{q_right + 4};{q_right + 4};{q_left - 6};{q_left - 6};{q_right + 4}" keyTimes="0;.08;.55;.96;1" dur="{dur}s" repeatCount="indefinite"/>
  <animate attributeName="width" values="0;0;{qw + 10};{qw + 10};0" keyTimes="0;.08;.55;.96;1" dur="{dur}s" repeatCount="indefinite"/>
</rect></clipPath>
<linearGradient id="beam" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{c['gold']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['gold']}"/><stop offset="1" stop-color="{c['gold']}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-200%" y="-20%" width="500%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>''']
    b.append(f'<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="{c["bg"]}"/>'
             f'<rect width="{w}" height="{h}" fill="url(#ga)"/><rect width="{w}" height="{h}" fill="url(#gb)"/>'
             f'<rect width="{w}" height="{h}" fill="url(#grid)" mask="url(#gm)" opacity=".9"/></g>')
    b.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{c["line"]}"/>')

    # Top meta line
    b.append(T("basira://engine · deterministic", 34, 40, family="mono", size=11, tracking=.6, fill=c["mute"]))
    b.append(f'<circle cx="25" cy="36" r="3.5" fill="{c["mint"]}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    b.append(T("SANA'A · YEMEN — 2026", w - 34, 40, family="mono", size=11, tracking=1.2, fill=c["mute"], anchor="end"))

    # Engine facts (left)
    facts = [("sha256", "9f2c…a71e", True), ("corpus", "71,987 records", False), ("index", "4.5M tokens · <5ms", False)]
    for i, (k, v, hi) in enumerate(facts):
        y = 92 + i * 22
        b.append(T(k, 34, y, family="mono", size=11.5, fill=c["dim"]))
        b.append(T(v, 96, y, family="mono", size=11.5, fill=c["gold"] if hi else c["dim"]))

    # Name (right)
    name_ar_1, name_ar_2 = "م. معين ", "العباسي"
    s = 50
    w2 = W(name_ar_2, "ar", 700, s)
    w1 = W(name_ar_1, "ar", 700, s)
    xr = w - 36
    # RTL: first word on the right
    b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".9s" begin=".1s" fill="freeze"/>'
             f'{T(name_ar_1, xr, 112, family="ar", weight=700, size=s, anchor="end", fill=c["text"])}'
             f'{T(name_ar_2, xr - w1, 112, family="ar", weight=700, size=s, anchor="end", fill=c["gold"])}</g>')
    b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".9s" begin=".5s" fill="freeze"/>'
             f'{T("MOAIN AL-ABBASI", xr, 146, family="sans", weight=300, size=17, tracking=6.2, anchor="end", fill=c["mute"])}</g>')
    role = "Applied-AI · Security · Full-stack Engineer"
    rw = W(role, "mono", 500, 13.5)
    b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".9s" begin=".9s" fill="freeze"/>'
             f'{T(role, xr - 14, 180, family="mono", weight=500, size=13.5, anchor="end", fill=c["mint"])}'
             f'<rect x="{xr - 9}" y="167" width="8" height="16" fill="{c["mint"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.05s" repeatCount="indefinite"/></rect></g>')
    _ = rw

    # Engine strip
    sx, sy, sw_, sh = 34, 206, w - 68, 76
    b.append(f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh}" rx="11" fill="{c["panel"]}" fill-opacity=".92" stroke="{c["line"]}"/>')
    # verdict column
    vx = sx + 20
    b.append(f'<line x1="{sx + 228}" y1="{sy + 14}" x2="{sx + 228}" y2="{sy + sh - 14}" stroke="{c["line"]}"/>')
    b.append(T("STATE", vx, sy + 26, family="mono", weight=500, size=11, fill=c["mute"]))
    b.append(T("diff", vx, sy + 45, family="mono", weight=500, size=11, fill=c["mute"]))
    b.append(T("hash", vx, sy + 64, family="mono", weight=500, size=11, fill=c["mute"]))
    # states: scanning… -> VERIFIED (synced to the beam)
    kt = "0;.55;.56;.95;.96;1"
    b.append(f'<g>{T("scanning…", vx + 62, sy + 26, family="mono", weight=500, size=11, fill=c["gold"])}'
             f'<animate attributeName="opacity" values="1;1;0;0;1;1" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></g>')
    b.append(f'<g opacity="0">{check(vx + 62, sy + 16, 11, c["mint"], 2)}{T("VERIFIED", vx + 80, sy + 26, family="mono", weight=700, size=11, fill=c["mint"])}'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></g>')
    b.append(T("letter-level", vx + 62, sy + 45, family="mono", size=11, fill=c["soft"]))
    b.append(f'<g>{T("pending", vx + 62, sy + 64, family="mono", size=11, fill=c["dim"])}'
             f'<animate attributeName="opacity" values="1;1;0;0;1;1" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></g>')
    b.append(f'<g opacity="0">{T("determinism_ok", vx + 62, sy + 64, family="mono", size=11, fill=c["soft"])}'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></g>')

    # quote: pending layer + verified layer revealed right-to-left
    b.append(T(quote, q_right, q_base, family="ar", weight=500, size=qsize, anchor="end", fill=c["pending"]))
    b.append(f'<g clip-path="url(#reveal)">{T(quote, q_right, q_base, family="ar", weight=500, size=qsize, anchor="end", fill=c["mint"])}</g>')
    # letter-level diff underline grows with reveal
    b.append(f'<rect x="{q_right}" y="{q_base + 12}" width="0" height="2" rx="1" fill="{c["mint"]}" opacity=".55">'
             f'<animate attributeName="x" values="{q_right};{q_right};{q_left};{q_left};{q_right}" keyTimes="0;.08;.55;.96;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="width" values="0;0;{qw};{qw};0" keyTimes="0;.08;.55;.96;1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    # scanning beam
    bx = [q_right + 4, q_right + 4, q_left - 6, q_left - 6, q_right + 4]
    vals = ";".join(f"{x - 1:.1f}" for x in bx)
    b.append(f'<g><rect y="{sy - 10}" width="2.5" height="{sh + 20}" fill="url(#beam)" x="0"><animate attributeName="x" values="{vals}" keyTimes="0;.08;.55;.96;1" dur="{dur}s" repeatCount="indefinite"/></rect>'
             f'<rect y="{sy - 4}" width="10" height="{sh + 8}" fill="{c["gold"]}" opacity=".35" filter="url(#glow)" x="0"><animate attributeName="x" values="{";".join(f"{x - 5:.1f}" for x in bx)}" keyTimes="0;.08;.55;.96;1" dur="{dur}s" repeatCount="indefinite"/></rect>'
             f'<animate attributeName="opacity" values="0;1;1;0;0;0" keyTimes="0;.07;.55;.6;.96;1" dur="{dur}s" repeatCount="indefinite"/></g>')
    # source reference chip after verify
    ref = "الإسراء · ٨٥"
    rfw = W(ref, "ar", 400, 12) + 20
    rx0 = sx + 248
    b.append(f'<g opacity="0"><rect x="{rx0}" y="{sy + 25}" width="{rfw}" height="26" rx="6" fill="none" stroke="{c["mint"]}" stroke-opacity=".5"/>'
             f'{T(ref, rx0 + rfw / 2, sy + 43, family="ar", size=12, anchor="middle", fill=c["mint"])}'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.58;.62;.94;.96;1" dur="{dur}s" repeatCount="indefinite"/></g>')

    return svg(w, h, "".join(b), "Moain Al-Abbasi — Applied-AI, Security and Full-stack Engineer")


# ─────────────────────────────────────────────── ROLES (typing line) ──
def roles(c, theme):
    w, h = 900, 46
    lines = [
        ("building Arabic-first products that prove, not guess", "mono"),
        ("deterministic engines · LLMs propose, code decides", "mono"),
        ("multi-tenant platforms · offline-first apps · MCP", "mono"),
        ("security by design — SOC, forensics, zero-trust access", "mono"),
    ]
    size = 15
    per = 5.0
    total = per * len(lines)
    parts = [f'<defs>']
    body = []
    dots_y = 24
    for i, (ln, fam) in enumerate(lines):
        lw = W(ln, fam, 500, size)
        prompt_w = W("> ", "mono", 500, size)
        full = prompt_w + lw
        x0 = (w - full) / 2 - 30
        tx = x0 + prompt_w
        t0, t1, t2, t3 = i * per / total, (i * per + 1.6) / total, (i * per + 4.2) / total, (i * per + 4.6) / total
        t3 = min(t3, 1)
        kt = f"0;{t0:.4f};{t1:.4f};{t2:.4f};{t3:.4f};1" if t0 > 0 else f"0;{t1:.4f};{t2:.4f};{t3:.4f};1"
        if t0 > 0:
            wv = f"0;0;{lw:.1f};{lw:.1f};0;0"
            op = f"0;1;1;1;0;0"
            cx = f"{tx:.1f};{tx:.1f};{tx + lw:.1f};{tx + lw:.1f};{tx:.1f};{tx:.1f}"
        else:
            wv = f"0;{lw:.1f};{lw:.1f};0;0"
            op = f"1;1;1;0;0"
            cx = f"{tx:.1f};{tx + lw:.1f};{tx + lw:.1f};{tx:.1f};{tx:.1f}"
        # visibility window
        if t0 > 0:
            vis = f"0;0;1;1;0;0"
            vkt = f"0;{t0 - .0001:.4f};{t0:.4f};{t3:.4f};{min(t3 + .0001, 1):.4f};1"
        else:
            vis = "1;1;0;0"
            vkt = f"0;{t3:.4f};{min(t3 + .0001, 1):.4f};1"
        parts.append(f'<clipPath id="c{i}"><rect x="{tx:.1f}" y="0" height="{h}" width="0">'
                     f'<animate attributeName="width" values="{wv}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite" calcMode="linear"/></rect></clipPath>')
        body.append(f'<g opacity="0"><animate attributeName="opacity" values="{vis}" keyTimes="{vkt}" dur="{total}s" repeatCount="indefinite"/>'
                    f'{T(">", x0, 29, family="mono", weight=500, size=size, fill=c["gold"])}'
                    f'<g clip-path="url(#c{i})">{T(ln, tx, 29, family=fam, weight=500, size=size, fill=c["text"])}</g>'
                    f'<rect y="15" width="8" height="18" fill="{c["mint"]}" x="{tx:.1f}"><animate attributeName="x" values="{cx}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/></rect>'
                    f'</g>')
        _ = op
    parts.append('</defs>')
    # progress dots
    dx0 = w - 120
    for i in range(len(lines)):
        t0 = i * per / total
        t3 = (i + 1) * per / total
        if i == 0:
            vals, kt = f"{c['gold']};{c['gold']};{c['line']};{c['line']}", f"0;{t3 - .001:.4f};{t3:.4f};1"
        else:
            vals, kt = f"{c['line']};{c['line']};{c['gold']};{c['gold']};{c['line']};{c['line']}", f"0;{t0 - .001:.4f};{t0:.4f};{t3 - .001:.4f};{min(t3, .9999):.4f};1"
        body.append(f'<circle cx="{dx0 + i * 14}" cy="{dots_y}" r="3.5" fill="{c["line"]}"><animate attributeName="fill" values="{vals}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite" calcMode="discrete"/></circle>')
    return svg(w, h, "".join(parts) + "".join(body), "Building Arabic-first products that prove, not guess")


# ─────────────────────────────────────────────── STACK ──
STACK = [
    ("Python", "#3776AB"), ("TypeScript", "#3178C6"), ("Go", "#00ADD8"), ("Dart · Flutter", "#0175C2"),
    ("FastAPI", "#009688"), ("React 19", "#61DAFB"), ("Next.js", None), ("Hono", "#E36002"),
    ("PostgreSQL", "#4169E1"), ("MCP", "gold"), ("Docker", "#2496ED"), ("Wazuh SIEM", "mint"),
]


def stack(c, theme):
    w = 900
    size = 12.5
    padx, gap, ch = 13, 8, 32
    items = []
    for name, col in STACK:
        tw = W(name, "mono", 500, size)
        items.append((name, col, tw + padx * 2 + 15))
    rows, cur, cw = [], [], 0
    for it in items:
        if cur and cw + it[2] + gap > w - 40:
            rows.append(cur)
            cur, cw = [], 0
        cur.append(it)
        cw += it[2] + gap
    rows.append(cur)
    h = len(rows) * (ch + 10) + 4
    b = []
    k = 0
    for r, row in enumerate(rows):
        rw = sum(i[2] for i in row) + gap * (len(row) - 1)
        x = (w - rw) / 2
        y = 2 + r * (ch + 10)
        for name, col, iw in row:
            color = c["text"] if col is None else c.get(col, col)
            delay = .05 * k
            b.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".5s" fill="freeze"/>'
                     f'<rect x="{x:.1f}" y="{y}" width="{iw:.1f}" height="{ch}" rx="7" fill="{c["panel"]}" stroke="{c["line"]}"/>'
                     f'<rect x="{x + padx:.1f}" y="{y + ch / 2 - 4}" width="8" height="8" rx="2" fill="{color}"/>'
                     f'{T(name, x + padx + 15, y + 20.5, family="mono", weight=500, size=size, fill=c["soft"])}</g>')
            x += iw + gap
            k += 1
    return svg(w, h, "".join(b), "Stack: " + ", ".join(n for n, _ in STACK))


# ─────────────────────────────────────────────── BASIRA CARD ──
def basira(c, theme):
    w, h = 900, 350
    b = [f'<defs><clipPath id="cf"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16"/></clipPath>'
         f'<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{c["gold"]}" stop-opacity="0"/><stop offset=".5" stop-color="{c["gold"]}" stop-opacity=".5"/><stop offset="1" stop-color="{c["gold"]}" stop-opacity="0"/></linearGradient></defs>']
    b.append(f'<g clip-path="url(#cf)"><rect width="{w}" height="{h}" fill="{c["panel"]}"/>'
             f'<rect x="512" width="{w - 512}" height="{h}" fill="{c["bg"]}"/></g>')
    b.append(f'<line x1="512" y1="1" x2="512" y2="{h - 1}" stroke="{c["line"]}"/>')
    b.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{c["line"]}"/>')

    # Left: title
    L = 32
    b.append(T("FEATURED PROJECT", L, 42, family="mono", weight=700, size=10.5, tracking=2.2, fill=c["gold"]))
    tw = W("بصيرة", "ar", 700, 44)
    b.append(T("بصيرة", L + tw, 98, family="ar", weight=700, size=44, anchor="end", fill=c["gold"]))
    b.append(T("BASIRA", L + tw + 16, 92, family="sans", weight=300, size=19, tracking=5, fill=c["mute"]))
    b.append(T("Deterministic verification of Quran & Hadith", L, 134, family="sans", weight=400, size=15.5, fill=c["text"]))
    b.append(T("quotations — before you publish.", L, 157, family="sans", weight=400, size=15.5, fill=c["text"]))
    s1 = "The model only proposes; "
    b.append(T(s1, L, 186, family="sans", weight=300, size=14, fill=c["soft"]))
    b.append(T("the engine decides.", L + W(s1, "sans", 300, 14), 186, family="sans", weight=600, size=14, fill=c["gold"]))

    # pipeline with travelling pulse
    steps = ["text / image", "seed & extend", "BM25 + RRF", "byte-exact", "validator"]
    x, y = L, 214
    boxes = []
    for i, st in enumerate(steps):
        bw = W(st, "mono", 400, 11) + 18
        if x + bw > 486:
            x, y = L, y + 36
        key = st == "byte-exact"
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="26" rx="6" fill="{c["bg"]}" stroke="{c["gold"] if key else c["line"]}"/>')
        b.append(T(st, x + 9, y + 17.5, family="mono", size=11, fill=c["gold"] if key else c["mute"]))
        boxes.append((x, y, bw))
        x += bw
        if i < len(steps) - 1:
            b.append(f'<path d="M{x + 5:.1f} {y + 13} h10 m-4 -4 l4 4 l-4 4" fill="none" stroke="{c["dim"]}" stroke-width="1.3"/>')
            x += 20
    # pulse highlight walking through steps
    n = len(boxes)
    for i, (bx, by, bw) in enumerate(boxes):
        t0 = i / n
        b.append(f'<rect x="{bx:.1f}" y="{by}" width="{bw:.1f}" height="26" rx="6" fill="{c["mint"]}" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;.22;0;0" keyTimes="0;{t0:.3f};{t0 + .08:.3f};{t0 + .2:.3f};1" dur="5s" repeatCount="indefinite"/></rect>')

    # links row
    links = [("basirapp.site", True), ("Repository", False), ("API docs", False), ("Telegram bot", False)]
    x, y = L, 316
    for lab, primary in links:
        bw = W(lab, "mono", 700, 11) + 24 + (14 if primary else 0)
        b.append(f'<rect x="{x:.1f}" y="{y - 18}" width="{bw:.1f}" height="28" rx="6" fill="{c["gold"] if primary else "none"}" stroke="{c["gold"] if primary else c["line"]}"/>')
        b.append(T(lab, x + 12, y + 0.5, family="mono", weight=700, size=11, fill=c["ink_on_gold"] if primary else c["text"]))
        if primary:
            ax = x + bw - 20
            b.append(f'<path d="M{ax:.1f} {y + 1} l7 -7 m-5 0 h5 v5" fill="none" stroke="{c["ink_on_gold"]}" stroke-width="1.6" stroke-linecap="round"/>')
        x += bw + 8

    # Right: metrics 2×2
    mets = [
        ("150", "/150", "evaluation · variance 0", 1.0, "mint"),
        ("0", "/500", "false alarms on corpus", 1.0, "mint"),
        ("78.54", "%", "IslamicEval 2025 · 1B", .7854, "mint"),
        ("487", "", "tests · mypy --strict", 1.0, "gold"),
    ]
    gx, gy, cw_, chh, g = 532, 24, 172, 144, 14
    for i, (v, suf, lab, p, col) in enumerate(mets):
        cx = gx + (i % 2) * (cw_ + g)
        cy = gy + (i // 2) * (chh + g)
        color = c[col]
        d = .35 + i * .25
        b.append(f'<rect x="{cx}" y="{cy}" width="{cw_}" height="{chh}" rx="11" fill="none" stroke="{c["line"]}"/>')
        # ring
        r = 15
        circ = 2 * 3.14159 * r
        rx_, ry_ = cx + cw_ - 30, cy + 32
        b.append(f'<circle cx="{rx_}" cy="{ry_}" r="{r}" fill="none" stroke="{c["line"]}" stroke-width="4.5"/>')
        b.append(f'<circle cx="{rx_}" cy="{ry_}" r="{r}" fill="none" stroke="{color}" stroke-width="4.5" stroke-linecap="round" '
                 f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ:.2f}" transform="rotate(-90 {rx_} {ry_})">'
                 f'<animate attributeName="stroke-dashoffset" from="{circ:.2f}" to="{circ * (1 - p):.2f}" begin="{d:.2f}s" dur="1.6s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1" keyTimes="0;1"/></circle>')
        # value slides up
        vw = W(v, "mono", 700, 30)
        b.append(f'<g opacity="0" transform="translate(0 10)">'
                 f'<animate attributeName="opacity" from="0" to="1" begin="{d:.2f}s" dur=".7s" fill="freeze"/>'
                 f'<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" begin="{d:.2f}s" dur=".7s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1" keyTimes="0;1"/>'
                 f'{T(v, cx + 16, cy + 82, family="mono", weight=700, size=30, fill=c["text"])}'
                 f'{T(suf, cx + 18 + vw, cy + 82, family="mono", weight=500, size=14, fill=c["mute"])}</g>')
        b.append(T(lab, cx + 16, cy + 106, family="sans", weight=400, size=11.5, fill=c["mute"]))
        # bar
        bw_ = cw_ - 32
        b.append(f'<rect x="{cx + 16}" y="{cy + 122}" width="{bw_}" height="4" rx="2" fill="{c["line"]}"/>')
        b.append(f'<rect x="{cx + 16}" y="{cy + 122}" width="0" height="4" rx="2" fill="{color}">'
                 f'<animate attributeName="width" from="0" to="{bw_ * p:.1f}" begin="{d:.2f}s" dur="1.6s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1" keyTimes="0;1"/></rect>')
    # periodic shimmer across the card
    b.append(f'<rect y="0" width="160" height="{h}" fill="url(#sh)" opacity=".10" x="-200" clip-path="url(#cf)">'
             f'<animate attributeName="x" values="-200;-200;{w + 40}" keyTimes="0;.75;1" dur="8s" repeatCount="indefinite"/></rect>')
    return svg(w, h, "".join(b), "Basira — deterministic verification of Quran and Hadith quotations. 150/150 evaluation, 0/500 false alarms, 78.54% IslamicEval 2025, 487 tests")


# ─────────────────────────────────────────────── SECTION LABELS ──
def label(c, theme, text, star=False):
    w, h = 900, 34
    b = []
    x = 2
    if star:
        b.append(f'<path d="M9 7 l2.6 5.6 6 .7 -4.5 4.1 1.2 6 -5.3 -3 -5.3 3 1.2 -6 -4.5 -4.1 6 -.7z" transform="translate(-1 2)" fill="{c["gold"]}"/>')
        x = 26
    b.append(T(text, x, 23, family="mono", weight=700, size=12.5, tracking=2.6, fill=c["mute"]))
    tw = W(text, "mono", 700, 12.5, 2.6)
    b.append(f'<line x1="{x + tw + 16:.1f}" y1="19" x2="{w}" y2="19" stroke="{c["line"]}"/>')
    b.append(f'<circle cx="{x + tw + 16:.1f}" cy="19" r="2.5" fill="{c["gold"]}"><animate attributeName="cx" values="{x + tw + 16:.1f};{w - 3};{x + tw + 16:.1f}" dur="12s" repeatCount="indefinite" calcMode="spline" keySplines=".5 0 .5 1;.5 0 .5 1" keyTimes="0;.5;1"/></circle>')
    return svg(w, h, "".join(b), text.title())


# ─────────────────────────────────────────────── FOOTER ──
def footer(c, theme):
    w, h = 900, 150
    def wave(amp, off, ybase):
        pts = []
        import math
        for i in range(0, 61):
            x = i * (w * 2) / 60
            y = ybase + amp * math.sin(i / 60 * 4 * math.pi + off)
            pts.append(f"{x:.1f} {y:.1f}")
        return "M" + " L".join(pts) + f" V{h} H0Z"
    b = [f'<defs><clipPath id="ff"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16"/></clipPath></defs>']
    b.append(f'<g clip-path="url(#ff)"><rect width="{w}" height="{h}" fill="{c["bg"]}"/>')
    for amp, off, yb, col, op, dur in [(10, 0, 110, c["panel"], 1, 14), (8, 1.6, 122, c["line"], .7, 10), (6, 3.1, 134, c["gold"], .10, 7)]:
        b.append(f'<path d="{wave(amp, off, yb)}" fill="{col}" opacity="{op}">'
                 f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-w} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{c["line"]}"/>')
    b.append(T("بصيرة: تعرض أين وُجد النص… ولا تحكم عليه", w / 2, 60, family="ar", weight=500, size=20, anchor="middle", fill=c["text"]))
    b.append(T("ARABIC-FIRST · MEASURED, NOT CLAIMED", w / 2, 88, family="mono", weight=500, size=11, tracking=2.4, anchor="middle", fill=c["mute"]))
    return svg(w, h, "".join(b), "Basira: shows where the text was found, and does not judge it")


if __name__ == "__main__":
    for theme, c in THEMES.items():
        write("header", theme, header(c, theme))
        write("roles", theme, roles(c, theme))
        write("stack", theme, stack(c, theme))
        write("basira", theme, basira(c, theme))
        write("label-work", theme, label(c, theme, "SELECTED WORK"))
        write("label-live", theme, label(c, theme, "LIVE · AUTO-UPDATED DAILY"))
        write("label-toolbox", theme, label(c, theme, "HOW I BUILD"))
        write("footer", theme, footer(c, theme))


# ─────────────────────────────────────────────── PROJECT CARDS ──
PROJECTS = {
    "platforms": ("PLATFORMS & SYSTEMS", [
        ("nexus-notify", "TypeScript", "Multi-tenant, multi-channel notifications", "behind one API"),
        ("scam2027", "Next.js 16 · RLS", "University course & assessment manager", "PostgreSQL RLS · 114 RBAC permissions"),
        ("motech-platform", "Go", "Secure remote access — SSH over NetBird", "mesh + one-command cross-platform agent"),
    ]),
    "ai": ("AI & SECURITY", [
        ("Ai_Alabbasi", "Python", "Swappable-brain autonomous coding agent", "API model ⇄ local model, one config"),
        ("telegram-mcp-2", "MCP", "Expanded Telegram MCP server", "safe tools + HTTP wrapper"),
        ("my-bro", "Wazuh SIEM", "Open-source Security Operations Center", "SOC graduation project"),
    ]),
    "offline": ("OFFLINE-FIRST APPS", [
        ("دفتر البقالة", "Flutter", "Grocery accounting — append-only ledgers", "barcode · PDF/Excel · 157 tests"),
        ("سجلاتي · Sijilati", "Flutter", "Digital debt ledger for Yemeni shops", "works fully without internet"),
        ("electricity-billing", "Flutter · PWA", "Billing for a power-generation company", "local-only PWA · IndexedDB"),
    ]),
}


def _has_ar(s):
    return any("\u0600" <= ch <= "\u06ff" for ch in s)


def project_card(c, theme, key):
    title, items = PROJECTS[key]
    w, h = 292, 300
    b = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>']
    b.append(f'<rect x="20" y="0" width="34" height="2.5" rx="1" fill="{c["gold"]}"/>')
    b.append(T(title, 20, 34, family="mono", weight=700, size=10.5, tracking=1.8, fill=c["gold"]))
    for i, (name, stack_, d1, d2) in enumerate(items):
        y = 76 + i * 76
        if _has_ar(name):
            # mixed: draw Arabic part with Arabic font
            parts = name.split(" · ")
            x = 20
            for j, p in enumerate(parts):
                if j:
                    b.append(T(" · ", x, y, family="mono", weight=700, size=14, fill=c["dim"]))
                    x += W(" · ", "mono", 700, 14)
                if _has_ar(p):
                    pw = W(p, "ar", 600, 15)
                    b.append(T(p, x + pw, y, family="ar", weight=600, size=15, anchor="end", fill=c["text"]))
                    x += pw
                else:
                    b.append(T(p, x, y, family="mono", weight=700, size=14, fill=c["text"]))
                    x += W(p, "mono", 700, 14)
        else:
            b.append(T(name, 20, y, family="mono", weight=700, size=14, fill=c["text"]))
        b.append(T(stack_, w - 20, y, family="mono", size=10, fill=c["mute"], anchor="end"))
        b.append(T(d1.replace("⇄", "<>"), 20, y + 21, family="sans", weight=400, size=12, fill=c["soft"]))
        b.append(T(d2.replace("⇄", "<>"), 20, y + 38, family="sans", weight=300, size=11.5, fill=c["mute"]))
        if i < 2:
            b.append(f'<line x1="20" y1="{y + 54}" x2="{w - 20}" y2="{y + 54}" stroke="{c["line"]}" stroke-dasharray="2 4"/>')
    return svg(w, h, "".join(b), title.title() + ": " + ", ".join(n for n, *_ in items))


def work(c, theme):
    w, h, cw, g = 900, 300, 292, 11
    inner = []
    for i, k in enumerate(PROJECTS):
        card = project_card(c, theme, k)
        body = re.sub(r"^<svg[^>]*>.*?</style>", "", card, flags=re.S)[:-6]
        body = re.sub(r"<title>.*?</title>", "", body)
        inner.append(f'<g transform="translate({i * (cw + g) + 1} 0)">{body}</g>')
    names = ", ".join(n for k in PROJECTS for n, *_ in PROJECTS[k][1])
    return svg(w, h, "".join(inner), "Selected work: " + names)


if __name__ == "__main__":
    for theme, c in THEMES.items():
        write("work", theme, work(c, theme))
