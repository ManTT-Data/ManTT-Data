"""SVG frame building utilities and styling, cloned from georgekobaidze's console design."""

import html
import math
import re

CYAN = "#00d9ff"
MAGENTA = "#ff2bd6"
GREEN = "#3fb950"
AMBER = "#f59e0b"
BG_DARK = "#03040a"

W, M = 880, 16            # slice width, transparent side margin
FL, FR = M, W - M         # frame left / right (16, 864)
X = 52                    # text left edge


def esc(text: str) -> str:
    """Escape XML characters."""
    return html.escape(str(text))


def up40(v: float) -> int:
    """Round up to multiple of 40 so the background grid aligns across slices."""
    return int(math.ceil(v / 40) * 40)


BASE_CSS = f"""text{{font-family:'JBM',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:15px}}
.dim{{fill:#8b949e}}.cy{{fill:{CYAN}}}.fg{{fill:#c9d1d9}}.gr{{fill:{GREEN}}}.wh{{fill:#f0fbff}}
@keyframes fadein{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
.ln{{animation:fadein .35s ease-out both}}
.cursor{{animation:blink 1.05s step-end infinite}}
.dot{{animation:pulse 2s ease-in-out infinite}}"""

DEFS = f"""<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{CYAN}" stroke-opacity=".06"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="g" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>"""


def slice_svg(h: int, body: str, *, title: str, desc: str, top: bool = False, bottom: bool = False, css: str = "", defs: str = "") -> str:
    """Generate a continuous console slice SVG."""
    y0 = M if top else 0
    y1 = h - M if bottom else h
    rails = f"M{FL} {y0}V{y1}M{FR} {y0}V{y1}"
    if top:
        rails += f"M{FL} {y0}H{FR}"
    if bottom:
        rails += f"M{FL} {y1}H{FR}"

    gy0 = y0 if top else -40
    gy1 = y1 if bottom else h + 40
    glow = f"M{FL} {gy0}V{gy1}M{FR} {gy0}V{gy1}" + (f"M{FL} {y0}H{FR}" if top else "") + (f"M{FL} {y1}H{FR}" if bottom else "")

    corners = ""
    if top:
        corners += f'<path d="M{FL-7} {y0+18}V{y0-7}H{FL+18}"/><path d="M{FR-18} {y0-7}H{FR+7}V{y0+18}"/>'
    if bottom:
        corners += f'<path d="M{FL-7} {y1-18}V{y1+7}H{FL+18}"/><path d="M{FR-18} {y1+7}H{FR+7}V{y1-18}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<style>
{BASE_CSS}
{css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
{DEFS}
{defs}
</defs>
<path d="{glow}" fill="none" stroke="{CYAN}" stroke-width="3" opacity=".55" filter="url(#glow)"/>
<rect x="{FL}" y="{y0}" width="{FR-FL}" height="{y1-y0}" fill="{BG_DARK}"/>
<rect x="{FL}" y="{y0}" width="{FR-FL}" height="{y1-y0}" fill="url(#grid)"/>
{body}
<path d="{rails}" fill="none" stroke="{CYAN}" stroke-width="1.2"/>
<g fill="none" stroke="{CYAN}" stroke-width="2">{corners}</g>
</svg>
"""


def heading(y: int, name: str, counter: str) -> str:
    """Render the standard console section heading."""
    return f"""<text x="{X}" y="{y}" font-weight="700" fill="{CYAN}" filter="url(#g)" opacity=".8" style="font-size:20px">~/</text>
<text x="{X}" y="{y}" font-weight="700" style="font-size:20px"><tspan class="cy">~/</tspan><tspan class="wh">{esc(name)}</tspan></text>
<text x="{FR-36}" y="{y}" text-anchor="end" letter-spacing="2" fill="#6e7681" style="font-size:12px">{esc(counter)}</text>
<line x1="{X}" y1="{y+14}" x2="{FR-36}" y2="{y+14}" stroke="{CYAN}" stroke-opacity=".4"/>
<line x1="{X}" y1="{y+14}" x2="{X+120}" y2="{y+14}" stroke="{CYAN}" stroke-width="2"/>
<line x1="{X}" y1="{y+14}" x2="{X+120}" y2="{y+14}" stroke="{CYAN}" stroke-width="3" filter="url(#g)"/>"""
