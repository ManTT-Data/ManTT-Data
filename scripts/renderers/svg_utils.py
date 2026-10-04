"""Cyberpunk SVG utilities, styling, and path helpers."""

import html

# Palette constants
COLOR_BG_DEEP = "#070b12"
COLOR_BG_PANEL = "#0b1220"
COLOR_BG_SURFACE = "#0f192c"
COLOR_BORDER_MUTED = "#172b45"
COLOR_BORDER_CYAN = "#00f0ff"
COLOR_BORDER_MAGENTA = "#ff007f"
COLOR_CYAN_NEON = "#00f0ff"
COLOR_CYAN_DIM = "#009bb3"
COLOR_MAGENTA_NEON = "#ff007f"
COLOR_PURPLE_NEON = "#a855f7"
COLOR_GREEN_NEON = "#00ff9f"
COLOR_AMBER_NEON = "#ffe600"
COLOR_TEXT_BRIGHT = "#e2f1f8"
COLOR_TEXT_PRIMARY = "#c4dbeb"
COLOR_TEXT_MUTED = "#607b96"
COLOR_TEXT_DIM = "#3d546b"

FONT_MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', 'Segoe UI Mono', 'Roboto Mono', 'Fira Code', Menlo, Monaco, Consolas, monospace"


def esc(text: str) -> str:
    """Escape XML characters."""
    return html.escape(str(text))


def chamfered_rect_path(x: float, y: float, w: float, h: float, chamfer: float = 12, corner: str = "top-right") -> str:
    """Generate SVG path data for a rectangle with a clipped/chamfered corner.
    
    corner: 'top-right', 'top-left', 'bottom-right', 'bottom-left', or 'both-top'
    """
    if corner == "top-right":
        return (
            f"M {x} {y} "
            f"L {x + w - chamfer} {y} "
            f"L {x + w} {y + chamfer} "
            f"L {x + w} {y + h} "
            f"L {x} {y + h} "
            "Z"
        )
    elif corner == "both-top":
        return (
            f"M {x} {y + chamfer} "
            f"L {x + chamfer} {y} "
            f"L {x + w - chamfer} {y} "
            f"L {x + w} {y + chamfer} "
            f"L {x + w} {y + h} "
            f"L {x} {y + h} "
            "Z"
        )
    elif corner == "all":
        return (
            f"M {x} {y + chamfer} "
            f"L {x + chamfer} {y} "
            f"L {x + w - chamfer} {y} "
            f"L {x + w} {y + chamfer} "
            f"L {x + w} {y + h - chamfer} "
            f"L {x + w - chamfer} {y + h} "
            f"L {x + chamfer} {y + h} "
            f"L {x} {y + h - chamfer} "
            "Z"
        )
    # Default to top-right
    return (
        f"M {x} {y} "
        f"L {x + w - chamfer} {y} "
        f"L {x + w} {y + chamfer} "
        f"L {x + w} {y + h} "
        f"L {x} {y + h} "
        "Z"
    )


def common_defs() -> str:
    """Return common SVG gradients, patterns, and filters."""
    return f"""
    <defs>
      <!-- Cyberpunk Grid -->
      <pattern id="cyber-grid" width="24" height="24" patternUnits="userSpaceOnUse">
        <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#00f0ff" stroke-width="1" stroke-opacity="0.04" />
      </pattern>

      <!-- Finer Grid -->
      <pattern id="cyber-grid-dense" width="12" height="12" patternUnits="userSpaceOnUse">
        <path d="M 12 0 L 0 0 0 12" fill="none" stroke="#00f0ff" stroke-width="0.75" stroke-opacity="0.025" />
      </pattern>

      <!-- Diagonal Scanlines -->
      <pattern id="cyber-scanlines" width="6" height="6" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="0" y2="6" stroke="#00f0ff" stroke-width="1" stroke-opacity="0.03" />
      </pattern>

      <!-- Glow Filters -->
      <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>

      <filter id="glow-cyan-subtle" x="-10%" y="-10%" width="120%" height="120%">
        <feGaussianBlur stdDeviation="1.5" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>

      <filter id="glow-magenta" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>

      <!-- Background Gradients -->
      <linearGradient id="bg-grad-dark" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0a101d" />
        <stop offset="50%" stop-color="#070b13" />
        <stop offset="100%" stop-color="#05080f" />
      </linearGradient>

      <linearGradient id="panel-grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#0e1728" />
        <stop offset="100%" stop-color="#080e1a" />
      </linearGradient>

      <linearGradient id="cyan-glow-line" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.1" />
        <stop offset="20%" stop-color="#00f0ff" stop-opacity="0.9" />
        <stop offset="80%" stop-color="#00f0ff" stop-opacity="0.9" />
        <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.1" />
      </linearGradient>

      <linearGradient id="accent-cyan-magenta" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#00f0ff" />
        <stop offset="100%" stop-color="#ff007f" />
      </linearGradient>
    </defs>
    """


def common_styles() -> str:
    """Return common CSS styles for SVG typography and animations."""
    return f"""
    <style>
      .mono {{ font-family: {FONT_MONO}; }}
      .cursor-blink {{ animation: blink 1.1s infinite; }}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      .cyber-hover {{ transition: all 0.3s ease; }}
      .cyber-hover:hover {{ stroke: #00f0ff; stroke-width: 1.5; filter: url(#glow-cyan); }}
    </style>
    """


def terminal_top_bar(x: float, y: float, w: float, path: str = "~/terminal", sec_tag: str = "// SEC_01") -> str:
    """Render terminal window top chrome bar."""
    return f"""
      <!-- Terminal Top Chrome -->
      <path d="{chamfered_rect_path(x, y, w, 32, chamfer=8, corner='top-right')}" fill="#0f192b" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
      
      <!-- Traffic lights -->
      <circle cx="{x + 16}" cy="{y + 16}" r="4" fill="#ff4d4d" opacity="0.85" />
      <circle cx="{x + 28}" cy="{y + 16}" r="4" fill="#ffb830" opacity="0.85" />
      <circle cx="{x + 40}" cy="{y + 16}" r="4" fill="#00f0ff" opacity="0.85" />

      <!-- Path / Title -->
      <text x="{x + 58}" y="{y + 20}" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="12" font-weight="700" letter-spacing="0.5">{esc(path)}</text>
      
      <!-- Right Security/Status Tag -->
      <text x="{x + w - 18}" y="{y + 20}" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="11" font-weight="600" text-anchor="end" letter-spacing="1">{esc(sec_tag)}</text>
      
      <!-- Bottom separator line -->
      <line x1="{x}" y1="{y + 32}" x2="{x + w}" y2="{y + 32}" stroke="{COLOR_BORDER_MUTED}" stroke-width="1" />
    """


def command_prompt_line(x: float, y: float, command: str, prefix: str = "$") -> str:
    """Render terminal prompt line with blinking cursor."""
    return f"""
      <text x="{x}" y="{y}" fill="{COLOR_MAGENTA_NEON}" font-family="{FONT_MONO}" font-size="13" font-weight="700">{esc(prefix)}</text>
      <text x="{x + 16}" y="{y}" fill="{COLOR_TEXT_BRIGHT}" font-family="{FONT_MONO}" font-size="13" font-weight="600" letter-spacing="0.5">{esc(command)}</text>
      <rect x="{x + 18 + len(command) * 8}" y="{y - 11}" width="7" height="13" fill="{COLOR_CYAN_NEON}" class="cursor-blink" />
    """
