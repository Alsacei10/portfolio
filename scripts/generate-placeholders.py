# -*- coding: utf-8 -*-
"""Generate placeholder PNG assets for the portfolio site (run once)."""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"

def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)

def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def gradient(size, top, bottom):
    w, h = size
    t = np.linspace(0.0, 1.0, h, dtype=np.float64)[:, None, None]
    top = np.array(top, dtype=np.float64)
    bottom = np.array(bottom, dtype=np.float64)
    arr = (top + (bottom - top) * t).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, w, axis=1), "RGB")

def rounded(size, radius, color, outline=None, ow=0):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=color, outline=outline, width=ow)
    return img

def overlay_circles(base, alpha=16, n=3):
    d = ImageDraw.Draw(base, "RGBA")
    w, h = base.size
    for i in range(n):
        r = int(min(w, h) * (0.35 + 0.18 * i))
        cx = int(w * (0.18 + 0.32 * i))
        cy = int(h * (0.20 + 0.30 * (i % 2)))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, alpha))
    return base

def box(d, x, y, w, h, fill, radius=10):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill)

def browser_mockup(w, h, accent, layout="dashboard"):
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 44], fill="#f3f4f8")
    d.line([0, 44, w, 44], fill="#e5e7ef", width=1)
    for i, c in enumerate(["#f87171", "#fbbf24", "#34d399"]):
        d.ellipse([20 + i * 26, 16, 32 + i * 26, 28], fill=c)
    d.rounded_rectangle([w - 260, 12, w - 16, 32], radius=10, fill="#ffffff", outline="#e5e7ef", width=1)
    accent = hx(accent)
    accent_soft = tuple(min(255, c + 70) for c in accent)
    sw = 200
    d.rectangle([0, 44, sw, h], fill="#f7f8fb")
    d.line([sw, 44, sw, h], fill="#eceef4", width=1)
    for i in range(5):
        sy = 70 + i * 56
        active = (i == 0)
        fill = accent if active else "#e8eaf1"
        w2 = 150 if active else 130
        box(d, 26, sy, w2, 26, fill, radius=13)
    cx = sw
    mw = w - sw
    if layout == "dashboard":
        box(d, cx + 28, 72, mw - 56, 96, accent, radius=14)
        box(d, cx + 28, 98, 140, 14, (255, 255, 255), radius=7)
        for i in range(3):
            bx = cx + 28 + i * ((mw - 56 - 24) // 3 + 8)
            bw = (mw - 56 - 24) // 3
            box(d, bx, 196, bw, 96, "#ffffff", radius=12)
            d.rounded_rectangle([bx, 196, bx + bw, 196 + 96], radius=12, outline="#e5e7ef", width=1)
            box(d, bx + 18, 220, 60, 14, accent_soft, radius=7)
            box(d, bx + 18, 246, bw - 36, 10, "#e2e5ec", radius=5)
            box(d, bx + 18, 262, bw - 70, 10, "#eceef3", radius=5)
        for i in range(2):
            bx = cx + 28
            by = 316 + i * 108
            bw = mw - 56
            box(d, bx, by, bw, 92, "#ffffff", radius=12)
            d.rounded_rectangle([bx, by, bx + bw, by + 92], radius=12, outline="#e5e7ef", width=1)
            box(d, bx + 20, by + 22, 90, 10, "#e2e5ec", radius=5)
            box(d, bx + 20, by + 44, bw - 40, 10, "#eceef3", radius=5)
            box(d, bx + 20, by + 60, int((bw - 40) * 0.62), 10, "#eceef3", radius=5)
    elif layout == "chat":
        box(d, cx + 28, 72, mw - 56, 40, accent, radius=12)
        box(d, cx + 48, 84, 120, 12, (255, 255, 255), radius=6)
        for i in range(3):
            left = (i % 2 == 0)
            by = 140 + i * 96
            bw = int((mw - 56) * 0.55)
            if left:
                box(d, cx + 28, by, bw, 64, "#f0f2f7", radius=14)
                box(d, cx + 46, by + 18, 80, 10, "#d9dce6", radius=5)
                box(d, cx + 46, by + 36, int(bw * 0.6), 10, "#e4e7ef", radius=5)
            else:
                bx = cx + 28 + (mw - 56) - bw
                box(d, bx, by, bw, 64, accent_soft, radius=14)
                box(d, bx + 18, by + 18, 90, 10, accent, radius=5)
                box(d, bx + 18, by + 36, int(bw * 0.55), 10, accent, radius=5)
        box(d, cx + 28, h - 64, mw - 56, 40, "#ffffff", radius=20)
        d.rounded_rectangle([cx + 28, h - 64, cx + 28 + mw - 56, h - 24], radius=20, outline="#d9dce6", width=1)
        box(d, cx + 46, h - 52, mw - 56 - 100, 16, "#eceef3", radius=8)
        box(d, cx + 28 + mw - 56 - 66, h - 52, 48, 16, accent, radius=8)
    elif layout == "form":
        box(d, cx + 28, 72, mw - 56, 40, accent, radius=12)
        for i in range(4):
            fy = 140 + i * 84
            box(d, cx + 28, fy, 90, 12, "#c9cdd9", radius=6)
            box(d, cx + 28, fy + 26, mw - 56, 34, "#ffffff", radius=10)
            d.rounded_rectangle([cx + 28, fy + 26, cx + 28 + mw - 56, fy + 60], radius=10, outline="#e0e3ec", width=1)
        box(d, cx + 28, 140 + 4 * 84 + 8, 200, 40, accent, radius=20)
    else:
        box(d, cx + 28, 72, mw - 56, 40, accent, radius=12)
        for r in range(2):
            for c in range(3):
                bx = cx + 28 + c * ((mw - 56 - 24) // 3 + 8)
                bw = (mw - 56 - 24) // 3
                by = 140 + r * 150
                box(d, bx, by, bw, 128, "#ffffff", radius=12)
                d.rounded_rectangle([bx, by, bx + bw, by + 128], radius=12, outline="#e5e7ef", width=1)
                box(d, bx + 16, by + 16, bw - 32, 52, accent_soft, radius=8)
                box(d, bx + 16, by + 80, 70, 10, "#d9dce6", radius=5)
                box(d, bx + 16, by + 98, bw - 32, 10, "#eceef3", radius=5)
    return img

def cover(title, subtitle, accent_top, accent_bottom, out, layout):
    W, H = 1200, 750
    img = gradient((W, H), hx(accent_top), hx(accent_bottom)).convert("RGBA")
    overlay_circles(img)
    d = ImageDraw.Draw(img)
    d.text((64, 44), title, font=f(40, True), fill=(255, 255, 255, 255))
    d.text((66, 104), subtitle, font=f(21), fill=(255, 255, 255, 235))
    mh = 560
    mw = int(mh * 1000 / 640)
    m = browser_mockup(1000, 640, accent_top, layout).resize((mw, mh), Image.LANCZOS)
    x = (W - mw) // 2
    y = 150
    img.paste(m, (x, y), m)
    d = ImageDraw.Draw(img)
    d.text((64, H - 52), "示例作品 · 原型图占位，替换为你的真实截图", font=f(17), fill=(255, 255, 255, 200))
    img.convert("RGB").save(out, "PNG")

def screenshot(title, caption, accent, out, layout, idx):
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), "#f2f4f8")
    d = ImageDraw.Draw(img)
    d.text((64, 44), title, font=f(30, True), fill="#1f2430")
    d.text((66, 96), caption, font=f(19), fill="#8a90a0")
    mw, mh = 940, 600
    m = browser_mockup(1000, 640, accent, layout).resize((mw, mh), Image.LANCZOS)
    x, y = (W - mw) // 2, 150
    sh = rounded((mw, mh), 16, (0, 0, 0, 36))
    img.paste(sh, (x + 8, y + 10), sh)
    img.paste(m, (x, y), m)
    img.convert("RGB").save(out, "PNG")

def avatar(out):
    S = 512
    img = gradient((S, S), hx("#818cf8"), hx("#4f46e5")).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.ellipse([26, 26, S - 26, S - 26], outline=(255, 255, 255, 90), width=8)
    d.text((S // 2, S // 2 + 6), "PM", font=f(190, True), fill=(255, 255, 255, 255), anchor="mm")
    img.convert("RGB").save(out, "PNG")

def favicon(out):
    S = 256
    img = gradient((S, S), hx("#818cf8"), hx("#4f46e5")).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([8, 8, S - 8, S - 8], radius=56, outline=(255, 255, 255, 70), width=6)
    d.text((S // 2, S // 2 + 4), "P", font=f(120, True), fill=(255, 255, 255, 255), anchor="mm")
    img.convert("RGB").save(out, "PNG")

def og_cover(out):
    W, H = 1200, 630
    img = gradient((W, H), hx("#4f46e5"), hx("#312e81")).convert("RGBA")
    overlay_circles(img)
    d = ImageDraw.Draw(img)
    d.text((80, 150), "戴章勇", font=f(72, True), fill=(255, 255, 255, 255))
    d.text((84, 260), "B 端产品经理作品集 · 原型设计与 PRD", font=f(32), fill=(255, 255, 255, 235))
    d.text((80, 360), "展示产品设计原型与产品需求文档（PRD）", font=f(24), fill=(255, 255, 255, 190))
    d.text((W - 80, H - 60), "个人作品集网站", font=f(20), fill=(255, 255, 255, 170), anchor="rs")
    img.convert("RGB").save(out, "PNG")

def main():
    A = os.path.join(ROOT, "assets", "img")
    os.makedirs(A, exist_ok=True)
    avatar(os.path.join(A, "avatar.png"))
    favicon(os.path.join(A, "favicon.png"))
    og_cover(os.path.join(A, "og-cover.png"))
    P = os.path.join(ROOT, "projects")
    cover("AI 面试刷题助手", "AI 驱动的面试准备与模拟练习工具", "#6366f1", "#312e81",
          os.path.join(P, "ai-interview-assistant", "cover.png"), "dashboard")
    screenshot("界面示意 01 · 首页与生成面试题", "AI 面试刷题助手 · 原型图占位", "#6366f1",
               os.path.join(P, "ai-interview-assistant", "01-home.png"), "dashboard", 1)
    screenshot("界面示意 02 · AI 模拟面试对话", "AI 面试刷题助手 · 原型图占位", "#6366f1",
               os.path.join(P, "ai-interview-assistant", "02-chat.png"), "chat", 2)
    screenshot("界面示意 03 · 错题与能力复盘", "AI 面试刷题助手 · 原型图占位", "#6366f1",
               os.path.join(P, "ai-interview-assistant", "03-dashboard.png"), "grid", 3)
    cover("轻运动打卡 App", "游戏化激励的日常运动与习惯养成", "#06b6d4", "#0e7490",
          os.path.join(P, "fitness-app", "cover.png"), "form")
    screenshot("界面示意 01 · 今日打卡首页", "轻运动打卡 App · 原型图占位", "#0ea5e9",
               os.path.join(P, "fitness-app", "01-home.png"), "dashboard", 1)
    screenshot("界面示意 02 · 打卡记录与数据", "轻运动打卡 App · 原型图占位", "#0ea5e9",
               os.path.join(P, "fitness-app", "02-record.png"), "form", 2)
    screenshot("界面示意 03 · 成就与勋章墙", "轻运动打卡 App · 原型图占位", "#0ea5e9",
               os.path.join(P, "fitness-app", "03-achievements.png"), "grid", 3)
    print("placeholders generated")

if __name__ == "__main__":
    main()
