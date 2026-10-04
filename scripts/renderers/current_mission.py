"""Current Mission / Activity section SVG renderer."""

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


def render_current_mission(config: dict) -> str:
    """Render the CURRENT MISSION / ACTIVITY section SVG."""
    w, h = 900, 215
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=14, corner="top-right")

    missions = config.get("current_mission", [
        "Build useful software",
        "Improve engineering fundamentals",
        "Explore scalable systems",
        "Learn by building",
    ])

    thread_meta = [
        {"thread": "THREAD_01", "status": "EXECUTING", "pct": 95, "accent": COLOR_CYAN_NEON},
        {"thread": "THREAD_02", "status": "OPTIMIZING", "pct": 85, "accent": COLOR_GREEN_NEON},
        {"thread": "THREAD_03", "status": "EXPLORING", "pct": 78, "accent": COLOR_MAGENTA_NEON},
        {"thread": "THREAD_04", "status": "BUILDING", "pct": 92, "accent": COLOR_AMBER_NEON},
    ]

    items_svg = []
    item_y = 74
    for i, m in enumerate(missions[:4]):
        meta = thread_meta[i % len(thread_meta)]
        pct = meta["pct"]
        bar_total_w = 140
        bar_fill_w = (bar_total_w * pct) / 100

        items_svg.append(f"""
        <!-- Thread Item {i + 1} -->
        <g transform="translate(24, {item_y})">
          <!-- Item Background Bar -->
          <rect x="0" y="0" width="{w - 48}" height="28" rx="4" fill="#09111f" stroke="{COLOR_BORDER_MUTED}" stroke-width="0.75" />
          <line x1="0" y1="2" x2="0" y2="26" stroke="{meta['accent']}" stroke-width="3" />

          <!-- Thread Label -->
          <text x="14" y="18" fill="{meta['accent']}" font-family="{FONT_MONO}" font-size="11" font-weight="700">[{meta['thread']}]</text>

          <!-- Objective Description -->
          <text x="120" y="18" fill="{COLOR_TEXT_BRIGHT}" font-family="{FONT_MONO}" font-size="11.5" font-weight="600">{esc(m)}</text>

          <!-- Progress Bar -->
          <rect x="{w - 320}" y="10" width="{bar_total_w}" height="8" rx="2" fill="#142136" />
          <rect x="{w - 320}" y="10" width="{bar_fill_w}" height="8" rx="2" fill="{meta['accent']}" />

          <!-- Status Tag -->
          <text x="{w - 165}" y="18" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700">{pct}%</text>
          <text x="{w - 60}" y="18" fill="{meta['accent']}" font-family="{FONT_MONO}" font-size="10" font-weight="700" text-anchor="end">[{meta['status']}]</text>
        </g>
        """)
        item_y += 33

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Main Terminal Frame -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Terminal Chrome Top Bar -->
  {terminal_top_bar(1, 1, w - 2, path="~/mission", sec_tag="// SEC_04: ACTIVE_DIRECTIVES")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 56)">
    {command_prompt_line(0, 0, "cat current_objectives.log --watch-threads")}
  </g>

  <!-- Mission Threads List -->
  {''.join(items_svg)}
</svg>"""
    return svg
