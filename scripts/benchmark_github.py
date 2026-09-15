#!/usr/bin/env python3
"""Fetch public GitHub metadata for launch benchmarks.

Read-only usage:
  python3 scripts/benchmark_github.py --config benchmarks/representative-tools.json

GITHUB_TOKEN is optional and is never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


API_ROOT = "https://api.github.com/repos"


def load_config(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("benchmark config must be a JSON array")
    normalized: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("repo"), str):
            raise ValueError("each benchmark entry must be an object with a repo string")
        normalized.append(
            {
                "repo": item["repo"],
                "category": str(item.get("category", "")),
                "why": str(item.get("why", "")),
            }
        )
    return normalized


def fetch_repo(repo: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{API_ROOT}/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-launch-studio-benchmark",
            "X-GitHub-Api-Version": "2022-11-28",
            **(
                {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
                if os.environ.get("GITHUB_TOKEN")
                else {}
            ),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code in {403, 429}:
            raise RuntimeError(
                "GitHub API rate limit reached; set GITHUB_TOKEN or rerun later"
            ) from error
        if error.code == 404:
            return {"full_name": repo, "missing": True}
        raise RuntimeError(f"GitHub API failed for {repo}: HTTP {error.code}") from error


def normalize(entry: dict[str, str], raw: dict[str, Any]) -> dict[str, Any]:
    if raw.get("missing"):
        return {"repo": entry["repo"], "missing": True, "category": entry["category"], "why": entry["why"]}
    license_info = raw.get("license") or {}
    return {
        "repo": raw.get("full_name", entry["repo"]),
        "url": raw.get("html_url", f"https://github.com/{entry['repo']}"),
        "category": entry["category"],
        "why": entry["why"],
        "description": raw.get("description"),
        "stars": raw.get("stargazers_count", 0),
        "forks": raw.get("forks_count", 0),
        "open_issues": raw.get("open_issues_count", 0),
        "language": raw.get("language"),
        "license": license_info.get("spdx_id") if isinstance(license_info, dict) else None,
        "homepage": raw.get("homepage") or None,
        "topics": raw.get("topics", []),
        "created_at": raw.get("created_at"),
        "pushed_at": raw.get("pushed_at"),
        "archived": bool(raw.get("archived")),
    }


def markdown(rows: list[dict[str, Any]], observed_at: str) -> str:
    lines = [
        f"Observed: {observed_at}",
        "",
        "| Category | Repository | Stars | Forks | Last push | License | Job |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        if row.get("missing"):
            lines.append(f"| {row['category']} | `{row['repo']}` | — | — | — | — | Missing repository |")
            continue
        lines.append(
            "| {category} | [{repo}]({url}) | {stars:,} | {forks:,} | {last_push} | {license} | {why} |".format(
                category=row["category"],
                repo=row["repo"],
                url=row["url"],
                stars=int(row["stars"]),
                forks=int(row["forks"]),
                last_push=(row.get("pushed_at") or "")[:10],
                license=row.get("license") or "—",
                why=row["why"].replace("|", "\\|"),
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch read-only GitHub benchmark metadata")
    parser.add_argument("repos", nargs="*", help="owner/repo slugs")
    parser.add_argument("--config", type=Path, help="JSON config with repo, category, and why fields")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    entries: list[dict[str, str]] = []
    if args.config:
        entries.extend(load_config(args.config))
    entries.extend({"repo": repo, "category": "", "why": ""} for repo in args.repos)
    if not entries:
        parser.error("provide at least one owner/repo or --config")

    seen: set[str] = set()
    unique_entries = [
        entry for entry in entries
        if not (entry["repo"].lower() in seen or seen.add(entry["repo"].lower()))
    ]

    try:
        rows = [normalize(entry, fetch_repo(entry["repo"])) for entry in unique_entries]
    except Exception as error:  # noqa: BLE001 - CLI should print a concise actionable error
        print(f"error: {error}", file=sys.stderr)
        return 1

    observed_at = datetime.now(timezone.utc).date().isoformat()
    if args.format == "markdown":
        print(markdown(rows, observed_at))
    else:
        print(json.dumps({"observed_at": observed_at, "repositories": rows}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
