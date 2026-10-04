"""Tech stack renderer - Cloned from georgekobaidze console design."""

from .svg_utils import (
    CYAN,
    X,
    esc,
    heading,
    slice_svg,
    up40,
)

DEFAULT_STACK = [
    ("languages", ["C#", "Java", "TypeScript", "JavaScript", "Python"]),
    ("frameworks", [".NET", "Node.js", "FastAPI"]),
    ("databases", ["PostgreSQL", "MS SQL", "MySQL", "Redis", "MongoDB"]),
    ("cloud", ["AWS", "Azure"]),
    ("front-end", ["React", "Next.js", "Three.js", "Tailwind CSS"]),
]


def render_tech_stack(config: dict) -> str:
    """Render tech stack slice matching Image 2 and georgekobaidze design."""
    stack_data = config.get("stack", DEFAULT_STACK)
    parts = [
        heading(44, "stack", "// 04"),
        f'<g class="ln" style="animation-delay:.15s"><text x="{X}" y="96" class="dim"><tspan class="gr">$</tspan> scan --loadout --top-level</text></g>',
    ]

    y, rowh = 126, 44
    cw = 0.6 * 13          # char advance at 13px font size

    for r, (cat, items) in enumerate(stack_data):
        parts.append(f'<g class="ln" style="animation-delay:{.25 + r*.1:.2f}s">')
        parts.append(f'<text x="{X}" y="{y+20}" class="dim" style="font-size:13px">{esc(cat)}</text>')
        parts.append(f'<text x="{X+104}" y="{y+20}" class="cy" style="font-size:13px">›</text>')
        x = X + 124
        for it in items:
            w = len(it) * cw + 26
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="30" fill="{CYAN}" fill-opacity=".06" stroke="{CYAN}" stroke-opacity=".55"/>')
            parts.append(f'<path d="M{x:.1f} {y+8}V{y}H{x+8:.1f}" fill="none" stroke="{CYAN}" stroke-width="2"/>')
            parts.append(f'<text x="{x+13:.1f}" y="{y+20}" font-weight="700" class="cy" style="font-size:13px">{esc(it)}</text>')
            x += w + 10
        parts.append("</g>")
        y += rowh

    h = up40(y + 10)
    desc = "Tech stack. " + " ".join(f"{c}: {', '.join(i)}." for c, i in stack_data)
    return slice_svg(h, "\n".join(parts), title="Tech stack", desc=desc)
