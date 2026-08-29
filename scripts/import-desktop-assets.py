# -*- coding: utf-8 -*-
"""Copy + optimize prototype screenshots from Desktop/素材 into the project folder."""
import os
from PIL import Image

SRC = r"C:\Users\Administrator\Desktop\素材"
DST = r"C:\Users\Administrator\Documents\ChatGPT\个人作品集网站\projects\store-management-system"
MAX_W = 1280
QUALITY = 82

# source filename -> ascii target filename
MAP = {
    "订货推荐.png": "order-recommend.webp",
    "订单评价.png": "order-review.webp",
    "门店监控.png": "store-monitor.webp",
    "门店监控 (2).png": "store-monitor-2.webp",
    "门店客流统计.png": "store-traffic.webp",
    "加盟.png": "franchise-overview.webp",
    "填写加盟申请页.png": "franchise-apply-form.webp",
    "申请加盟状态.png": "franchise-apply-status.webp",
    "地址审核状态.png": "address-review-status.webp",
    "地址审核状态详情.png": "address-review-detail.webp",
    "查看审核详情.png": "review-detail.webp",
    "警告信.png": "warning-letter.webp",
    "稽核问题管理.png": "audit-issue-management.webp",
    "稽核问题管理2.png": "audit-issue-management-2.webp",
    "稽核草稿删除.png": "audit-draft-delete.webp",
    "稽核查新建看.png": "audit-create-view.webp",
    "门店稽核问题.png": "store-audit-issues.webp",
    "app稽核.png": "app-audit.webp",
    "APP稽核2.png": "app-audit-2.webp",
}

os.makedirs(DST, exist_ok=True)
missing = [f for f in MAP if not os.path.exists(os.path.join(SRC, f))]
if missing:
    raise SystemExit("missing sources: " + ", ".join(missing))

total_in = total_out = 0
for src_name, dst_name in MAP.items():
    src_path = os.path.join(SRC, src_name)
    dst_path = os.path.join(DST, dst_name)
    im = Image.open(src_path)
    total_in += os.path.getsize(src_path)
    # flatten alpha onto white
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im).convert("RGB")
    else:
        im = im.convert("RGB")
    w, h = im.size
    if w > MAX_W:
        nh = int(h * MAX_W / w)
        im = im.resize((MAX_W, nh), Image.LANCZOS)
    im.save(dst_path, "WEBP", quality=QUALITY, method=6)
    total_out += os.path.getsize(dst_path)
    print("%-24s %sx%s -> %s  %6.0f KB" % (src_name, w, h, dst_name, os.path.getsize(dst_path) / 1024))

print("TOTAL in %.1f MB -> out %.1f MB" % (total_in / 1024 / 1024, total_out / 1024 / 1024))
