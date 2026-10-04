"""Links Section SVG renderer - Exactly 3 Channels (Facebook, LinkedIn, Blog)."""

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

# Vector SVG icons
ICON_FACEBOOK_PATH = """<path fill="#00f0ff" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>"""

ICON_LINKEDIN_PATH = """<path fill="#00f0ff" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451c.979 0 1.778-.773 1.778-1.729V1.73C24 .774 23.205 0 22.225 0z"/>"""

ICON_BLOG_DEV_PATH = """<path fill="#00f0ff" d="M7.42 10.05c-.18-.16-.46-.23-.84-.23H5.34v4.36h1.24c.38 0 .66-.07.84-.23.18-.16.27-.42.27-.8v-2.3c0-.38-.09-.64-.27-.8zm1.88 3.1c0 .7-.2 1.25-.6 1.63-.4.39-.98.58-1.73.58H4.07V8.64h2.9c.75 0 1.33.19 1.73.58.4.39.6.93.6 1.63v2.3zm2.5-4.51h3.32v1.18h-2.05v1.27h1.86v1.18h-1.86v1.27h2.05v1.18h-3.32V8.64zm7.39 3.91l1.32-3.91h1.36l-2.01 5.36h-1.34l-2.01-5.36h1.36l1.32 3.91zM0 3.75v16.5C0 21.438.812 22.25 1.812 22.25h20.376c1 0 1.812-.812 1.812-1.812V3.75c0-1-.812-1.812-1.812-1.812H1.812C.812 1.938 0 2.75 0 3.75z"/>"""


def render_links_header(config: dict) -> str:
    """Render assets/links-header.svg (terminal command header)."""
    w, h = 900, 88
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=14, corner="top-right")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Terminal Frame -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Terminal Chrome Top Bar -->
  {terminal_top_bar(1, 1, w - 2, path="~/links", sec_tag="// CHANNELS: 3 ONLINE")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 56)">
    {command_prompt_line(0, 0, "ping temazzdev --all-channels")}
  </g>

  <!-- Ping Feedback Subtext -->
  <text x="24" y="78" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="10.5" font-weight="600">&gt;&gt; PING temazzdev (127.0.0.1): 3 active channels responding [0% packet loss]</text>
</svg>"""
    return svg


def render_single_link_card(
    platform_name: str,
    secondary_text: str,
    icon_path: str,
    ping_ms: int = 12,
    target_url: str = "",
    width: int = 292,
    height: int = 108,
) -> str:
    """Render an individual standalone clickable cyberpunk card SVG."""
    w, h = width, height
    cpath = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=12, corner="top-right")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Card Background with Chamfered Top-Right Corner -->
  <path d="{cpath}" fill="{COLOR_BG_PANEL}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.5" class="cyber-hover" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Top Accent Highlight -->
  <line x1="2" y1="2" x2="48" y2="2" stroke="{COLOR_CYAN_NEON}" stroke-width="2.5" filter="url(#glow-cyan)" />

  <!-- Small Platform Icon -->
  <g transform="translate(20, 22)">
    <rect x="-4" y="-4" width="34" height="34" rx="4" fill="#080f1c" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
    <g transform="translate(1, 1) scale(0.95)">
      <svg width="24" height="24" viewBox="0 0 24 24">
        {icon_path}
      </svg>
    </g>
  </g>

  <!-- Platform Name (Neon Cyan) -->
  <text x="64" y="34" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="14" font-weight="800" letter-spacing="1.5">{esc(platform_name)}</text>
  
  <!-- Secondary Username / Subtext (Muted) -->
  <text x="64" y="52" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="11.5" font-weight="600">{esc(secondary_text)}</text>

  <!-- Ping / Status Indicator -->
  <g transform="translate(20, 78)">
    <rect x="0" y="0" width="{w - 40}" height="20" rx="3" fill="#070c16" stroke="{COLOR_BORDER_MUTED}" stroke-width="0.75" />
    <circle cx="10" cy="10" r="3" fill="{COLOR_GREEN_NEON}" />
    <text x="20" y="14" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">PING: <tspan fill="{COLOR_GREEN_NEON}">{ping_ms}ms</tspan> // <tspan fill="{COLOR_CYAN_NEON}">200 OK</tspan></text>
    <text x="{w - 48}" y="14" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" text-anchor="end">&gt;&gt; CONNECT</text>
  </g>
</svg>"""
    return svg


def render_link_facebook(config: dict) -> str:
    """Render assets/link-facebook.svg."""
    links_cfg = config.get("links", {})
    url = links_cfg.get("facebook", "https://www.facebook.com/teaman.2606")
    return render_single_link_card(
        platform_name="FACEBOOK",
        secondary_text="teaman.2606",
        icon_path=ICON_FACEBOOK_PATH,
        ping_ms=12,
        target_url=url,
    )


def render_link_linkedin(config: dict) -> str:
    """Render assets/link-linkedin.svg."""
    links_cfg = config.get("links", {})
    url = links_cfg.get("linkedin", "https://www.linkedin.com/in/temazzdev")
    return render_single_link_card(
        platform_name="LINKEDIN",
        secondary_text="temazzdev",
        icon_path=ICON_LINKEDIN_PATH,
        ping_ms=15,
        target_url=url,
    )


def render_link_blog(config: dict) -> str:
    """Render assets/link-blog.svg."""
    links_cfg = config.get("links", {})
    url = links_cfg.get("blog", "https://dev.to/temaz_2606")
    return render_single_link_card(
        platform_name="BLOG",
        secondary_text="DEV.to",
        icon_path=ICON_BLOG_DEV_PATH,
        ping_ms=18,
        target_url=url,
    )


def render_links_footer(config: dict) -> str:
    """Render assets/links-footer.svg (terminal frame bottom)."""
    w, h = 900, 36
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=8, corner="bottom-right")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <path d="{outer_path}" fill="#080e1a" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <text x="24" y="22" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="600">--- temazzdev ping statistics: 3 packets transmitted, 3 received, 0% packet loss ---</text>
  <text x="{w - 24}" y="22" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="10" font-weight="700" text-anchor="end">[ CHANNELS: 100% RESPONSIVE ]</text>
</svg>"""
    return svg


def render_unified_links(config: dict) -> str:
    """Render unified assets/links.svg for direct SVG viewing."""
    w, h = 900, 220
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=14, corner="top-right")

    card_w = 268
    card_h = 100
    gap = 18
    start_x = 24
    card_y = 80

    links_data = [
        {
            "name": "FACEBOOK",
            "user": "teaman.2606",
            "url": "https://www.facebook.com/teaman.2606",
            "icon": ICON_FACEBOOK_PATH,
            "ping": 12,
        },
        {
            "name": "LINKEDIN",
            "user": "temazzdev",
            "url": "https://www.linkedin.com/in/temazzdev",
            "icon": ICON_LINKEDIN_PATH,
            "ping": 15,
        },
        {
            "name": "BLOG",
            "user": "DEV.to",
            "url": "https://dev.to/temaz_2606",
            "icon": ICON_BLOG_DEV_PATH,
            "ping": 18,
        },
    ]

    cards_svg = []
    for i, item in enumerate(links_data):
        cx = start_x + i * (card_w + gap)
        cpath = chamfered_rect_path(cx, card_y, card_w, card_h, chamfer=10, corner="top-right")

        cards_svg.append(f"""
        <!-- {item['name']} Card with Embedded Link -->
        <a href="{esc(item['url'])}" target="_blank" rel="noopener noreferrer">
          <g class="cyber-hover" cursor="pointer">
            <path d="{cpath}" fill="#0b1220" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
            <line x1="{cx}" y1="{card_y + 2}" x2="{cx + 40}" y2="{card_y + 2}" stroke="{COLOR_CYAN_NEON}" stroke-width="2" />
            
            <!-- Platform Icon -->
            <g transform="translate({cx + 14}, {card_y + 14})">
              <rect x="-2" y="-2" width="28" height="28" rx="4" fill="#070c14" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
              <svg width="24" height="24" viewBox="0 0 24 24">
                {item['icon']}
              </svg>
            </g>

            <!-- Name and Username -->
            <text x="{cx + 52}" y="{card_y + 26}" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="13" font-weight="800" letter-spacing="1">{esc(item['name'])}</text>
            <text x="{cx + 52}" y="{card_y + 42}" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="11" font-weight="600">{esc(item['user'])}</text>

            <!-- Status Indicator -->
            <rect x="{cx + 14}" y="{card_y + 64}" width="{card_w - 28}" height="20" rx="3" fill="#070c16" stroke="{COLOR_BORDER_MUTED}" stroke-width="0.75" />
            <circle cx="{cx + 24}" cy="{card_y + 74}" r="3" fill="{COLOR_GREEN_NEON}" />
            <text x="{cx + 34}" y="{card_y + 78}" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9" font-weight="600">PING: <tspan fill="{COLOR_GREEN_NEON}">{item['ping']}ms</tspan> // <tspan fill="{COLOR_CYAN_NEON}">200 OK</tspan></text>
            <text x="{cx + card_w - 20}" y="{card_y + 78}" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="9" font-weight="700" text-anchor="end">&gt;&gt; VISIT</text>
          </g>
        </a>
        """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Main Terminal Frame -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.2" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />

  <!-- Terminal Chrome Top Bar -->
  {terminal_top_bar(1, 1, w - 2, path="~/links", sec_tag="// CHANNELS: 3 ONLINE")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 56)">
    {command_prompt_line(0, 0, "ping temazzdev --all-channels")}
  </g>

  <!-- 3 Cyberpunk Cards -->
  {''.join(cards_svg)}

  <!-- Terminal Bottom Summary -->
  <text x="24" y="{h - 12}" fill="{COLOR_TEXT_DIM}" font-family="{FONT_MONO}" font-size="9.5">--- 3 packets transmitted, 3 received, 0% packet loss ---</text>
</svg>"""
    return svg
