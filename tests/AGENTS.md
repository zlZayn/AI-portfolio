# tests/ — 规则层

继承根规则，见 [../AGENTS.md](../AGENTS.md)。

tests/ 特有约束：
- 增删用例后必须同步根 [AGENTS.md](../AGENTS.md) 验证快照数字
- 测试只写临时目录，不覆盖根 index.html
- [test_content_contract.py](test_content_contract.py) 是内容数据强制闸门，改数据必须全绿