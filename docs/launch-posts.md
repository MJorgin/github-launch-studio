# Draft launch posts

These are drafts for review. Do not post them automatically. Attach the final demo GIF/MP4 and use the actual repository URL.

Repository: <https://github.com/MJorgin/github-launch-studio>

## X / English

Suggested first post:

```text
GitHub Launch Studio — a Codex skill for OSS launch day.

It audits a repo for positioning, README/quickstart gaps, demo assets, benchmarks, release notes, and EN/中文 launch copy. Offline report, no fake growth or auto-posting.

https://github.com/MJorgin/github-launch-studio
```

Suggested follow-up after the demo:

```text
The part I care about most is the five-minute test:

A stranger should understand who it is for, how to try it, what proof exists, and where to get help—without reading the maintainer's mind.

The audit is a starting point, not a substitute for judgment.
```

## V2EX / 中文

Suggested node: 分享创造（先确认节点规则）

Title:

```text
做了个 Codex Skill：给开源项目做 GitHub 发布前体检和中英文启动包
```

Body:

```markdown
最近在整理自己的几个 GitHub 项目，发现“代码能跑”和“适合公开发布”之间差了不少东西：README 是否讲清楚、陌生人能不能五分钟试起来、有没有 Demo/截图/示例、Release Notes 怎么写、英文社区和中文社区分别怎么发。

所以做了一个 Codex Skill：GitHub Launch Studio。

它主要做几件事：

1. 离线扫描仓库，输出清晰度、激活率、证明、信任、传播性、维护准备六个评分；
2. 找出 README、Quick Start、LICENSE、CI、Issue 模板、疑似密钥文件等问题；
3. 生成可分享的 Markdown 报告 `LAUNCH.md`；
4. 辅助整理项目定位、五分钟价值、差异化和非目标；
5. 规划截图/GIF/社交卡片，并准备中英文 Release Notes 和发布文案；
6. 内置 README 编辑器、semantic-release、release-please、git-cliff、Changesets、Star History、spec-kit 等相邻工具的对标地图。

仓库：
https://github.com/MJorgin/github-launch-studio

边界也写得比较明确：不刷 Star、不伪造指标、不抓联系方式、不群发私信、不会未经确认自动发帖。它更像发布前的产品包装和检查流程，不替代版本发布自动化。

目前已经有本地只读审计脚本、中英文 README、CI、Issue 模板和一个 30 秒 Demo 分镜。想听听大家：

- 你们发开源项目时最容易漏掉什么？
- README、Demo、Release Notes、社区发帖，哪个最痛？
- 这种 Skill 还应该接入哪些检查？

欢迎试用和拍砖。
```

## 即刻 / 中文

Draft 1:

```text
做了个有点功利但实用的东西：GitHub Launch Studio。

它不是帮你刷 Star，而是在开源项目发布前做一次“陌生人视角体检”：README 有没有讲清楚、五分钟能不能试起来、有没有可信 Demo、Release Notes 和中英文发布文案是否准备好。

先拿自己的仓库 dogfood，结果发现社交卡片都能做出重叠问题，于是连着修了两版……这种细节真的需要流程化检查。
```

Draft 2, after attaching the demo:

```text
给 GitHub Launch Studio 录了一个 30 秒 Demo：

离线仓库体检 → Markdown 报告 → README/快速上手改造建议 → 相邻工具对标 → 中英文发布文案。

我觉得这类 Agent Skill 的价值不是“多写点字”，而是把发布前容易漏的判断变成一个可重复流程。
```

## Posting notes

- X should lead with the concrete job and attach the demo; avoid hashtag stuffing.
- V2EX should be factual, acknowledge limitations, and ask specific questions.
- 即刻 can be more personal and build in public; post the bug-fix story only if the tone feels natural.
- Wait until the demo asset is ready before the main external launch.
