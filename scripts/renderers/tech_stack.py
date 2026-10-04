"""Tech Stack section SVG renderer."""

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


def render_tech_stack(config: dict) -> str:
    """Render the TECH STACK section SVG."""
    w, h = 900, 245
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=14, corner="top-right")

    categories = [
        {
            "title": "LANGUAGES",
            "accent": COLOR_CYAN_NEON,
            "items": ["Python", "Go", "TypeScript", "SQL", "Bash"],
        },
        {
            "title": "BACKEND & CLOUD",
            "accent": COLOR_GREEN_NEON,
            "items": ["FastAPI", "Node.js", "Docker", "Kubernetes", "AWS"],
        },
        {
            "title": "DATA & STORAGE",
            "accent": COLOR_AMBER_NEON,
            "items": ["PostgreSQL", "MongoDB", "Redis", "pgvector"],
        },
        {
            "title": "SYSTEM ARCH",
            "accent": COLOR_MAGENTA_NEON,
            "items": ["Microservices", "REST/gRPC", "CI/CD", "Linux"],
        },
    ]

    col_w = 202
    col_h = 145
    gap = 14
    start_x = 22
    card_y = 75

    cards_svg = []
    for i, cat in enumerate(categories):
        cx = start_x + i * (col_w + gap)
        cpath = chamfered_rect_path(cx, card_y, col_w, col_h, chamfer=8, corner="top-right")

        items_markup = []
        item_y = card_y + 44
        for item in cat["items"]:
            items_markup.append(f"""
              <rect x="{cx + 12}" y="{item_y - 12}" width="{col_w - 24}" height="19" rx="3" fill="#0d1829" stroke="{COLOR_BORDER_MUTED}" stroke-width="0.75" />
              <circle cx="{cx + 22}" cy="{item_y - 2}" r="2.5" fill="{cat['accent']}" />
              <text x="{cx + 32}" y="{item_y + 1}" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="10.5" font-weight="600">{esc(item)}</text>
            """)
            item_y += 22

        cards_svg.append(f"""
        <g>
          <path d="{cpath}" fill="#09101c" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
          <line x1="{cx}" y1="{card_y + 2}" x2="{cx + 40}" y2="{card_y + 2}" stroke="{cat['accent']}" stroke-width="2" />
          <text x="{cx + 14}" y="{card_y + 20}" fill="{cat['accent']}" font-family="{FONT_MONO}" font-size="11" font-weight="700" letter-spacing="1">// {esc(cat['title'])}</text>
          {''.join(items_markup)}
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
  {terminal_top_bar(1, 1, w - 2, path="~/stack", sec_tag="// SEC_03: CAPABILITIES")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 56)">
    {command_prompt_line(0, 0, "cat /etc/capabilities.conf --active-modules")}
  </g>

  <!-- Categories Grid -->
  {cards_markup}
</svg>"""
    return svg
