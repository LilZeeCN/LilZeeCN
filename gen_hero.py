#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animated hero, v3 — VISIBLE motion + real signal.

v2 mistake: motion amplitude was ~1.4%, invisible. Felt like a logo page.
v3 fixes:
  · accent light-band flowing through the title (3.5s, full-width travel)
  · travelling-wave dot grid (8 bands, staggered) instead of global opacity breathe
  · a skewed scan beam sweeping across (7s)
Content stays visible in every render path — no "from hidden" states.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

FONT = ("-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text',"
        "'Helvetica Neue','PingFang SC','Hiragino Sans GB',"
        "'Microsoft YaHei',Helvetica,Arial,sans-serif")

W, H = 860, 360
CX = W / 2

TOK = {
    "light": dict(
        bg="#ffffff", dot="#c9ccd1", primary="#1d1d1f", secondary="#6e6e73",
        tertiary="#86868b", separator="#c7c7cc", accent="#0071e3",
    ),
    "dark": dict(
        bg="#0d1117", dot="#2d343d", primary="#f5f5f7", secondary="#a1a1a6",
        tertiary="#86868b", separator="#3a3a3c", accent="#2997ff",
    ),
}

BANDS = 8
BAND_H = H / BANDS


def wave_css():
    rows = ["@keyframes wave { 0%,100% { opacity: .18; } 50% { opacity: 1; } }"]
    for i in range(BANDS):
        rows.append(f".w{i} {{ animation: wave 4.2s ease-in-out {i * 0.13:.2f}s infinite; }}")
    return "\n".join(rows)


CSS = """
@keyframes flow {
  0%   { transform: translateX(-300px); }
  100% { transform: translateX(560px); }
}
@keyframes scan {
  0%        { transform: translateX(-140px) skewX(-18deg); opacity: 0; }
  8%, 92%   { opacity: .9; }
  100%      { transform: translateX(1000px) skewX(-18deg); opacity: 0; }
}
@keyframes pulse {
  0%, 88%, 100% { transform: scale(1);    opacity: 1; }
  94%           { transform: scale(2.1);  opacity: .35; }
}

.flow  { animation: flow 3.5s linear infinite; }
.scan  { animation: scan 7s ease-in-out infinite; }
.runner{ animation: pulse 4.5s ease-in-out infinite;
         transform-box: fill-box; transform-origin: center; }

@media (prefers-reduced-motion: reduce) {
  .flow, .scan, .runner, [class^="w"] { animation: none; opacity: 1; }
}
"""


def txt(y, s, size, weight, fill, textlen=None):
    tl = f' textLength="{textlen}" lengthAdjust="spacing"' if textlen else ""
    return (f'<text x="{CX}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle"{tl}>{s}</text>')


def build(mode):
    t = TOK[mode]

    bands = "\n".join(
        f'<g class="w{i}"><rect y="{i * BAND_H:.1f}" width="{W}" height="{BAND_H:.1f}" '
        f'fill="url(#dots)"/></g>' for i in range(BANDS)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<style>{wave_css()}
{CSS}</style>
<defs>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.4" fill="{t["dot"]}"/>
  </pattern>
  <radialGradient id="fade" cx="50%" cy="46%" r="60%">
    <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
    <stop offset="70%" stop-color="#fff" stop-opacity=".5"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="dotsMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>

  <linearGradient id="flowGrad" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0%"   stop-color="{t["accent"]}" stop-opacity="0"/>
    <stop offset="45%"  stop-color="{t["accent"]}" stop-opacity=".95"/>
    <stop offset="55%"  stop-color="{t["accent"]}" stop-opacity=".95"/>
    <stop offset="100%" stop-color="{t["accent"]}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="scanGrad" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0%"   stop-color="{t["accent"]}" stop-opacity="0"/>
    <stop offset="50%"  stop-color="{t["accent"]}" stop-opacity=".10"/>
    <stop offset="100%" stop-color="{t["accent"]}" stop-opacity="0"/>
  </linearGradient>

  <clipPath id="titleClip">
    <text x="{CX}" y="152" font-size="72" font-weight="680" text-anchor="middle"
          textLength="248" lengthAdjust="spacing">LilZee</text>
  </clipPath>
</defs>

<rect width="{W}" height="{H}" fill="{t["bg"]}"/>

<g mask="url(#dotsMask)">
{bands}
</g>

<g class="scan"><rect x="0" y="-40" width="120" height="{H + 80}" fill="url(#scanGrad)"/></g>

<g clip-path="url(#titleClip)">
  {txt(152, "LilZee", 72, 680, t["primary"], textlen=248)}
  <rect class="flow" x="0" y="86" width="200" height="82" fill="url(#flowGrad)"/>
</g>

<line x1="352" y1="206" x2="508" y2="206" stroke="{t["separator"]}"
      stroke-width="1" stroke-linecap="round"/>
<circle class="runner" cx="430" cy="206" r="3.2" fill="{t["accent"]}"/>

{txt(262, "CS student · AI × Education", 22, 500, t["secondary"], textlen=252)}
{txt(300, "让 AI 学会如何教学", 17, 400, t["tertiary"], textlen=158)}
</svg>
'''


for mode in ("light", "dark"):
    p = os.path.join(OUT, f"hero-{mode}.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write(build(mode))
    print("wrote", p)
