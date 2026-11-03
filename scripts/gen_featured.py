#!/usr/bin/env python3
"""Generate assets/featured.svg — one all-in-one poster for the profile README.

The poster contains the hero, intro, the four featured projects (with live
stars / forks / latest release from the GitHub API), the "thread" statement
and the also-list. Stdlib only.
Token (optional): GH_TOKEN or GITHUB_TOKEN env var.
"""
import json
import os
import urllib.request
from xml.sax.saxutils import escape

OWNER = "LilZeeCN"
REPOS = [
    {"name": "zee-rp", "tagline": "让 AI 画出原型，在 Axure 里继续改",
     "desc": "RP/1 源码生成原生 .rp · 读改现有工程 · 截图重建", "accent": "#6483FF"},
    {"name": "agy-argon-bridge", "tagline": "把 Antigravity CLI 接到云端旗舰模型",
     "desc": "协议转换 · 完整 Tool Calling · 多账号轮换 · 长思考防断", "accent": "#B388FF"},
    {"name": "youtube-summary", "tagline": "看完视频，带走可回看的知识",
     "desc": "时间戳总结 · 思维导图 · 追问对话 · 跨视频长期记忆", "accent": "#2EE6A8"},
    {"name": "zee-tutor", "tagline": "让课程不止停在对话里",
     "desc": "证据化课程规划 · 练习与测评 · 进度沉淀为 Markdown Wiki", "accent": "#0E9F6E"},
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
    return {**spec, "stars": repo["stargazers_count"], "forks": repo["forks_count"],
            "language": repo.get("language") or "", "chip": chip}


def card(it, x, y):
    name_size = 24 if len(it["name"]) <= 16 else 20
    chip_w = max(132, len(it["chip"]) * 7 + 28)
    return f"""
  <g>
    <rect x="{x}" y="{y}" width="532" height="202" rx="18" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.16"/>
    <rect x="{x}" y="{y}" width="532" height="4" rx="2" fill="{it['accent']}"/>
    <text x="{x + 28}" y="{y + 54}" font-size="{name_size}" font-weight="700" fill="#FFFFFF">{escape(it['name'])}</text>
    <text x="{x + 504}" y="{y + 54}" font-size="26" font-weight="800" fill="#FFFFFF" text-anchor="end">★ {it['stars']}</text>
    <text x="{x + 28}" y="{y + 88}" font-size="15.5" fill="#E7EAF3">{escape(it['tagline'])}</text>
    <text x="{x + 28}" y="{y + 118}" font-size="13.5" fill="#9AA3B5">{escape(it['desc'])}</text>
    <text x="{x + 28}" y="{y + 168}" font-size="13" fill="#8A919C">{escape(it['language'])} · {it['forks']} forks</text>
    <rect x="{x + 532 - 28 - chip_w}" y="{y + 146}" width="{chip_w}" height="30" rx="15" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.14"/>
    <text x="{x + 532 - 28 - chip_w / 2}" y="{y + 166}" font-size="12" fill="#E7EAF3" text-anchor="middle">{escape(it['chip'])}</text>
  </g>"""


def render(items):
    total = sum(i["stars"] for i in items)
    positions = [(40, 436), (628, 436), (40, 662), (628, 662)]
    cards = "".join(card(it, x, y) for it, (x, y) in zip(items, positions))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1180" viewBox="0 0 1200 1180" font-family="{FONT}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B1026"/>
      <stop offset="0.5" stop-color="#121E4C"/>
      <stop offset="1" stop-color="#07231B"/>
    </linearGradient>
    <linearGradient id="aurora" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#304FFE">
        <animate attributeName="stop-color" values="#304FFE;#7C4DFF;#0E9F6E;#304FFE" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="0.5" stop-color="#0E9F6E">
        <animate attributeName="stop-color" values="#0E9F6E;#304FFE;#2EE6A8;#0E9F6E" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="1" stop-color="#2EE6A8">
        <animate attributeName="stop-color" values="#2EE6A8;#0E9F6E;#7C4DFF;#2EE6A8" dur="14s" repeatCount="indefinite"/>
      </stop>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;0.25 0;0 0" dur="16s" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="glow1" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#304FFE" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#304FFE" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#0E9F6E" stop-opacity="0.4"/>
      <stop offset="1" stop-color="#0E9F6E" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="1180" rx="24" fill="url(#bg)"/>
  <circle cx="120" cy="40" r="300" fill="url(#glow1)"/>
  <circle cx="1150" cy="700" r="320" fill="url(#glow2)"/>
  <circle cx="1080" cy="90" r="200" fill="url(#glow1)" opacity="0.6"/>

  <text x="62" y="84" font-size="15" letter-spacing="4" fill="#C6CCDE">LILZEE · CS STUDENT · BUILDER</text>
  <text x="58" y="152" font-size="58" font-weight="800" fill="#FFFFFF">Hey, I'm Zee.</text>
  <text x="60" y="202" font-size="29" font-weight="700" fill="url(#aurora)">Less friction. More learning.</text>
  <text x="60" y="246" font-size="17" fill="#D8DCEA">让 AI Agent 接进真实工具干活，也陪人把学习走完。</text>
  <text x="60" y="274" font-size="15" fill="#9AA3B5">从生成原生 Axure 原型、桥接云端旗舰模型，到视频知识整理与可持续课程 Wiki —— 把想法做出来，再慢慢打磨。</text>

  <g font-size="14" fill="#E7EAF3">
    <rect x="60" y="298" width="118" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.3"/>
    <text x="119" y="320" text-anchor="middle">AI Agents</text>
    <rect x="192" y="298" width="76" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.3"/>
    <text x="230" y="320" text-anchor="middle">MCP</text>
    <rect x="282" y="298" width="112" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.3"/>
    <text x="338" y="320" text-anchor="middle">Axure RP</text>
    <rect x="408" y="298" width="148" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.3"/>
    <text x="482" y="320" text-anchor="middle">AI × Education</text>
  </g>

  <line x1="60" y1="362" x2="1140" y2="362" stroke="#FFFFFF" stroke-opacity="0.14"/>
  <circle cx="60" cy="398" r="6" fill="#2EE6A8">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="78" y="404" font-size="15" letter-spacing="3" fill="#E7EAF3">SELECTED WORK — LIVE</text>
  <text x="1140" y="404" font-size="15" fill="#8A919C" text-anchor="end">四个主力项目 · 合计 ★ {total} · 数据由 GitHub Action 每日自动重绘</text>
{cards}
  <line x1="60" y1="906" x2="1140" y2="906" stroke="#FFFFFF" stroke-opacity="0.14"/>
  <text x="60" y="946" font-size="13" letter-spacing="3" fill="#8A919C">THE THREAD</text>
  <text x="60" y="984" font-size="24" font-weight="700" fill="#FFFFFF">让 AI 接入真实工具，也让 AI 学会如何教学。</text>
  <text x="60" y="1018" font-size="15.5" fill="#C6CCDE">一边是工具：打通协议、格式与模型的边界，让 Agent 真的能交付文件和结果。</text>
  <text x="60" y="1046" font-size="15.5" fill="#C6CCDE">另一边是学习：把一次性的对话，变成能积累、能复习、能验证的长期过程。</text>

  <text x="60" y="1096" font-size="13" letter-spacing="3" fill="#8A919C">ALSO</text>
  <text x="140" y="1096" font-size="14.5" fill="#C6CCDE">DeepTutor（开源贡献 · PR #1388 已合并） · lexiary（Android 生词手账） · cs61b-cn（CS 61B 中文版）</text>

  <line x1="60" y1="1120" x2="1140" y2="1120" stroke="#FFFFFF" stroke-opacity="0.14"/>
  <text x="60" y="1152" font-size="13" fill="#8A919C">Built with curiosity. Shared with you.</text>
  <text x="1140" y="1152" font-size="13" fill="#8A919C" text-anchor="end">github.com/LilZeeCN · 2453972231@qq.com</text>
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
