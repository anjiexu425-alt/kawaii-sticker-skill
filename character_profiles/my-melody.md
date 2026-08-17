# Character Profile — 美乐蒂手绘文字风格示例（非默认）(Non-default My Melody-style Text Example)

> 本档案是**文字版**的角色风格与特征描述（纯 Markdown 文本，**不含任何图片素材**；非官方素材，非 Sanrio 资产——见 `NOTICE.md`）。
> 本档案为**非默认的文字风格示例**（第三方风格教学用途，非官方素材）；默认原创角色为「胖墩」（`character_profiles/pangdun.md`）。新增角色 = 在 `character_profiles/` 新增一个 `.md` 档案即可，无需改任何代码（SPEC §4.2 / SKILL.md §6.3）。
> 使用方式：用户无参考图时，助手加载本档案并按下方「feature_map 对照表」解析出锁定的 `feature_map`（`character.source = "profile"`）。

| 元数据 | 值 |
|---|---|
| 档案 | `character_profiles/my-melody.md` |
| 类型 | 文字版角色档案（text profile，无图片） |
| 角色来源 | `source: "profile"` |
| 对应规格 | SPEC §4.2–§4.3 / SKILL.md §6.2–§6.3 |
| 语言 | 中文为主，英文术语为辅 |

## 1. 角色概述 (Overview)

一只**软萌的白色小兔系角色**：圆润的奶油色脸蛋、红色连帽头巾遮住耳朵上部并露出粉嫩内耳、豆豆眼配小圆鼻与 w 嘴，气质委屈又元气。整体为**手绘铅笔线稿 + 柔和粉彩**的可爱画风，适合制作手帐风（journal-diary）聊天贴纸。

> ⚠️ 本档案是对一种**画风与角色特征的通用文字描述**，用于示例教学；不代表、不复制任何第三方官方角色形象。生成时不得复现任何商标、Logo 或官方原图（SKILL.md §9）。

## 2. 视觉特征 (Visual Characteristics)

| 特征 | 描述 |
|---|---|
| 头型 head_shape | 圆润（cream 奶油感），脸部圆嘟 |
| 耳朵 ears | 红色连帽头巾遮住耳朵上部，露出内耳（蜜桃粉色调）；头巾两侧有小垂耳轮廓 |
| 眼睛 eyes | 豆豆眼（细线黑豆眼），无大高光；委屈时眼角下垂 |
| 鼻子与嘴 nose_mouth | 小圆鼻（几乎无鼻梁）+ w 嘴 / 微嘟嘴 |
| 主色 palette | 主色：奶油粉；辅色：白色；点缀色：草莓红 |
| 标志性配饰 signature_accessories | 红色头巾（连帽、带系带）、小蝴蝶结（可选：头巾一侧） |
| 身体比例 body_proportions | Q 版 2 头身，短手短脚，四肢圆润 |
| 性格关键词 personality_keywords | 软萌、委屈、元气（偶尔小傲娇） |
| 质感 texture | 铅笔手绘线稿 + 粉彩平涂；线条干净、描边圆润 |

## 3. 贴纸化建议 (Sticker-ization Notes)

- 表情适合：委屈巴巴 / 无语 / 开心眯眼 / 元气比心——变化表情即可得到同一角色的不同候选贴纸。
- 装饰元素：手帐虚线框、小花、星星、便签条、闪粉、气泡（SKILL.md §5 手帐风）。
- 文案排版：圆体加粗 / 手写体，白色描边 + 深色字芯，横排或竖排均可，须保证 64px 缩放下可读。

## 4. feature_map 对照表 (Parsing into `feature_map`)

助手解析本档案时，按以下映射生成 `character.feature_map`（JSON 对象，字段规范见 SPEC §4.3 / PROMPT_CONTRACT §3.1）：

| `feature_map` 字段 | 本档案取值（示例） |
|---|---|
| `head_shape` | `"圆润"` |
| `ears` | `"头巾遮耳，露出内耳"` |
| `eyes` | `"豆豆眼"` |
| `nose_mouth` | `"小圆鼻，w 嘴"` |
| `palette` | `{"主色": "奶油粉", "辅色": "白色", "点缀": "草莓红"}` |
| `signature_accessories` | `["红色头巾", "小蝴蝶结"]` |
| `body_proportions` | `"Q 版 2 头身"` |
| `personality_keywords` | `["软萌", "委屈"]` |
| `texture` | `"铅笔手绘线稿"` |
| `derivation_notes` | `"取自 character_profiles/my-melody.md（示例文字档案，source=profile）"` |

> 与 `examples/single-line/output-3-candidates.md` 中 `source: "profile"` 的 `feature_map` 保持一致（黄金样本，tests 阶段校验）。实际运行时可结合用户指令微调 `palette` / 配饰，但角色身份字段（head_shape/ears/eyes/nose_mouth/signature_accessories）一经锁定不得漂移（SKILL.md §6.2 锁定）。
