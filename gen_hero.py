#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animated hero for GitHub profile README (v2 — robustness over entrance flair).

Design constraint: elements must be VISIBLE in any render path
(real browser, headless screenshot, HTML fetch). No "from hidden" states.
All flair comes from continuous, slow, looped motion.
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
        bg="#ffffff", dot="#dadce0", primary="#1d1d1f", secondary="#6e6e73",
        tertiary="#86868b", separator="#c7c7cc", accent="#0071e3",
        glow_op=0.14, shine="#ffffff",
    ),
    "dark": dict(
        bg="#0d1117", dot="#262c34", primary="#f5f5f7", secondary="#a1a1a6",
        tertiary="#86868b", separator="#3a3a3c", accent="#2997ff",
        glow_op=0.22, shine="#ffffff",
    ),
}

CSS = """
/* continuous, low-amplitude motion only — never hides content */
@keyframes drift {
  0%,100% { transform: translateX(-80px); }
  50%     { transform: translateX(80px); }
}
@keyframes breathe-opacity {
  0%,100% { opacity: .40; }
  50%     { opacity: 1; }
}
@keyframes title-breathe {
  0%,100% { transform: scale(1); }
  50%     { transform: scale(1.014); }
}
@keyframes shimmer-sweep {
  0%        { transform: translateX(-360px); }
  100%      { transform: translateX(360px); }
}
@keyframes dot-blink {
  0%, 92%, 100% { transform: scale(1); opacity: 1; }
  96%           { transform: scale(1.8); opacity: 0.55; }
}

.glow    { animation: drift 16s ease-in-out infinite; transform-origin: center; }
.dots    { animation: breathe-opacity 10s ease-in-out infinite; }
.title-grp {
  animation: title-breathe 7s ease-in-out infinite;
  transform-box: fill-box; transform-origin: center;
}
.shimmer { animation: shimmer-sweep 4.5s cubic-bezier(.4,0,.2,1) infinite; }
.runner  { animation: dot-blink 4.5s ease-in-out infinite; }

@media (prefers-reduced-motion: reduce) {
  .glow, .dots, .title-grp, .shimmer, .runner { animation: none; }
}
"""


def txt(y, s, size, weight, fill, textlen=None, cls=None):
    tl = f' textLength="{textlen}" lengthAdjust="spacing"' if textlen else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{CX}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle"{tl}{c}>{s}</text>')


def build(mode):
    t = TOK[mode]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<style>{CSS}</style>
<defs>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.3" fill="{t["dot"]}"/>
  </pattern>
  <radialGradient id="fade" cx="50%" cy="46%" r="58%">
    <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
    <stop offset="70%" stop-color="#fff" stop-opacity=".55"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="dotsMask">
    <rect width="{W}" height="{H}" fill="url(#fade)"/>
  </mask>
  <radialGradient id="glow">
    <stop offset="0%" stop-color="{t["accent"]}" stop-opacity="{t["glow_op"]}"/>
    <stop offset="55%" stop-color="{t["accent"]}" stop-opacity="{t["glow_op"] * .3:.3f}"/>
    <stop offset="100%" stop-color="{t["accent"]}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="shine" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0%" stop-color="{t["shine"]}" stop-opacity="0"/>
    <stop offset="45%" stop-color="{t["shine"]}" stop-opacity=".95"/>
    <stop offset="55%" stop-color="{t["shine"]}" stop-opacity=".95"/>
    <stop offset="100%" stop-color="{t["shine"]}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="titleClip">
    <text x="{CX}" y="152" font-size="72" font-weight="680" text-anchor="middle"
          textLength="248" lengthAdjust="spacing">LilZee</text>
  </clipPath>
</defs>

<rect width="{W}" height="{H}" fill="{t["bg"]}"/>

<g class="dots" mask="url(#dotsMask)">
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
</g>

<ellipse class="glow" cx="{CX}" cy="150" rx="340" ry="195" fill="url(#glow)"/>

<g class="title-grp">
  {txt(152, "LilZee", 72, 680, t["primary"], textlen=248)}
</g>
<g clip-path="url(#titleClip)">
  <rect class="shimmer" x="0" y="88" width="150" height="78" fill="url(#shine)"/>
</g>

<line x1="352" y1="206" x2="508" y2="206" stroke="{t["separator"]}"
      stroke-width="1" stroke-linecap="round"/>
<circle class="runner" cx="430" cy="206" r="3" fill="{t["accent"]}"/>

{txt(262, "Teach the machine to teach.", 26, 400, t["secondary"], textlen=282)}
{txt(300, "让 AI 学会如何教学", 17, 400, t["tertiary"], textlen=158)}
</svg>
'''


for mode in ("light", "dark"):
    p = os.path.join(OUT, f"hero-{mode}.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write(build(mode))
    print("wrote", p)
