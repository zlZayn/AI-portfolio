# src/diagrams/ — 编辑性 SVG 图表包

- 职责：为 9 个项目渲染确定性、可访问的编辑性 SVG
- __init__.py：DIAGRAMS 注册表 + render_all()，被 build.py 依赖；新图必须先注册；改后必跑 tests/test_diagrams.py
- theme.py：THEME 语义色令牌，被全部 projects/*.py 依赖；改配色必须同步 static/style.css
- svg.py：Canvas 与节点/区间/连线/标签基元，被全部 projects/*.py 依赖；改后必跑 tests/test_diagram_svg.py
- projects/*.py：每项目一个手调布局，只写内容与几何，不定义色彩与无障碍
- projects/imagora.py：Imagora 双模式生图工作台图（注册键 imagora）
- 变更影响路由：改这里 → 同步根 [AGENTS.md](../../AGENTS.md) 待办/坑 + 架构影响写 [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md)
- 使用约束与工作偏好 → 见 [AGENTS.md](AGENTS.md)