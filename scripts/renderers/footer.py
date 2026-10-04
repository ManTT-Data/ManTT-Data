"""Footer renderer - Cloned from georgekobaidze console design."""

from .svg_utils import (
    X,
    esc,
    slice_svg,
)


def render_footer(config: dict) -> str:
    """Render footer slice closing the console frame with bottom=True."""
    handle = config.get("display_name", "temazzdev").lower()
    body = f"""<text x="{X}" y="30" class="dim"><tspan class="gr">$</tspan> exit</text>
<text x="{X}" y="52" class="dim">connection to <tspan class="cy">{esc(handle)}</tspan> closed. <tspan fill="#484f58">// EOF</tspan></text>"""
    return slice_svg(80, body, title="End of profile", desc="Connection closed.", bottom=True)
