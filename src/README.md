# src/ — 源码包手册

- 职责：构建期生成数据表 HTML（data_tables.py）与 SVG 图表（diagrams/）
- data_tables.py：generate_all() 读快照生成 HTML 表，被 [build.py](../build.py) 依赖；改后必跑 tests/test_build.py
- diagrams/：编辑性 SVG 图表包，被 build.py 依赖 → [diagrams/README.md](diagrams/README.md)
- 变更影响路由：改这里 → 同步根 [AGENTS.md](../AGENTS.md) 待办/坑 + 架构影响写 [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)
- 使用约束与工作偏好 → 见 [AGENTS.md](AGENTS.md)