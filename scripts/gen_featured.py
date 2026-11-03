#!/usr/bin/env python3
"""Generate assets/featured.svg — a live-data banner for the profile README.

Fetches stars / forks / latest release for the featured repos from the
GitHub API and renders a bespoke glassmorphism SVG. Stdlib only.
Token (optional): GH_TOKEN or GITHUB_TOKEN env var.
"""
import json
import os
import urllib.request
from xml.sax.saxutils import escape

OWNER = "LilZeeCN"
REPOS = [
    {"name": "zee-rp", "tagline": "AI 生成原生 Axure 原型", "accent": "#6483FF"},
    {"name": "agy-argon-bridge", "tagline": "agy × Vertex AI 旗舰模型", "accent": "#B388FF"},
    {"name": "youtube-summary", "tagline": "看完视频，带走知识", "accent": "#2EE6A8"},
    {"name": "zee-tutor", "tagline": "课程 Wiki 化 · 证据化学习", "accent": "#0E9F6E"},
]
FONT = "'PingFang SC','Microsoft YaHei','Noto Sans SC','Segoe UI',sans-serif"


def fetch(url):
    headers = {"User-Agent": "zee-profile-gen", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def repo_data(spec):
    repo = fetch(f"https://api.github.com/repos/{OWNER}/{spec['name']}")
    chip = ""
    try:
        rel = fetch(f"https://api.github.com/repos/{OWNER}/{spec['name']}/releases/latest")
        if rel.get("tag_name"):
            chip = f"Release {rel['tag_name']} · {rel['published_at'][:10]}"
    except Exception:
        chip = ""
    if not chip:
        chip = f"Updated {repo['pushed_at'][:10]}"
    return {
        **spec,
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "language": repo.get("language") or "",
        "chip": chip,
    }


def render(items):
    total_stars = sum(i["stars"] for i in items)
    cards = []
    for idx, it in enumerate(items):
        x = 40 + idx * 285
        name_size = 19 if len(it["name"]) <= 12 else (16 if len(it["name"]) <= 18 else 14)
        cards.append(f"""
  <g>
    <rect x="{x}" y="128" width="261" height="272" rx="18" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.16"/>
    <rect x="{x}" y="128" width="261" height="4" rx="2" fill="{it['accent']}"/>
    <text x="{x + 24}" y="188" font-size="{name_size}" font-weight="700" fill="#FFFFFF">{escape(it['name'])}</text>
    <text x="{x + 24}" y="220" font-size="13.5" fill="#C6CCDE">{escape(it['tagline'])}</text>
    <text x="{x + 24}" y="292" font-size="34" font-weight="800" fill="#FFFFFF">★ {it['stars']}</text>
    <text x="{x + 24}" y="318" font-size="12.5" fill="#8A919C">stars · {escape(it['language'])} · {it['forks']} forks</text>
    <rect x="{x + 24}" y="340" width="{max(120, len(it['chip']) * 7 + 24)}" height="28" rx="14" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.14"/>
    <text x="{x + 38}" y="359" font-size="12" fill="#E7EAF3">{escape(it['chip'])}</text>
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="452" viewBox="0 0 1200 452" font-family="{FONT}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B1026"/>
      <stop offset="0.55" stop-color="#14204A"/>
      <stop offset="1" stop-color="#0A2E23"/>
    </linearGradient>
    <radialGradient id="glow1" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#304FFE" stop-opacity="0.5"/>
      <stop offset="1" stop-color="#304FFE" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#0E9F6E" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#0E9F6E" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="452" rx="24" fill="url(#bg)"/>
  <circle cx="150" cy="30" r="220" fill="url(#glow1)"/>
  <circle cx="1120" cy="452" r="240" fill="url(#glow2)"/>
  <circle cx="60" cy="66" r="6" fill="#2EE6A8">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="78" y="73" font-size="15" letter-spacing="3" fill="#E7EAF3">SELECTED WORK — LIVE</text>
  <text x="1160" y="73" font-size="15" fill="#8A919C" text-anchor="end">四个主力项目 · 合计 ★ {total_stars}</text>
  <text x="40" y="106" font-size="12.5" fill="#8A919C">数据来自 GitHub API，由本仓库的 GitHub Action 每日自动重绘</text>
{''.join(cards)}
  <text x="40" y="430" font-size="12" fill="#5A6472">github.com/LilZeeCN</text>
  <text x="1160" y="430" font-size="12" fill="#5A6472" text-anchor="end">Designed &amp; generated in-repo — no templates</text>
</svg>
"""


def main():
    items = [repo_data(spec) for spec in REPOS]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "featured.svg")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(render(items))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
