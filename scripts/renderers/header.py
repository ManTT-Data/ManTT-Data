"""Header / Hero section SVG renderer."""

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
    common_defs,
    common_styles,
    esc,
)


def render_header(config: dict) -> str:
    """Render the BOOT / HERO cyberpunk header banner SVG."""
    w, h = 900, 210
    display_name = config.get("display_name", "Temazz").upper()
    role = config.get("role", "Software Engineer").upper()
    github_user = config.get("github_username", "ManTT-Data")
    version = config.get("system_version", "CYBER_DECK v4.2")

    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=16, corner="top-right")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Background Base -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.5" />
  
  <!-- Subtle Background Grid -->
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-grid)" />
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#cyber-scanlines)" opacity="0.6" />

  <!-- Terminal Top Chrome -->
  <path d="{chamfered_rect_path(1, 1, w - 2, 34, chamfer=16, corner='top-right')}" fill="#0e172a" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
  
  <!-- Terminal Controls -->
  <circle cx="20" cy="17" r="4.5" fill="#ff4d4d" opacity="0.9" />
  <circle cx="34" cy="17" r="4.5" fill="#ffb830" opacity="0.9" />
  <circle cx="48" cy="17" r="4.5" fill="{COLOR_CYAN_NEON}" opacity="0.9" />

  <!-- Terminal Title -->
  <text x="68" y="21" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="12" font-weight="700" letter-spacing="1">ROOT@{esc(github_user).upper()}:~ (zsh)</text>
  
  <!-- Right Status -->
  <text x="{w - 24}" y="21" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="11" font-weight="700" text-anchor="end" letter-spacing="1.5">[ SYSTEM: ONLINE ]</text>

  <!-- Cyberpunk Top Accent Bar -->
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
  <line x1="20" y1="34" x2="160" y2="34" stroke="{COLOR_CYAN_NEON}" stroke-width="2" filter="url(#glow-cyan-subtle)" />

  <!-- Boot HUD Telemetry Strip -->
  <g transform="translate(24, 52)">
    <text x="0" y="10" fill="{COLOR_MAGENTA_NEON}" font-family="{FONT_MONO}" font-size="11" font-weight="700">SYS_BOOT:</text>
    <text x="75" y="10" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="11" font-weight="600">SEQUENCE INITIALIZED</text>
    <text x="240" y="10" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11">//</text>
    <text x="260" y="10" fill="{COLOR_CYAN_DIM}" font-family="{FONT_MONO}" font-size="11" font-weight="600">KERNEL: CYBER_CORE_64</text>
    <text x="440" y="10" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11">//</text>
    <text x="460" y="10" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11">SEC_LEVEL:</text>
    <text x="545" y="10" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="11" font-weight="700">ROOT_ACCESS</text>
    <text x="660" y="10" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11">//</text>
    <text x="680" y="10" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11">{esc(version)}</text>
  </g>

  <!-- Main Hero Graphic / Typography -->
  <g transform="translate(24, 114)">
    <!-- Decorative Tech Brackets -->
    <path d="M 0 -24 L -10 -24 L -10 28 L 0 28" fill="none" stroke="{COLOR_CYAN_NEON}" stroke-width="2" />
    <path d="M {w - 48} -24 L {w - 38} -24 L {w - 38} 28 L {w - 48} 28" fill="none" stroke="{COLOR_CYAN_NEON}" stroke-width="2" />

    <!-- Name Shadow / Glow layer -->
    <text x="12" y="12" fill="{COLOR_MAGENTA_NEON}" font-family="{FONT_MONO}" font-size="36" font-weight="900" letter-spacing="4" opacity="0.4" transform="translate(2, 2)">{esc(display_name)}</text>
    <!-- Main Neon Name -->
    <text x="12" y="12" fill="{COLOR_TEXT_BRIGHT}" font-family="{FONT_MONO}" font-size="36" font-weight="900" letter-spacing="4">{esc(display_name)}</text>
    <text x="{14 + len(display_name) * 23}" y="12" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="36" font-weight="900" letter-spacing="3" filter="url(#glow-cyan)">// MAN TT</text>

    <!-- Role / Spec Line -->
    <text x="14" y="38" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="13" font-weight="700" letter-spacing="2">&gt; {esc(role)}</text>
    <text x="240" y="38" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="12" font-weight="600">|</text>
    <text x="255" y="38" fill="{COLOR_TEXT_PRIMARY}" font-family="{FONT_MONO}" font-size="12" font-weight="500" letter-spacing="1">BACKEND SYSTEMS &amp; DISTRIBUTED ARCHITECTURE</text>
  </g>

  <!-- Bottom Telemetry Badges -->
  <g transform="translate(24, 178)">
    <!-- Badge 1: Location -->
    <rect x="0" y="0" width="160" height="22" rx="3" fill="#0d192c" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
    <circle cx="12" cy="11" r="3" fill="{COLOR_GREEN_NEON}" />
    <text x="22" y="15" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="600">LOC: REMOTE // VN</text>

    <!-- Badge 2: Latency -->
    <rect x="170" y="0" width="130" height="22" rx="3" fill="#0d192c" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
    <text x="180" y="15" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="600">PING: <tspan fill="{COLOR_CYAN_NEON}">14ms</tspan></text>

    <!-- Badge 3: Uptime -->
    <rect x="310" y="0" width="140" height="22" rx="3" fill="#0d192c" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
    <text x="320" y="15" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="600">UPTIME: <tspan fill="{COLOR_GREEN_NEON}">99.98%</tspan></text>

    <!-- Badge 4: Deck Status -->
    <rect x="460" y="0" width="160" height="22" rx="3" fill="#0d192c" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
    <text x="470" y="15" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="10" font-weight="600">DECK: <tspan fill="{COLOR_MAGENTA_NEON}">UNRESTRICTED</tspan></text>

    <!-- Right Hex Code -->
    <text x="{w - 48}" y="15" fill="{COLOR_TEXT_DIM}" font-family="{FONT_MONO}" font-size="10" text-anchor="end" letter-spacing="1">ID: 0x7E4A9F // PROTOCOL: READY</text>
  </g>
</svg>"""
    return svg
