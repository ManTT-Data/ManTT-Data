"""Cyberpunk Contribution City - The Visual Centerpiece SVG renderer."""

import math
import random
from .svg_utils import (
    COLOR_AMBER_NEON,
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
    command_prompt_line,
    common_defs,
    common_styles,
    esc,
    terminal_top_bar,
)


def render_contribution_city(config: dict) -> str:
    """Render the CYBERPUNK CONTRIBUTION CITY visual centerpiece SVG.
    
    Generates an isometric 3D neon cyberpunk metropolis where building heights,
    illuminated windows, rooftop beacons, and holographic signs represent
    GitHub contributions and developer velocity.
    """
    w, h = 900, 450
    outer_path = chamfered_rect_path(1, 1, w - 2, h - 2, chamfer=16, corner="top-right")

    # Cityscape canvas area
    city_top = 70
    city_height = h - city_top - 28

    # Isometric projection parameters
    origin_x = 450
    origin_y = 205
    tile_w = 26
    tile_h = 13

    # Seeded pseudo-random for deterministic, visually stunning skyline
    rng = random.Random(2606)

    # Grid definition: 14 columns x 9 rows of buildings
    # Depth sort key: (col + row) ascending -> back to front
    cols = 15
    rows = 9

    buildings = []
    for r in range(rows):
        for c in range(cols):
            # Distance from center for radial skyline density
            dx = (c - cols / 2.0) / (cols / 2.0)
            dy = (r - rows / 2.0) / (rows / 2.0)
            dist_sq = dx * dx + dy * dy

            # Higher probability of towering structures near center
            base_bias = max(0.1, 1.0 - dist_sq * 0.7)
            raw_val = rng.random() * base_bias

            # Determine level 0 to 4
            if raw_val > 0.65:
                level = 4
                b_height = rng.randint(70, 115)
            elif raw_val > 0.45:
                level = 3
                b_height = rng.randint(45, 75)
            elif raw_val > 0.25:
                level = 2
                b_height = rng.randint(25, 48)
            elif raw_val > 0.12:
                level = 1
                b_height = rng.randint(12, 28)
            else:
                level = 0
                b_height = rng.randint(4, 10)

            # Special landmark towers
            has_antenna = (level >= 3 and rng.random() > 0.4)
            has_billboard = (level >= 3 and rng.random() > 0.6)
            billboard_text = rng.choice(["GIT", "SYS", "NODE", "PUSH", "COMM", "TMZ"]) if has_billboard else ""

            buildings.append({
                "row": r,
                "col": c,
                "depth": r + c,
                "level": level,
                "height": b_height,
                "has_antenna": has_antenna,
                "has_billboard": has_billboard,
                "billboard_text": billboard_text,
            })

    # Sort back to front: lower depth rendered first
    # For identical depth, sort by col to maintain consistent overlap
    buildings.sort(key=lambda b: (b["depth"], b["col"]))

    # Color palettes per contribution level
    level_colors = {
        0: {
            "top": "#121d30",
            "left": "#0b1320",
            "right": "#070c14",
            "stroke": "#1b2c45",
            "win": None,
        },
        1: {
            "top": "#006d77",
            "left": "#00474e",
            "right": "#002b2f",
            "stroke": "#009bb3",
            "win": "#00d4e6",
        },
        2: {
            "top": "#00a8b5",
            "left": "#00737c",
            "right": "#00464c",
            "stroke": "#00f0ff",
            "win": "#5dfdff",
        },
        3: {
            "top": "#00f0ff",
            "left": "#009bb3",
            "right": "#005f6e",
            "stroke": "#ffffff",
            "win": "#ffffff",
        },
        4: {
            "top": "#ff007f",
            "left": "#b8005b",
            "right": "#700037",
            "stroke": "#ff80bf",
            "win": "#ffe600",
        },
    }

    # Render ground plane circuit traces first
    ground_circuits = []
    for r in range(rows + 1):
        x1 = origin_x + (0 - r) * tile_w
        y1 = origin_y + (0 + r) * tile_h
        x2 = origin_x + (cols - r) * tile_w
        y2 = origin_y + (cols + r) * tile_h
        ground_circuits.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#00f0ff" stroke-width="0.75" stroke-opacity="0.12" />')

    for c in range(cols + 1):
        x1 = origin_x + (c - 0) * tile_w
        y1 = origin_y + (c + 0) * tile_h
        x2 = origin_x + (c - rows) * tile_w
        y2 = origin_y + (c + rows) * tile_h
        ground_circuits.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#00f0ff" stroke-width="0.75" stroke-opacity="0.12" />')

    # Render buildings
    buildings_svg = []
    for b in buildings:
        r = b["row"]
        c = b["col"]
        bh = b["height"]
        lvl = b["level"]
        colors = level_colors[lvl]

        # Base center coordinates on isometric ground plane
        base_x = origin_x + (c - r) * tile_w
        base_y = origin_y + (c + r) * tile_h

        # Isometric 4 corners of tile
        # Top corner: (base_x, base_y - tile_h)
        # Right corner: (base_x + tile_w, base_y)
        # Bottom corner: (base_x, base_y + tile_h)
        # Left corner: (base_x - tile_w, base_y)

        half_w = tile_w * 0.88
        half_h = tile_h * 0.88

        # Building roof points (shifted up by bh)
        top_y = base_y - bh
        roof_top = (base_x, top_y - half_h)
        roof_right = (base_x + half_w, top_y)
        roof_bottom = (base_x, top_y + half_h)
        roof_left = (base_x - half_w, top_y)

        # Ground intersection points for walls
        ground_bottom = (base_x, base_y + half_h)
        ground_right = (base_x + half_w, base_y)
        ground_left = (base_x - half_w, base_y)

        # Left wall polygon: roof_left -> roof_bottom -> ground_bottom -> ground_left
        left_wall = f"M {roof_left[0]} {roof_left[1]} L {roof_bottom[0]} {roof_bottom[1]} L {ground_bottom[0]} {ground_bottom[1]} L {ground_left[0]} {ground_left[1]} Z"

        # Right wall polygon: roof_bottom -> roof_right -> ground_right -> ground_bottom
        right_wall = f"M {roof_bottom[0]} {roof_bottom[1]} L {roof_right[0]} {roof_right[1]} L {ground_right[0]} {ground_right[1]} L {ground_bottom[0]} {ground_bottom[1]} Z"

        # Roof top polygon
        roof_poly = f"M {roof_top[0]} {roof_top[1]} L {roof_right[0]} {roof_right[1]} L {roof_bottom[0]} {roof_bottom[1]} L {roof_left[0]} {roof_left[1]} Z"

        # Windows generation
        windows_svg = []
        if colors["win"] and bh > 22:
            num_floors = min(6, int((bh - 10) / 10))
            for floor in range(num_floors):
                fy_offset = 10 + floor * 10
                # Left wall windows
                wx1 = roof_left[0] * 0.4 + roof_bottom[0] * 0.6
                wy1 = (roof_left[1] * 0.4 + roof_bottom[1] * 0.6) + fy_offset
                windows_svg.append(f'<line x1="{wx1 - 5}" y1="{wy1 - 2}" x2="{wx1 + 5}" y2="{wy1 + 3}" stroke="{colors["win"]}" stroke-width="1.5" stroke-opacity="0.85" />')

                # Right wall windows
                wx2 = roof_bottom[0] * 0.5 + roof_right[0] * 0.5
                wy2 = (roof_bottom[1] * 0.5 + roof_right[1] * 0.5) + fy_offset
                windows_svg.append(f'<line x1="{wx2 - 5}" y1="{wy2 + 3}" x2="{wx2 + 5}" y2="{wy2 - 2}" stroke="{colors["win"]}" stroke-width="1.5" stroke-opacity="0.7" />')

        # Antenna
        antenna_svg = ""
        if b["has_antenna"]:
            ant_top = top_y - half_h - 22
            beacon_color = COLOR_MAGENTA_NEON if lvl == 4 else COLOR_CYAN_NEON
            antenna_svg = f"""
              <line x1="{base_x}" y1="{top_y - half_h}" x2="{base_x}" y2="{ant_top}" stroke="{beacon_color}" stroke-width="1.5" />
              <circle cx="{base_x}" cy="{ant_top}" r="2" fill="{beacon_color}" filter="url(#glow-cyan)" />
              <circle cx="{base_x}" cy="{ant_top}" r="5" fill="none" stroke="{beacon_color}" stroke-width="0.75" stroke-dasharray="2,2" opacity="0.6" />
            """

        # Neon Billboard
        billboard_svg = ""
        if b["has_billboard"] and bh > 45:
            bb_x = base_x - 10
            bb_y = top_y + 12
            bb_col = COLOR_AMBER_NEON if rng.random() > 0.5 else COLOR_MAGENTA_NEON
            billboard_svg = f"""
              <rect x="{bb_x}" y="{bb_y}" width="20" height="9" rx="1.5" fill="#0c121e" stroke="{bb_col}" stroke-width="1" />
              <text x="{bb_x + 10}" y="{bb_y + 7}" fill="{bb_col}" font-family="{FONT_MONO}" font-size="6.5" font-weight="900" text-anchor="middle" letter-spacing="0.5">{esc(b['billboard_text'])}</text>
            """

        building_markup = f"""
          <g>
            <path d="{left_wall}" fill="{colors['left']}" stroke="{colors['stroke']}" stroke-width="0.5" stroke-opacity="0.6" />
            <path d="{right_wall}" fill="{colors['right']}" stroke="{colors['stroke']}" stroke-width="0.5" stroke-opacity="0.4" />
            <path d="{roof_poly}" fill="{colors['top']}" stroke="{colors['stroke']}" stroke-width="0.8" />
            {''.join(windows_svg)}
            {antenna_svg}
            {billboard_svg}
          </g>
        """
        buildings_svg.append(building_markup)

    sky_elements = f"""
      <!-- Cyberpunk Sky Gradient -->
      <defs>
        <radialGradient id="sky-synth-orb" cx="50%" cy="30%" r="50%">
          <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.25" />
          <stop offset="40%" stop-color="#a855f7" stop-opacity="0.12" />
          <stop offset="100%" stop-color="#070b13" stop-opacity="0" />
        </radialGradient>
        <linearGradient id="sky-horizon" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#040710" />
          <stop offset="60%" stop-color="#091224" />
          <stop offset="100%" stop-color="#04070e" />
        </linearGradient>
      </defs>

      <!-- Sky Background -->
      <rect x="2" y="34" width="{w - 4}" height="{h - 36}" fill="url(#sky-horizon)" />

      <!-- Synthetic Cyber Moon / Target HUD -->
      <circle cx="710" cy="130" r="54" fill="url(#sky-synth-orb)" />
      <circle cx="710" cy="130" r="44" fill="none" stroke="{COLOR_CYAN_NEON}" stroke-width="1.2" stroke-dasharray="8,4" opacity="0.45" />
      <circle cx="710" cy="130" r="30" fill="none" stroke="{COLOR_MAGENTA_NEON}" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.6" />
      <line x1="650" y1="130" x2="770" y2="130" stroke="{COLOR_CYAN_NEON}" stroke-width="0.75" stroke-opacity="0.3" />
      <line x1="710" y1="70" x2="710" y2="190" stroke="{COLOR_CYAN_NEON}" stroke-width="0.75" stroke-opacity="0.3" />
      <text x="710" y="133" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="8" font-weight="700" text-anchor="middle" letter-spacing="1">SECTOR_NODE</text>

      <!-- Cyber Flying Data Streams / Drones in Sky -->
      <line x1="120" y1="100" x2="280" y2="85" stroke="{COLOR_CYAN_NEON}" stroke-width="1.5" stroke-dasharray="40,120" stroke-opacity="0.8" filter="url(#glow-cyan)" />
      <circle cx="280" cy="85" r="2" fill="{COLOR_CYAN_NEON}" filter="url(#glow-cyan)" />
      
      <line x1="380" y1="120" x2="520" y2="105" stroke="{COLOR_MAGENTA_NEON}" stroke-width="1.5" stroke-dasharray="30,100" stroke-opacity="0.7" filter="url(#glow-magenta)" />
      <circle cx="520" cy="105" r="2" fill="{COLOR_MAGENTA_NEON}" />
    """

    hud_overlay = f"""
      <!-- Floating Holographic HUD Overlay Box (Top Left) -->
      <g transform="translate(24, 76)">
        <path d="{chamfered_rect_path(0, 0, 220, 84, chamfer=8, corner='top-right')}" fill="#080e1a" fill-opacity="0.88" stroke="{COLOR_BORDER_CYAN}" stroke-width="1" />
        
        <text x="14" y="18" fill="{COLOR_CYAN_NEON}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" letter-spacing="1">SECTOR // CONTRIBUTIONS</text>
        <line x1="14" y1="24" x2="206" y2="24" stroke="{COLOR_BORDER_MUTED}" stroke-width="0.75" />

        <text x="14" y="40" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">GRID STATUS:</text>
        <text x="110" y="40" fill="{COLOR_GREEN_NEON}" font-family="{FONT_MONO}" font-size="9.5" font-weight="700">ONLINE // 100%</text>

        <text x="14" y="56" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">VELOCITY:</text>
        <text x="110" y="56" fill="{COLOR_TEXT_BRIGHT}" font-family="{FONT_MONO}" font-size="9.5" font-weight="700">HIGH TRAFFIC</text>

        <text x="14" y="72" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">TELEMETRY:</text>
        <text x="110" y="72" fill="{COLOR_MAGENTA_NEON}" font-family="{FONT_MONO}" font-size="9.5" font-weight="700">1,420+ COMMITS</text>
      </g>

      <!-- Heatmap Legend (Bottom Right) -->
      <g transform="translate({w - 230}, {h - 44})">
        <text x="0" y="11" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">LESS</text>
        <rect x="36" y="2" width="12" height="12" rx="2" fill="#121d30" stroke="#1b2c45" stroke-width="0.5" />
        <rect x="54" y="2" width="12" height="12" rx="2" fill="#006d77" />
        <rect x="72" y="2" width="12" height="12" rx="2" fill="#00a8b5" />
        <rect x="90" y="2" width="12" height="12" rx="2" fill="#00f0ff" />
        <rect x="108" y="2" width="12" height="12" rx="2" fill="#ff007f" />
        <text x="128" y="11" fill="{COLOR_TEXT_MUTED}" font-family="{FONT_MONO}" font-size="9.5" font-weight="600">MORE</text>
      </g>
    """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  {common_defs()}
  {common_styles()}

  <!-- Main Terminal Frame -->
  <path d="{outer_path}" fill="{COLOR_BG_DEEP}" stroke="{COLOR_BORDER_CYAN}" stroke-width="1.5" />
  
  <!-- Sky and Cyber Backdrop -->
  {sky_elements}

  <!-- Ground Plane Isometric Grid -->
  {''.join(ground_circuits)}

  <!-- Render Isometric Skyscraper Cityscape -->
  {''.join(buildings_svg)}

  <!-- Holographic HUD Overlays -->
  {hud_overlay}

  <!-- Terminal Chrome Top Bar -->
  {terminal_top_bar(1, 1, w - 2, path="~/matrix/cityscape", sec_tag="// CENTERPIECE: SECTOR_CONTRIBUTIONS")}

  <!-- Terminal Command Line -->
  <g transform="translate(24, 56)">
    {command_prompt_line(0, 0, "render_cityscape --isometric --stream-telemetry")}
  </g>

  <!-- Bottom Accent Line -->
  <line x1="20" y1="{h - 18}" x2="300" y2="{h - 18}" stroke="{COLOR_CYAN_NEON}" stroke-width="1.5" stroke-opacity="0.8" />
  <text x="312" y="{h - 15}" fill="{COLOR_TEXT_DIM}" font-family="{FONT_MONO}" font-size="9" letter-spacing="1">ISO_MATRIX_RENDER: v4.2 // NIGHT_CITY_PERSPECTIVE</text>
</svg>"""
    return svg
