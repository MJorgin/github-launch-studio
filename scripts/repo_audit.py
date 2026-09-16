#!/usr/bin/env python3
"""Read-only launch-readiness audit for a GitHub project.

The script collects repository signals that are useful before a first public
launch or major release. It does not contact the network and never prints the
contents of files that may contain credentials.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit, urlunsplit


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "coverage",
    ".next",
    ".turbo",
    ".cache",
    "__pycache__",
}

TEXT_LIMIT = 300_000
MAX_TREE_FILES = 30_000

DOC_DIR_HINTS = {"docs", "doc", "documentation", "references", "examples", "example", "demo", "demos"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".m4v"}

MANIFEST_FILES = [
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "composer.json",
    "pubspec.yaml",
    "deno.json",
    "deno.jsonc",
    "requirements.txt",
    "environment.yml",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
]

LOCK_FILES = [
    "pnpm-lock.yaml",
    "package-lock.json",
    "yarn.lock",
    "bun.lockb",
    "bun.lock",
    "poetry.lock",
    "uv.lock",
    "Pipfile.lock",
    "Cargo.lock",
    "go.sum",
    "composer.lock",
    "pubspec.lock",
]

SECRET_FILE_RE = re.compile(
    r"(^|/)(\.env(\.[\w.-]+)?|id_rsa(\.pub)?|.*\.(pem|key|p12|pfx|keystore)|"
    r".*(secret|credential|credentials)[\w.-]*\.(json|ya?ml|txt|config))$",
    re.IGNORECASE,
)


def read_text(path: Path, limit: int = TEXT_LIMIT) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def safe_remote_url(value: str | None) -> str | None:
    """Redact userinfo that can appear in a URL-shaped remote."""
    if not value:
        return None

    try:
        parsed = urlsplit(value)
        if parsed.username is not None or parsed.password is not None:
            host_and_port = parsed.netloc.rsplit("@", 1)[-1]
            return urlunsplit(parsed._replace(netloc=host_and_port))
    except ValueError:
        return value
    return value


def parse_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(read_text(path, 200_000))
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def first_match(pattern: str, text: str, group: int = 1) -> str | None:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(group).strip() if match else None


def discover_tree(root: Path) -> dict[str, Any]:
    files: list[Path] = []
    relative_files: set[str] = set()
    top_level_dirs: set[str] = set()
    secret_candidates: list[str] = []
    media: list[dict[str, Any]] = []
    manifests: list[str] = []
    lockfiles: list[str] = []
    truncated = False

    for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current = Path(dirpath)
        rel_parts = current.relative_to(root).parts
        depth = len(rel_parts)

        if depth == 0:
            top_level_dirs.update(d.casefold() for d in dirnames)

        dirnames[:] = [
            name for name in dirnames
            if name not in SKIP_DIRS and not (name.startswith(".") and depth >= 2)
        ]

        if depth >= 4:
            dirnames[:] = []

        for filename in filenames:
            path = current / filename
            rel = path.relative_to(root).as_posix()
            rel_lower = rel.casefold()
            files.append(path)
            relative_files.add(rel_lower)

            if len(files) >= MAX_TREE_FILES:
                truncated = True
                break

            basename = Path(filename).name
            if basename in MANIFEST_FILES:
                manifests.append(rel)
            if basename in LOCK_FILES:
                lockfiles.append(rel)
            is_env_template = re.search(
                r"(^|/)\.env\.(example|sample|template)(\.[\w-]+)?$",
                rel_lower,
            )
            if SECRET_FILE_RE.search(rel_lower) and not is_env_template:
                secret_candidates.append(rel)

            ext = path.suffix.casefold()
            if ext in IMAGE_EXTS | VIDEO_EXTS:
                try:
                    size = path.stat().st_size
                except OSError:
                    size = None
                media.append({"path": rel, "type": "video" if ext in VIDEO_EXTS else "image", "bytes": size})

        if truncated:
            break

    return {
        "files": files,
        "relative_files": relative_files,
        "top_level_dirs": top_level_dirs,
        "secret_candidates": sorted(set(secret_candidates)),
        "media": sorted(media, key=lambda item: item["path"]),
        "manifests": sorted(set(manifests)),
        "lockfiles": sorted(set(lockfiles)),
        "truncated": truncated,
    }


def choose_readme(root: Path, relative_files: set[str]) -> Path | None:
    preferred = [
        "readme.md",
        "readme_en.md",
        "readme.en.md",
        "readme-zh.md",
        "readme.zh-cn.md",
    ]
    for name in preferred:
        if name in relative_files:
            return root / name

    root_readmes = sorted(
        str(path) for path in relative_files
        if "/" not in path and re.fullmatch(r"readme(\.[\w-]+)?\.md", path)
    )
    if root_readmes:
        return root / root_readmes[0]

    nested = sorted(
        path for path in relative_files
        if re.fullmatch(r".*readme(\.[\w-]+)?\.md", path)
    )
    return root / nested[0] if nested else None


def analyze_readme(root: Path, readme_path: Path | None) -> dict[str, Any]:
    if readme_path is None or not readme_path.exists():
        return {"path": None, "exists": False}

    text = read_text(readme_path)
    lines = text.splitlines()
    headings = [
        re.sub(r"^#+\s*", "", line).strip()
        for line in lines
        if line.startswith("#")
    ]
    heading_lower = {heading.casefold() for heading in headings}

    links: list[dict[str, Any]] = []
    broken_links: list[str] = []
    images = 0
    empty_image_alts = 0

    for is_image, alt, raw_url in re.findall(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        url = raw_url.strip("<>")
        parsed = urlsplit(url)
        is_image_markdown = bool(is_image)
        if is_image_markdown:
            images += 1
            if not alt.strip():
                empty_image_alts += 1

        entry = {"url": url, "image": is_image_markdown}
        links.append(entry)

        if parsed.scheme in {"http", "https", "mailto", "tel"} or url.startswith("#"):
            continue

        relative = unquote(parsed.path or url.split("#", 1)[0])
        if not relative:
            continue
        target = (readme_path.parent / relative).resolve()
        entry["resolved_path"] = str(target.relative_to(root)) if target.is_relative_to(root) else str(target)
        if not target.exists():
            broken_links.append(url)

    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_chars = len(re.findall(r"[A-Za-z]", text))

    heading_terms = {
        "overview": bool(
            heading_lower
            & {"overview", "about", "introduction", "features", "when to use it", "what it does", "功能", "简介", "介绍"}
        ),
        "installation": any("install" in item or "setup" in item or "安装" in item for item in heading_lower),
        "quick_start": any(
            "quick" in item or "getting started" in item or "快速" in item or "上手" in item
            for item in heading_lower
        ),
        "usage": any("usage" in item or "use " in item or "usage" in item or "使用" in item or "用法" in item for item in heading_lower),
        "examples": any("example" in item or "示例" in item or "例子" in item for item in heading_lower),
        "limitations": any("limitation" in item or "faq" in item or "known issue" in item or "限制" in item or "常见问题" in item for item in heading_lower),
        "contributing": any("contribut" in item or "贡献" in item for item in heading_lower),
    }

    return {
        "path": readme_path.relative_to(root).as_posix(),
        "exists": True,
        "line_count": len(lines),
        "title": next((re.sub(r"^#\s*", "", line).strip() for line in lines if line.startswith("# ")), None),
        "headings": headings[:40],
        "heading_signals": heading_terms,
        "code_fences": len(re.findall(r"^```", text, re.MULTILINE)),
        "images": images,
        "empty_image_alts": empty_image_alts,
        "links": len(links),
        "broken_relative_links": sorted(set(broken_links)),
        "badge_count": len(re.findall(r"img\.shields\.io|badge/|github\.com/.+/actions/workflows", text)),
        "cjk_ratio": round(cjk_chars / max(cjk_chars + latin_chars, 1), 3),
        "has_english_readme": cjk_chars < latin_chars,
        "bilingual_readme_link": any(
            re.search(r"readme[._-]?zh|中文|chinese", link["url"], re.IGNORECASE)
            for link in links
        ),
    }


def analyze_manifests(root: Path, manifest_paths: list[str]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for rel in manifest_paths:
        path = root / rel
        name = path.name
        entry: dict[str, Any] = {"path": rel, "type": name}

        if name == "package.json":
            data = parse_json(path)
            entry.update(
                name=data.get("name"),
                description=data.get("description"),
                package_manager=data.get("packageManager"),
                scripts=sorted((data.get("scripts") or {}).keys()) if isinstance(data.get("scripts"), dict) else [],
            )
        elif name in {"pyproject.toml", "Cargo.toml", "composer.json", "pubspec.yaml", "deno.json", "deno.jsonc"}:
            text = read_text(path, 120_000)
            if name.endswith(".json") or name.endswith(".jsonc"):
                cleaned = re.sub(r"//.*", "", text) if name.endswith(".jsonc") else text
                try:
                    data = json.loads(cleaned)
                    entry.update(name=data.get("name"), description=data.get("description"))
                except json.JSONDecodeError:
                    pass
            else:
                entry["name"] = first_match(r"^\s*name\s*=\s*['\"]([^'\"]+)['\"]", text)
                entry["description"] = first_match(r"^\s*description\s*=\s*['\"]([^'\"]+)['\"]", text)
        elif name == "go.mod":
            entry["name"] = first_match(r"^module\s+(.+)$", read_text(path, 20_000))

        result.append(entry)
    return result


def analyze_ci(root: Path) -> dict[str, Any]:
    workflow_dir = root / ".github" / "workflows"
    workflows: list[dict[str, Any]] = []
    if workflow_dir.is_dir():
        for path in sorted(workflow_dir.glob("*.y*ml")):
            text = read_text(path, 160_000).casefold()
            workflows.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "mentions_test": any(term in text for term in ["test", "pytest", "vitest", "jest", "cargo test", "go test"]),
                    "mentions_build": any(term in text for term in ["build", "compile", "tsc", "cargo build"]),
                    "mentions_lint": any(term in text for term in ["lint", "eslint", "ruff", "clippy", "golangci"]),
                }
            )
    return {
        "workflows": workflows,
        "has_ci": bool(workflows),
        "has_test_check": any(item["mentions_test"] for item in workflows),
        "has_build_check": any(item["mentions_build"] for item in workflows),
        "has_lint_check": any(item["mentions_lint"] for item in workflows),
    }


def score_launch(signals: dict[str, Any]) -> dict[str, int]:
    readme = signals["readme"]
    ci = signals["ci"]
    files = signals["files"]
    heading = readme.get("heading_signals", {})

    clarity = 0
    clarity += int(bool(readme.get("exists")))
    clarity += int(bool(readme.get("title")))
    clarity += int(readme.get("line_count", 0) >= 40)
    clarity += int(bool(heading.get("overview")))
    clarity += int(any(manifest.get("description") for manifest in signals["manifests"]))

    activation = 0
    activation += int(readme.get("code_fences", 0) > 0)
    activation += int(bool(heading.get("installation") or heading.get("quick_start")))
    activation += int(bool(heading.get("usage") or heading.get("examples")))
    activation += int(bool(signals["manifests"] or signals["lockfiles"]))
    activation += int(bool("examples" in files["top_level_dirs"] or heading.get("examples")))

    trust = 0
    trust += int(bool(files["relative_files"].intersection({"license", "license.md", "license.txt"})))
    trust += int(bool(ci["has_ci"]))
    trust += int(bool(ci["has_test_check"]))
    trust += int(signals["git"]["tag_count"] > 0)
    trust += int(bool(files["relative_files"].intersection({"contributing.md", "security.md", ".github/security.md"})))

    proof = 0
    proof += int(readme.get("images", 0) > 0)
    proof += int(any(item["type"] == "video" or Path(item["path"]).suffix.casefold() == ".gif" for item in files["media"]))
    proof += int(bool({"examples", "example", "demo", "demos"} & set(files["top_level_dirs"])))
    proof += int(bool(heading.get("examples")))
    proof += int(bool(ci["has_test_check"]))

    distribution = 0
    distribution += int(bool(readme.get("has_english_readme")))
    distribution += int(bool(readme.get("bilingual_readme_link")))
    distribution += int(readme.get("images", 0) > 0 or readme.get("badge_count", 0) > 0)
    distribution += int(signals["git"]["tag_count"] > 0 or "changelog.md" in files["relative_files"])
    distribution += int(any(manifest.get("description") for manifest in signals["manifests"]))

    maintenance = 0
    maintenance += int(bool(DOC_DIR_HINTS & set(files["top_level_dirs"])))
    maintenance += int(bool(files["has_issue_templates"]))
    maintenance += int(bool(ci["has_ci"]))
    maintenance += int(bool(files["relative_files"].intersection({"contributing.md", ".github/contributing.md"})))
    maintenance += int(bool(files["relative_files"].intersection({"roadmap.md", "security.md", "changelog.md", ".github/security.md"})))

    return {
        "clarity": min(clarity, 5),
        "activation": min(activation, 5),
        "trust": min(trust, 5),
        "proof": min(proof, 5),
        "distribution": min(distribution, 5),
        "maintenance": min(maintenance, 5),
    }


def build_findings(signals: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    readme = signals["readme"]
    files = signals["files"]
    file_set = files["relative_files"]

    def add(severity: str, evidence: str, impact: str, recommendation: str) -> None:
        findings.append(
            {"severity": severity, "evidence": evidence, "impact": impact, "recommendation": recommendation}
        )

    if not readme.get("exists"):
        add("blocker", "No README.md found", "Visitors cannot understand or try the project", "Create a root README with positioning, quickstart, example, limits, and license link")
    if not file_set.intersection({"license", "license.md", "license.txt"}):
        add("blocker", "No LICENSE file found", "Public code has unclear usage rights", "Add the intended OSI-approved license before publishing")
    if readme.get("broken_relative_links"):
        add("blocker", f"Broken README relative links: {', '.join(readme['broken_relative_links'][:5])}", "Quickstart or demo paths appear broken", "Fix paths or move the linked assets into the repository")
    if files["secret_candidates"]:
        add("blocker", f"Possible secret-bearing files: {', '.join(files['secret_candidates'][:5])}", "Credentials could be exposed in a public repository", "Remove, ignore, and rotate secrets before publishing; the audit does not print their contents")
    if readme.get("exists") and readme.get("code_fences", 0) == 0:
        add("high", "README has no code fence", "The first trial path is not obvious", "Add copy-pasteable install and run commands")
    if not signals["ci"]["has_test_check"]:
        add("medium", "No CI test workflow detected", "Users have less confidence that releases work", "Add a minimal test workflow or document the release QA process")
    if not signals["git"].get("origin"):
        add("medium", "No origin remote detected", "Repository may not be connected to GitHub", "Add the intended GitHub remote before release")
    if signals["git"].get("last_commit_age_days") is not None and signals["git"]["last_commit_age_days"] > 180:
        add("low", f"Last commit is {signals['git']['last_commit_age_days']} days old", "Visitors may question maintenance", "Refresh dependencies/docs and acknowledge current maturity in the README")

    return findings


SCORE_LABELS = {
    "clarity": "Clarity",
    "activation": "Activation",
    "trust": "Trust",
    "proof": "Proof",
    "distribution": "Distribution",
    "maintenance": "Maintenance",
}


def markdown_cell(value: Any) -> str:
    text = "—" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip() or "—"


def score_verdict(score: float) -> str:
    if score >= 4.5:
        return "Ready for broad launch after final channel preparation"
    if score >= 3.5:
        return "Ready for a targeted launch with noted gaps"
    if score >= 2.5:
        return "Usable by an expert audience; package the basics first"
    return "Not ready for public attention yet"


def yes_no(value: Any) -> str:
    return "Yes" if bool(value) else "No"


def render_markdown(result: dict[str, Any]) -> str:
    scores = result.get("scores", {})
    average = sum(scores.values()) / len(scores) if scores else 0
    findings = result.get("findings", [])
    readme = result.get("readme", {})
    git_info = result.get("git", {})
    ci = result.get("ci", {})
    files = result.get("files", {})

    lines = [
        "# GitHub Launch Readiness Report",
        "",
        f"**Repository:** `{markdown_cell(result.get('name'))}`  ",
        f"**Generated (UTC):** `{markdown_cell((result.get('generated_at') or '')[:19])}`  ",
        f"**Overall score:** **{average:.1f} / 5** — {score_verdict(average)}",
        "",
        "## Scores",
        "",
        "| Dimension | Score | Signal |",
        "| --- | ---: | --- |",
    ]

    score_notes = {
        "clarity": "Can a first-time visitor understand who it is for and what it does?",
        "activation": "Can a new user reach a meaningful result quickly?",
        "trust": "Are rights, validation, maintenance signals, and support paths credible?",
        "proof": "Is there visible evidence that the project works?",
        "distribution": "Can the project be understood and shared beyond the repository?",
        "maintenance": "Are issues, docs, CI, and future triage realistic?",
    }
    for key, label in SCORE_LABELS.items():
        lines.append(f"| {label} | {scores.get(key, 0)} / 5 | {score_notes[key]} |")

    lines.extend(["", "## Prioritized findings", ""])
    if findings:
        lines.extend(
            [
                "| Severity | Evidence | User impact | Recommendation |",
                "| --- | --- | --- | --- |",
            ]
        )
        severity_rank = {"blocker": 0, "high": 1, "medium": 2, "low": 3}
        for finding in sorted(findings, key=lambda item: severity_rank.get(item.get("severity"), 9)):
            lines.append(
                "| {severity} | {evidence} | {impact} | {recommendation} |".format(
                    severity=markdown_cell(finding.get("severity")).upper(),
                    evidence=markdown_cell(finding.get("evidence")),
                    impact=markdown_cell(finding.get("impact")),
                    recommendation=markdown_cell(finding.get("recommendation")),
                )
            )
    else:
        lines.append(
            "No rule-based findings were detected by the offline heuristic audit. "
            "This does not replace semantic positioning review, clean-install testing, or launch copy review."
        )

    lines.extend(
        [
            "",
            "## Repository signals",
            "",
            "| Area | Signal |",
            "| --- | --- |",
            f"| Git branch / head | `{markdown_cell(git_info.get('branch'))}` / `{markdown_cell(git_info.get('head'))}` |",
            f"| Origin remote | `{markdown_cell(git_info.get('origin'))}` |",
            f"| Tags | {git_info.get('tag_count', 0)} |",
            f"| Last commit (UTC) | `{markdown_cell((git_info.get('last_commit_at') or '')[:10])}` |",
            f"| README | `{markdown_cell(readme.get('path'))}` |",
            f"| README title | {markdown_cell(readme.get('title'))} |",
            f"| Code blocks / images / badges | {readme.get('code_fences', 0)} / {readme.get('images', 0)} / {readme.get('badge_count', 0)} |",
            f"| Broken relative README links | {len(readme.get('broken_relative_links', []))} |",
            f"| CI | Present: `{yes_no(ci.get('has_ci'))}`; test: `{yes_no(ci.get('has_test_check'))}`; build: `{yes_no(ci.get('has_build_check'))}`; lint: `{yes_no(ci.get('has_lint_check'))}` |",
            f"| Project manifests / lockfiles | {len(result.get('manifests', []))} / {len(result.get('lockfiles', []))} |",
            f"| Issue templates / contributing / security policy | `{yes_no(files.get('has_issue_templates'))}` / `{yes_no(files.get('has_contributing'))}` / `{yes_no(files.get('has_security_policy'))}` |",
            f"| Possible secret-bearing files | {len(files.get('secret_candidates', []))} |",
        ]
    )

    broken_links = readme.get("broken_relative_links", [])
    secret_candidates = files.get("secret_candidates", [])
    if broken_links or secret_candidates:
        lines.extend(["", "## Items to inspect before publishing", ""])
        if broken_links:
            lines.extend(["### Broken relative README links", ""])
            lines.extend(f"- `{link}`" for link in broken_links)
            lines.append("")
        if secret_candidates:
            lines.extend(["### Possible secret-bearing files", "", "Filenames only; contents are intentionally not printed.", ""])
            lines.extend(f"- `{path}`" for path in secret_candidates)
            lines.append("")

    lines.extend(
        [
            "",
            "## Recommended next actions",
            "",
            "1. Resolve blocker/high findings before driving external traffic.",
            "2. Confirm the target user, five-minute value path, proof, and differentiator semantically.",
            "3. Run the documented quickstart from a clean environment.",
            "4. Prepare one real demo asset and channel-specific launch copy.",
            "5. Re-run this audit after packaging changes.",
            "",
            "---",
            "Generated by GitHub Launch Studio's offline, read-only repository audit. Scores are heuristic and should be interpreted alongside repository-specific review.",
        ]
    )
    return "\n".join(lines) + "\n"


def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    tree = discover_tree(root)
    relative_files = tree["relative_files"]

    git_info = {
        "is_git": (root / ".git").exists(),
        "branch": git(root, "branch", "--show-current"),
        "head": git(root, "rev-parse", "--short", "HEAD"),
        "origin": safe_remote_url(git(root, "remote", "get-url", "origin")),
        "tag_count": len((git(root, "tag", "--list") or "").splitlines()) if git(root, "tag", "--list") is not None else 0,
        "last_commit_at": git(root, "log", "-1", "--format=%cI"),
    }
    if git_info["last_commit_at"]:
        try:
            commit_time = datetime.fromisoformat(git_info["last_commit_at"].replace("Z", "+00:00"))
            git_info["last_commit_age_days"] = max((datetime.now(timezone.utc) - commit_time).days, 0)
        except ValueError:
            git_info["last_commit_age_days"] = None
    else:
        git_info["last_commit_age_days"] = None

    readme_path = choose_readme(root, relative_files)
    readme = analyze_readme(root, readme_path)
    ci = analyze_ci(root)
    manifests = analyze_manifests(root, tree["manifests"])

    # Keep the output compact: report only the largest few media files.
    media = sorted(
        tree["media"],
        key=lambda item: item.get("bytes") or 0,
        reverse=True,
    )[:12]

    signals = {
        "root": str(root),
        "name": root.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git": git_info,
        "readme": readme,
        "manifests": manifests,
        "lockfiles": tree["lockfiles"],
        "ci": ci,
        "files": {
            "count_scanned": len([path for path in tree["files"]]),
            "truncated": tree["truncated"],
            "relative_files": relative_files,
            "top_level_dirs": sorted(tree["top_level_dirs"]),
            "secret_candidates": tree["secret_candidates"],
            "media": media,
            "has_issue_templates": bool(
                list((root / ".github" / "issue_template").glob("*"))
                or list((root / ".github" / "ISSUE_TEMPLATE").glob("*"))
                or (root / ".github" / "ISSUE_TEMPLATE").exists()
            ),
            "has_contributing": any(
                path in relative_files for path in ["contributing.md", ".github/contributing.md", "docs/contributing.md"]
            ),
            "has_security_policy": any(
                path in relative_files for path in ["security.md", ".github/security.md", "docs/security.md"]
            ),
            "has_roadmap_or_changelog": any(
                path in relative_files for path in ["roadmap.md", "changelog.md", "changes.md"]
            ),
        },
    }
    signals["scores"] = score_launch(signals)
    signals["findings"] = build_findings(signals)
    signals["files"]["relative_files"] = sorted(signals["files"]["relative_files"])
    return signals


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only GitHub launch readiness audit")
    parser.add_argument("path", nargs="?", default=".", help="Repository path (defaults to current directory)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format")
    parser.add_argument("--output", type=Path, help="Write the report to a file instead of stdout")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists() or not root.is_dir():
        parser.error(f"repository path does not exist or is not a directory: {root}")

    try:
        result = audit(root)
        if args.format == "markdown":
            rendered = render_markdown(result)
        else:
            rendered = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=False)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(args.output.resolve())
        else:
            print(rendered)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
