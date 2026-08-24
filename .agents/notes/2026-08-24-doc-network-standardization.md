# 决策：文档网络标准化（2026-08-24）

已实施。

## 问题
- 根目录存在独立 ARCHITECTURE.md，违反「架构文档统一放 docs/ARCHITECTURE.md」的约定
- 项目缺根 AGENTS.md 仪表盘，src/、src/diagrams/、tests/ 缺双件，文档网络无法双向索引

## 决策
- 根 ARCHITECTURE.md 经 git mv 移入 docs/ARCHITECTURE.md
- 根 AGENTS.md 建仪表盘，文档地图以相对链接指向 docs/ARCHITECTURE.md 与各子手册
- src/、src/diagrams/ 补 AGENTS.md（规则层）+ README.md（文档层），tests/ 补 README.md
- 全库检索并更新指向 ARCHITECTURE.md 的路径引用（README.md 链接 + .codex-context.md 提及）

## 替代方案（强制）
- 保留根 ARCHITECTURE.md 只加指针：根目录同层文件继续堆积，位置约定仍分裂
- 仅移动不建根 AGENTS.md：文档地图无载体，子 README 无处回根，网络单向断链
- 合并进 README.md：用户文档混入开发者设计细节，违反分层职责分离

## 影响
- 代价：一次性的相对路径迁移（README.md 链接 + .codex-context.md 路径提及）
- 收益：任意文档两跳可达根索引，双向不断链；根仪表盘自动注入
- 验证：check-links.py 全库零 ERROR；pytest 15 passed 不变