"""Contribution city renderer - Cloned from georgekobaidze console design (Image 1)."""

import datetime
import hashlib
import json
import math
from pathlib import Path
from .svg_utils import (
    CYAN,
    FL,
    FR,
    X,
    heading,
    slice_svg,
)

CITY_TW, CITY_TH = 25, 12.5                  # iso tile width / height
CITY_OX, CITY_OY = 152.5, 262                # grid origin inside the 880-wide slice
CITY_HMAX = 118                              # tallest building, px
ROOFS = ["#0c2d6b", "#1554c0", "#2f81f7", "#1fd5ff"]   # navy → electric blue
WIN_ON, WIN_ON_SIDE, WIN_OFF = "#7df9ff", "#4cc9f0", "#111827"


def _p(x: float, y: float) -> str:
    return f"{x:.1f},{y:.1f}"


def _rng(seed: str):
    """Tiny deterministic PRNG, so the same data always draws the same windows."""
    state = int(hashlib.sha256(seed.encode()).hexdigest()[:16], 16)
    while True:
        state = (state * 6364136223846793005 + 1442695040888963407) % 2**64
        yield (state >> 11) / 2**53


def _levels(counts):
    """Quartile thresholds over non-zero days."""
    nz = sorted(c for c in counts if c > 0)
    if not nz:
        return [1, 1, 1]
    q = lambda f: nz[min(len(nz) - 1, int(len(nz) * f))]
    return [q(0.25), q(0.5), q(0.75)]


def load_calendar_data() -> list:
    """Load daily calendar data from data/calendar.json."""
    data_path = Path(__file__).resolve().parent.parent.parent / "data" / "calendar.json"
    if data_path.exists():
        try:
            return json.loads(data_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Fallback synthetic realistic 365-day calendar
    today = datetime.date.today()
    rng = _rng("temazz-contributions")
    result = []
    for i in range(365, 0, -1):
        d = today - datetime.timedelta(days=i)
        val = int(next(rng) * 15) if next(rng) > 0.4 else 0
        if d.month == 5 and d.day == 23:
            val = 43
        result.append([d.isoformat(), val])
    return result


def render_contribution_city(config: dict) -> str:
    """Render the contribution-city.svg slice exactly matching georgekobaidze's implementation."""
    calendar = load_calendar_data()
    days = [(datetime.date.fromisoformat(d), n) for d, n in calendar]
    counts = [n for _, n in days]
    total, peak = sum(counts), max(counts) if counts else 0
    lv = _levels(counts)
    rnd = _rng(f"2026-10-04-{total}")
    start = days[0][0]

    cells = []
    for d, n in days:
        idx = (d - start).days
        cells.append((idx // 7, (d.weekday() + 1) % 7, n))      # week column, Sunday = 0
    cells.sort(key=lambda c: (c[0] + c[1], c[0]))                 # back to front

    shapes, flick = [], 0
    for w, dow, n in cells:
        cx = CITY_OX + (w - dow) * CITY_TW / 2
        cy = CITY_OY + (w + dow) * CITY_TH / 2
        L, R = (cx - CITY_TW / 2, cy), (cx + CITY_TW / 2, cy)
        T, B = (cx, cy - CITY_TH / 2), (cx, cy + CITY_TH / 2)
        if n == 0:
            shapes.append(f'<path d="M{_p(*T)}L{_p(*R)}L{_p(*B)}L{_p(*L)}Z" fill="#161b22" stroke="#0d1117" stroke-width=".6"/>')
            continue
        h = 8 + (CITY_HMAX - 8) * math.sqrt(n / peak)
        level = sum(n > t for t in lv)
        Tu, Ru, Bu, Lu = [(x, y - h) for x, y in (T, R, B, L)]
        shapes.append(f'<path d="M{_p(*L)}L{_p(*B)}L{_p(*Bu)}L{_p(*Lu)}Z" fill="#1a2440"/>'
                      f'<path d="M{_p(*B)}L{_p(*R)}L{_p(*Ru)}L{_p(*Bu)}Z" fill="#111831"/>'
                      f'<path d="M{_p(*Tu)}L{_p(*Ru)}L{_p(*Bu)}L{_p(*Lu)}Z" fill="{ROOFS[level]}"/>')
        on, side, off, fl = [], [], [], []
        for face, (a, b) in (("l", (L, B)), ("r", (B, R))):
            for r in range(int((h - 6) // 7)):
                v0 = 5 + r * 7
                for u0 in (0.18, 0.58):
                    lit = next(rnd) < 0.55
                    if not lit and next(rnd) < 0.5:
                        continue
                    pts = [(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - v)
                           for u, v in ((u0, v0), (u0 + 0.26, v0), (u0 + 0.26, v0 + 3.2), (u0, v0 + 3.2))]
                    seg = "M" + "L".join(_p(*q) for q in pts) + "Z"
                    if not lit:
                        off.append(seg)
                    elif next(rnd) < 0.03:
                        fl.append((seg, face))
                    else:
                        (on if face == "l" else side).append(seg)
        if off:
            shapes.append(f'<path d="{"".join(off)}" fill="{WIN_OFF}"/>')
        if on:
            shapes.append(f'<path d="{"".join(on)}" fill="{WIN_ON}"/>')
        if side:
            shapes.append(f'<path d="{"".join(side)}" fill="{WIN_ON_SIDE}"/>')
        for seg, face in fl:
            flick += 1
            shapes.append(f'<path class="f{flick % 3}" d="{seg}" fill="{WIN_ON if face == "l" else WIN_ON_SIDE}"/>')

    # Night sky in top-right corner: stars, crescent moon, crossing plane
    stars = []
    for i in range(46):
        sx, sy = 470 + next(rnd) * 350, 118 + next(rnd) * 150
        if sx > 700 and sy < 215:           # keep the moon clear
            continue
        cls = f' class="s{i % 3}"' if i % 3 == 0 else ""
        stars.append(f'<circle{cls} cx="{sx:.1f}" cy="{sy:.1f}" r="{(.6, .8, 1.1)[i % 3]}" fill="#c9d1d9" opacity="{.35 + next(rnd) * .5:.2f}"/>')

    busiest_d, busiest_n = max(days, key=lambda t: t[1]) if days else (None, 0)
    info = [
        f'<tspan class="cy" font-weight="700">{total:,}</tspan> contributions · last 365 days',
        f'busiest day <tspan class="fg">{busiest_d:%b} {busiest_d.day}</tspan> · {busiest_n}' if busiest_n else "",
        f'{sum(1 for n in counts if n)} active days',
    ]
    info_svg = "".join(f'<text x="{FR-36}" y="{300 + i*20}" text-anchor="end" class="dim" style="font-size:12px">{t}</text>'
                       for i, t in enumerate(info) if t)

    legend = "".join(f'<rect x="{X + 52 + i*16}" y="642" width="11" height="11" fill="{c}"/>'
                     for i, c in enumerate(["#161b22"] + ROOFS))

    body = heading(44, "contribution-city", "// 03") + f"""
<g class="ln" style="animation-delay:.15s"><text x="{X}" y="96" class="dim"><tspan class="gr">$</tspan> render-city --last 365d <tspan fill="#484f58"># one building per day</tspan></text></g>
<g>{"".join(stars)}</g>
<circle cx="{FR-80}" cy="160" r="40" fill="url(#moonglow)"/>
<circle cx="{FR-80}" cy="160" r="14" fill="#e6edf3"/>
<circle cx="{FR-74}" cy="155" r="12.5" fill="#03040a"/>
<g class="plane"><g transform="translate(0 132)"><rect x="0" y="0" width="14" height="2" rx="1" fill="#484f58"/><circle class="bl" cx="0" cy="1" r="1.6" fill="#ff7b72"/><circle class="bl" cx="14" cy="1" r="1.6" fill="#f0f6fc" style="animation-delay:.7s"/></g></g>
{info_svg}
{"".join(shapes)}
<text x="{X}" y="652" class="dim" style="font-size:11px">quiet</text>{legend}<text x="{X + 52 + 5*16 + 6}" y="652" class="dim" style="font-size:11px">skyscraper</text>"""

    css = f"""@keyframes tw{{0%,100%{{opacity:.9}}50%{{opacity:.15}}}}
@keyframes fl{{0%,40%,100%{{opacity:1}}45%,60%{{opacity:.1}}}}
@keyframes blink{{0%,90%,100%{{opacity:0}}93%{{opacity:1}}}}
@keyframes fly{{from{{transform:translate({FL - 40}px,0)}}to{{transform:translate({FR + 40}px,-30px)}}}}
.s0{{animation:tw 3s infinite}}
.f0{{animation:fl 5s infinite}}.f1{{animation:fl 7s infinite 2s}}.f2{{animation:fl 9s infinite 4s}}
.plane{{animation:fly 26s linear infinite}}.bl{{animation:blink 1.4s infinite}}"""

    defs = '<radialGradient id="moonglow"><stop offset="0" stop-color="#f0f6fc" stop-opacity=".22"/><stop offset="1" stop-color="#f0f6fc" stop-opacity="0"/></radialGradient>'
    desc = f"Contribution city: an isometric night skyline with one building per day of the last year. {total:,} contributions."

    return slice_svg(680, body, title="Contribution city", desc=desc, css=css, defs=defs)
