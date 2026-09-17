# Direction Approved · huashu-design Gate

## 用户原话（2026-09-16）

> 我觉得这个也不错啊 装好之后 用这个给我优化一下？

指 https://github.com/alchaincyf/huashu-design ，优化对象为已迭代多轮的
30 秒 `assets/launch-demo.mp4` / `launch-demo.gif`。

## 三方向硬门豁免理由

- 同一产品、同一支 30 秒 Demo 的既有视觉方向迭代，不是新项目。
- 用户已反复看过并多轮修改当前深色开发者工具版（最近一次问题：Report/CTA
  评分区视觉拥挤、像元素重叠）。
- 本次目标不是重新选风格，而是让当前艺术总监/视觉设计/动效/验收按
  huashu-design 标准升级。

按 SKILL.md「已选定方向后的迭代」豁免：不重出三版方向初稿。

## 本轮方向（艺术总监决策）

**概念：Launch Preflight Field Manual（发布前飞行手册）。**

产品的核心动作是「公开发布前的就绪体检」。视觉从内容长出，而不是套通用
深色 dashboard：

- 母题：贯穿 7 个场景的左侧 preflight 流程轨（AUDIT→LAUNCH），节点随
  叙事推进完成；终镜盖章 "CLEARED FOR LAUNCH" 收束全片。
- 皮肤：暖色纸面 + 墨色 + 单一朱砂红强调色（配文档/手册气质），刻意避开
  critique-guide 点名的「深蓝 #0D1117 + 霓虹」默认审美；产品交付物本来
  就是一份 Markdown 报告，纸面文档语言与其同构。
- 评分语言：Report 与 CTA 复用同一套五段式 gauge，形成 before/after。
- 纪律：近直角与发丝线替代同质大圆角卡片；删掉无功能图标；每镜一个主动作；
  终镜印章是全片唯一的「hero 特效」。
- 媒介：保留确定性 Pillow 渲染（CI 可复现、不录屏、不泄露本机路径），
  不重写为 HTML/HyperFrames。

用户确认终帧后再更新文档、提交、发 v0.3.0。
