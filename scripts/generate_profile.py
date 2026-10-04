#!/usr/bin/env python3
"""Cyberpunk GitHub Profile Generator.

Orchestrates rendering of all profile SVG assets and generates the README.md
following the simplified cyberpunk profile specification.
"""

import json
import os
import shutil
import sys
from pathlib import Path

# Add project root and scripts directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.renderers.contribution_city import render_contribution_city
from scripts.renderers.current_mission import render_current_mission
from scripts.renderers.footer import render_footer
from scripts.renderers.header import render_header
from scripts.renderers.identity import render_identity
from scripts.renderers.links import (
    ICON_BLOG_DEV_PATH,
    ICON_FACEBOOK_PATH,
    ICON_LINKEDIN_PATH,
    render_link_facebook,
    render_link_linkedin,
    render_link_blog,
    render_links_footer,
    render_links_header,
    render_single_link_card,
    render_unified_links,
)
from scripts.renderers.system_status import render_system_status
from scripts.renderers.tech_stack import render_tech_stack


def load_config() -> dict:
    """Load configuration from config.json."""
    config_path = BASE_DIR / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def cleanup_dead_directories(assets_dir: Path):
    """Enforce requirement: No assets/projects/ or assets/writing/."""
    for unwanted in ["projects", "writing"]:
        unwanted_path = assets_dir / unwanted
        if unwanted_path.exists() and unwanted_path.is_dir():
            print(f"[*] Removing dead directory: {unwanted_path}")
            shutil.rmtree(unwanted_path)


def generate_assets(config: dict, assets_dir: Path):
    """Generate all SVG assets into the assets/ directory."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    cleanup_dead_directories(assets_dir)

    print("[*] Generating Hero Header (assets/header.svg)...")
    (assets_dir / "header.svg").write_text(render_header(config), encoding="utf-8")

    print("[*] Generating Identity (assets/identity.svg)...")
    (assets_dir / "identity.svg").write_text(render_identity(config), encoding="utf-8")

    print("[*] Generating System Status (assets/system-status.svg)...")
    (assets_dir / "system-status.svg").write_text(render_system_status(config), encoding="utf-8")

    print("[*] Generating Tech Stack (assets/tech-stack.svg)...")
    (assets_dir / "tech-stack.svg").write_text(render_tech_stack(config), encoding="utf-8")

    print("[*] Generating Contribution City Centerpiece (assets/contribution-city.svg)...")
    (assets_dir / "contribution-city.svg").write_text(render_contribution_city(config), encoding="utf-8")

    print("[*] Generating Current Mission (assets/current-mission.svg)...")
    (assets_dir / "current-mission.svg").write_text(render_current_mission(config), encoding="utf-8")

    print("[*] Generating Links Section SVGs...")
    (assets_dir / "links-header.svg").write_text(render_links_header(config), encoding="utf-8")

    # Generate the 3 individual clickable cards
    (assets_dir / "link-facebook.svg").write_text(render_link_facebook(config), encoding="utf-8")
    (assets_dir / "link-linkedin.svg").write_text(render_link_linkedin(config), encoding="utf-8")
    (assets_dir / "link-blog.svg").write_text(render_link_blog(config), encoding="utf-8")


    (assets_dir / "links-footer.svg").write_text(render_links_footer(config), encoding="utf-8")
    (assets_dir / "links.svg").write_text(render_unified_links(config), encoding="utf-8")

    print("[*] Generating Footer (assets/footer.svg)...")
    (assets_dir / "footer.svg").write_text(render_footer(config), encoding="utf-8")

    print("[+] All assets generated successfully!")


def generate_readme(config: dict, output_file: Path):
    """Generate README.md with the updated profile flow and clickable links."""
    links_cfg = config.get("links", {})
    fb_url = links_cfg.get("facebook", "https://www.facebook.com/teaman.2606")
    li_url = links_cfg.get("linkedin", "https://www.linkedin.com/in/temazzdev")
    blog_url = links_cfg.get("blog", "https://dev.to/temaz_2606")

    content = f"""<div align="center">

<!-- ================================================================ -->
<!-- 1. BOOT / HERO                                                   -->
<!-- ================================================================ -->
<img src="assets/header.svg" width="900" alt="Cyberpunk Profile Header" />

<br/><br/>

<!-- ================================================================ -->
<!-- 2. WHOAMI / IDENTITY                                             -->
<!-- ================================================================ -->
<img src="assets/identity.svg" width="900" alt="Whoami Identity" />

<br/><br/>

<!-- ================================================================ -->
<!-- 3. SYSTEM STATUS / GITHUB STATS                                  -->
<!-- ================================================================ -->
<img src="assets/system-status.svg" width="900" alt="System Status &amp; GitHub Telemetry" />

<br/><br/>

<!-- ================================================================ -->
<!-- 4. TECH STACK                                                    -->
<!-- ================================================================ -->
<img src="assets/tech-stack.svg" width="900" alt="Tech Stack &amp; Runtime Capabilities" />

<br/><br/>

<!-- ================================================================ -->
<!-- 5. CYBERPUNK CONTRIBUTION CITY (VISUAL CENTERPIECE)              -->
<!-- ================================================================ -->
<img src="assets/contribution-city.svg" width="900" alt="Cyberpunk Contribution City Centerpiece" />

<br/><br/>

<!-- ================================================================ -->
<!-- 6. CURRENT MISSION / ACTIVITY                                    -->
<!-- ================================================================ -->
<img src="assets/current-mission.svg" width="900" alt="Current Mission Directives" />

<br/><br/>

<!-- ================================================================ -->
<!-- 7. LINKS / TERMINAL CHANNELS (INDIVIDUALLY CLICKABLE)            -->
<!-- ================================================================ -->
<img src="assets/links-header.svg" width="900" alt="~/links - ping temazzdev --all-channels" /><br/>
<table border="0" cellpadding="0" cellspacing="6" align="center" style="border: none; background: transparent; width: 100%; max-width: 900px; margin: 4px 0;">
  <tr>
    <td width="33.33%" align="center" style="border: none; padding: 0;">
      <a href="{fb_url}" target="_blank" rel="noopener noreferrer">
        <img src="assets/link-facebook.svg" width="100%" alt="Facebook: teaman.2606" />
      </a>
    </td>
    <td width="33.33%" align="center" style="border: none; padding: 0;">
      <a href="{li_url}" target="_blank" rel="noopener noreferrer">
        <img src="assets/link-linkedin.svg" width="100%" alt="LinkedIn: temazzdev" />
      </a>
    </td>
    <td width="33.33%" align="center" style="border: none; padding: 0;">
      <a href="{blog_url}" target="_blank" rel="noopener noreferrer">
        <img src="assets/link-blog.svg" width="100%" alt="Blog: DEV.to" />
      </a>
    </td>
  </tr>
</table>
<img src="assets/links-footer.svg" width="900" alt="Terminal Ping Footer" />

<br/><br/>

<!-- ================================================================ -->
<!-- 8. FOOTER / EOF                                                  -->
<!-- ================================================================ -->
<img src="assets/footer.svg" width="900" alt="Cyberpunk Profile Footer" />

</div>
"""

    output_file.write_text(content, encoding="utf-8")
    print(f"[+] README.md written to {output_file}")


def main():
    config = load_config()
    assets_dir = BASE_DIR / "assets"
    readme_path = BASE_DIR / "README.md"

    print("==================================================")
    print("  CYBERPUNK PROFILE GENERATOR (SIMPLIFIED V4.2)   ")
    print("==================================================")
    print(f"Target User: {config.get('github_username')}")
    print(f"Display Name: {config.get('display_name')}")
    print(f"Role: {config.get('role')}")

    generate_assets(config, assets_dir)
    generate_readme(config, readme_path)
    print("==================================================")
    print("  BUILD COMPLETE                                  ")
    print("==================================================")


if __name__ == "__main__":
    main()
