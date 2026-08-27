# -*- coding: utf-8 -*-
"""Copy + optimize prototype screenshots from Desktop/素材 into the project folder."""
import os
from PIL import Image

SRC = r"C:\Users\Administrator\Desktop\素材"
DST = r"C:\Users\Administrator\Documents\ChatGPT\个人作品集网站\projects\store-management-system"
MAX_W = 1600

# source filename -> ascii target filename
MAP = {
    "订货推荐.png": "order-recommend.png",
    "订单评价.png": "order-review.png",
    "门店监控.png": "store-monitor.png",
    "门店监控 (2).png": "store-monitor-2.png",
    "门店客流统计.png": "store-traffic.png",
    "加盟.png": "franchise-overview.png",
    "填写加盟申请页.png": "franchise-apply-form.png",
    "申请加盟状态.png": "franchise-apply-status.png",
    "地址审核状态.png": "address-review-status.png",
    "地址审核状态详情.png": "address-review-detail.png",
    "查看审核详情.png": "review-detail.png",
    "警告信.png": "warning-letter.png",
    "稽核问题管理.png": "audit-issue-management.png",
    "稽核问题管理2.png": "audit-issue-management-2.png",
    "稽核草稿删除.png": "audit-draft-delete.png",
    "稽核查新建看.png": "audit-create-view.png",
    "门店稽核问题.png": "store-audit-issues.png",
    "app稽核.png": "app-audit.png",
    "APP稽核2.png": "app-audit-2.png",
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
    im.save(dst_path, "PNG", optimize=True)
    total_out += os.path.getsize(dst_path)
    print("%-24s %sx%s -> %s  %6.0f KB" % (src_name, w, h, dst_name, os.path.getsize(dst_path) / 1024))

print("TOTAL in %.1f MB -> out %.1f MB" % (total_in / 1024 / 1024, total_out / 1024 / 1024))
