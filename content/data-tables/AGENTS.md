# data-tables/ — 规则层

继承根规则，见 [../../AGENTS.md](../../AGENTS.md)。

data-tables/ 特有约束：
- 快照只读 source 项目产物，刷新必须 review 数据 diff
- 刷新后必须重建 index.html 并跑 pytest（同一次变更内）