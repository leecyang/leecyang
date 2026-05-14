#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import math
import os
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests


USER_AGENT = "leecyang-profile-assets/1.0 (+https://github.com/leecyang/leecyang)"
BG = "#0D1117"
PANEL = "#111827"
PANEL_ALT = "#0F172A"
BORDER = "#1F2937"
TEXT = "#E5E7EB"
TEXT_MUTED = "#94A3B8"
ACCENT = "#38BDF8"
ACCENT_2 = "#22C55E"
WARN = "#F59E0B"
BAD = "#EF4444"


@dataclass
class MonitorTarget:
    name: str
    url: str
    ok_statuses: tuple[int, ...] | None = None
    ok_status_ranges: tuple[tuple[int, int], ...] = ()
    retries: int = 1
    expect_content_prefix: str | None = None
    rule_label: str = "2xx/3xx"


MONITOR_TARGETS = [
    MonitorTarget(
        name="golibrary.xyz",
        url="https://golibrary.xyz/",
        ok_status_ranges=((200, 399),),
        retries=2,
        rule_label="2xx/3xx + retry",
    ),
    MonitorTarget(
        name="lingxilearn.cn",
        url="https://lingxilearn.cn",
        ok_status_ranges=((200, 399),),
    ),
    MonitorTarget(
        name="christmas1314.xyz",
        url="https://christmas1314.xyz",
        ok_status_ranges=((200, 399),),
    ),
    MonitorTarget(
        name="lyyzka.xyz",
        url="https://lyyzka.xyz/",
        ok_status_ranges=((200, 399),),
    ),
    MonitorTarget(
        name="gen.letsapi.store",
        url="https://gen.letsapi.store/overview",
        ok_statuses=(200,),
        rule_label="200",
    ),
    MonitorTarget(
        name="letsapi.store API",
        url="https://letsapi.store/v1/responses",
        ok_statuses=(404,),
        expect_content_prefix="application/json",
        rule_label="404 JSON",
    ),
]


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def api_get(url: str, headers: dict[str, str] | None = None) -> requests.Response:
    merged_headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}
    if headers:
        merged_headers.update(headers)
    return requests.get(url, headers=merged_headers, timeout=30)


def is_status_ok(status: int, ranges: tuple[tuple[int, int], ...], statuses: tuple[int, ...] | None) -> bool:
    if statuses and status in statuses:
        return True
    return any(start <= status <= end for start, end in ranges)


def monitor(out_dir: Path) -> None:
    ensure_dir(out_dir)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    results: list[dict[str, Any]] = []

    for target in MONITOR_TARGETS:
        last_error = None
        last_status = None
        last_content_type = ""
        latency_ms = None
        ok = False

        for attempt in range(1, target.retries + 1):
            started = time.perf_counter()
            try:
                response = session.get(target.url, allow_redirects=True, timeout=15, stream=True)
                latency_ms = round((time.perf_counter() - started) * 1000, 1)
                last_status = response.status_code
                last_content_type = response.headers.get("content-type", "")
                ok = is_status_ok(response.status_code, target.ok_status_ranges, target.ok_statuses)
                if ok and target.expect_content_prefix:
                    ok = last_content_type.lower().startswith(target.expect_content_prefix.lower())
                response.close()
                if ok:
                    break
            except requests.RequestException as exc:
                latency_ms = round((time.perf_counter() - started) * 1000, 1)
                last_error = str(exc)
            if attempt < target.retries:
                time.sleep(0.8)

        results.append(
            {
                "name": target.name,
                "url": target.url,
                "ok": ok,
                "status": last_status,
                "content_type": last_content_type,
                "latency_ms": latency_ms,
                "rule": target.rule_label,
                "retries": target.retries,
                "error": last_error,
            }
        )

    payload = {
        "generated_at": now_iso(),
        "summary": {
            "online": sum(1 for item in results if item["ok"]),
            "offline": sum(1 for item in results if not item["ok"]),
            "targets": len(results),
            "avg_latency_ms": round(
                statistics.mean(item["latency_ms"] for item in results if item["latency_ms"] is not None), 1
            )
            if any(item["latency_ms"] is not None for item in results)
            else None,
        },
        "targets": results,
    }
    (out_dir / "status.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "status-summary.svg").write_text(render_status_summary_svg(payload), encoding="utf-8")
    (out_dir / "status-grid.svg").write_text(render_status_grid_svg(payload), encoding="utf-8")


def gh_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def github_stats(username: str, out_dir: Path) -> None:
    ensure_dir(out_dir)
    headers = gh_headers()
    user = api_get(f"https://api.github.com/users/{username}", headers=headers).json()

    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        response = api_get(
            f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&type=owner&sort=updated",
            headers=headers,
        )
        chunk = response.json()
        if not chunk:
            break
        repos.extend(chunk)
        page += 1

    repos = [repo for repo in repos if not repo.get("fork")]
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos)
    most_starred = max(repos, key=lambda repo: repo.get("stargazers_count", 0), default=None)
    updated_repos = sorted(repos, key=lambda repo: repo.get("updated_at", ""), reverse=True)[:4]

    language_totals: dict[str, int] = {}
    for repo in repos:
        languages_url = repo.get("languages_url")
        if not languages_url:
            continue
        try:
            data = api_get(languages_url, headers=headers).json()
        except requests.RequestException:
            continue
        if not isinstance(data, dict):
            continue
        for language, count in data.items():
            language_totals[language] = language_totals.get(language, 0) + int(count)

    top_languages = sorted(language_totals.items(), key=lambda item: item[1], reverse=True)[:6]
    total_language_bytes = sum(count for _, count in top_languages) or 1

    payload = {
        "generated_at": now_iso(),
        "username": username,
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "public_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "most_starred": most_starred,
        "recent_repos": updated_repos,
        "top_languages": [
            {"name": name, "bytes": count, "percent": round((count / total_language_bytes) * 100, 1)}
            for name, count in top_languages
        ],
    }

    (out_dir / "github-stats.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "github-overview.svg").write_text(render_github_overview_svg(payload), encoding="utf-8")
    (out_dir / "github-languages.svg").write_text(render_github_languages_svg(payload), encoding="utf-8")


def card_shell(width: int, height: int, title: str, subtitle: str, inner: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="bg" x1="0%" x2="100%" y1="0%" y2="100%">
      <stop offset="0%" stop-color="{PANEL_ALT}" />
      <stop offset="100%" stop-color="{BG}" />
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="18" fill="url(#bg)" stroke="{BORDER}" />
  <text x="28" y="38" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700" fill="{TEXT}">{escape(title)}</text>
  <text x="28" y="64" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="{TEXT_MUTED}">{escape(subtitle)}</text>
  {inner}
</svg>"""


def escape(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def render_status_summary_svg(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    items = [
        ("Targets", summary["targets"], ACCENT),
        ("Online", summary["online"], ACCENT_2),
        ("Offline", summary["offline"], BAD if summary["offline"] else ACCENT),
        ("Avg Latency", f'{summary["avg_latency_ms"]} ms' if summary["avg_latency_ms"] is not None else "n/a", WARN),
    ]
    blocks = []
    for index, (label, value, color) in enumerate(items):
        x = 28 + index * 170
        blocks.append(
            f"""
      <rect x="{x}" y="94" width="150" height="90" rx="14" fill="{PANEL}" stroke="{BORDER}" />
      <circle cx="{x+24}" cy="120" r="7" fill="{color}" />
      <text x="{x+40}" y="126" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="{TEXT_MUTED}">{escape(label)}</text>
      <text x="{x+20}" y="160" font-family="Segoe UI, Arial, sans-serif" font-size="26" font-weight="700" fill="{TEXT}">{escape(value)}</text>
"""
        )
    footer = f"""
      <text x="28" y="220" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{TEXT_MUTED}">Generated at {escape(payload["generated_at"])} · README-embedded ops snapshot</text>
"""
    return card_shell(720, 248, "Live Ops / Monitoring", "Uptime Kuma-style summary for production sites and API edges", "".join(blocks) + footer)


def render_status_grid_svg(payload: dict[str, Any]) -> str:
    row_height = 58
    height = 110 + len(payload["targets"]) * row_height + 20
    rows = []
    for idx, item in enumerate(payload["targets"]):
        y = 96 + idx * row_height
        fill = PANEL if idx % 2 == 0 else PANEL_ALT
        color = ACCENT_2 if item["ok"] else BAD
        status_label = "UP" if item["ok"] else "DOWN"
        status_code = item["status"] if item["status"] is not None else "ERR"
        latency = f'{item["latency_ms"]} ms' if item["latency_ms"] is not None else "timeout"
        detail = item["rule"]
        if item["content_type"]:
            detail += f' · {item["content_type"].split(";")[0]}'
        rows.append(
            f"""
      <rect x="22" y="{y}" width="1056" height="46" rx="12" fill="{fill}" stroke="{BORDER}" />
      <circle cx="48" cy="{y+23}" r="7" fill="{color}" />
      <text x="66" y="{y+28}" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600" fill="{TEXT}">{escape(item["name"])}</text>
      <text x="340" y="{y+28}" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{TEXT_MUTED}">{escape(status_label)} · HTTP {status_code}</text>
      <text x="560" y="{y+28}" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{TEXT_MUTED}">{escape(detail)}</text>
      <text x="930" y="{y+28}" font-family="Segoe UI, Arial, sans-serif" font-size="14" text-anchor="end" fill="{TEXT_MUTED}">{escape(latency)}</text>
      <text x="1060" y="{y+28}" font-family="Segoe UI, Arial, sans-serif" font-size="12" text-anchor="end" fill="{ACCENT}">{escape(item["url"])}</text>
"""
        )
    return card_shell(1100, height, "Service Matrix", "Live target-by-target probe results", "".join(rows))


def render_github_overview_svg(payload: dict[str, Any]) -> str:
    most_starred = payload["most_starred"] or {}
    recent = payload["recent_repos"]
    blocks = [
        ("Owned repos", payload["public_repos"]),
        ("Followers", payload["followers"]),
        ("Stars", payload["total_stars"]),
        ("Forks", payload["total_forks"]),
    ]
    inner = []
    for index, (label, value) in enumerate(blocks):
        x = 28 + index * 165
        inner.append(
            f"""
      <rect x="{x}" y="92" width="145" height="86" rx="14" fill="{PANEL}" stroke="{BORDER}" />
      <text x="{x+18}" y="122" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="{TEXT_MUTED}">{escape(label)}</text>
      <text x="{x+18}" y="158" font-family="Segoe UI, Arial, sans-serif" font-size="27" font-weight="700" fill="{TEXT}">{escape(value)}</text>
"""
        )
    inner.append(
        f"""
      <rect x="28" y="194" width="664" height="122" rx="14" fill="{PANEL}" stroke="{BORDER}" />
      <text x="46" y="224" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{TEXT_MUTED}">Most starred repo</text>
      <text x="46" y="258" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700" fill="{TEXT}">{escape(most_starred.get("name", "n/a"))}</text>
      <text x="46" y="286" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{TEXT_MUTED}">stars {escape(most_starred.get("stargazers_count", 0))} · updated {escape((most_starred.get("updated_at", "") or "")[:10])}</text>
"""
    )
    inner.append(
        f"""
      <text x="46" y="340" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{TEXT_MUTED}">Recently updated: {' · '.join(escape(repo.get('name', '')) for repo in recent) if recent else 'n/a'}</text>
"""
    )
    inner.append(
        f"""
      <text x="28" y="370" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{TEXT_MUTED}">Generated at {escape(payload["generated_at"])} from GitHub API</text>
"""
    )
    return card_shell(720, 392, "GitHub Overview", "Self-rendered stats card with no external Vercel dependency", "".join(inner))


def render_github_languages_svg(payload: dict[str, Any]) -> str:
    top_languages = payload["top_languages"] or [{"name": "n/a", "percent": 100.0}]
    palette = ["#38BDF8", "#22C55E", "#F59E0B", "#A855F7", "#EF4444", "#14B8A6"]
    bar_x = 30
    bar_y = 96
    bar_width = 660
    segments = []
    offset = bar_x
    for idx, item in enumerate(top_languages):
        width = max(16, round(bar_width * (item["percent"] / 100)))
        if offset + width > bar_x + bar_width or idx == len(top_languages) - 1:
            width = bar_x + bar_width - offset
        segments.append(
            f'<rect x="{offset}" y="{bar_y}" width="{width}" height="18" rx="9" fill="{palette[idx % len(palette)]}" />'
        )
        offset += width

    legend = []
    for idx, item in enumerate(top_languages):
        y = 150 + idx * 28
        color = palette[idx % len(palette)]
        legend.append(
            f"""
      <circle cx="40" cy="{y-5}" r="6" fill="{color}" />
      <text x="56" y="{y}" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{TEXT}">{escape(item["name"])}</text>
      <text x="680" y="{y}" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{TEXT_MUTED}">{escape(item["percent"])}%</text>
"""
        )
    inner = "".join(segments) + "".join(legend)
    inner += f"""
      <text x="30" y="300" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{TEXT_MUTED}">Aggregated from owned repositories only · Generated at {escape(payload["generated_at"])}</text>
"""
    return card_shell(720, 328, "Top Languages", "Language share aggregated from repository byte counts", inner)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate profile README assets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    monitor_parser = subparsers.add_parser("monitor")
    monitor_parser.add_argument("--out-dir", required=True)

    github_parser = subparsers.add_parser("github")
    github_parser.add_argument("--username", default="leecyang")
    github_parser.add_argument("--out-dir", required=True)

    args = parser.parse_args(argv)
    out_dir = Path(args.out_dir)

    if args.command == "monitor":
        monitor(out_dir)
    elif args.command == "github":
        github_stats(args.username, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

