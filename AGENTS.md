# AI Portfolio — 维护索引

## 全局规则
- 架构设计 → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 双件分离：AGENTS.md 只写规则，README.md 只写文件职责与变更路由
- index.html 是构建产物，只许 build.py 重新生成，禁止手动编辑
- 快照数据 → [content/data-tables/README.md](content/data-tables/README.md)，刷新后必须重建并跑测试

## 常用命令
- `uv run python build.py` — 重建 index.html
- `uv run pytest` — 跑测试（等价 `uv run python -m unittest discover -s tests`）

## 验证快照（2026-08-24 实测）
- pytest: 15 passed / 0 failed
- 构建: 连续两次构建字节一致（由测试覆盖）

## 待办
- （暂无）

## 活跃坑
- 换页面色板 → 同时改 static/style.css 与 src/diagrams/theme.py 的同语义令牌，否则图表配色脱节
- 跑测试会打印 8 张图表的渲染日志，属正常输出

## 文档地图
- 架构设计 → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 源码手册 → [src/README.md](src/README.md)
- 图表包 → [src/diagrams/README.md](src/diagrams/README.md)
- 测试手册 → [tests/README.md](tests/README.md)
- 决策记录 → [.agents/notes/](.agents/notes/)