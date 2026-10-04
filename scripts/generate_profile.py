#!/usr/bin/env python3
"""Cyberpunk GitHub Profile Generator.

Generates the profile SVG slices and README.md with the flow:
links -> Stat -> contribution city -> stack -> EOF
matching the console style of georgekobaidze/georgekobaidze.
"""

import json
import os
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.renderers.contribution_city import render_contribution_city
from scripts.renderers.footer import render_footer
from scripts.renderers.links import (
    render_link_blog,
    render_link_facebook,
    render_link_linkedin,
    render_links_head,
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


def cleanup_stale_assets(assets_dir: Path):
    """Remove obsolete asset files from previous flows."""
    stale_files = [
        "identity.svg",
        "current-mission.svg",
        "header.svg",
        "system-status.svg",
        "tech-stack.svg",
        "links.svg",
        "links-footer.svg",
    ]
    for stale in stale_files:
        p = assets_dir / stale
        if p.exists():
            p.unlink()
    # Remove unwanted folders if any
    for unwanted in ["projects", "writing"]:
        p = assets_dir / unwanted
        if p.exists() and p.is_dir():
            shutil.rmtree(p)


def generate_assets(config: dict, assets_dir: Path):
    """Generate all SVG assets for the profile."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    cleanup_stale_assets(assets_dir)

    print("[*] Generating Links Header (assets/links-header.svg)...")
    (assets_dir / "links-header.svg").write_text(render_links_head(config), encoding="utf-8")

    print("[*] Generating 3 Clickable Link Buttons (Facebook, LinkedIn, Blog)...")
    (assets_dir / "link-facebook.svg").write_text(render_link_facebook(config), encoding="utf-8")
    (assets_dir / "link-linkedin.svg").write_text(render_link_linkedin(config), encoding="utf-8")
    (assets_dir / "link-blog.svg").write_text(render_link_blog(config), encoding="utf-8")

    print("[*] Generating Stats (assets/stats.svg)...")
    (assets_dir / "stats.svg").write_text(render_system_status(config), encoding="utf-8")

    print("[*] Generating Contribution City (assets/contribution-city.svg)...")
    (assets_dir / "contribution-city.svg").write_text(render_contribution_city(config), encoding="utf-8")

    print("[*] Generating Tech Stack (assets/stack.svg)...")
    (assets_dir / "stack.svg").write_text(render_tech_stack(config), encoding="utf-8")

    print("[*] Generating Footer (assets/footer.svg)...")
    (assets_dir / "footer.svg").write_text(render_footer(config), encoding="utf-8")

    print("[+] All assets generated successfully!")


def generate_readme(config: dict, output_file: Path):
    """Generate README.md with the flow: links -> Stat -> contribution city -> stack -> EOF."""
    links_cfg = config.get("links", {})
    fb_url = links_cfg.get("facebook", "https://www.facebook.com/teaman.2606")
    li_url = links_cfg.get("linkedin", "https://www.linkedin.com/in/temazzdev")
    blog_url = links_cfg.get("blog", "https://dev.to/temaz_2606")

    content = f"""<p align="center">
<img src="./assets/links-header.svg" width="100%" align="top" alt="Links">
<a href="{fb_url}" target="_blank" rel="noopener noreferrer"><img src="./assets/link-facebook.svg" width="33.333%" align="top" alt="Facebook: teaman.2606"></a><a href="{li_url}" target="_blank" rel="noopener noreferrer"><img src="./assets/link-linkedin.svg" width="33.333%" align="top" alt="LinkedIn: temazzdev"></a><a href="{blog_url}" target="_blank" rel="noopener noreferrer"><img src="./assets/link-blog.svg" width="33.333%" align="top" alt="Blog: DEV.to"></a>
<img src="./assets/stats.svg" width="100%" align="top" alt="Stats: GitHub Telemetry">
<img src="./assets/contribution-city.svg" width="100%" align="top" alt="Contribution city: an isometric night skyline with one building per day of the last year">
<img src="./assets/stack.svg" width="100%" align="top" alt="Tech stack">
<img src="./assets/footer.svg" width="100%" align="top" alt="Connection closed. // EOF">
</p>
"""
    output_file.write_text(content, encoding="utf-8")
    print(f"[+] README.md written to {output_file}")


def main():
    config = load_config()
    assets_dir = BASE_DIR / "assets"
    readme_path = BASE_DIR / "README.md"

    print("==================================================")
    print("  CYBERPUNK PROFILE GENERATOR (GEORGEKOBAIDZE)    ")
    print("==================================================")
    print(f"Target User: {config.get('github_username')}")
    print(f"Flow: links -> Stat -> contribution city -> stack -> EOF")

    generate_assets(config, assets_dir)
    generate_readme(config, readme_path)
    print("==================================================")
    print("  BUILD COMPLETE                                  ")
    print("==================================================")


if __name__ == "__main__":
    main()
