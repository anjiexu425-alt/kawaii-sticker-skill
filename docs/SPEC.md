# Kawaii Sticker Skill — 规格说明书 (SPEC)

> 本文件是本项目的**权威规格（authoritative spec）**。所有后续产出（PROMPT_CONTRACT.md、STRUCTURE.md、SKILL.md、adapters/、examples/、tests/、README.md）必须与本文件一致；如有冲突，以本文件为准，并回改本文件。

| 元数据 | 值 |
|---|---|
| 文档 | `docs/SPEC.md` |
| 版本 | 1.0（Phase: spec / planning） |
| 状态 | 生效（authoritative） |
| 语言 | 中文为主，英文术语为辅（English keywords） |
| 适用范围 | 所有宿主助手：OpenAI Codex、Anthropic Claude Code、DeepSeek Harness 及任意兼容 Skill 机制的助手 |

## 目录 (TOC)

1. [项目定位与边界](#1-项目定位与边界)
2. [两种模式 (Modes)](#2-两种模式-modes)
3. [用户流程 (User Flows)](#3-用户流程-user-flows)
4. [角色参考机制 (Character Reference)](#4-角色参考机制-character-reference)
5. [生图能力协商 (Capability Negotiation)](#5-生图能力协商-capability-negotiation)
6. [Prompt Contract v1 字段清单](#6-prompt-contract-v1-字段清单)
7. [视觉规则硬约束 (Visual Hard Constraints)](#7-视觉规则硬约束-visual-hard-constraints)
8. [验收标准 (Acceptance Criteria)](#8-验收标准-acceptance-criteria)
9. [术语表 (Glossary)](#9-术语表-glossary)
10. [文档地图与后续阶段](#10-文档地图与后续阶段)

---

## 1. 项目定位与边界

### 1.1 一句话定位

Kawaii Sticker Skill 是一个**通用的、开源的 AI Skill**：用户将其安装进 AI 助手后，助手会为用户生成 kawaii 聊天贴纸（手绘绘本 × 日系萌系，hand-drawn picture-book × Japanese kawaii；默认角色为原创「胖墩」）。

### 1.2 它是什么

- 一套**指令 + 资产包（Skill）**：`SKILL.md` 作为入口指令，配套角色档案、适配文档、契约文档、示例与测试。
- **宿主无关（host-agnostic）**：不绑定任何单一模型/厂商；能调用原生生图工具就用，不能则输出标准化提示词契约（见 §5、§6）。
- **内容生成器**：产出 1:1 方形、透明背景 PNG、文字烧录（text baked）在画面内的贴纸图。

### 1.3 非目标 (Non-Goals)

- ❌ **不是网站/应用**：无服务器、无后端、无 Web UI、无 API 服务、无数据库。
- ❌ **不打包官方素材**：仓库内不包含任何第三方受版权保护的官方角色图片、Logo、商标、水印。IP 处理见 `NOTICE.md`。
- ❌ **不绑定供应商**：不依赖某个特定生图 API；Prompt Contract 保证任何宿主都能消费输出。
- ❌ **不做图库/训练集**：不聚合、不分发用户生成图片。
- ❌ **不做图片编辑器**：不提供图层/画布/导出等编辑能力。
- ❌ **不输出额外图文**：除贴纸图（及其必要的提示词/契约）外，不生成海报、长图、GIF、视频。

---

## 2. 两种模式 (Modes)

| 维度 | 单行模式 single-line mode | 主题模式 theme mode |
|---|---|---|
| 用户输入 | 一行**原样**文案，如「我真的会谢」 | 一个主题词，如「打工人」 |
| 文案来源 | 用户提供，**逐字保留（verbatim）** | 助手自拟（每次生成 distinct copy） |
| 贴纸数量 | **恰好 3 张** | **恰好 6 张（1 套）** |
| 文案约束 | 3 张**共享同一句文案** | 6 句文案**互不相同** |
| 差异维度 | 表情、姿势/动作、构图、贴纸装饰 | 文案、情绪、姿势、构图 |
| 风格一致性 | 同一角色、同一风格锚点 | 整套统一风格锚点（同一角色） |

模式是**互斥**的：一次生成运行要么是单行模式，要么是主题模式，由输入判定（见 §3.1）。

---

## 3. 用户流程 (User Flows)

### 3.1 模式识别 (Mode Detection)

按优先级判定：

1. 用户输入被引号包裹，或明确说明「这句话 / 按原样 / 文案不要改」→ **单行模式**。
2. 用户输入是贴纸诉求 + 一个短文案/短语（非引号，≤ 20 字左右、口语化、像聊天话术）→ **单行模式**。
3. 用户输入是名词性主题（如「打工人」「恋爱脑」「考试周」）且非口语话术 → **主题模式**。
4. 无法判定时（如用户只说「做表情包」而未给文案或主题）：**必须先询问用户**（单句模式＝一句原样文案→3 张；主题模式＝一个主题词→6 张），**未确认前禁止生成**。仅当宿主完全不支持追问时才允许默认主题模式，并须在交付中显著标注假设。

### 3.2 单行模式流程 (Single-line Flow)

1. **锁定文案**：将输入行原样存为 `text.content`，标记 `text.verbatim = true`；此后**任何环节不得增删改一个字符**（允许仅调整排版换行，内容不变）。
2. **解析角色**：若有参考图 → 特征图管线（§4.1）；否则回退角色档案（§4.3）。角色在本次运行内**锁定（locked）**。
3. **能力协商**：按 §5 决策——调用原生生图工具，或输出 Prompt Contract。
4. **设计 3 个候选**：构建 3 份契约/提示词，共享同一 `text` 与同一 `character.feature_map`，在 `expression`、`pose_action`、`composition`、`sticker_elements` 上差异化，并明确要求「画面中恰好出现这句文案一次」。
5. **生成与校验**：每张按 §7 硬约束自检，填写 `review_flags`；失败项重试。
6. **交付**：输出 3 张 1:1 透明 PNG（文字烧录），逐张附契约/说明（若走契约路径）。

### 3.3 主题模式流程 (Theme Flow)

1. **解析主题**：提取主题词，明确情绪范围与目标受众。
2. **撰写文案**：自拟 **6 句互不相同**的短文案（中文，口语化、有梗、可单句成贴纸）。
3. **解析角色**：同 §3.2-2。
4. **能力协商**：同 §3.2-3。
5. **设计整套**：构建 6 份契约，共享同一 `style_anchor` 与 `character.feature_map`；6 张在文案、情绪、姿势、构图上**彼此可区分**，但视觉上**像同一套**（统一配色倾向、统一描边粗细、统一字体风格）。
6. **生成、校验、交付**：同 §3.2-5/6，数量为 6。

### 3.4 通用管道 (Shared Pipeline)

`输入 → 模式识别 → 角色解析（锁定） → 能力协商 → 契约/提示词构建 → 生成 → 硬约束校验(review_flags) → 交付`

---

## 4. 角色参考机制 (Character Reference)

### 4.1 参考图管线 (Reference-image Pipeline)

当用户上传 **1–3 张**参考图时：

1. **收集**：确认图片数量（超出 3 张则取前 3 张并提示）。
2. **逐图分析**：对每张图按 §4.4 字段逐项提取视觉特征（头型、耳朵、五官、配色、配饰、比例、质感…）。
3. **交叉一致性**：多图时取多数一致的取值；不一致但可共存（如不同角度）则合并记录。
4. **不确定性处理**：无法确定的字段必须显式写 `unknown`，并记入 `derivation_notes`；禁止编造细节。
5. **锁定**：产出 `character.source = "image"` + 完整 `feature_map`，本次运行内冻结，所有贴纸共用。
6. **致命冲突**（如两图明显是两个角色且无法取舍）→ 询问用户；无法询问时默认取第一张图，并在输出中说明。

### 4.2 回退：角色档案 (Fallback: Character Profile)

- 无参考图时，加载 `character_profiles/` 下的**文字档案**。
- 选择规则：用户指定档案名 > `SKILL.md` 中声明的默认档案 > 仓库首个可用档案（当前默认原创角色 `character_profiles/pangdun.md`，胖墩）。
- 将档案文字内容解析为同样的 `feature_map` 结构，`character.source = "profile"`。
- 仓库保持**通用**：`pangdun.md` 为默认原创角色；新增角色只需增加一个 `.md` 档案文件，无需改代码。

### 4.3 特征图字段清单 (Feature-map Field List)

`feature_map` 为 JSON 对象。`源=image` 时「必填」指**必须能从参考图得出**（无法得出则显式 `unknown`）；`源=profile` 时所有字段由档案文字推导，标识字段（identity fields）必填。

| 字段 field | 必填 | 类型 | 说明 (Description) |
|---|---|---|---|
| `head_shape` | ✅ | string | 头型：圆润 / 椭圆 / 心形等 |
| `ears` | ✅ | string | 耳朵：形状、大小、内耳颜色、是否被头饰遮挡（如「头巾遮耳，露出内耳」） |
| `eyes` | ✅ | string | 眼睛风格：豆豆眼 / 线条眼 / 大眼高光等 |
| `nose_mouth` | ✅ | string | 鼻子与嘴：小圆鼻 / 无鼻、w 嘴 / 嘟嘴等 |
| `palette` | ✅ | object | 主色/辅色/点缀色（建议 2–5 色，可附 HEX 或中文色名） |
| `signature_accessories` | ✅ | array | 标志性配饰：头巾 / 蝴蝶结 / 帽子 / 花等 |
| `body_proportions` | ⭕ | string | 身体比例：Q 版头身比、四肢样式（建议填写） |
| `personality_keywords` | ⭕ | array | 性格关键词：软萌 / 委屈 / 元气 / 傲娇 |
| `texture` | ⭕ | string | 质感：铅笔手绘线稿 / 水彩 / 蜡笔颗粒 |
| `derivation_notes` | ⭕ | string | 推导说明：每字段的来源依据、置信度、unknown 原因 |

✅ = 必填（identity-critical）；⭕ = 推荐（recommended）。

---

## 5. 生图能力协商 (Capability Negotiation)

### 5.1 决策流程 (Decision Flow)

```
用户请求贴纸
   │
   ├─(A) 宿主暴露原生生图工具？───────── 是 ──► 路径 ①：调用原生工具（§5.2）
   │      检测：助手可用工具列表中存在名称/描述匹配
   │      /image|illustration|draw|generate.*(image|picture)|dall|imagen|diffusion|flux/i
   │      —— 或 adapters/ 中该宿主的 capability 表声明可用
   │
   └─ 否（或调用失败且无法重试）─────────────► 路径 ②：输出标准化 Prompt Contract（§5.3）
```

- **协商时机**：每次生成运行开始时执行一次（角色锁定之后、构建提示词之前）。
- **回退**：原生工具存在但调用失败 → 重试 1 次 → 仍失败则自动走路径 ②，并在交付说明中标注。
- **双路径禁止**：路径 ① 生效时**不得**额外输出契约块（避免噪声）；路径 ② 时契约块是**唯一**机器输出。

### 5.2 路径 ①：原生工具调用 (Native Tool Path)

- 将 §6 契约字段**内联翻译为自然语言提示词**传给原生工具（如 DALL·E / Imagen / Flux 类工具）。
- 提示词必须包含：角色特征（feature_map）、风格锚点、该张的 expression / pose_action / composition / sticker_elements、**逐字文案**（要求恰好出现一次）、输出硬约束（1:1、透明背景 PNG、文字烧录、无文字缺失）。
- 仍按 §7 校验产出并填写 `review_flags`。

### 5.3 路径 ②：标准化提示词输出 (Standardized Prompt Output)

- 输出**一个** fenced code block，info string 为 `kss-prompt`，块内为符合 §6 的 JSON 契约。
- 契约即交付物的一部分：用户/宿主可将契约喂给任何支持该契约的生图能力。
- 契约块前后可附自然语言说明，但机器校验只认契约块。

### 5.4 触发条件 (Trigger Conditions)

- **激活**：用户表达贴纸诉求（「帮我做贴纸 / 给这句话配个贴纸 / 来一套 xx 主题贴纸」等），且角色参考（如有）与模式已判定。
- **协商**：见 5.1；不满足任意路径条件时默认路径 ②。
- **契约输出触发**：无原生工具，或原生工具调用失败降级。

### 5.5 一致性要求 (Consistency)

两条路径产出的贴纸必须满足**完全相同**的 §7 硬约束与 §4 角色锁定；差异仅在于「谁执行生图」。

---

## 6. Prompt Contract v1 字段清单

### 6.1 定位与序列化 (Purpose & Serialization)

- **定位**：宿主无关、机器可校验（machine-checkable）的标准化生图指令。单行模式产出 **3 份**契约，主题模式产出 **6 份**契约，每份对应一张贴纸。
- **序列化**：单个 fenced code block，info string 固定为 `kss-prompt`，内容为 **JSON**（RFC 8259）。正则 `` ^```kss-prompt$ `` 可定位，`JSON.parse` 可解析。
- **命名**：本规格定义 **Contract v1**（顶层 `format_version: "1.0"`）；后续版本只增不改字段语义。

### 6.2 字段表 (Field List)

✅ = 必填；⭕ = 可选（推荐）。`character` / `text` / `output` 为嵌套对象。

| 字段路径 field path | 必填 | 类型 / 取值 | 说明 (Description) |
|---|---|---|---|
| `format_version` | ✅ | string，恒为 `"1.0"` | 契约版本 |
| `mode` | ✅ | enum：`"single_line"` \| `"theme"` | 模式；须与 §3.1 判定一致 |
| `character.source` | ✅ | enum：`"image"` \| `"profile"` | 角色来源 |
| `character.feature_map` | ✅ | object（§4.3） | 锁定的角色特征，本次运行内所有契约相同 |
| `style_anchor` | ✅ | string | 风格锚点，由角色档案的画风决定（默认胖墩：手绘绘本 × 日系萌系，hand-drawn picture-book × Japanese kawaii）；主题模式整套一致 |
| `expression` | ✅ | string | 表情：开心 / 委屈 / 无语 / 元气…（单行模式 3 张互异） |
| `pose_action` | ✅ | string | 姿势/动作：举手 / 蹲墙角 / 比心…（单行模式 3 张互异） |
| `composition` | ✅ | string | 构图：居中特写 / 全身 / 对角 / 贴纸气泡…（单行模式 3 张互异） |
| `sticker_elements` | ⭕ | array of string | 贴纸装饰：虚线框 / 闪粉 / 小花 / 星星 / 手帐贴纸层 |
| `text.content` | ✅ | string | 文案原文；`single_line` 下必须与用户输入**逐字相等** |
| `text.verbatim` | ✅ | boolean | `true` 表示逐字保留；`single_line` 必须为 `true` |
| `text.typography` | ⭕ | object | 字体建议：圆体/手写风、描边、对齐（横排/竖排）、气泡样式 |
| `output.format` | ✅ | const：`"png"` | 输出格式 |
| `output.background` | ✅ | const：`"transparent"` | 背景透明 |
| `output.aspect_ratio` | ✅ | const：`"1:1"` | 正方形 |
| `output.text_baked` | ✅ | const：`true` | 文字烧录进画面，不依赖外部字幕 |
| `review_flags` | ⭕ | object of boolean | 生成后自检（§8.1 字段：`verbatim_preserved`、`text_baked`、`transparent`、`square_1to1`、`readable_at_small`、`no_watermark`、`no_trademark`） |

### 6.3 机器校验规则 (Machine Validation Rules)

1. 契约块定位：`` ^```kss-prompt$ `` … 闭合 `` ^```$ ``。
2. JSON 可解析（`JSON.parse` 成功）。
3. 所有 ✅ 字段存在且类型/取值合法（enum/const 逐值校验）。
4. `mode = "single_line"` ⇒ `text.verbatim === true` 且 `text.content` 与用户输入逐字相等。
5. 同一次运行的所有契约：`format_version`、`style_anchor`、`character.feature_map`、`output.*` 完全一致。
6. `review_flags` 若存在：字段名合法、值为 boolean（真实性由人工/视觉校验，见 §8.2）。

### 6.4 最小示例 (Minimal Example)

````markdown
```kss-prompt
{
  "format_version": "1.0",
  "mode": "single_line",
  "character": {
    "source": "profile",
    "feature_map": {
      "head_shape": "圆润", "ears": "头巾遮耳，露出内耳",
      "eyes": "豆豆眼", "nose_mouth": "小圆鼻，w 嘴",
      "palette": {"主色": "奶油粉", "辅色": "白色", "点缀": "草莓红"},
      "signature_accessories": ["红色头巾", "小蝴蝶结"],
      "body_proportions": "Q 版 2 头身", "personality_keywords": ["软萌", "委屈"],
      "texture": "柔软铅笔/细线稿、细腻绒毛、低饱和", "derivation_notes": "取自 character_profiles/pangdun.md"
    }
  },
  "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
  "expression": "委屈巴巴", "pose_action": "蹲在角落画圈圈",
  "composition": "居中全身特写，配手帐虚线框", "sticker_elements": ["星星", "小花"],
  "text": {"content": "我真的会谢", "verbatim": true, "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边"}},
  "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
  "review_flags": {"verbatim_preserved": true, "text_baked": true, "transparent": true,
                   "square_1to1": true, "readable_at_small": true, "no_watermark": true, "no_trademark": true}
}
```
````

---

## 7. 视觉规则硬约束 (Visual Hard Constraints)

以下为**硬约束**，任何一条不满足即为不合格（fail），须重试。标注「🔧可机检」的条目可由 `tests/` 对图 fixtures 自动校验。

1. 🔧 **1:1 方形**：`output.aspect_ratio = "1:1"`，宽高相等。
2. 🔧 **PNG + 透明背景**：输出为 PNG，含 alpha 通道，背景透明（无实色底、无底框填满）。
3. 🔧 **文字烧录（text baked）**：文案绘制在画面内，非外部字幕；`single_line` 下文案逐字出现**恰好一次**。
4. 🔧 **无水印**：不得出现任何来源水印、平台角标。
5. 🔧 **无商标/官方元素**：不出现真实 Logo、注册商标、官方角色原图。
6. 🔧 **贴纸友好（sticker-friendly）**：粗而干净的描边（bold clean outlines）、高对比、表情/肢体在 64px 缩放下仍可读。
7. 🔧 **方形留白安全边**：主体不贴边，四周留白 ≥ 5% 边距，避免裁切。
8. **画风遵循角色档案 `style_anchor`**（默认胖墩：手绘绘本 × 日系萌系——柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、柔和低饱和配色、贴纸装饰层、圆润造型、手绘感）；非默认档案按该档案画风执行。
9. **中文可读**：若文案为中文，字体必须有中文字形（圆体/手写体），避免豆腐块/缺字。
10. **角色一致**：同一次运行内所有贴纸符合锁定的 `feature_map`。

🔧 可机检条目由 `tests/` 的图片校验器（fixture 模式）与契约校验器（contract 模式）共同覆盖；其余（8–10）依赖生成能力，由 §8.2 人工检查兜底。

---

## 8. 验收标准 (Acceptance Criteria)

### 8.1 机器可测 (Machine-testable) — 由 `tests/` 自动执行，CI 入口 `bash tests/run_tests.sh`

| # | 验收项 | 如何测 |
|---|---|---|
| M1 | 仓库存在 `SKILL.md`，YAML frontmatter 含 `name` 与 `description` | 解析 frontmatter |
| M2 | 仓库存在 `docs/SPEC.md`、`docs/PROMPT_CONTRACT.md`、`docs/STRUCTURE.md` | 文件存在性 |
| M3 | `character_profiles/` 至少含一个档案；默认 `pangdun.md`（原创）+ 参考图 `pangdun.png`（用户原创资产，允许） | 文件检查 + 图片白名单（仅 `character_profiles/`） |
| M4 | 仓库**不包含**官方图片素材；`tests/fixtures/` 内图片均为原创 | 目录策略 + fixture 声明 |
| M5 | `examples/` 中单行模式示例契约与主题模式示例契约全部通过 §6.3 机器校验 | 契约校验器 |
| M6 | 契约校验器（§6.3 规则 1–6）实现并可运行 | 单元测试通过 |
| M7 | 图 fixtures（如有）满足 §7 中 🔧 条目：1:1、PNG、alpha、无实色背景 | 图片校验器 |
| M8 | `bash tests/run_tests.sh` 退出码为 0 | CI 直接调用 |

### 8.2 人工检查清单 (Manual Checklist) — 面向每套生成的贴纸

- [ ] 文案逐字正确、恰好出现一次、无乱码/缺字（单行模式）。
- [ ] 画风一致：按档案 `style_anchor`（默认手绘绘本 × 日系萌系：柔软线稿、细腻绒毛、低饱和、圆润、手绘感）。
- [ ] 单行模式 3 张：表情/姿势/构图明显可区分；主题模式 6 张：文案与情绪彼此不同、整套风格统一。
- [ ] 64px 缩放下文案与表情仍可读。
- [ ] 无第三方水印、Logo、商标、官方角色原图特征。
- [ ] 角色与参考图（或档案）一致，无漂移。
- [ ] `review_flags` 各布尔值与实际画面相符（若走契约路径）。

### 8.3 交付物验收

- 单行模式：恰好 3 张 PNG；主题模式：恰好 6 张 PNG。
- 每张图：1:1、透明、文字烧录。
- 契约路径下：每张图对应一份 §6 合法契约；原生路径下：无契约块但产出同质。

---

## 9. 术语表 (Glossary)

| 中文 | English | 说明 |
|---|---|---|
| 技能 | Skill | 可安装进 AI 助手的指令+资产包 |
| 宿主 | Host | 承载 Skill 的 AI 助手（Codex / Claude Code / Harness…） |
| 单行模式 | single-line mode | 用户给一句原样文案，产 3 张同文案贴纸 |
| 主题模式 | theme mode | 用户给主题，助手自拟 6 句文案产 1 套贴纸 |
| 逐字保留 | verbatim | 文案一字不改地出现在画面中 |
| 角色参考 | character reference | 用户提供的 1–3 张参考图或文字档案 |
| 特征图 | feature map | 从参考图/档案提取的结构化角色特征（§4.3） |
| 角色档案 | character profile | `character_profiles/` 下的文字角色描述 |
| 角色锁定 | character lock | 本次运行内角色特征冻结、全套一致 |
| 能力协商 | capability negotiation | 判断用原生生图工具还是输出契约（§5） |
| 提示词契约 | Prompt Contract | 机器可校验的标准化生图 JSON（§6） |
| 风格锚点 | style anchor | 整套贴纸统一的视觉风格描述 |
| 贴纸元素 | sticker elements | 装饰性元素（虚线框、闪粉、小花等） |
| 硬约束 | hard constraints | 必须满足的视觉/格式规则（§7） |
| 日系萌系手绘 | hand-drawn picture-book × Japanese kawaii | 柔软铅笔线稿、细腻绒毛、低饱和配色的萌系手绘美学（默认角色画风） |
| 验收标准 | acceptance criteria | 机器可测 + 人工检查的达标清单（§8） |

---

## 10. 文档地图与后续阶段

| 文档 | 阶段 | 与本规格的关系 |
|---|---|---|
| `docs/SPEC.md`（本文件） | spec | 权威规格 |
| `docs/PROMPT_CONTRACT.md` | 后续 | 将 §6 展开为完整契约文档（字段、示例、校验器规范） |
| `docs/STRUCTURE.md` | 后续 | 仓库结构与各目录职责 |
| `SKILL.md` | 后续 | 助手入口指令，须含 frontmatter `name`/`description`，实现 §3–§5 流程 |
| `adapters/` | 后续 | 各宿主能力协商表（对应 §5.1 检测规则） |
| `examples/` | 后续 | 单行/主题示例契约，须通过 §6.3 校验 |
| `tests/` | 后续 | 实现 §8.1 的校验器与 fixtures |

**变更规则**：任何阶段发现本规格与实现冲突时，先修改本规格再改实现；本规格为唯一仲裁源。
