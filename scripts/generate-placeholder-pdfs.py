# -*- coding: utf-8 -*-
"""Generate placeholder PDFs (resume + sample PRDs) using reportlab."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCENT = colors.HexColor("#4f46e5")
INK = colors.HexColor("#21242c")
MUTED = colors.HexColor("#6b7280")

try:
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("SiteCJK", "C:/Windows/Fonts/simhei.ttf"))
    FONT = "SiteCJK"
    print("using SimHei TTF")
except Exception as exc:  # pragma: no cover
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    FONT = "STSong-Light"
    print("SimHei unavailable, using STSong-Light:", exc)

ST = {
    "title": ParagraphStyle("title", fontName=FONT, fontSize=22, leading=28, textColor=ACCENT, spaceAfter=6),
    "sub": ParagraphStyle("sub", fontName=FONT, fontSize=9, leading=13, textColor=MUTED, spaceAfter=10),
    "h": ParagraphStyle("h", fontName=FONT, fontSize=13, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=4),
    "p": ParagraphStyle("p", fontName=FONT, fontSize=10.5, leading=16, textColor=INK, wordWrap="CJK"),
    "kv": ParagraphStyle("kv", fontName=FONT, fontSize=10.5, leading=19, textColor=INK),
    "note": ParagraphStyle("note", fontName=FONT, fontSize=9.5, leading=14, textColor=MUTED, spaceBefore=16),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def blocks_to_flowables(blocks):
    flow = []
    for b in blocks:
        t = b["t"]
        if t == "title":
            flow.append(Paragraph(esc(b["x"]), ST["title"]))
            flow.append(Spacer(1, 4))
        elif t == "sub":
            flow.append(Paragraph(esc(b["x"]), ST["sub"]))
        elif t == "h":
            flow.append(Paragraph(esc(b["x"]), ST["h"]))
        elif t == "p":
            flow.append(Paragraph(esc(b["x"]), ST["p"]))
        elif t == "kv":
            flow.append(Paragraph("<font color='#6b7280'>%s</font>　%s" % (esc(b["k"]), esc(b["v"])), ST["kv"]))
        elif t == "sp":
            flow.append(Spacer(1, b["h"]))
    return flow

RESUME_ZH = [
    {"t": "title", "x": "个人简历（占位）"},
    {"t": "sub", "x": "占位文件 · 请将你的真实简历导出为 PDF 后替换 assets/resume.pdf"},
    {"t": "sp", "h": 12},
    {"t": "kv", "k": "姓名", "v": "你的姓名"},
    {"t": "kv", "k": "求职方向", "v": "产品经理"},
    {"t": "kv", "k": "联系方式", "v": "your@email.com · 微信：your-wechat-id"},
    {"t": "sp", "h": 10},
    {"t": "h", "x": "教育经历"},
    {"t": "p", "x": "· 学校 / 专业 / 时间（占位，请替换）"},
    {"t": "h", "x": "工作经历"},
    {"t": "p", "x": "· 公司 / 岗位 / 时间（占位，请替换）"},
    {"t": "p", "x": "· 主要职责与业绩亮点（占位，请替换）"},
    {"t": "h", "x": "项目经历"},
    {"t": "p", "x": "· 项目一：项目名 / 我的角色 / 结果（占位，请替换）"},
    {"t": "p", "x": "· 项目二：项目名 / 我的角色 / 结果（占位，请替换）"},
    {"t": "h", "x": "技能"},
    {"t": "p", "x": "· 需求分析 / 原型设计 / 数据分析 / 项目管理 / 跨部门协作（占位，请替换）"},
]

PRD_ZH = [
    {"t": "title", "x": "产品需求文档（PRD）"},
    {"t": "sub", "x": "示例项目 · 占位文档 · 请替换为你的完整 PRD（PDF）"},
    {"t": "sp", "h": 8},
    {"t": "kv", "k": "文档版本", "v": "v1.0（占位）"},
    {"t": "kv", "k": "作者", "v": "你的姓名"},
    {"t": "kv", "k": "日期", "v": "2025.01（占位）"},
    {"t": "h", "x": "1. 项目背景"},
    {"t": "p", "x": "· 描述项目要解决的问题、业务背景与机会点（占位，请替换）"},
    {"t": "p", "x": "· 说明当前方案存在的痛点与用户诉求（占位，请替换）"},
    {"t": "h", "x": "2. 产品目标"},
    {"t": "p", "x": "· 明确核心目标与衡量指标，例如注册转化率、次日留存等（占位，请替换）"},
    {"t": "h", "x": "3. 目标用户"},
    {"t": "p", "x": "· 描述核心用户画像、使用场景与需求洞察（占位，请替换）"},
    {"t": "h", "x": "4. 核心功能"},
    {"t": "p", "x": "· 功能一：说明功能流程与交互要点（占位，请替换）"},
    {"t": "p", "x": "· 功能二：说明功能流程与交互要点（占位，请替换）"},
    {"t": "p", "x": "· 功能三：说明功能流程与交互要点（占位，请替换）"},
    {"t": "h", "x": "5. 功能需求列表"},
    {"t": "p", "x": "· 按模块列出需求编号、优先级与验收标准（占位，请替换）"},
    {"t": "h", "x": "6. 数据指标"},
    {"t": "p", "x": "· 核心指标与北极星指标定义（占位，请替换）"},
    {"t": "h", "x": "7. 非功能需求"},
    {"t": "p", "x": "· 性能、安全、兼容性、可访问性要求（占位，请替换）"},
    {"t": "h", "x": "8. 里程碑与排期"},
    {"t": "p", "x": "· 版本计划与迭代节奏（占位，请替换）"},
    {"t": "note", "x": "—— 本 PDF 为占位文件，请用真实 PRD 替换 ——"},
]

def build_pdf(out_path, blocks, title):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT, 8.5)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(A4[0] / 2, 12 * mm, "%d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm, bottomMargin=18 * mm,
        title=title, author="你的姓名",
    )
    doc.build(blocks_to_flowables(blocks), onFirstPage=on_page, onLaterPages=on_page)
    print("wrote", os.path.relpath(out_path, ROOT), os.path.getsize(out_path), "bytes")

def main():
    A = os.path.join(ROOT, "assets")
    P = os.path.join(ROOT, "projects")
    build_pdf(os.path.join(A, "resume.pdf"), RESUME_ZH, "个人简历（占位）")
    build_pdf(os.path.join(P, "ai-interview-assistant", "PRD.pdf"), PRD_ZH, "产品需求文档 · AI 面试刷题助手（占位）")
    build_pdf(os.path.join(P, "fitness-app", "PRD.pdf"), PRD_ZH, "产品需求文档 · 轻运动打卡 App（占位）")

if __name__ == "__main__":
    main()
