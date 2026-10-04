#!/usr/bin/env python3
"""GitHub Profile Telemetry Fetcher.

Fetches live GitHub telemetry via GitHub GraphQL API:
- User stats (stars, forks, PRs, merged PRs, followers, member since)
- Contribution history (53-week calendar, contributions year & all time)
- Streak calculations (current streak, longest streak)
- Language breakdown across public repositories

Saves outputs to:
- data/calendar.json
- data/stats.json

Provides graceful fallbacks so builds and local runs never crash if
GITHUB_TOKEN is missing or API limits are encountered.
"""

import datetime
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UA = "cyberpunk-profile-telemetry-bot"

DEFAULT_STATS = {
    "username": "ManTT-Data",
    "created_at": "2023-10-15T00:00:00Z",
    "followers": 12,
    "prs": 52,
    "prs_merged": 48,
    "stars": 48,
    "forks": 8,
    "repo_stars": {},
    "languages": {
        "Python": 154200,
        "TypeScript": 98400,
        "C#": 72500,
        "Go": 48100,
        "SQL": 28900,
    },
    "year": 2026,
    "commits_year": 940,
    "commits_all": 1420,
    "contributions_year": 1322,
    "contributions_all": 1649,
    "streak_current": 34,
    "streak_longest": 42,
    "updated": "2026-10-04",
}


def log_warn(msg: str):
    """Print warning, formatting for GitHub Actions annotations if in CI."""
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::warning::{msg}", file=sys.stderr)
    else:
        print(f"[!] Warning: {msg}", file=sys.stderr)


def load_config() -> dict:
    """Load configuration from config.json."""
    config_path = BASE_DIR / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as ex:
            log_warn(f"Failed to read config.json: {ex}")
    return {}


def load_json(filename: str, default=None):
    """Load a json file from data/ directory."""
    path = DATA_DIR / filename
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as ex:
            log_warn(f"Could not parse {filename}: {ex}")
    return default


def save_json(filename: str, obj):
    """Save an object to data/ directory formatted as JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[+] Saved {path}")


def http_json(url: str, *, headers=None, body=None, timeout: int = 30):
    """Perform HTTP JSON request using standard library."""
    data = None if body is None else json.dumps(body).encode("utf-8")
    req_headers = {"User-Agent": UA, "Accept": "application/json", **(headers or {})}
    if body is not None:
        req_headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def graphql_query(token: str, query: str, variables: dict = None) -> dict:
    """Execute GraphQL query against GitHub API."""
    res = http_json(
        "https://api.github.com/graphql",
        headers={"Authorization": f"bearer {token}"},
        body={"query": query, "variables": variables or {}},
    )
    if res.get("errors"):
        msg = "; ".join(e.get("message", "?") for e in res["errors"])
        raise RuntimeError(f"GitHub GraphQL error: {msg}")
    return res["data"]


PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    pullRequests { totalCount }
    merged: pullRequests(states: MERGED) { totalCount }
    contributionsCollection { contributionYears }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      nodes {
        name
        stargazerCount
        forkCount
        languages(first: 20) { edges { size node { name } } }
      }
    }
  }
}
"""


def build_years_query(years: list) -> str:
    """Build GraphQL query for multiple contribution years."""
    parts = []
    for y in years:
        parts.append(f"""
    y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") {{
      totalCommitContributions
      contributionCalendar {{
        totalContributions
        weeks {{
          contributionDays {{
            date
            contributionCount
          }}
        }}
      }}
    }}""")
    return "query($login: String!) {\n  user(login: $login) {" + "".join(parts) + "\n  }\n}"


def calculate_streaks(days: dict, today: datetime.date) -> tuple:
    """Calculate current and longest contribution streaks."""
    dates = sorted(d for d in days.keys() if d <= today)
    longest = run = 0
    for d in dates:
        run = run + 1 if days[d] > 0 else 0
        longest = max(longest, run)

    current, d = 0, today
    # If today has no contributions yet, streak might continue from yesterday
    if days.get(d, 0) == 0:
        d -= datetime.timedelta(days=1)
    while days.get(d, 0) > 0:
        current += 1
        d -= datetime.timedelta(days=1)

    return current, longest


def fetch_github_telemetry(username: str, token: str, today: datetime.date) -> dict:
    """Fetch profile data and contribution calendar from GitHub GraphQL API."""
    data = graphql_query(token, PROFILE_QUERY, {"login": username})
    user = data.get("user")
    if not user:
        raise ValueError(f"GitHub user '{username}' not found.")

    years = sorted(user["contributionsCollection"]["contributionYears"])
    ydata = graphql_query(token, build_years_query(years), {"login": username})["user"] if years else {}

    days = {}
    commits_all = 0
    contribs_all = 0

    for y in years:
        c = ydata.get(f"y{y}")
        if not c:
            continue
        commits_all += c.get("totalCommitContributions", 0)
        cal = c.get("contributionCalendar", {})
        contribs_all += cal.get("totalContributions", 0)
        for w in cal.get("weeks", []):
            for day in w.get("contributionDays", []):
                try:
                    d_obj = datetime.date.fromisoformat(day["date"])
                    days[d_obj] = day["contributionCount"]
                except Exception:
                    pass

    current_streak, longest_streak = calculate_streaks(days, today)

    # 53 weeks back, aligned to Sunday like GitHub contribution graph
    start = today - datetime.timedelta(weeks=52)
    start -= datetime.timedelta(days=(start.weekday() + 1) % 7)
    calendar_list = [
        [d.isoformat(), days.get(d, 0)]
        for d in (start + datetime.timedelta(days=i) for i in range((today - start).days + 1))
    ]

    repos = user.get("repositories", {}).get("nodes", [])
    langs = {}
    for r in repos:
        for edge in r.get("languages", {}).get("edges", []):
            lang_name = edge["node"]["name"]
            langs[lang_name] = langs.get(lang_name, 0) + edge["size"]

    cur_year = ydata.get(f"y{today.year}", {})
    commits_this_year = cur_year.get("totalCommitContributions", 0)
    contribs_this_year = cur_year.get("contributionCalendar", {}).get("totalContributions", 0)

    stats = {
        "username": username,
        "created_at": user.get("createdAt"),
        "followers": user.get("followers", {}).get("totalCount", 0),
        "prs": user.get("pullRequests", {}).get("totalCount", 0),
        "prs_merged": user.get("merged", {}).get("totalCount", 0),
        "stars": sum(r.get("stargazerCount", 0) for r in repos),
        "forks": sum(r.get("forkCount", 0) for r in repos),
        "repo_stars": {r["name"]: r.get("stargazerCount", 0) for r in repos if "name" in r},
        "languages": dict(sorted(langs.items(), key=lambda kv: -kv[1])),
        "year": today.year,
        "commits_year": commits_this_year,
        "commits_all": commits_all,
        "contributions_year": contribs_this_year,
        "contributions_all": contribs_all,
        "streak_current": current_streak,
        "streak_longest": longest_streak,
        "updated": today.isoformat(),
        "_calendar": calendar_list,
    }
    return stats


def main():
    config = load_config()
    username = config.get("github_username", "ManTT-Data")
    today = datetime.datetime.now(datetime.timezone.utc).date()

    print(f"[*] Starting GitHub Telemetry Fetch for user: {username}")
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")

    if not token:
        log_warn("No GITHUB_TOKEN or PROFILE_TOKEN found in environment.")
        print("[*] Retaining existing data in data/ or generating default stats.")
        existing_stats = load_json("stats.json")
        if not existing_stats:
            fallback = DEFAULT_STATS.copy()
            fallback["username"] = username
            fallback["year"] = today.year
            fallback["updated"] = today.isoformat()
            save_json("stats.json", fallback)
        return

    try:
        print("[*] Querying GitHub GraphQL API...")
        stats = fetch_github_telemetry(username, token, today)
        calendar = stats.pop("_calendar")
        save_json("calendar.json", calendar)
        save_json("stats.json", stats)
        print(f"[+] Successfully synchronized live GitHub telemetry for {username}!")
    except Exception as ex:
        log_warn(f"GitHub telemetry fetch failed: {ex}")
        existing_stats = load_json("stats.json")
        if not existing_stats:
            fallback = DEFAULT_STATS.copy()
            fallback["username"] = username
            fallback["year"] = today.year
            fallback["updated"] = today.isoformat()
            save_json("stats.json", fallback)


if __name__ == "__main__":
    main()
