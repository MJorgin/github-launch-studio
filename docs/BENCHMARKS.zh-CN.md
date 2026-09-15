# 对标地图

以下数据于 2026-09-15 通过 GitHub 公开 API 观察。Star 会持续变化，可用下面命令刷新：

```bash
python3 scripts/benchmark_github.py \
  --config benchmarks/representative-tools.json \
  --format markdown
```

## 相邻品类

| 品类 | 仓库 | Stars | Forks | 最近推送 | 许可证 | 强项 |
| --- | --- | ---: | ---: | --- | --- | --- |
| README 编辑器 | [octokatherine/readme.so](https://github.com/octokatherine/readme.so) | 4,628 | 362 | 2026-03-13 | MIT | 拖拽式 README 区块编辑，上手简单。 |
| Profile README | [rahuldkjain/github-profile-readme-generator](https://github.com/rahuldkjain/github-profile-readme-generator) | 24,439 | 8,405 | 2025-10-28 | Apache-2.0 | 个人主页 README 组件和可视化统计。 |
| Release 自动化 | [semantic-release/semantic-release](https://github.com/semantic-release/semantic-release) | 24,037 | 1,812 | 2026-09-14 | MIT | 自动版本管理、Changelog、发包和发布流程。 |
| Release 自动化 | [googleapis/release-please](https://github.com/googleapis/release-please) | 7,496 | 588 | 2026-09-14 | Apache-2.0 | 基于 Conventional Commits 的 Release PR 自动化。 |
| Changelog 生成 | [orhun/git-cliff](https://github.com/orhun/git-cliff) | 12,234 | 325 | 2026-09-13 | Apache-2.0 | 高度可定制的 Git Changelog 生成器。 |
| Release 自动化 | [changesets/changesets](https://github.com/changesets/changesets) | 12,391 | 831 | 2026-09-14 | MIT | 面向 monorepo 和包生态的版本/变更记录流程。 |
| GitHub 数据分析 | [star-history/star-history](https://github.com/star-history/star-history) | 9,501 | 372 | 2026-09-12 | MIT | Star 历史图表和趋势/社会证明分析。 |
| Agent 工作流工具包 | [github/spec-kit](https://github.com/github/spec-kit) | 136,906 | 12,271 | 2026-09-14 | MIT | 结构化的 Agent 驱动开发工作流。 |

## 任务覆盖差异

| 工具 / 工作流 | 定位与目标用户 | 仓库体检 | README 编写 | Demo/社交素材 | 版本/Changelog 自动化 | 中英文发布文案 | 分平台发布计划 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| readme.so | — | — | 强 | — | — | — | — |
| GitHub Profile README Generator | — | — | 仅个人主页 | 部分 | — | — | — |
| semantic-release | — | — | — | — | 强 | — | — |
| release-please | — | — | — | — | 强 | — | — |
| git-cliff | — | — | — | — | 强 | — | — |
| Changesets | — | — | — | — | 强 | — | — |
| Star History | — | 发布后分析 | — | — | — | — | — |
| Spec Kit | 开发规格流程 | — | — | — | — | — | — |
| **GitHub Launch Studio** | **强** | **强** | **指导与改写** | **强** | 起草说明，不自动发包 | **强** | **强** |

## 得到的定位启发

1. **README 工具解决的是“编辑”，不是“发布策略”。** 区块编辑器能帮用户填内容，但不会判断目标用户、五分钟价值、证据和差异化。
2. **Release 工具是互补关系。** `semantic-release`、`release-please`、`git-cliff` 和 Changesets 处理版本与 Changelog 机制；GitHub Launch Studio 处理面向人的发布叙事、包装和传播。
3. **Profile README 的传播逻辑不同。** 个人主页依靠个性化组件和嵌入统计，项目发布更依赖快速试用、可信证明、限制说明和反馈路径。
4. **数据分析发生在发布之后。** Star History 能展示趋势，但不能让第一次访问的人理解项目并完成 quickstart。
5. **Agent 工作流的流行验证了 Skill 形态。** 但开发规格工具和开源发布包装工具解决的是两个不同任务。

## 边界

GitHub Launch Studio 目前不会：

- 自动升版本或发布包；
- 替维护者决定路线图、定价、许可证或社区规则；
- 保证 Star、媒体报道、榜单或 Product Hunt 结果；
- 伪造用户评价、指标、联系方式或协同推广。

它的生态位置是：

> Release 自动化负责版本机制；GitHub Launch Studio 负责发布决策层——给谁看、解决什么、陌生人如何五分钟试起来、展示什么证据，以及如何用中英文把项目发出去。
