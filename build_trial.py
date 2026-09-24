# -*- coding: utf-8 -*-
"""Build free-trial site (preface + ch01-04) into docs/ for GitHub Pages."""
import os, io, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
TRIAL = os.path.join(ROOT, "trial")
OUT = os.path.join(ROOT, "docs")
REPO = "https://github.com/jiejin93/optic-textbook"
CSS_SRC = r"D:\play\optic\textbook\style.css"
COVER = r"D:\play\optic\textbook\cover_art.png"

CH = [
    ("preface.html", "前言"),
    ("ch01.html", "第 1 章 绪论：从一张掩模照片说起"),
    ("ch02.html", "第 2 章 复数与波动的数学"),
    ("ch03.html", "第 3 章 傅里叶分析"),
    ("ch04.html", "第 4 章 线性系统、卷积与采样"),
]

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
<style>.trial-banner{{background:#fff7ed;border:1px solid #fdba74;border-radius:8px;padding:.7em 1em;margin:0 0 1.5em;font-size:.95em}}</style>
</head>
<body>
<div class="layout">
<nav class="toc"><div class="title">掩模光学仿真<br><span style="font-size:.6em">免费试读版</span></div>
{nav}
<div class="part">完整版</div>
<a href="{repo}">GitHub 仓库 / 完整目录</a>
</nav>
<main>
<div class="trial-banner">📚 当前为免费试读版（前言 + 第 1–4 章）· 完整版四篇十九章 + 七附录见 <a href="{repo}" target="_blank">GitHub 仓库</a></div>
{body}
<div class="pager">{prev}{next}</div>
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

QR_SRC = "D:/play/llm/llm-textbook/branding/二维码.jpg"

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    if os.path.exists(QR_SRC): shutil.copy(QR_SRC, os.path.join(OUT, "wechat-qr.jpg"))
    shutil.copy(CSS_SRC, os.path.join(OUT, "style.css"))
    if os.path.exists(COVER): shutil.copy(COVER, os.path.join(OUT, "cover_art.png"))
    for i, (fn, title) in enumerate(CH):
        body = io.open(os.path.join(TRIAL, fn), encoding="utf-8").read()
        prev = '<a href="%s">← 上一页</a>' % CH[i-1][0] if i > 0 else ""
        nxt = '<a href="%s">下一页 →</a>' % CH[i+1][0] if i < len(CH)-1 else ""
        html = PAGE.format(title=title, nav=nav(fn), body=body, kateex=KATEX, prev=prev, next=nxt, repo=REPO)
        io.open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)
    TRIAL_FILES = {"preface.html", "ch01.html", "ch02.html", "ch03.html", "ch04.html"}
    PARTS = [
        ("第一部分 · 基础篇", [("preface.html", "前言"), ("ch01.html", "绪论：从一张掩模照片说起"), ("ch02.html", "复数与波动的数学"), ("ch03.html", "傅里叶分析"), ("ch04.html", "线性系统、卷积与采样"), (None, "电磁场与光的波动理论"), (None, "光与物质相互作用"), (None, "干涉与相干性"), (None, "衍射理论")]),
        ("第二部分 · 成像理论篇", [(None, "透镜作为傅里叶变换机"), (None, "成像系统：PSF、OTF 与分辨率"), (None, "部分相干成像：从阿贝到 Hopkins")]),
        ("第三部分 · 掩模光学仿真篇", [(None, "掩模版工程与版图数据"), (None, "仿真模块一：版图栅格化与薄掩模"), (None, "仿真模块二：Abbe 源点成像引擎"), (None, "仿真模块三：Hopkins 与 TCC 快速引擎"), (None, "仿真模块四：厚掩模与矢量电磁仿真"), (None, "仿真模块五：参考图渲染与设备标定")]),
        ("第四部分 · 应用篇", [(None, "die-to-database 检测算法全流程"), (None, "综合实战与工程化")]),
        ("附录", [(None, "A 公式速查 · B 术语对照 · C 参考文献 · D 习题解答 · E 实验指南 · F 数值实验 · G 调试手册")]),
    ]
    cards = []
    for pname, chapters in PARTS:
        lis = []
        for fn, title in chapters:
            if fn:
                lis.append('<li><a href="%s">%s</a><span class="free">免费试读</span></li>' % (fn, title))
            else:
                lis.append('<li>%s<span class="lock">完整版</span></li>' % title)
        cls = ' class="part-card app-card"' if pname == "附录" else ' class="part-card"'
        cards.append('<div%s><h3>%s</h3><ul>%s</ul></div>' % (cls, pname, "".join(lis)))
    parts_html = "".join(cards)
    cover_html = io.open(r"D:\play\optic\manuscript\cover.html", encoding="utf-8").read()
    cover_css = """
.cover{width:100%%;aspect-ratio:520/726;display:flex;align-items:center;justify-content:center;
background:#16243A url(cover_art.png) center/cover no-repeat;border-radius:10px;border:1px solid var(--line);box-shadow:0 12px 32px rgba(22,36,58,.18)}
.cover-inner{width:78%%;padding-bottom:8%%}
.cover-kicker{font-size:.72em;letter-spacing:.5em;color:#C9A45C;border:1px solid #C9A45C;display:inline-block;padding:.35em .9em;margin-bottom:1.2em}
.cover-title{font-size:1.9em;line-height:1.45;color:#F4F7FA;margin:0 0 .5em;font-weight:800;text-shadow:0 2pt 8pt rgba(10,18,32,.55)}
.cover-sub{font-size:.95em;color:#9FB6CC;margin-bottom:1.4em;letter-spacing:.15em}
.cover-summary{font-size:.78em;color:#C7D5E2;line-height:1.9;text-align:justify;border-left:2px solid #C9A45C;padding-left:1em;margin-bottom:1.6em}
.cover-meta{display:flex;justify-content:space-between;font-size:.72em;color:#8CA2B8;border-top:1px solid #3C5A78;padding-top:.8em}
"""
    idx = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>掩模版光学仿真与 die-to-database 缺陷检测 | 免费在线试读 · 波动光学/傅里叶/Abbe/Hopkins 教程</title>
<meta name="description" content="《掩模版光学仿真与 die-to-database 缺陷检测》中文教材免费在线试读：从复数与傅里叶分析、衍射、阿贝成像到 Hopkins/TCC 仿真引擎与参考图渲染，四篇十九章+七附录，含 Python 数值实验。">
<meta name="keywords" content="掩模版,光学仿真,缺陷检测,die-to-database,半导体,光刻,傅里叶光学,阿贝成像,Hopkins,TCC,FDTD,RCWA,中文教材,免费试读">
<meta property="og:type" content="book">
<meta property="og:title" content="掩模版光学仿真与 die-to-database 缺陷检测（免费试读）">
<meta property="og:description" content="从波动光学基础到参考图渲染仿真的完整中文教程，四篇十九章，含可运行数值实验。">
<meta property="og:url" content="https://jiejin93.github.io/optic-textbook/">
<meta property="og:image" content="https://jiejin93.github.io/optic-textbook/cover_art.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://jiejin93.github.io/optic-textbook/">
<link rel="stylesheet" href="style.css">%s
<style>
:root{--ink:#22303e;--muted:#5b6b7a;--brand:#1a56db;--line:#e4e8ee}
*{box-sizing:border-box}
body{margin:0;font-family:"Microsoft YaHei","Noto Sans SC",sans-serif;background:#f4f6f9;color:var(--ink);line-height:1.8;font-size:16px}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.5rem}
/* hero */
.hero{background:#fff;padding:3rem 0 2.2rem;border-bottom:1px solid var(--line)}
.wrap{max-width:1040px;margin:0 auto;padding:0 1.5rem}
.hero-grid{display:grid;grid-template-columns:360px 1fr;gap:3rem;align-items:center}
.badges{display:flex;flex-wrap:wrap;gap:.5em;margin-bottom:1.2em}
.badge{background:#f5f8fc;border:1px solid #dbe6f5;color:#1a56db;border-radius:999px;padding:.22em .95em;font-size:.82em}
.btn{display:inline-block;background:var(--brand);color:#fff!important;padding:.65em 1.7em;border-radius:8px;text-decoration:none;font-weight:600;margin:.2em .45em .2em 0;font-size:.95em}
.btn:hover{filter:brightness(1.08)}
.btn.ghost{background:#fff;color:var(--brand)!important;border:1px solid var(--brand)}
.toc-section{max-width:1040px;margin:0 auto;padding:2rem 1.5rem 2.5rem}
.toc-head{display:flex;align-items:baseline;justify-content:space-between;margin:0 0 1rem}
.toc-head h2{margin:0;font-size:1.25em}
.toc-head span{color:var(--muted);font-size:.86em}
.parts{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:.9rem}
.part-card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:1.05rem 1.25rem;transition:.15s}
.part-card:hover{border-color:#c6d6f0;box-shadow:0 4px 14px rgba(26,86,219,.06)}
.part-card h3{margin:0 0 .5em;font-size:.95em;color:var(--brand);border-bottom:2px solid #f0f4f9;padding-bottom:.35em}
.part-card ul{list-style:none;margin:0;padding:0}
.part-card li{padding:.24em 0;font-size:.9em;color:#3a4a55}
.part-card li a{color:var(--brand);text-decoration:none;font-weight:600}
.part-card li a:hover{text-decoration:underline}
.part-card li .free{background:#e8f6ee;color:#127a3d;font-size:.7em;border-radius:4px;padding:.08em .45em;margin-left:.45em}
.part-card li .lock{color:#a6b2bd;font-size:.76em;margin-left:.45em}
.app-card{grid-column:1/-1;background:#fbfcfe}
.app-card li{display:inline-block;margin-right:1.2em}
.contact-card{display:flex;gap:1.3em;align-items:center;background:#fff;border:1px solid var(--line);border-radius:12px;padding:1.2rem 1.5rem;max-width:620px;margin-top:1.6em;text-align:left;box-shadow:0 2px 8px rgba(20,30,50,.05)}
.contact-card .cqr{width:150px;height:auto;max-height:210px;border-radius:8px;border:1px solid #e4e8ee;flex:none}
.contact-card .ctitle{font-size:1.1em;font-weight:800;color:var(--brand);margin-bottom:.3em}
.contact-card .cinfo{color:#3a4a55;font-size:.92em}
.contact-card .cnote{color:#6b7a89;font-size:.84em;margin-top:.45em}
@media (max-width:840px){.hero-grid{grid-template-columns:1fr}.hero{padding:2rem 0 1.6rem}}
@media (max-width:640px){.contact-card{flex-direction:column;text-align:center}}</style></head><body>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Book","name":"掩模版光学仿真与 die-to-database 缺陷检测","inLanguage":"zh-CN","author":{"@type":"Organization","name":"析微视觉实验室"},"bookFormat":"https://schema.org/EBook","numberOfPages":200,"description":"从波动光学基础到掩模参考图渲染仿真与缺陷检测算法的完整中文教程。","isAccessibleForFree":false,"hasPart":{"@type":"Book","name":"免费试读版（前言+第1-4章）","isAccessibleForFree":true}}</script>
<section class="hero"><div class="wrap hero-grid">
  %s
  <div class="hero-copy">
    <div class="badges"><span class="badge">四篇 · 十九章</span><span class="badge">七个附录</span><span class="badge">Python 数值实验</span><span class="badge">零基础友好</span></div>
    <a class="btn" href="preface.html">开始免费试读</a>
    <a class="btn ghost" href="%s" target="_blank">GitHub 仓库</a>
    <div class="contact-card">
      <img class="cqr" src="wechat-qr.jpg" alt="作者微信二维码">
      <div class="cinfo">
        <div class="ctitle">添加作者微信 · 获取完整版</div>
        <div>完整版（四篇十九章 + 七附录，A4 排版 PDF）<br>限时优惠 <b style="font-size:1.22em;color:#c9281e">¥49.9</b> <s style="color:#9aa8b5">¥89.9</s> · 微信备注 <b>光学教材</b></div>
        <div class="cnote">姊妹篇《大模型：从 Transformer 到部署》见 <a href="https://jiejin93.github.io/llm-textbook/" target="_blank">LLM 教材站</a></div>
      </div>
    </div>
  </div>
</div></section>
<section class="toc-section">
  <div class="toc-head"><h2>完整目录</h2><span>绿色标记章节可免费试读</span></div>
  <div class="parts">%s</div>
</section>
</body></html>""" % (KATEX, cover_html, REPO, parts_html)
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(idx)
    print("trial site built:", OUT)
