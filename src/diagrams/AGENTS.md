# src/diagrams/ — 规则层

继承根规则，见 [../../AGENTS.md](../../AGENTS.md)。

src/diagrams/ 特有约束：
- 新项目图 → 在 projects/ 建模块并在 [__init__.py](__init__.py) 注册入 DIAGRAMS，否则 render_all() 不可见
- 色彩与无障碍 → 只经 [theme.py](theme.py) / [svg.py](svg.py) 统一提供，项目模块不许自定义
- 每张图必须通过 [tests/README.md](../../tests/README.md) 列出的契约测试
- 文件职责 → 见 [README.md](README.md)