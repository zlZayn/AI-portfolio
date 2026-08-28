# content/ — 作品集数据契约

- 职责：站点全部数据（用户文案 + 项目元数据 + 数据表快照），build.py 唯一数据源

## 字段表（projects.yaml 每个条目）

| 字段 | 含义 | 必填 |
| --- | --- | --- |
| id | 唯一标识（kebab-case，同时是页面锚点与图注册键） | 是 |
| name / tagline / quote | 展示文案 | 是 |
| domain | 7 类枚举之一（见下表） | 是 |
| description / grid_overview | 详情与卡片摘要 | 是 |
| ai_role / code_role | AI 与代码分工说明 | 是 |
| metric | 一句话指标 | 是 |
| github_url | 仓库链接，必须以 https://github.com/zlZayn/ 开头 | 是 |
| tech_stack.architecture / technology / delivery | 标签三组，均不许为空 | 是 |
| highlights[] | title + text；metric 可选 | 是 |

## domain 7 类枚举（判定标准）

| domain | 判定标准 | 当前项目 |
| --- | --- | --- |
| 数据处理 | 清洗 / 映射 / 统计计算类 | decision-maker、schema-mapper |
| RAG 检索 | 检索增强生成 | rag-embed |
| Agent 基础设施 | 工具 / 编排 / 框架层 | tool-calling、collaborate |
| 内容安全 | 审核 / 安全裁决 | tier-guardian |
| 视觉识别 | 截图 / 图像理解 | tablesnap |
| 离线内容生成 | 素材 → 离线产物 | raw-to-guide |
| AIGC 创作 | 生成式创作工作台 | imagora |

新增 domain 需同步 static/style.css 的 .tag-domain 色值与 tests/test_content_contract.py 的 DOMAINS 枚举。

## traits 规则（profile.yaml）

- 任一 tech_stack.architecture 标签覆盖率 ≥ 6/9 → 自动上移为 profile.traits（单一真相源，项目层删除），由测试强制
- traits 每项含 name + 一句"全部项目一致"的 note
- 当前已上移 4 项；覆盖率以上移时点实测为准（9 项目基线 = 8 个既有项目声明数 + 1（imagora 经核对具备同种设计、拍板归入 trait））：

| trait | 上移时点实测覆盖率 | 阈值 |
| --- | --- | --- |
| Prompt Engineering | 7/9 | ≥6/9 |
| Business / Third-Party API | 7/9 | ≥6/9 |
| Permission & Security Control | 6/9 | ≥6/9 |
| Atomic Tool | 6/9 | ≥6/9 |

- Permission & Security Control 的 6/9 = 5 个已声明项目（decision-maker / schema-mapper / tool-calling / tier-guardian / tablesnap）+ imagora（密钥铁律、路径白名单 pathtrust、类型契约同属该设计）
- Structured Output Parser 5/9 未达阈值，留在项目层；升到 6/9 时测试自动报错提示上移

## 图片命名规范（build.py 机制）

- 截图目录 = project id：images/\<id\>/
- 同批多图用 -top / -middle / -bottom 后缀堆叠成一张连续截图，其余按文件名升序内嵌
- 新图加入无需改配置，构建自动内嵌

## 数据表快照

- 版本化快照 → [data-tables/README.md](data-tables/README.md)

## 新项目入职 5 步

1. 在 projects.yaml 写条目（含 domain 与全部必填字段）
2. 对照 traits 覆盖率规则，确认无 ≥6/9 标签漏上移
3. 截图放 images/\<id\>/
4. 注册图模块（见 [../src/diagrams/README.md](../src/diagrams/README.md)）
5. 跑 `uv run pytest` + `uv run python build.py`

- 使用约束与工作偏好 → 见 [AGENTS.md](AGENTS.md)