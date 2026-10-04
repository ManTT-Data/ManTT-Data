"""Automated verification suite for simplified cyberpunk profile."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_config_compliance():
    """Verify Section 7: Updated Config."""
    config_file = BASE_DIR / "config.json"
    assert config_file.exists()
    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Required fields
    assert "github_username" in data
    assert "display_name" in data
    assert "role" in data
    assert "tagline" in data
    assert "interests" in data
    assert "current_mission" in data
    assert "links" in data

    # Prohibited fields
    forbidden_keys = [
        "dev_username",
        "featured_projects",
        "youtube",
        "twitter",
        "discord",
        "email",
        "portfolio",
    ]
    for key in forbidden_keys:
        assert key not in data, f"Forbidden config key '{key}' found in config.json"

    # Only the 3 authorized links
    links = data["links"]
    assert set(links.keys()) == {"facebook", "linkedin", "blog"}
    assert links["facebook"] == "https://www.facebook.com/teaman.2606"
    assert links["linkedin"] == "https://www.linkedin.com/in/temazzdev"
    assert links["blog"] == "https://dev.to/temaz_2606"


def test_no_projects_or_writing_sections_in_readme():
    """Verify Sections 2, 3 & 5: No Projects or Writing in README."""
    readme_file = BASE_DIR / "README.md"
    assert readme_file.exists()
    content = readme_file.read_text(encoding="utf-8").lower()

    # Banned terminal commands & markers
    assert "$ ls ~/projects" not in content
    assert "featured projects" not in content
    assert "latest transmissions" not in content
    assert "$ fetch ~/writing" not in content
    assert "assets/projects" not in content
    assert "assets/writing" not in content


def test_links_in_readme_and_exact_urls():
    """Verify Section 1 & 8: Clickable link behavior in README."""
    readme_file = BASE_DIR / "README.md"
    content = readme_file.read_text(encoding="utf-8")

    assert "https://www.facebook.com/teaman.2606" in content
    assert "https://www.linkedin.com/in/temazzdev" in content
    assert "https://dev.to/temaz_2606" in content

    # Verify link wrapping
    assert '<a href="https://www.facebook.com/teaman.2606"' in content
    assert '<a href="https://www.linkedin.com/in/temazzdev"' in content
    assert '<a href="https://dev.to/temaz_2606"' in content

    # Verify no other social platforms in links
    forbidden_domains = ["twitter.com", "x.com", "youtube.com", "discord.gg", "mailto:"]
    for domain in forbidden_domains:
        assert domain not in content


def test_assets_integrity():
    """Verify Section 6: Assets structure."""
    assets_dir = BASE_DIR / "assets"
    assert assets_dir.exists()

    required_assets = [
        "header.svg",
        "identity.svg",
        "system-status.svg",
        "tech-stack.svg",
        "contribution-city.svg",
        "current-mission.svg",
        "links-header.svg",
        "link-facebook.svg",
        "link-linkedin.svg",
        "link-blog.svg",
        "links-footer.svg",
        "links.svg",
        "footer.svg",
    ]
    for asset in required_assets:
        asset_path = assets_dir / asset
        assert asset_path.exists(), f"Missing required asset: {asset}"
        assert asset_path.stat().st_size > 0, f"Asset is empty: {asset}"

    # Ensure no project or writing asset dirs
    assert not (assets_dir / "projects").exists()
    assert not (assets_dir / "writing").exists()


def test_no_dead_code_or_dev_api():
    """Verify Section 4: Remove unused code & DEV API calls."""
    scripts_dir = BASE_DIR / "scripts"
    py_files = list(scripts_dir.rglob("*.py"))
    
    for f in py_files:
        code = f.read_text(encoding="utf-8")
        assert "api.forem.com" not in code, f"DEV API found in {f}"
        assert "dev_api" not in f.name, f"dev_api found in filename {f}"
        assert "project" not in f.name, f"project renderer found in {f}"
        assert "writing" not in f.name, f"writing renderer found in {f}"
