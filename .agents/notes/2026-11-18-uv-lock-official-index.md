# 决策：锁文件源由 pyproject 钉死，不再依赖「本机别配镜像」的自觉（2026-11-18）

状态：生效

## 问题

- uv.lock 的 10 行 registry 全是清华镜像 `https://pypi.tuna.tsinghua.edu.cn/simple/`
- 成因：本机全局 `%APPDATA%\uv\uv.toml` 配了 `index-url` 指向镜像，其优先级高于锁文件里既有的 registry 记录
- 于是任何一次 `uv lock` 都会把锁文件整片改写成镜像源，而锁文件是生成物，手改一次没用
- 本机连镜像很快，问题不在本地暴露；只在境外 CI 暴露 —— GitHub Actions 拉清华镜像 tcp 超时，`uv sync --frozen` 直接失败
- 同批事故已在 AI-batch-raw-to-offline-guide 复现过（Pages 部署失败，markupsafe 下载超时）

## 决策

- `pyproject.toml` 用 `[[tool.uv.index]]` 显式声明官方源并 `default = true`
- 项目级配置优先级高于用户级 `uv.toml`，`uv lock` 不再被本机镜像改写
- 判定标准：在配了镜像的机器上，不带任何参数跑 `uv lock`，`uv.lock` 里 `tsinghua` 出现次数必须为 0
- uv.lock 的 10 个包 registry 全部回 `https://pypi.org/simple`，**包版本零变化**（纯 URL 改写）

## 替代方案

- **只改锁文件、不改 pyproject**：锁文件是生成物，下一次 relock 就被打回，等于没修
- **`[tool.uv] default-index = "..."`**：uv 0.11 不认这个字段，报 `unknown field` 并整体忽略 `[tool.uv]` 节，看起来配了其实没生效（实测），必须用 `[[tool.uv.index]]` 表
- **让每台机器删掉 uv.toml 的 index-url**：属个人环境，换机器/换人即失效，不能作为仓库约束
- **只在 CI 侧覆盖 `UV_DEFAULT_INDEX`**：能救 CI，但本地 relock 仍会污染锁文件，问题只被推迟

## 影响

- 收益：锁文件不再可能被本机镜像悄悄改写；CI 与本地解析同一组 URL，可复现
- 代价：本机下载依赖走官方源，速度低于镜像（如需加速，用命令行 `--default-index` 临时覆盖，不落盘）
- 验证：`uv lock`（无参数）后 tsinghua=0；`uv sync --frozen --group dev` 正常；ruff check/format 全绿；pytest 27 passed；build.py 重建 index.html 与 9 个 SVG 无 diff
- 关联：[2026-08-24-doc-network-standardization.md](2026-08-24-doc-network-standardization.md)（同属仓库可移植性）
