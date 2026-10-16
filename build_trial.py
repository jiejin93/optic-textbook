# -*- coding: utf-8 -*-
"""Build free-trial reading pages (preface + ch01-04) into docs/ for GitHub Pages.
首页 docs/index.html 为手工维护文件，本脚本不生成、不覆盖它。
样式源：trial_style_src.css（阅读页专属，不共用主教材 style.css）。
"""
import os, io, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
TRIAL = os.path.join(ROOT, "trial")
OUT = os.path.join(ROOT, "docs")
REPO = "https://github.com/jiejin93/optic-textbook"
CSS_SRC = os.path.join(ROOT, "trial_style_src.css")
COVER_SRC = r"D:\play\optic\textbook\cover-gpt.png"     # 定稿封面 → docs/cover.png
QR_SRC = "D:/play/llm/llm-textbook/branding/二维码.jpg"

CH = [
    ("preface.html", "前言"),
    ("ch01.html", "第 1 章 绪论"),
    ("ch02.html", "第 2 章 复数与波动的数学"),
    ("ch03.html", "第 3 章 傅里叶分析"),
    ("ch04.html", "第 4 章 线性系统、卷积与采样"),
]
FULL_TITLE = dict(CH)
FULL_TITLE["preface.html"] = "前言"
FULL_TITLE["ch01.html"] = "第 1 章 绪论：从一张掩模照片说起"
FULL_TITLE["ch02.html"] = "第 2 章 复数与波动的数学"
FULL_TITLE["ch03.html"] = "第 3 章 傅里叶分析"
FULL_TITLE["ch04.html"] = "第 4 章 线性系统、卷积与采样"

KATEX = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\\\(',right:'\\\\)',display:false}],throwOnError:false});"></script>"""

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 掩模版光学仿真与缺陷检测（试读版）</title>
<link rel="stylesheet" href="style.css">
{kateex}
</head>
<body>
<div class="mobile-top"><a class="mt-title" href="index.html">掩模版光学仿真与缺陷检测</a><a class="mt-home" href="index.html">目录 · 定价</a></div>
<div class="layout">
<nav class="toc">
<a class="book" href="index.html"><img src="cover.png" alt="封面"><span class="bt">掩模版光学仿真<br>与缺陷检测<small>免费试读版</small></span></a>
<div class="part">免费试读</div>
{nav}
<div class="part">完整版</div>
<a class="ext" href="index.html#buy">获取完整版</a>
<a class="ext" href="{repo}" target="_blank">GitHub 仓库</a>
</nav>
<main>
<div class="trial-banner">📚 免费试读：前言 + 第 1–4 章 · 完整版（四篇十九章 + 七附录，另有教材+运行代码版本）见 <a href="{repo}" target="_blank">GitHub 仓库</a> 或 <a href="index.html#buy">定价页</a></div>
{body}
<div class="pager">{prev}{next}</div>
<footer class="colophon">© 析微视觉实验室 · <a href="index.html">返回目录与定价</a> · <a href="{repo}" target="_blank">GitHub</a></footer>
</main>
</div>
</body>
</html>"""


def nav(active):
    items = []
    for fn, title in CH:
        cls = ' class="active"' if fn == active else ""
        items.append('<a href="%s"%s>%s</a>' % (fn, cls, title))
    return "".join(items)


def pager_card(href, label, title, align_right=False):
    if not href:
        return ""
    return ('<a href="%s"><span>%s</span><b>%s</b></a>'
            % (href, ("下一章 →" if align_right else "← 上一章"), title))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(CSS_SRC, os.path.join(OUT, "style.css"))
    if os.path.exists(COVER_SRC):
        shutil.copy(COVER_SRC, os.path.join(OUT, "cover.png"))
    if os.path.exists(QR_SRC) and not os.path.exists(os.path.join(OUT, "wechat-qr.jpg")):
        shutil.copy(QR_SRC, os.path.join(OUT, "wechat-qr.jpg"))
    stale = os.path.join(OUT, "cover_art.png")
    if os.path.exists(stale):
        os.remove(stale)          # 旧 CSS 封面底图，已被 cover.png 取代
    for i, (fn, title) in enumerate(CH):
        body = io.open(os.path.join(TRIAL, fn), encoding="utf-8").read()
        prev = pager_card(CH[i-1][0], "← 上一章", FULL_TITLE[CH[i-1][0]]) if i > 0 else ""
        nxt = pager_card(CH[i+1][0], "下一章 →", FULL_TITLE[CH[i+1][0]], True) if i < len(CH)-1 else ""
        html = PAGE.format(title=FULL_TITLE[fn], nav=nav(fn), body=body,
                           kateex=KATEX, prev=prev, next=nxt, repo=REPO)
        io.open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)
        print("built", fn)
    print("done (index.html 未触碰)")
