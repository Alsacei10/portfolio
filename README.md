# 个人作品集网站

一个纯静态的个人作品集网站，用于展示**产品设计原型图**与**产品需求文档（PRD）**，可免费部署到 GitHub Pages，面试官通过公开链接即可访问。

- 技术栈：HTML + CSS + 原生 JavaScript + JSON，零构建、无外部 CDN/字体依赖
- 语言：中文
- 结构：首页（个人介绍 + 项目卡片）→ 项目详情页（图集 + PRD 查看/下载）

> 当前站点已填入真实简历信息：姓名「戴章勇」、邮箱 809968881@qq.com、证件照头像、真实简历 PDF（`assets/resume.pdf`）。微信号待补充，补充后在 `data/projects.json` 的 `profile.wechat` 填入即可。

## 目录结构

```
个人作品集网站/
├─ index.html              # 首页
├─ project.html            # 项目详情页（?id=xxx）
├─ 404.html                # 404 页面
├─ data/
│  └─ projects.json        # ★ 个人资料 + 项目数据（唯一需要维护的接口）
├─ assets/
│  ├─ css/style.css
│  ├─ js/main.js           # 首页渲染
│  ├─ js/project.js        # 详情页渲染
│  ├─ js/lightbox.js       # 图片放大预览
│  ├─ img/                 # 头像、favicon、分享图
│  └─ resume.pdf           # ★ 简历（占位，请替换）
├─ projects/
│  ├─ ai-interview-assistant/   # 示例项目一：素材 + PRD
│  │  ├─ cover.png
│  │  ├─ 01-home.png ...
│  │  └─ PRD.pdf
│  └─ fitness-app/               # 示例项目二：素材 + PRD
├─ scripts/
│  ├─ check-content.js           # 内容校验脚本
│  ├─ generate-placeholders.py   # （可选）重新生成占位图（谨慎：会覆盖真实头像）
│  └─ generate-placeholder-pdfs.py # （可选）重新生成占位 PDF（谨慎：会覆盖真实简历）
└─ README.md
```

## 本地预览

直接用浏览器打开 `index.html` 会因浏览器安全策略无法读取 JSON，请使用本地静态服务器：

```bash
# 方式一：Python（推荐）
python -m http.server 8000
# 然后访问 http://localhost:8000

# 方式二：Node
npx serve .
```

## 替换为你的真实内容

网站所有展示内容都来自 `data/projects.json`，**不需要改任何 HTML/JS/CSS**。

### 1. 替换个人信息（profile 字段）

| 字段 | 说明 |
| --- | --- |
| `name` | 你的姓名 |
| `role` | 求职方向，如「产品经理」 |
| `tagline` | 首页一句话定位 |
| `avatar` | 头像图片路径（推荐正方形 PNG，如 512×512） |
| `email` / `wechat` | 联系方式 |
| `resumePdf` | 简历 PDF 路径 |
| `bio` | 「关于我」段落（数组，每项一段） |
| `skills` | 技能/工具标签（数组） |

替换 `assets/img/avatar.png` 和 `assets/resume.pdf` 为你的真实头像与简历即可。

### 2. 新增/替换项目

1. 在 `projects/` 下新建文件夹，建议用英文/拼音命名（如 `projects/ai-interview-assistant/`）。
2. 放入素材（PNG/JPG 均可）：
   - `cover.*`：项目封面，推荐 **16:10**（如 1200×750）；
   - 若干界面截图：如 `01-home.*`、`02-chat.*`；
   - `PRD.pdf`：产品需求文档 PDF。
   - 然后用 `python scripts/import-desktop-assets.py` 导入，`python scripts/optimize-images.py` 统一压缩为 WebP。
3. 在 `data/projects.json` 的 `projects` 数组中新增一条记录。

| 字段 | 说明 |
| --- | --- |
| `id` | 唯一标识（英文/拼音），用于链接 `project.html?id=xxx`，同时对应文件夹名 |
| `title` | 项目名称 |
| `tagline` | 一句话简介（卡片与详情页顶部） |
| `role` | 你在项目中的角色 |
| `period` | 项目周期 |
| `tags` | 标签数组（如 `["AI", "Web"]`） |
| `cover` | 封面图路径 |
| `images` | 界面截图数组，可用字符串路径，或 `{"src": "路径", "caption": "说明文字"}`（带说明更利于面试官理解） |
| `prdPdf` | PRD PDF 路径（可选，不填则详情页不显示查看/下载按钮） |
| `summary` | 项目概述（数组，每项一段） |
| `links.prototype` | （可选）在线原型链接，留空字符串则不显示 |

### 3. 校验内容

```bash
node scripts/check-content.js
```

脚本会检查 JSON 中引用的图片/PDF 是否都存在、必填字段是否完整，避免上线后出现 404。

## 素材建议

- 图片格式：你提供 PNG / JPG 即可；站点内会自动转换为 WebP（宽度 ≤1280），总大小约 1MB，国内访问更快
- 原型截图宽度 ≤1600px（2 倍屏下约 800dp），控制文件大小
- 封面建议 16:10；详情图建议宽度一致，观感更整齐
- PRD 导出为 PDF（不要用 Word 直接放，浏览器预览体验差）

## 部署到 GitHub Pages

1. 在 GitHub 新建仓库（公开），例如 `username.github.io`（站点将位于 https://username.github.io/）或任意公开仓库名 `portfolio`（站点将位于 https://username.github.io/portfolio/）。
2. 在项目目录执行：

```bash
git init                              # 若尚未初始化
git add -A
git commit -m "feat: 个人作品集网站 v1"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

3. 打开 GitHub 仓库 → **Settings → Pages** → Source 选择 **Deploy from a branch**，Branch 选择 `main`，目录选 **/ (root)** → Save。
4. 等待 1-2 分钟，访问 https://<你的用户名>.github.io/<仓库名>/ 即可看到网站。

> 本项目所有资源均使用相对路径，因此部署在子路径（如 `/portfolio/`）下也能正常访问。

## 常见问题

- **双击 index.html 打不开/内容空白**：浏览器安全策略禁止 `file://` 下读取 JSON，请用本地服务器预览或部署后访问。
- **手机上 PDF 无法预览**：部分手机浏览器不支持内嵌 PDF，请点「下载 PRD」按钮。
- **微信中分享预览图不显示**：`og:image` 使用相对路径，部署后可将 `index.html` 中的 `og:image` 改为完整链接（如 `https://username.github.io/portfolio/assets/img/og-cover.png`）。
