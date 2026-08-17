# 单行模式输入示例（带参考图）：一句原样文案 + 1 张参考图

<!-- input: 我真的会谢 -->
<!-- reference: 1, text-described (详见正文描述，不嵌入图片) -->

> 本文件是**机器可读的输入声明**：`<!-- input: ... -->` 声明用户输入原文；`<!-- reference: ... -->` 声明参考图数量与形态（约定见 `examples/README.md` §3）。校验器须断言：输出契约中所有 `text.content` 与该输入标记**逐字、字节级相等**。

## 用户请求 (User Request)

> 帮我做贴纸：**「我真的会谢」**，用我这张参考图的角色。

用户给了一句原样文案，并上传了 **1 张参考图**（本示例以**文字描述**代替真实图片——仓库不嵌入任何图片素材，SPEC §1.3 / NOTICE.md）。

## 参考图描述（文字形式，非真实图片）

> 一张**手绘风格的角色头部特写**：奶油白、圆润的兔头；戴着红色连帽头巾，头巾遮住耳朵上部、露出蜜桃粉色的内耳；眼睛为**大眼高光、圆溜溜**，脸颊有淡粉腮红；头巾右侧别着一枚**草莓小发夹**；整体铅笔线稿 + 粉彩平涂。画面**仅头部特写，无身体与四肢**。

## 运行前解析（本示例的判定过程）

1. **模式判定 → 单行模式（single_line）**：被引号包裹的短口语话术 → SPEC §3.1 优先级 1。
2. **角色解析 → 有参考图 → 特征图管线（feature-map pipeline）**
   - 按 SPEC §4.1 / SKILL.md §6.1 对参考图逐项提取视觉特征，产出 `feature_map`，`character.source = "image"`。
   - **不确定性处理**：参考图为头部特写 → `body_proportions` 无法确定，显式写 `unknown` 并记入 `derivation_notes`（SPEC §4.1-4，禁止编造）。
   - 角色**锁定**：本次运行内 3 张候选共享同一份 `feature_map`。
3. **文案锁定 → 逐字保留**：「我真的会谢」原样存为 `text.content`，`verbatim = true`，任何环节不得增删改一个字符。
4. **能力协商 → 路径 ②（契约输出）**：假设宿主无原生生图工具 → 输出一个 `kss-prompt` 块（见 `output-with-reference.md`）。

## 与无参考图示例的差异 (Difference vs `input.md`)

- 角色来源：`image`（参考图推导）而非 `profile`（档案回退）。
- 输出契约中的 `feature_map` 应体现参考图特征（如大眼高光、草莓发夹、头巾红主色），与档案推导版（豆豆眼、红色头巾+小蝴蝶结、奶油粉主色）**明显不同**——见 `output-with-reference.md`。

## 校验要点 (Validator Notes)

- [ ] 机器标记 `<!-- input: 我真的会谢 -->` 与 `<!-- reference: 1, ... -->` 存在且可解析。
- [ ] 对应输出 `output-with-reference.md` 的 3 个对象：`character.source` 全部为 `"image"`；`text.content` 全部与「我真的会谢」逐字相等、`verbatim: true`。
- [ ] 输出 `feature_map` 与 `output-3-candidates.md`（profile 版）的 `feature_map` **可见不同**；且 `body_proportions` 为 `unknown` 并有 `derivation_notes` 说明。
