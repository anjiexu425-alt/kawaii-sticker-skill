---
name: kawaii-sticker-skill
description: "Use when the user asks for kawaii chat stickers (贴纸 / 表情包) in a hand-drawn picture-book × Japanese kawaii style (手绘绘本 × 日系萌系), character-reference-based sticker generation, or a sticker pack built from one sentence or one theme. Two modes: single-line mode keeps the user's copy verbatim and produces exactly 3 candidate stickers that share the same text and differ in expression, pose/action, composition, and sticker decorations; theme mode writes the copy itself and produces one set of 6 stickers with clearly distinct copy, emotion, pose, and composition but one consistent style. The character is locked from 1-3 user-provided reference images (derived as a structured feature map) or falls back to a text character profile from character_profiles/ (default original character 胖墩 Pangdun, pangdun.md). Output is 1:1 transparent-background PNG with the text baked into the image, produced through the host's native image tool when available, otherwise through a standardized machine-checkable prompt contract."
---

# Kawaii Sticker Skill — 助手指令 (Skill Rules)

> 本文件是技能的**入口指令（entry instructions）**。权威内容规格见 `docs/SPEC.md`；机器校验细节以 `docs/PROMPT_CONTRACT.md` 为准；仓库结构与文件归属见 `docs/STRUCTURE.md`；第三方 IP 边界见 `NOTICE.md`。本技能是**通用**的：默认原创角色为「胖墩」（`character_profiles/pangdun.md`）；仓库中的美乐蒂（My Melody）仅为文字版风格示例档案（非默认、非官方素材）。

## 1. 用途与触发条件 (When to Use)

当用户表达**贴纸/表情包诉求**时使用本技能，典型触发包括：

- 「帮我做贴纸 / 给这句话配个贴纸 / 来一套 xx 主题贴纸」
- 要求**手绘绘本 × 日系萌系**可爱贴纸（hand-drawn picture-book × Japanese kawaii；默认角色「胖墩」画风见 `character_profiles/pangdun.md`）
- 要求**基于角色参考图**生成贴纸（character-reference-based sticker generation）
- 给出一句**原样文案**（单行模式）或一个**主题词**（主题模式）

不适用：用户要海报/长图/GIF/视频、图片编辑、图库聚合等（见 SPEC §1.3 非目标）。

## 2. 总流程 (Workflow)

每次生成运行按以下 6 步执行（通用管道：输入 → 模式识别 → 角色解析（锁定） → 能力协商 → 契约/提示词构建 → 生成 → 硬约束校验 → 交付）：

1. **判定模式**（Mode Detection）：判定本次是单行模式还是主题模式（细则见 §2.1）。
2. **角色设定**（Character Setup）：有参考图 → 走特征图（feature map）提取协议（§6）；无参考图 → 从 `character_profiles/` 加载文字档案。角色在本次运行内**锁定（locked）**。
3. **能力协商**（Capability Negotiation）：检测宿主是否有原生生图工具（§2.3）。有 → 直接调用；没有 → 输出标准化 Prompt Contract。**绝不声称宿主不存在的工具**。
4. **生成**（Generation）：按模式构建 3 或 6 份契约/提示词并生成。
5. **自检**（Self-Check）：对每张贴纸按 §8 清单核对，填写 `review_flags`。
6. **迭代**（Iteration）：自检失败的项重试（建议最多 2 轮）；仍失败则交付 best-effort 结果并如实填写 `review_flags`，**不得虚报**。

### 2.1 模式判定细则 (Mode Detection Rules)

按优先级判定，模式**互斥**：

1. 输入被引号包裹，或用户明确「这句话 / 按原样 / 文案不要改」→ **单行模式**。
2. 输入是贴纸诉求 + 一句短口语话术（非引号、≤ 20 字左右、像聊天话术）→ **单行模式**。
3. 输入是名词性主题（如「打工人」「恋爱脑」「考试周」）且非口语话术 → **主题模式**。
4. 无法判定 → **询问用户**；若宿主不支持追问，默认按主题模式处理，并在输出中说明该假设。

### 2.2 角色设定 (Character Setup)

- **有参考图（1–3 张）**：按 §6.1 特征图提取协议逐图分析 → 交叉一致 → 锁定 `character.source = "image"` + 完整 `feature_map`。
- **无参考图**：加载 `character_profiles/` 下文字档案。选择顺序：用户指定档案名 > 本技能默认档案（`character_profiles/pangdun.md`，原创角色「胖墩」）> 仓库首个可用档案。解析为同一 `feature_map` 结构，`character.source = "profile"`。
- 若目录为空且无参考图：明确告知用户并询问；无法询问时按风格锚点生成无角色锁定贴纸，并在交付说明中标注。

### 2.3 能力协商 (Capability Negotiation)

1. **检测**：宿主工具列表中存在名称/描述匹配以下正则之一，或 `adapters/` 中该宿主的 capability 表声明可用：
   `/image|illustration|draw|generate.*(image|picture)|dall|imagen|diffusion|flux/i`
2. **路径 ①（原生工具）**：将契约字段内联翻译为自然语言提示词，调用原生工具。提示词必须携带：角色特征、风格锚点、该张的表情/动作/构图/贴纸元素、**逐字文案（要求恰好出现一次）**、输出硬约束（1:1、透明 PNG、文字烧录）。**双路径禁止**：路径 ① 生效时不得额外输出契约块。
3. **路径 ②（契约输出）**：输出**一个** fenced code block，info string 为 `kss-prompt`，块内为符合 `docs/PROMPT_CONTRACT.md` 的 JSON 契约（3 或 6 个契约对象）。契约块是路径 ② 下**唯一**的机器输出。
4. **降级**：原生工具存在但调用失败 → 重试 1 次 → 仍失败自动走路径 ②，并在交付说明中标注。
5. **绝不假装生成**：没有任何生图能力且无法输出合法契约时，如实告知用户，不得输出伪造的图片文件、占位图或虚假承诺。

## 3. 单句模式规则 (Single-line Mode Rules)

- **文案逐字保留（verbatim）**：将用户输入行原样存为 `text.content`，`text.verbatim = true`；此后**任何环节不得增删改一个字符**（允许仅调整排版换行，内容不变）。
- **恰好 3 个候选**：3 张贴纸**共享同一句文案**（画面中该文案恰好出现一次）。
- **差异维度**：3 张仅在以下维度差异化——表情（expression）、姿势/动作（pose_action）、构图（composition）、贴纸装饰（sticker_elements）。
- 每张输出对应一份契约或原生提示词；3 份的 `character.feature_map`、`style_anchor`、`text`、`output` 完全一致。

## 4. 主题模式规则 (Theme Mode Rules)

- **自拟文案**：由助手撰写 **6 句互不相同**的短文案（中文，口语化、有梗、可单句成贴纸，如「打工人」→「咖啡续命」「摸鱼被抓」…）。
- **恰好 6 张（1 套）**。
- **区分度要求**：6 张的**文案、情绪、姿势、构图**彼此清楚可辨（distinct）。
- **一致性要求**：整套共享同一 `style_anchor`、同一 `character.feature_map`、统一配色倾向、统一描边粗细、统一字体风格——视觉上像同一套。
- 每张输出对应一份契约或原生提示词；契约中 `text.content` 即权威文案（`verbatim: true` 表示画面逐字呈现该内容）。

## 5. 视觉规则 (Visual Hard Constraints)

以下为**硬约束**，任何一条不满足即为不合格（fail），须按 §2 第 6 步重试：

1. **1:1 方形**：宽高相等（`output.aspect_ratio = "1:1"`）。
2. **PNG + 透明背景**：输出 PNG，含 alpha 通道，背景透明（无实色底、无底框填满）。
3. **文字烧录（text baked）**：文案绘制在画面内，非外部字幕；单行模式文案逐字出现**恰好一次**。
4. **无水印**：不出现任何来源水印、平台角标。
5. **无商标/官方元素**：不出现真实 Logo、注册商标、官方角色原图。
6. **贴纸友好**：粗而干净的描边（bold clean outlines）、高对比；表情与肢体在 64px 缩放下仍可读。
7. **安全边**：主体不贴边，四周留白 ≥ 5% 边距，避免裁切。
8. **画风遵循角色档案 `style_anchor`**（默认胖墩：手绘绘本 × 日系萌系——柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、柔和低饱和配色、贴纸装饰层、圆润造型、手绘感）；非默认档案按该档案画风执行。
9. **中文可读**：中文文案必须使用含中文字形的字体（圆体/手写体），避免豆腐块/缺字。
10. **角色一致**：本次运行内所有贴纸符合锁定的 `feature_map`。

**排版指引（typography）**：文字用手写/涂鸦（doodle）风格、圆体加粗、清晰描边（如白色描边 + 深色字芯）以保证小尺寸可读；排版方向（横排/竖排）与气泡样式须适配构图，不得遮挡主体表情。

## 6. Character Profile 使用与 Feature Map 提取协议 (Character & Feature-Map Protocol)

### 6.1 参考图提取协议 (Reference-image Pipeline)

用户上传 **1–3 张**参考图时：

1. 确认数量；超过 3 张取前 3 张并提示。
2. 对每张图按下列字段逐项提取视觉特征。
3. 多图交叉一致：取多数一致的取值；不一致但可共存（如不同角度）则合并记录。
4. **不确定性处理**：无法确定的字段显式写 `unknown`，记入 `derivation_notes`；**禁止编造细节**。
5. **锁定**：产出 `character.source = "image"` + 完整 `feature_map`，本次运行内冻结，所有贴纸共用。
6. **致命冲突**（两图明显是不同角色且无法取舍）→ 询问用户；无法询问时默认取第一张图并说明。

### 6.2 特征图字段清单 (Feature-map Fields)

`feature_map` 为 JSON 对象。源=image 时「必填」指必须能从参考图得出（无法得出则显式 `unknown`）；源=profile 时所有字段由档案文字推导。

| 字段 field | 必填 | 说明 (Description) |
|---|---|---|
| `head_shape` | ✅ | 头型：圆润 / 椭圆 / 心形等 |
| `ears` | ✅ | 耳朵：形状、大小、内耳颜色、是否被头饰遮挡（如「头巾遮耳，露出内耳」） |
| `eyes` | ✅ | 眼睛风格：豆豆眼 / 线条眼 / 大眼高光等 |
| `nose_mouth` | ✅ | 鼻子与嘴：小圆鼻 / 无鼻、w 嘴 / 嘟嘴等 |
| `palette` | ✅ | 对象：主色 / 辅色 / 点缀色（建议 2–5 色，可附 HEX 或中文色名） |
| `signature_accessories` | ✅ | 数组：标志性配饰：头巾 / 蝴蝶结 / 帽子 / 花等 |
| `body_proportions` | ⭕ | 身体比例：Q 版头身比、四肢样式（建议填写） |
| `personality_keywords` | ⭕ | 数组：性格关键词：软萌 / 委屈 / 元气 / 傲娇 |
| `texture` | ⭕ | 质感：铅笔手绘线稿 / 水彩 / 蜡笔颗粒 |
| `derivation_notes` | ⭕ | 推导说明：每字段的来源依据、置信度、unknown 原因 |

**「锁定」含义**：本次运行内所有贴纸复用同一份 `feature_map`（与同一 `style_anchor`），任何贴纸不得擅自改变角色外观。

### 6.3 档案使用 (Profile Usage)

- 档案为纯文字 Markdown，可附**用户原创**参考图（如 `character_profiles/pangdun.png`）。`character_profiles/pangdun.md` 为默认**原创角色档案**；`character_profiles/my-melody.md` 仅为文字风格示例（非默认）。新增角色 = 在 `character_profiles/` 新增一个 `.md`，无需改任何代码。
- 从档案解析出同样的 `feature_map` 结构，`character.source = "profile"`，同样锁定。

## 7. 输出契约 (Output Contract)

- **路径 ①（原生工具）**：调用原生工具，不输出契约块（双路径禁止）。
- **路径 ②（契约输出）**：输出**恰好一个** fenced code block，info string 为 `kss-prompt`，块内为 JSON（RFC 8259）：单行模式 = 3 个契约对象的数组；主题模式 = 6 个契约对象的数组。字段完整规范见 `docs/PROMPT_CONTRACT.md`（机器校验以该文件为准）。
- 契约块必须携带全部契约字段：`format_version`、`mode`、`character{source, feature_map}`、`style_anchor`、`expression`、`pose_action`、`composition`、`sticker_elements`、`text{content, verbatim, typography}`、`output{format, background, aspect_ratio, text_baked}`、`review_flags`。
- **任何 Markdown 提示词块（含原生路径的自然语言提示词）都必须携带与契约相同的语义字段**，不得省略输出硬约束。
- **绝不伪造图像**：没有生图能力时如实说明，不输出假图。

## 8. 自检清单 (Review Checklist)

生成后对**每一张**贴纸逐项核对（两种模式通用；标注“模式相关”的条目按模式执行），并填写 `review_flags`（布尔值必须与实际画面相符）：

- [ ] **文案**：单行模式——用户文案逐字保留、画面中恰好出现一次、无乱码/缺字；主题模式——6 句互不相同、逐字呈现契约内容。
- [ ] **数量**：单行模式恰好 3 张；主题模式恰好 6 张。
- [ ] **格式**：1:1 方形；PNG 透明背景；文字已烧录进画面（`transparent`、`square_1to1`、`text_baked`）。
- [ ] **角色一致**：所有贴纸复用同一锁定的 `feature_map`，与参考图（或档案）一致、无漂移（`verbatim_preserved` 之外的角色维度）。
- [ ] **风格一致**：同一 `style_anchor`；配色倾向、描边粗细、字体风格全套统一。
- [ ] **可读性**：64px 缩放下文案与表情仍可读（`readable_at_small`）。
- [ ] **合规**：无水印（`no_watermark`）、无商标/Logo/官方元素（`no_trademark`）。
- [ ] **区分度**：单行模式 3 张表情/姿势/构图明显可区分；主题模式 6 张文案与情绪彼此不同。

## 9. 边界与合规 (Boundaries & Compliance)

- 仓库**不包含**任何官方受版权保护的图片素材（Sanrio 美乐蒂及其衍生产品、Logo、商标、水印）——详见 `NOTICE.md`。
- 用户上传的参考图必须为用户拥有合法权利的图片；基于参考图生成的贴纸，其使用与发布责任由用户自行承担。
- 生成结果中**不得复现**第三方商标、水印、官方 Logo，也不得声称与 Sanrio 等品牌存在关联。
- 本技能为**通用**技能：默认角色「胖墩」为**原创设计**（`character_profiles/pangdun.md` + 原创参考图 `pangdun.png`，可公开商用）；美乐蒂仅为文字风格示例（非默认），商用请使用原创角色。
- 输出仅限贴纸图（及其必要的契约/提示词）；不生成海报、长图、GIF、视频。
