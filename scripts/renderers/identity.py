"""Identity / Whoami section SVG renderer."""

from .svg_utils import (
    COLOR_BG_DEEP,
    COLOR_BG_PANEL,
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
    command_prompt_line,
    common_defs,
    common_styles,
    esc,
    terminal_top_bar,
)


def render_identity(config: dict) -> str:
    """Render the WHOAMI / IDENTITY section SVG."""
    w, h = 900, 185
    tagline = config.get("tagline", "Building, learning and experimenting with software.")
    role = config.get("role", "Software Engineer")
    interests = config.get("interests", [
        "Software Engineering",
        "Backend Systems",
        "Cloud",
        "Automation",
        "Open Source",
    ])

    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=14, corner="top-right")

    # Render interests chips
    chips_svg = []
    curr_x = 24
    curr_y = 138
    for item in interests:
        chip_label = f"#{item.replace(' ', '')}"
        chip_width = len(chip_label) * 8.5 + 26
        chip_path = chamfered_rect_path(curr_x, curr_y, chip_width, 26, chamfer=6, corner="top-right")
        chips_svg.append(f"""
          <path d="{chip_path}" fill="#0e172a" stroke="{COLOR_CYAN_DIM}" stroke-width="1" />
          <text x="{curr_x + 12}" y="{curr_y + 17}" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="11" font-weight="600">{esc(chip_label)}</text>
        """)
        curr_x += chip_width + 12

    chips_markup = "\n".join(chips_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Terminal Frame -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Terminal Chrome Top Bar -->
  {terminal_top_bar(1, 1, w - 2, path="~/identity", sec_tag="// SEC_01: WHOAMI")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 60)">
    {command_prompt_line(0, 0, "whoami --verbose")}
  </g>

  <!-- Dossier / Bio Content -->
  <g transform="translate(24, 88)">
    <text x="0" y="0" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="12" font-weight="700">&gt;&gt; IDENTITY VERIFIED:</text>
    <text x="160" y="0" fill="{COLOR_TEXT_BRIGHT}" font-family="{FONT_MONO}" font-size="12" font-weight="600">{esc(role)}</text>
    <text x="320" y="0" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="12">//</text>
    <text x="340" y="0" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="12" font-style="italic">"{esc(tagline)}"</text>

    <!-- Subtitle Interests Tag -->
    <text x="0" y="32" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11" font-weight="700" letter-spacing="1">CORE SPECIALIZATIONS &amp; DOMAINS:</text>
  </g>

  <!-- Chips row -->
  {chips_markup}

  <!-- Bottom Right Hex Stamp -->
  <text x="{w - 24}" y="{h - 14}" fill="{COLOR_TEXT_DIM}" font-family="{FONT_MONO}" font-size="10" font-weight="600" text-anchor="end">SYS_UID: 0x902F // AUTH: VALID</text>
</svg>"""
    return svg
