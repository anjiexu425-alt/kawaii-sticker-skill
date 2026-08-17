# Adapter — 通用生图能力 (Generic Image Models)

当宿主没有原生图像工具，且用户希望把契约（路径 ②）交给**任意**生图能力时，按本文件把每个契约对象翻译为自然语言提示词。契约字段规范见 `docs/PROMPT_CONTRACT.md`；规则本体见 `SKILL.md` §7。

## 1. 翻译规则（一个契约对象 → 一条提示词）

| 契约字段 | 翻译进提示词 |
|---|---|
| `character.feature_map` | 逐字段拼写：头型、耳朵、眼睛、鼻子嘴、配色、标志性配饰、身体比例、质感 |
| `style_anchor` | 原样放入（由角色档案画风决定；默认胖墩：`手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)`） |
| `expression` / `pose_action` / `composition` / `sticker_elements` | 组成该张的画面描述（一张一景） |
| `text.content` | **逐字**放入，并要求「画面中该文案恰好出现一次」，配合 `text.typography`（字体 / 描边 / 排版） |
| `output` | 硬约束原样声明：1:1 方形、PNG、透明背景、文字烧录、无水印 |

**负面提示（示例）**：`blurry, watermark, logo, extra text, duplicate text, cropped, low quality, busy background`

## 2. 透明背景处理

- 首选支持 alpha 透明输出的模型/参数（如部分 gpt-image、Stable Diffusion 生态的透明模式）。
- 不支持时：以纯色背景（如纯白 / 纯绿）生成 → 后处理去底（背景移除工具 / chroma key / 图像编辑 API），并在交付说明中标注后处理步骤。

## 3. 中文文字

- 选择支持中文字形的模型与字体；提示词写明「中文文案、圆体/手写体、白色描边、深色字芯」，避免缺字/豆腐块。
- 若模型文字渲染能力弱：先出**无字图**，再用图像编辑能力叠加文字（保持逐字），并在交付说明标注叠加步骤。

## 4. 批量一致性

- 单行模式：3 条提示词并行，共享**同一份** `feature_map` 与 `style_anchor` 字符串（逐字符一致），仅画面维度不同。
- 主题模式：6 条提示词并行，`feature_map` / `style_anchor` / 输出约束完全一致，文案与画面互异。
- 生成后按 SKILL.md §8 自检清单逐张核对并填写 `review_flags`。
