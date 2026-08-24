# src/ — 规则层

继承根规则，见 [../AGENTS.md](../AGENTS.md)。

src/ 特有约束：
- 数据表生成只读 content/data-tables/ 快照，不许读外部仓库
- 新增渲染逻辑 → 必须补 [tests/](../tests/) 契约测试
- 文件职责与导出 → 见 [README.md](README.md)