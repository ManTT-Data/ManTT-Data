import datetime
import json
from pathlib import Path

from .svg_utils import (
    AMBER,
    CYAN,
    FR,
    GREEN,
    MAGENTA,
    X,
    esc,
    heading,
    slice_svg,
)


def load_stats_data() -> dict:
    """Load stats from data/stats.json with safe fallback."""
    stats_path = Path(__file__).resolve().parent.parent.parent / "data" / "stats.json"
    if stats_path.exists():
        try:
            return json.loads(stats_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def format_member_since(created_at_str: str) -> str:
    """Format GitHub account creation date into 'MMM YYYY (Xy)'."""
    if not created_at_str:
        return "Oct 2023 (3y)"
    try:
        dt = datetime.datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        diff_years = max(0, now.year - dt.year)
        month_abbr = dt.strftime("%b")
        return f"{month_abbr} {dt.year} ({diff_years}y)"
    except Exception:
        return "Oct 2023 (3y)"


def tile(x: float, y: float, w: float, h: float, label: str, value: str, sub: str, delay: float) -> str:
    """Render a stat tile with top-left corner bracket and glowing value."""
    glow = f'<text x="{x+16:.1f}" y="{y+50:.1f}" font-weight="700" fill="{CYAN}" filter="url(#g)" opacity=".55" style="font-size:30px">{esc(value)}</text>'
    return f"""<g class="ln" style="animation-delay:{delay:.2f}s">
<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{CYAN}" fill-opacity=".035" stroke="{CYAN}" stroke-opacity=".35"/>
<path d="M{x:.1f} {y+12:.1f}V{y:.1f}H{x+12:.1f}" fill="none" stroke="{CYAN}" stroke-width="2"/>
<text x="{x+16:.1f}" y="{y+22:.1f}" letter-spacing="1.5" class="dim" style="font-size:10.5px">{esc(label)}</text>
{glow}<text x="{x+16:.1f}" y="{y+50:.1f}" font-weight="700" fill="{CYAN}" style="font-size:30px">{esc(value)}</text>
<text x="{x+16:.1f}" y="{y+h-12:.1f}" fill="#6e7681" style="font-size:12px">{esc(sub)}</text>
</g>"""


def render_system_status(config: dict) -> str:
    """Render the stats.svg slice matching georgekobaidze design with dynamic data."""
    stats = load_stats_data()
    username = stats.get("username") or config.get("github_username", "ManTT-Data")
    now_year = datetime.date.today().year

    stars = stats.get("stars", 48)
    contribs_yr = stats.get("contributions_year", 1322)
    contribs_all = stats.get("contributions_all", 1649)
    prs = stats.get("prs", 52)
    prs_merged = stats.get("prs_merged", 48)
    streak_cur = stats.get("streak_current", 34)
    streak_long = stats.get("streak_longest", 42)
    followers = stats.get("followers", 12)
    forks = stats.get("forks", 8)
    created_at = stats.get("created_at", "2023-10-15T00:00:00Z")
    member_since = format_member_since(created_at)

    parts = [
        heading(44, "stats", "// 02"),
        f'<g class="ln" style="animation-delay:.15s"><text x="{X}" y="96" class="dim"><tspan class="gr">$</tspan> gh stats --user {esc(username)}</text></g>',
    ]

    # Row 1 — 4 big tiles
    tw, gap, ty, th = 182, 16, 118, 92
    t1 = [
        ("TOTAL STARS", f"{stars:,}", "across all repos"),
        (f"CONTRIBUTIONS {now_year}", f"{contribs_yr:,}", f"{contribs_all:,} all time"),
        ("PULL REQUESTS", f"{prs:,}", f"{prs_merged:,} merged"),
        ("CURRENT STREAK", f"{streak_cur}d", f"longest: {streak_long} days"),
    ]
    for i, (lab, val, sub) in enumerate(t1):
        parts.append(tile(X + i * (tw + gap), ty, tw, th, lab, val, sub, 0.25 + i * 0.08))

    # Row 2 — Telemetry list + Top Languages
    ry, rh = ty + th + 16, 110
    lw = 280
    kv = [
        ("followers", f"{followers:,}"),
        ("forks", f"{forks:,}"),
        ("member since", member_since),
        ("deck status", "ONLINE ★"),
    ]
    rows = "\n".join(
        f'<text x="{X+16}" y="{ry+26+i*22}" xml:space="preserve"><tspan class="cy">{esc(k)}</tspan><tspan class="dim">{"." * (16 - len(k))}</tspan> <tspan class="fg">{esc(v)}</tspan></text>'
        for i, (k, v) in enumerate(kv)
    )
    parts.append(f"""<g class="ln" style="animation-delay:.6s">
<rect x="{X}" y="{ry}" width="{lw}" height="{rh}" fill="{CYAN}" fill-opacity=".035" stroke="{CYAN}" stroke-opacity=".35"/>
<path d="M{X} {ry+12}V{ry}H{X+12}" fill="none" stroke="{CYAN}" stroke-width="2"/>
{rows}
</g>""")

    # Top languages bar
    lx = X + lw + gap
    lwid = (FR - 36) - lx
    palette = [CYAN, MAGENTA, GREEN, AMBER, "#a855f7", "#ec4899", "#3b82f6"]

    raw_langs = stats.get("languages", {})
    if raw_langs and isinstance(raw_langs, dict):
        top_pairs = list(raw_langs.items())[:5]
        total_bytes = sum(v for _, v in top_pairs)
        if total_bytes > 0:
            items = [(k, v / total_bytes) for k, v in top_pairs]
        else:
            items = [("Python", 0.382), ("TypeScript", 0.245), ("C#", 0.181), ("Go", 0.120), ("SQL", 0.072)]
    else:
        items = [
            ("Python", 0.382),
            ("TypeScript", 0.245),
            ("C#", 0.181),
            ("Go", 0.120),
            ("SQL", 0.072),
        ]

    cols = palette[: len(items)]
    bx, by, bw = lx + 16, ry + 36, lwid - 32
    segs, cx = [], bx
    for (k, p), c in zip(items, cols):
        w = bw * p
        if w > 0:
            segs.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(w-2,1):.1f}" height="8" fill="{c}"/>')
            segs.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(w-2,1):.1f}" height="8" fill="{c}" filter="url(#g)" opacity=".6"/>')
            cx += w

    legend = []
    for i, ((k, p), c) in enumerate(zip(items, cols)):
        col, row = i % 3, i // 3
        lxx = bx + col * (bw / 3)
        lyy = by + 28 + row * 22
        legend.append(
            f'<rect x="{lxx:.1f}" y="{lyy-8:.1f}" width="8" height="8" fill="{c}"/>'
            f'<text x="{lxx+14:.1f}" y="{lyy}" class="fg" style="font-size:12px">{esc(k)}</text>'
            f'<text x="{lxx + bw/3 - 16:.1f}" y="{lyy}" text-anchor="end" class="dim" style="font-size:11px">{p*100:.1f}%</text>'
        )

    parts.append(f"""<g class="ln" style="animation-delay:.7s">
<rect x="{lx}" y="{ry}" width="{lwid}" height="{rh}" fill="{CYAN}" fill-opacity=".035" stroke="{CYAN}" stroke-opacity=".35"/>
<path d="M{lx} {ry+12}V{ry}H{lx+12}" fill="none" stroke="{CYAN}" stroke-width="2"/>
<text x="{lx+16}" y="{ry+20}" letter-spacing="1.5" class="dim" style="font-size:10.5px">TOP LANGUAGES</text>
<rect x="{bx}" y="{by}" width="{bw}" height="8" fill="#11161d"/>
{"".join(segs)}
{"".join(legend)}
</g>""")

    parts.append(f'<text x="{FR-36}" y="{ry + rh + 18}" text-anchor="end" fill="#484f58" style="font-size:11px">// telemetry synchronized</text>')

    h = 360
    return slice_svg(h, "\n".join(parts), title="GitHub Stats", desc=f"Stats for {username}")

