"""Links section renderer - Cloned from georgekobaidze console design with exactly 3 channels."""

from .svg_utils import (
    BASE_CSS,
    BG_DARK,
    CYAN,
    DEFS,
    FL,
    FR,
    W,
    X,
    esc,
    heading,
    slice_svg,
)

# Vector SVG icons
ICON_FB = """<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>"""

ICON_LI = """<rect width="20" height="20" rx="3" fill="#00d9ff"/><text x="10" y="15" text-anchor="middle" font-weight="700" fill="#03040a" style="font-size:12px;font-family:ui-monospace,monospace">in</text>"""

ICON_DEV = """<path d="M7.42 10.05c-.18-.16-.46-.23-.84-.23H5.34v4.36h1.24c.38 0 .66-.07.84-.23.18-.16.27-.42.27-.8v-2.3c0-.38-.09-.64-.27-.8zm1.88 3.1c0 .7-.2 1.25-.6 1.63-.4.39-.98.58-1.73.58H4.07V8.64h2.9c.75 0 1.33.19 1.73.58.4.39.6.93.6 1.63v2.3zm2.5-4.51h3.32v1.18h-2.05v1.27h1.86v1.18h-1.86v1.27h2.05v1.18h-3.32V8.64zm7.39 3.91l1.32-3.91h1.36l-2.01 5.36h-1.34l-2.01-5.36h1.36l1.32 3.91zM0 3.75v16.5C0 21.438.812 22.25 1.812 22.25h20.376c1 0 1.812-.812 1.812-1.812V3.75c0-1-.812-1.812-1.812-1.812H1.812C.812 1.938 0 2.75 0 3.75z"/>"""


def render_links_head(config: dict) -> str:
    """Render links header slice with top=True to close top frame."""
    body = heading(44, "links", "// 01") + f"""
<g class="ln" style="animation-delay:.15s"><text x="{X}" y="96" class="dim"><tspan class="gr">$</tspan> ping temazzdev --all-channels</text></g>"""
    return slice_svg(
        120,
        body,
        title="Links",
        desc="Where to find me: Facebook, LinkedIn, Blog",
        top=True,
    )


def render_link_button(k: int, config: dict) -> str:
    """Render one of the 3 button slices (width = 33.333%)."""
    links_cfg = config.get("links", {})
    channels = [
        ("facebook", "Facebook", "teaman.2606", links_cfg.get("facebook", "https://www.facebook.com/teaman.2606"), ICON_FB),
        ("linkedin", "LinkedIn", "temazzdev", links_cfg.get("linkedin", "https://www.linkedin.com/in/temazzdev"), ICON_LI),
        ("blog", "Blog", "DEV.to", links_cfg.get("blog", "https://dev.to/temaz_2606"), ICON_DEV),
    ]

    key, label, handle, url, icon_markup = channels[k]
    h = 80
    n = len(channels)
    seg = W / n                        # 293.333
    x0 = seg * k
    btn_w = 240
    btn_gap = 28
    lx = X + k * (btn_w + btn_gap) - x0

    first, last = (k == 0), (k == n - 1)
    bg0 = FL - x0 if first else 0
    bg1 = FR - x0 if last else seg
    rails = (f"M{FL - x0} 0V{h}" if first else "") + (f"M{FR - x0} 0V{h}" if last else "")
    glow = (f"M{FL - x0} -40V{h+40}" if first else "") + (f"M{FR - x0} -40V{h+40}" if last else "")

    by, bh, cut = 12, 56, 12
    box = f"M{lx:.1f} {by}H{lx+btn_w-cut:.1f}L{lx+btn_w:.1f} {by+cut}V{by+bh}H{lx:.1f}Z"

    if key == "linkedin":
        icon_svg = f'<g transform="translate({lx+12:.1f} {by+12}) scale(0.9)">{icon_markup}</g>'
    else:
        icon_svg = f'<g transform="translate({lx+12:.1f} {by+12}) scale({18/24})"><path fill="{CYAN}" d="{icon_markup[9:-3]}"/></g>'

    body = f"""<g class="ln" style="animation-delay:{.25 + k*.08:.2f}s">
<path d="{box}" fill="{CYAN}" fill-opacity=".05"/>
<path d="{box}" fill="none" stroke="{CYAN}" stroke-opacity=".55"/>
<path d="M{lx+btn_w-cut:.1f} {by}L{lx+btn_w:.1f} {by+cut}" stroke="{CYAN}" stroke-width="2"/>
{icon_svg}
<text x="{lx+38:.1f}" y="{by+25}" font-weight="700" class="cy" style="font-size:13px">{esc(label)}</text>
<text x="{lx+12:.1f}" y="{by+46}" class="dim" style="font-size:10px">{esc(handle)}</text>
</g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{seg:.3f}" height="{h}" viewBox="0 0 {seg:.3f} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(label)}</title>
<desc id="d">{esc(label)}: {esc(url)}</desc>
<style>
{BASE_CSS}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<pattern id="grid" x="{(-x0) % 40:.1f}" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{CYAN}" stroke-opacity=".06"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="g" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
{f'<path d="{glow}" fill="none" stroke="{CYAN}" stroke-width="3" opacity=".55" filter="url(#glow)"/>' if glow else ""}
<rect x="{bg0:.1f}" y="0" width="{bg1-bg0:.1f}" height="{h}" fill="{BG_DARK}"/>
<rect x="{bg0:.1f}" y="0" width="{bg1-bg0:.1f}" height="{h}" fill="url(#grid)"/>
{body}
{f'<path d="{rails}" fill="none" stroke="{CYAN}" stroke-width="1.2"/>' if rails else ""}
</svg>
"""


def render_link_facebook(config: dict) -> str:
    return render_link_button(0, config)


def render_link_linkedin(config: dict) -> str:
    return render_link_button(1, config)


def render_link_blog(config: dict) -> str:
    return render_link_button(2, config)
