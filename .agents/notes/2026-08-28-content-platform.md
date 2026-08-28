# 决策：作品集内容平台化（2026-08-28）

已实施。

## 问题
- 作品集 8 项目纯手工维护，无类别维度，卡片无法一眼归位
- 大量公共标签（Prompt Engineering 等）重复出现在每个项目，项目层与全局特性混淆
- 新项目无入职约束，缺字段、漏标签只能靠人眼

## 决策
- domain 7 类枚举（数据处理 / RAG 检索 / Agent 基础设施 / 内容安全 / 视觉识别 / 离线内容生成 / AIGC 创作）
- traits 覆盖率规则：任一 architecture 标签覆盖率 ≥6/9 自动上移为 profile.traits（单一真相源），项目层只留差异化标签
- 契约测试强制：必填字段 / id 唯一 / domain 枚举 / github_url 前缀 / 覆盖率双向防漂移（漏上移、乱上移都红）
- content/ 建双件：README.md 数据契约 + AGENTS.md 规则层
- imagora 作为第 9 项目收录（domain = AIGC 创作）

## 替代方案（强制）
- 不分类保持现状：无法表达项目结构，新项目无约束，公共标签继续重复
- 粗类只有 4 种：同类多项目区分度低，卡片归位意义弱（维护者拍板 7 细类）
- traits 人工维护：项目层 + traits 双份声明，漂移风险靠人记；规则驱动才可机器校验

## 影响
- 新项目入职 5 步（见 [content/README.md](../../content/README.md) 契约），漏步测试即红
- 代价：新增 domain 需同步 3 处（README 枚举 / static/style.css 色值 / 测试 DOMAINS）
- 交叉引用：契约细节 → [content/README.md](../../content/README.md)；本记录与 [2026-08-24-doc-network-standardization.md](2026-08-24-doc-network-standardization.md) 同属文档体系建设