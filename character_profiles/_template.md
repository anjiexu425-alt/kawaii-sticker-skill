# Character Profile — <角色名>（示例模板）

> 用途：用户**没有参考图**时的文字版角色档案（fallback）。纯 Markdown 文本，**不含图片素材**；不得包含受版权保护的官方形象 / 商标（见 `NOTICE.md`）。完整字段规范见 `docs/PROMPT_CONTRACT.md` §3.1 与 `docs/SPEC.md` §4.3。
> 使用方式：复制本文件为 `character_profiles/<角色名>.md` 后填写；助手会把档案解析为锁定的 `feature_map`（`character.source = "profile"`）。如为**原创角色**，可另放参考图 `<角色名>.png`（有图时走 `source: "image"`）。

| 元数据 | 值 |
|---|---|
| 档案 | `character_profiles/<角色名>.md` |
| 类型 | 文字版角色档案（text profile） |
| 角色来源 | `source: "profile"` |
| 参考图 | 可选：用户原创参考图（如 `<角色名>.png`），有图时 `source: "image"` |
| 语言 | 中文为主，英文术语为辅 |

## 1. 角色概述 (Overview)

<2–3 句话：物种 / 造型、气质、画风一句话>

## 2. 画风（style_anchor）

<画风一句话，如：手绘绘本 × 日系萌系——柔软铅笔/细线稿、细腻绒毛、低饱和配色>（本字段决定契约 `style_anchor`，见 PROMPT_CONTRACT §2；整套贴纸必须统一该画风）

## 3. 视觉特征 (Visual Characteristics)

| 特征 | 描述 |
|---|---|
| 头型 head_shape | <如：圆润 / 椭圆 / 心形> |
| 耳朵 ears | <形状、大小、是否被头饰遮挡、内耳颜色> |
| 眼睛 eyes | <豆豆眼 / 线条眼 / 大眼高光> |
| 鼻子与嘴 nose_mouth | <小圆鼻 + w 嘴 / 嘟嘴> |
| 主色 palette | 主色：<…>；辅色：<…>；点缀色：<…> |
| 标志性配饰 signature_accessories | <如：头巾 / 蝴蝶结 / 帽子 / 花> |
| 身体比例 body_proportions | <如：Q 版 2 头身> |
| 性格关键词 personality_keywords | <软萌 / 元气 / 傲娇…> |
| 质感 texture | <铅笔手绘线稿 / 水彩 / 蜡笔颗粒> |

## 4. 贴纸化建议 (Sticker-ization Notes)

- 适合表情：<委屈巴巴 / 无语 / 开心眯眼…>
- 装饰元素：<手帐虚线框 / 小花 / 星星 / 便签条 / 闪粉>
- 文案排版：<字体、描边、横竖排、气泡样式；须保证 64px 缩放下可读>

## 5. feature_map 对照表 (Parsing into `feature_map`)

| `feature_map` 字段 | 本档案取值 |
|---|---|
| `head_shape` | `"<…>"` |
| `ears` | `"<…>"` |
| `eyes` | `"<…>"` |
| `nose_mouth` | `"<…>"` |
| `palette` | `{"主色": "<…>", "辅色": "<…>", "点缀": "<…>"}` |
| `signature_accessories` | `["<…>"]` |
| `body_proportions` | `"<…>"` |
| `personality_keywords` | `["<…>"]` |
| `texture` | `"<…>"` |
| `derivation_notes` | `"取自 character_profiles/<角色名>.md（文字档案，source=profile）"` |

> 角色身份字段（`head_shape` / `ears` / `eyes` / `nose_mouth` / `signature_accessories`）一经锁定不得漂移（SKILL.md §6.2）；运行时可按用户指令微调 `palette` / 配饰。
