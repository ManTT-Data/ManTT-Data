"""Footer / EOF section SVG renderer."""

from .svg_utils import (
    COLOR_BG_DEEP,
    COLOR_BORDER_CYAN,
    COLOR_BORDER_MUTED,
    COLOR_CYAN_DIM,
    COLOR_CYAN_NEON,
    COLOR_GREEN_NEON,
    COLOR_MAGENTA_NEON,
    COLOR_TEXT_BRIGHT,
    COLOR_TEXT_DIM,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    FONT_MONO,
    chamfered_rect_path,
    common_defs,
    common_styles,
    esc,
)


def render_footer(config: dict) -> str:
    """Render the FOOTER / EOF section SVG."""
    w, h = 900, 95
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=12, corner="all")
    display_name = config.get("display_name", "Temazz").upper()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Main Terminal Base -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Top Line Accent -->
  <line x1="24" y1="2" x2="160" y2="2" stroke="{COLOR_CYAN_NEON}" stroke-width="2" filter="url(#glow-cyan-subtle)" />

  <!-- Content -->
  <g transform="translate(24, 28)">
    <text x="0" y="0" fill="{COLOR_MAGENTA_NEON}" font-family="{FONT_MONO}" font-size="11" font-weight="700">[EOF]</text>
    <text x="45" y="0" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="11" font-weight="600">// TERMINAL SESSION COMPLETE // CYBER_PROFILE v4.2</text>
    <text x="{w - 48}" y="0" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" text-anchor="end">[ STATUS: ALL SYSTEMS NOMINAL ]</text>
  </g>

  <!-- Security Hash and Cyber Identity -->
  <g transform="translate(24, 52)">
    <text x="0" y="0" fill="{COLOR_TEXT_DIM}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">HASH_ID: SHA256(7F83B1657FF1FC53B92DC18148A1D65DFC2D4B1FA3D677284ADDD200126D9069)</text>
    <text x="{w - 48}" y="0" fill="{COLOR_CYAN_DIM}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600" text-anchor="end">SIGNAL: ENCRYPTED // NODE: PERSISTENT</text>
  </g>

  <!-- Bottom Accent -->
  <g transform="translate(24, 76)">
    <text x="0" y="0" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="600">&#169; 2026 {esc(display_name)} // MAN TT &#8212; CYBERNETIC DEVELOPER PORTFOLIO</text>
    <text x="{w - 48}" y="0" fill="{COLOR_TEXT_DIM}" font-family="{FONT_MONO}" font-size="9" text-anchor="end">&lt;/SESSION_CLOSED&gt;</text>
  </g>
</svg>"""
    return svg
