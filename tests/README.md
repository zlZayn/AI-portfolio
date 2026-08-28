# tests/ — 测试手册

- 测试与源码对应关系：
- test_build.py：数据表快照 + 重复构建字节一致 → 对应 src/data_tables.py 与 build.py
- test_diagrams.py：9 图注册、架构表述、无障碍元数据、移动端画布 → 对应 src/diagrams/
- test_content_contract.py：内容契约（必填字段 / id 唯一 / domain 枚举 / github_url 前缀 / traits 覆盖率规则）→ 对应 content/projects.yaml 与 profile.yaml
- test_diagram_svg.py：Canvas 基元、对角线拒绝、连线标签层级与语义、对比度 → 对应 src/diagrams/svg.py 与 theme.py
- 运行：`uv run pytest`（等价 `uv run python -m unittest discover -s tests`）
- 特殊坑：
- 测试里的 build.assemble() 只写临时目录，不覆盖根 index.html
- 增删用例后 → 同步根 [AGENTS.md](../AGENTS.md) 验证快照数字
- 设计背景 → 见 [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)
- 使用约束与工作偏好 → 见 [AGENTS.md](AGENTS.md)