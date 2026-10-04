"""Automated test suite verifying the updated profile flow and georgekobaidze style."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_config_structure():
    config_file = BASE_DIR / "config.json"
    assert config_file.exists()
    data = json.loads(config_file.read_text(encoding="utf-8"))

    # Required fields
    assert "github_username" in data
    assert "display_name" in data
    assert "role" in data
    assert "links" in data
    assert "stack" in data

    # Mission and identity must be removed
    assert "interests" not in data
    assert "current_mission" not in data

    # Only 3 links
    links = data["links"]
    assert set(links.keys()) == {"facebook", "linkedin", "blog"}
    assert links["facebook"] == "https://www.facebook.com/teaman.2606"
    assert links["linkedin"] == "https://www.linkedin.com/in/temazzdev"
    assert links["blog"] == "https://dev.to/temaz_2606"


def test_readme_flow_and_no_identity_or_mission():
    readme_file = BASE_DIR / "README.md"
    assert readme_file.exists()
    content = readme_file.read_text(encoding="utf-8")

    # Flow check: links -> stats -> contribution-city -> stack -> footer
    idx_links = content.find("links-header.svg")
    idx_fb = content.find("link-facebook.svg")
    idx_stats = content.find("stats.svg")
    idx_city = content.find("contribution-city.svg")
    idx_stack = content.find("stack.svg")
    idx_footer = content.find("footer.svg")

    assert idx_links != -1
    assert idx_fb != -1
    assert idx_stats != -1
    assert idx_city != -1
    assert idx_stack != -1
    assert idx_footer != -1

    assert idx_links < idx_fb < idx_stats < idx_city < idx_stack < idx_footer

    # Identity and mission must not be present
    assert "identity.svg" not in content
    assert "current-mission.svg" not in content
    assert "whoami" not in content.lower()
    assert "current_objectives" not in content.lower()

    # Verify exact link URLs
    assert 'href="https://www.facebook.com/teaman.2606"' in content
    assert 'href="https://www.linkedin.com/in/temazzdev"' in content
    assert 'href="https://dev.to/temaz_2606"' in content


def test_assets_presence_and_cleanup():
    assets_dir = BASE_DIR / "assets"
    assert assets_dir.exists()

    required = [
        "links-header.svg",
        "link-facebook.svg",
        "link-linkedin.svg",
        "link-blog.svg",
        "stats.svg",
        "contribution-city.svg",
        "stack.svg",
        "footer.svg",
    ]
    for r in required:
        p = assets_dir / r
        assert p.exists(), f"Missing required asset: {r}"
        assert p.stat().st_size > 0

    # Ensure removed assets do not exist
    banned = ["identity.svg", "current-mission.svg", "header.svg", "projects", "writing"]
    for b in banned:
        assert not (assets_dir / b).exists(), f"Banned asset {b} should not exist"
