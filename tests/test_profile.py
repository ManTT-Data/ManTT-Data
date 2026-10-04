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


def test_data_files_and_schema():
    calendar_file = BASE_DIR / "data" / "calendar.json"
    stats_file = BASE_DIR / "data" / "stats.json"

    assert calendar_file.exists(), "data/calendar.json must exist"
    assert stats_file.exists(), "data/stats.json must exist"

    calendar = json.loads(calendar_file.read_text(encoding="utf-8"))
    stats = json.loads(stats_file.read_text(encoding="utf-8"))

    # Calendar validations
    assert isinstance(calendar, list)
    assert len(calendar) >= 365
    assert len(calendar[0]) == 2
    assert isinstance(calendar[0][0], str)
    assert isinstance(calendar[0][1], int)

    # Stats validations
    assert "stars" in stats
    assert "contributions_year" in stats
    assert "contributions_all" in stats
    assert "streak_current" in stats
    assert "streak_longest" in stats
    assert "followers" in stats
    assert "languages" in stats
    assert isinstance(stats["languages"], dict)


def test_github_workflow_configuration():
    workflow_file = BASE_DIR / ".github" / "workflows" / "update-profile.yml"
    assert workflow_file.exists(), "Workflow file update-profile.yml must exist"
    content = workflow_file.read_text(encoding="utf-8")

    assert "fetch_data.py" in content
    assert "generate_profile.py" in content
    assert "test_profile.py" in content
    assert "GITHUB_TOKEN" in content
    assert "contents: write" in content

