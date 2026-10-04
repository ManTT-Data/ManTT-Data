"""System Status / GitHub Stats section SVG renderer."""

from .svg_utils import (
    COLOR_AMBER_NEON,
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


def render_system_status(config: dict) -> str:
    """Render the SYSTEM STATUS / GITHUB STATS section SVG."""
    w, h = 900, 215
    github_user = config.get("github_username", "ManTT-Data")

    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=14, corner="top-right")

    card_w = 202
    card_h = 118
    gap = 14
    start_x = 22
    card_y = 74

    cards_data = [
        {
            "tag": "COMMITS // VOL",
            "val": "1,420+",
            "sub": "CODE COMMITS",
            "stat": "VELOCITY: HIGH",
            "stat_color": COLOR_CYAN_NEON,
            "bar_pct": 0.88,
            "accent": COLOR_CYAN_NEON,
        },
        {
            "tag": "PULL_REQS // MERGE",
            "val": "52+",
            "sub": "MERGED WORKFLOWS",
            "stat": "CI/CD: 100% GREEN",
            "stat_color": COLOR_GREEN_NEON,
            "bar_pct": 0.95,
            "accent": COLOR_GREEN_NEON,
        },
        {
            "tag": "STREAK // UPTIME",
            "val": "42 DAYS",
            "sub": "CONCURRENT CYCLE",
            "stat": "STABILITY: OPTIMAL",
            "stat_color": COLOR_AMBER_NEON,
            "bar_pct": 0.82,
            "accent": COLOR_AMBER_NEON,
        },
        {
            "tag": "SECURITY // CODE",
            "val": "S-TIER",
            "sub": "CODE INTEGRITY",
            "stat": "0 DEFECTS / SEC_OK",
            "stat_color": COLOR_MAGENTA_NEON,
            "bar_pct": 0.98,
            "accent": COLOR_MAGENTA_NEON,
        },
    ]

    cards_svg = []
    for i, card in enumerate(cards_data):
        cx = start_x + i * (card_w + gap)
        cpath = chamfered_rect_path(cx, card_y, card_w, card_h, chamfer=8, corner="top-right")
        bar_full_w = card_w - 28
        bar_fill_w = bar_full_w * card["bar_pct"]

        cards_svg.append(f"""
        <!-- Card {i + 1} -->
        <g>
          <path d="{cpath}" fill="#0a1220" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
          <line x1="{cx}" y1="{card_y + 2}" x2="{cx + 36}" y2="{card_y + 2}" stroke="{card['accent']}" stroke-width="2" />
          
          <!-- Tag Header -->
          <text x="{cx + 14}" y="{card_y + 20}" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="700" letter-spacing="0.5">{esc(card['tag'])}</text>
          
          <!-- Primary Metric Value -->
          <text x="{cx + 14}" y="{card_y + 52}" fill="{COLOR_TEXT_BRIGHT}" font-family="{FONT_MONO}" font-size="22" font-weight="900" letter-spacing="1">{esc(card['val'])}</text>
          
          <!-- Subtitle -->
          <text x="{cx + 14}" y="{card_y + 70}" fill="{COLOR_CYAN_DIM}" font-family="{FONT_MONO}" font-size="10" font-weight="600" letter-spacing="0.5">{esc(card['sub'])}</text>

          <!-- Gauge Progress Bar -->
          <rect x="{cx + 14}" y="{card_y + 82}" width="{bar_full_w}" height="4" rx="2" fill="#142338" />
          <rect x="{cx + 14}" y="{card_y + 82}" width="{bar_fill_w}" height="4" rx="2" fill="{card['accent']}" />

          <!-- Bottom Telemetry Status -->
          <circle cx="{cx + 17}" cy="{card_y + 102}" r="3" fill="{card['stat_color']}" />
          <text x="{cx + 26}" y="{card_y + 105}" fill="{card['stat_color']}" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" letter-spacing="0.5">{esc(card['stat'])}</text>
        </g>
        """)

    cards_markup = "\n".join(cards_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Main Terminal Frame -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Terminal Chrome Top Bar -->
  {terminal_top_bar(1, 1, w - 2, path="~/metrics", sec_tag="// SEC_02: TELEMETRY")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 56)">
    {command_prompt_line(0, 0, f"sys_stat --github-telemetry @{github_user}")}
  </g>

  <!-- Metric Cards Grid -->
  {cards_markup}

  <!-- Bottom Terminal Status Bar -->
  <line x1="22" y1="{h - 10}" x2="{w - 22}" y2="{h - 10}" stroke="{COLOR_BORDER_MUTED}" stroke-width="0.5" />
</svg>"""
    return svg
