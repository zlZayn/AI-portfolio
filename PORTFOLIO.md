# AI 项目作品集 — 项目文档

## 概述

Python 脚本 + Jinja2 模板生成的单页 HTML 作品集，展示 6 个 AI 项目。
部署到 GitHub Pages，输出单个自包含 HTML 文件。

**托管仓库：** [github.com/zlZayn/AI-tool-calling](https://github.com/zlZayn/AI-tool-calling)
（GitHub Pages 通过 `.github/workflows/static.yml` 自动部署，静态文件在 `index.html`）

每个项目也有独立仓库，各自右上方有 GitHub 图标链接跳转。

## 目录结构

```text
d:\PythonDirectory\AI-portfolio\
├── build.py                     # 主构建（YAML→Jinja2→单HTML）
├── generate_content.py          # 从项目源码生成数据对比表（HTML）
├── diagrams.py                  # Mermaid 流程图定义 + 调用 mmdc 渲染 SVG
├── puppeteer-config.json        # Puppeteer 的 Chrome 路径
├── requirements.txt             # jinja2, pyyaml, pygments
├── PORTFOLIO.md                 # ← 本文档，下次会话先读这个
│
├── content/
│   ├── profile.yaml             # 网站标题/描述/GitHub 链接
│   └── projects.yaml            # 6 个项目数据（描述/亮点/tech_stack/github_url）
│
├── templates/
│   ├── base.html                # HTML 骨架 + KaTeX CDN
│   └── sections/
│       ├── hero.html            # 理念区（大字排版 + 装饰 stat）
│       ├── grid.html            # 项目卡片网格（含 AI/Code 角色、指标、标签）
│       └── project.html         # 项目详情区块
│
├── assets/
│   ├── style.css                # 全部样式（构建时内联到 HTML）
│   ├── script.js                # JS 交互（构建时内联，含滚动隐现逻辑）
│   └── images/                  # 截图，按项目 ID 分子目录
│
└── index.html               # 最终产物（~1.4MB）
```

## 设计系统

### 配色（Warm & Playful 主题）

| 角色 | 色值 | 用途 |
| --- | --- | --- |
| 页面底色 | `#faf6ef` | 暖白背景 |
| 主色 | `#f97316` | 橙色，用于按钮/标题/accent |
| 辅色 | `#6366f1` | 靛蓝，AI 标签/图表 AI 节点 |
| 文本 | `#2d2b55` | 深暖色正文 |
| 辅助 | `#6c757d` | 灰色辅助文字 |

### 导航栏

- 背景完全透明，覆有规则橙色圆点矩阵
- 圆点从顶部到底部渐小（6px → 3px），密度 10px 间距
- 滚动监听：下滑时内容（Logo + 菜单）平滑淡出，上滑立即出现
- 圆点始终保持，文字悬停变橙色

### Hero 区域

- 左栏：大号字体（5.5rem）哲学标题 "AI 做理解 / 代码做执行"
- 右栏：极简 stat 装饰（"6 / 项目" + 橙色分隔线）
- 橙底渐变装饰条分隔标题与描述

### Grid 卡片

每张卡片展示：

- 标题 + GitHub 图标链接（新窗口打开仓库）
- 指标 badge（右上角）
- 一句话定位
- AI 角色 + Code 角色（紫色/橙色标签）
- 概要文字（grid_overview）
- 全部三组标签：architecture / technology / delivery

### 项目详情区块

- 白色圆角卡片（16px）在暖色背景上
- 标题 + GitHub 图标
- 引用块（橙色左边框 + 暖底色）
- 三组标签（同 grid）
- Mermaid 流程图（SVG，字体匹配系统字体）
- Highlights 要点卡片
- Generated content（数据对比 + 分类分析结果）

## 标签系统（三组分类）

2026年6月重构，从旧的扁平 category 改为三组：

### Architecture 标签（橙色渐变实心）

从架构图叶子节点选取：

- Prompt Engineering, Chain-of-Thought (CoT), RAG
- MCP, Function Calling, Tool Calling
- Structured Output Parser, Task Planner, Atomic Tool
- Multi-Agent, Sandbox
- Permission & Security, Timeout & Retry
- Business / Third-Party API

### Technology 标签（灰色边框透明底）

编程语言和具体库：

- Python, TypeScript, R
- pandas, Flask, SSE, ChromaDB, diskcache
- Zod, JSON Schema
- Sentence-Transformer, pytest

### Delivery 标签（浅灰填充）

交付方式：

- CLI, Web

## 构建流程

```text
build.py
├── 1. load_yaml()           ← content/profile.yaml + content/projects.yaml
├── 2. inline_images()       ← assets/images/{id}/*.png → base64 data URI
├── 3. generate_all()        ← 读取项目数据 CSV，生成对比表 HTML
├── 4. render_diagrams()     ← diagrams.py → mmdc → SVG（后处理替换字体）
├── 5. Jinja2 渲染           ← hero → grid → 6×project → base 拼装
├── 6. 注入 CSS + JS        ← style.css + table_css() + script.js
└── 7. 写出 output/index.html
```

## 构建命令

```bash
cd d:\PythonDirectory\AI-portfolio
python build.py                  # 完整构建
python diagrams.py               # 仅测试 Mermaid 渲染
python generate_content.py       # 仅测试数据表生成
```

构建产物：`index.html`，直接双击或 live-server 打开。

## ⚠️ 重要：容易踩坑的地方

### 1. Jinja2 访问字典键

```jinja
{# 正确——用中括号 #}
{% for item in category['items'] %}

{# 错误——不可用 category.items（Jinja2 解析为 Python 方法） #}
```

### 2. YAML description 格式

使用 `>-`（折叠块）。段落用空行分隔，会自动转 `<br>`。

### 3. YAML 文件编码

`yaml.safe_load()` 必须指定 `encoding="utf-8"`，Windows 默认 GBK。

### 4. Mermaid CLI 安装

```bash
$env:PUPPETEER_SKIP_DOWNLOAD = "true"
npm install -g @mermaid-js/mermaid-cli --registry=https://registry.npmmirror.com
```

构建参数：`-b transparent`（透明背景）、`--width 900`。
mmdc 必须写 `mmdc.cmd`（Windows 上 npm cmd wrapper）。

### 5. 字体统一

Mermaid SVG 默认字体是 "trebuchet ms"，在 `render_mermaid()` 中后处理替换为系统字体：

```python
svg = svg.replace(
    'font-family:"trebuchet ms",verdana,arial,sans-serif',
    'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif',
)
```

### 6. 表格 hover 颜色冲突

```css
.data-table tr.changed-row:hover { background: #fef3c7; }
```

### 7. Grid 卡片嵌套 `<a>` 陷阱

卡片容器是 `<div onclick="location.hash='#...'">`，内部 GitHub 图标用独立的 `<a>`。
不可用 `<a>` 作为卡片容器，否则嵌套 `<a>` 导致 HTML 非法、布局崩溃。

### 8. 导航栏滚动隐现

`script.js` 监听 scroll 方向：下滑隐藏内容、上滑显示、顶部 50px 内始终显示。
CSS `transition: opacity 0.08s linear` 保证平滑。

## 数学公式规范

KaTeX 通过 CDN 加载（`base.html`）：

- 行内：`\(...\)`
- 块级：`$$...$$`

只包真正的数学符号，算法描述不包。

## 修改指南

### 修改项目描述

1. 编辑 `content/projects.yaml` 中对应项目字段
2. `python build.py` 重建
3. 打开 `output/index.html` 看效果

### 新增项目

1. `projects.yaml` 添加项目块（含 github_url）
2. `diagrams.py` 添加 Mermaid 定义
3. `generate_content.py` 添加数据生成（可选）
4. 截图放 `assets/images/{project_id}/`
5. `python build.py` 重建

### 修改流程图

编辑 `diagrams.py` 中对应函数。classDef 颜色：

```text
input #faf6ef/#d1d5db  proc #fff7ed/#f97316
ai    #f5f3ff/#6366f1  dec  #fef3c7/#d97706
ok    #f0fdf4/#16a34a  stop #fef2f2/#dc2626
```

### 新增 CSS tag 颜色

三组标签统一用同一套尺寸（padding/border-radius/font-size），仅颜色不同：

- `.tag-arch` — 橙色渐变实心
- `.tag-tech` — 灰色边框透明
- `.tag-delivery` — 浅灰填充

## 环境与依赖

- 工作目录：`d:\PythonDirectory`
- Python 3.12
- Node.js（E:\nodejs\），全局装 mermaid-cli
- Chrome
- PowerShell 7.6.2
- npm registry 设为 npmmirror.com（国内镜像）
- **本目录是 git 仓库**，托管在 `zlZayn/AI-portfolio`
