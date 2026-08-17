# Tests — 人工/代理验收清单 (Manual & Agent-Run Acceptance Checklist)

> 面向**每套实际生成的贴纸**（或每次运行技能的助手自检），实现 SPEC §8.2。机器可测部分由 `validate_structure.py` / `validate_examples.py` 覆盖；本清单覆盖机器校验器无法自动判断的**视觉与真实性**条目。运行方法：逐项勾选，全部通过才算交付合格；任一项失败按 SKILL.md §2 第 6 步重试（最多约 2 轮）或交付 best-effort 并如实填写 `review_flags`。

## 0. 环境与准备 (Prep)

- [ ] 运行环境确认：`bash tests/run_tests.sh` 退出码为 0（SPEC M8）。
- [ ] 已读取 `SKILL.md`、`docs/SPEC.md`、`docs/PROMPT_CONTRACT.md` 的相关章节。
- [ ] 已判定本次模式（单行 or 主题）且与输入匹配（SPEC §3.1）；**输入不明确时已先询问用户，未在未确认模式下生成**。
- [ ] 已解析角色（有参考图 → feature map 管线；无参考图 → 文字档案），并**锁定** `feature_map`。

## 1. 单行模式 (Single-line Mode)

- [ ] 用户文案被**逐字保留**：`text.content` 与用户输入字节级相等，`text.verbatim === true`。
- [ ] **恰好 3 张**候选贴纸，3 张**共享同一句文案**。
- [ ] 每张画面中该文案**恰好出现一次**，无乱码/缺字。
- [ ] 3 张仅在表情 / 姿势动作 / 构图 / 贴纸装饰上不同（SPEC §2 / SKILL.md §3）。

## 2. 主题模式 (Theme Mode)

- [ ] **恰好 6 张（1 套）**。
- [ ] 6 句文案为助手**自拟**、两两不同、口语化有梗、可单句成贴纸。
- [ ] 6 张的情绪、姿势、构图彼此**清楚可辨**（expression/pose_action/composition 组合两两不同）。
- [ ] 整套视觉**像同一套**：同一 style_anchor、同一 feature_map、统一配色倾向、统一描边粗细、统一字体风格。

## 3. 角色参考：有参考图 (With Reference Image)

- [ ] 参考图数量 1–3 张（超出取前 3 张并提示）。
- [ ] 逐项提取 feature_map；无法确定的字段显式写 `unknown` 并记入 `derivation_notes`，**无编造细节**。
- [ ] 多图交叉一致处理正确（多数一致 / 可共存则合并 / 致命冲突询问用户）。
- [ ] `character.source === "image"`；角色**锁定**：全套贴纸外观一致、无漂移。

## 4. 角色参考：无参考图 (Without Reference Image)

- [ ] 已从 `character_profiles/` 加载文字档案（选择顺序：用户指定 > 默认 `pangdun.md`（胖墩）> 首个可用）。
- [ ] `character.source === "profile"`；档案解析出的 `feature_map` 与档案内容一致并锁定。
- [ ] 档案目录为空且无参考图时：明确告知用户并询问；无法询问时按风格锚点生成并在交付中说明。

## 5. 能力协商：原生工具路径 ① (Native Tool Path)

- [ ] 宿主确有原生生图工具（名称/描述匹配检测正则，或 `adapters/` 能力表声明），未虚报。
- [ ] 提示词携带全部契约语义字段：角色特征、风格锚点、expression/pose_action/composition/sticker_elements、逐字文案（要求恰好出现一次）、输出硬约束（1:1、透明 PNG、文字烧录）。
- [ ] 未同时输出契约块（双路径禁止）。
- [ ] 原生工具失败时：重试 1 次 → 仍失败自动降级路径 ② 并在交付说明中标注。

## 6. 能力协商：契约路径 ② (Standardized Prompt Contract Path)

- [ ] 输出**恰好一个** `` ```kss-prompt `` fenced 块，块内为合法 JSON（单行 3 对象数组 / 主题 6 对象数组）。
- [ ] 契约字段完整：`format_version`/`mode`/`character{source,feature_map}`/`style_anchor`/`expression`/`pose_action`/`composition`/`sticker_elements`/`text{content,verbatim,typography}`/`output{format,background,aspect_ratio,text_baked}`/`review_flags`。
- [ ] `output` 硬约束：`format=="png"`、`background=="transparent"`、`aspect_ratio=="1:1"`、`text_baked==true`。
- [ ] 契约块是路径 ② 下唯一机器输出；无伪造图片、无占位图、无虚假承诺。

## 7. 每张贴纸的视觉硬约束 (Golden Rules — SKILL.md §5)

- [ ] **1:1 方形**：宽高相等。
- [ ] **PNG + 透明背景**：含 alpha 通道，无实色底、无底框填满。
- [ ] **文字烧录**：文案绘制在画面内（非外部字幕）；单行模式文案逐字出现恰好一次。
- [ ] **无水印**：无来源水印、平台角标。
- [ ] **无商标/官方元素**：无真实 Logo、注册商标、官方角色原图。
- [ ] **贴纸友好**：粗而干净的描边、高对比；64px 缩放下表情与肢体仍可读。
- [ ] **安全边**：主体不贴边，四周留白 ≥ 5%，避免裁切。
- [ ] **画风一致**：按档案 `style_anchor`（默认手绘绘本 × 日系萌系：柔软线稿、细腻绒毛、低饱和、圆润、手绘感）。
- [ ] **中文可读**：中文文案使用含中文字形的字体（圆体/手写体），无豆腐块/缺字。
- [ ] **角色一致**：符合锁定的 `feature_map`。
- [ ] **排版**：手写/涂鸦风格、圆体加粗、清晰描边（如白描边+深色字芯）；横/竖排与气泡样式适配构图，不遮挡主体表情。

## 8. 自检与交付 (Self-Check & Delivery)

- [ ] `review_flags` 各布尔值（`verbatim_preserved`/`text_baked`/`transparent`/`square_1to1`/`readable_at_small`/`no_watermark`/`no_trademark`）与**实际画面相符**，不虚报。
- [ ] 单行模式交付恰好 3 张；主题模式交付恰好 6 张（SPEC §8.3）。
- [ ] 每张图均为 1:1、透明、文字烧录；契约路径下每张图对应一份合法契约。
- [ ] 重试失败项时如实填写 `review_flags`；超过重试轮次交付 best-effort 并说明。

## 9. 合规 (Compliance — NOTICE.md / SKILL.md §9)

- [ ] 参考图为用户拥有合法权利的图片。
- [ ] 结果未复现第三方商标、水印、官方 Logo，未声称与任何第三方品牌有关联。
- [ ] 输出仅限贴纸图（及必要契约/提示词），未产出海报、长图、GIF、视频。
