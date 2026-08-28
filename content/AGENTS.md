# content/ — 规则层

继承根规则，见 [../AGENTS.md](../AGENTS.md)。

content/ 特有约束：
- 改动数据后必须跑 `uv run pytest`，契约测试会强制校验
- domain 必须来自 7 类枚举（列表见 [README.md](README.md)），不许自造
- traits 按覆盖率规则维护（≥6/9 上移、项目层删除），不许拍脑袋增删
- content/ 只存数据不写逻辑；渲染逻辑在 src/ 与 templates/