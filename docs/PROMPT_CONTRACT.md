# Prompt Contract v1 — 提示词契约规范 (PROMPT_CONTRACT)

| 元数据 | 值 |
|---|---|
| 文档 | `docs/PROMPT_CONTRACT.md` |
| 版本 | 1.0（`format_version: "1.0"`） |
| 状态 | 生效（**机器校验权威**：contract 校验以本文件为准） |
| 语言 | 中文为主，英文术语为辅（English keywords） |
| 上级规格 | `docs/SPEC.md` §6 的完整展开；内容冲突时见 §8 |

> **权威关系声明**：本文件是 `docs/SPEC.md` §6 的展开与机器校验规范。任何**机器校验器**（如 `tests/validate_examples.py`）以本文件字段表与校验规则为准；`docs/SPEC.md` 负责整体规格。本文件与 SPEC 的差异与澄清逐条记录于 §8。

## 目录 (TOC)

1. [定位与序列化](#1-定位与序列化-purpose--serialization)
2. [顶层字段表（必填 vs 可选）](#2-顶层字段表-required-vs-optional)
3. [嵌套对象明细 (Nested Objects)](#3-嵌套对象明细-nested-objects)
4. [机器校验规则 (Machine Validation Rules)](#4-机器校验规则-machine-validation-rules)
5. [完整示例：单行模式（3 变体）](#5-完整示例单行模式3-变体)
6. [完整示例：主题模式（6 变体）](#6-完整示例主题模式6-变体)
7. [字段等价性 (Field Equivalence)](#7-字段等价性-field-equivalence)
8. [与 SPEC 的一致性说明 (Consistency with SPEC)](#8-与-spec-的一致性说明-consistency-with-spec)
9. [版本与变更 (Versioning & Changes)](#9-版本与变更-versioning--changes)

---

## 1. 定位与序列化 (Purpose & Serialization)

### 1.1 定位 (Purpose)

Prompt Contract v1 是**宿主无关（host-agnostic）、机器可校验（machine-checkable）**的标准化生图指令。当宿主没有原生生图工具（或原生工具调用失败降级）时，助手输出契约块作为**唯一**的机器输出；用户/宿主可把契约喂给任何支持该契约的生图能力。

- 单行模式：一次运行产出 **3** 个契约对象（每张贴纸 1 个）。
- 主题模式：一次运行产出 **6** 个契约对象（每张贴纸 1 个）。

### 1.2 序列化 (Serialization)

- 一次运行输出**恰好一个** fenced code block，info string 固定为 `kss-prompt`，块内为 **JSON**（RFC 8259）。
- 块内 JSON 的**聚合形态**：
  - `N = 1`：该值为**单个契约对象**。
  - `N > 1`（本项目固定为 3 或 6）：该值为 **JSON 数组**，长度**恰好为 N**，每个元素是一个契约对象（见 §1.1 数量约束）。
- 定位正则：块起始 `` ^```kss-prompt$ ``，闭合 `` ^```$ ``。
- 机器校验器必须接受以上两种形态；数组长度必须等于该模式要求的数量（`single_line` = 3，`theme` = 6），否则校验失败。
- 契约块前后可附自然语言说明，但机器校验**只认契约块**。

---

## 2. 顶层字段表 (Required vs Optional)

✅ = 必填；⭕ = 可选（推荐）。`character` / `text` / `output` / `review_flags` 为嵌套对象，明细见 §3。

| 字段路径 field path | 必填 | 类型 / 取值 | 说明 (Description) |
|---|---|---|---|
| `format_version` | ✅ | string，恒为 `"1.0"` | 契约版本；本文件 v1.0 |
| `mode` | ✅ | enum：`"single_line"` \| `"theme"` | 模式；须与 SPEC §3.1 判定一致 |
| `character.source` | ✅ | enum：`"image"` \| `"profile"` | 角色来源：参考图 / 文字档案 |
| `character.feature_map` | ✅ | object（§3.1） | 锁定的角色特征；本次运行内所有契约**完全相同** |
| `style_anchor` | ✅ | string | 风格锚点，固定为「美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)」；主题模式整套一致 |
| `expression` | ✅ | string | 表情：开心 / 委屈 / 无语 / 元气…（单行模式 3 张**互异**） |
| `pose_action` | ✅ | string | 姿势/动作：举手 / 蹲墙角 / 比心…（单行模式 3 张**互异**） |
| `composition` | ✅ | string | 构图：居中特写 / 全身 / 对角 / 贴纸气泡…（单行模式 3 张**互异**） |
| `sticker_elements` | ⭕ | array of string | 贴纸装饰：虚线框 / 闪粉 / 小花 / 星星 / 手帐贴纸层 |
| `text.content` | ✅ | string | 文案原文；`single_line` 下必须与用户输入**逐字相等**；`theme` 下为助手自拟权威文案 |
| `text.verbatim` | ✅ | boolean | `true` = 画面逐字呈现 `text.content`；`single_line` 必须为 `true` |
| `text.typography` | ⭕ | object（§3.3） | 字体建议：圆体/手写风、描边、对齐（横排/竖排）、气泡样式 |
| `output.format` | ✅ | const：`"png"` | 输出格式；机器校验值恒为**小写** `"png"`（人类可读写作 PNG，见 §8-2） |
| `output.background` | ✅ | const：`"transparent"` | 背景透明 |
| `output.aspect_ratio` | ✅ | const：`"1:1"` | 正方形 |
| `output.text_baked` | ✅ | const：`true` | 文字烧录进画面，不依赖外部字幕 |
| `review_flags` | ⭕ | object of boolean（§3.4） | 生成后自检（SPEC §8.1 字段集） |

---

## 3. 嵌套对象明细 (Nested Objects)

### 3.1 `character.feature_map`

| 字段 | 必填 | 类型 | 说明 (Description) |
|---|---|---|---|
| `head_shape` | ✅ | string | 头型：圆润 / 椭圆 / 心形等 |
| `ears` | ✅ | string | 耳朵：形状、大小、内耳颜色、是否被头饰遮挡 |
| `eyes` | ✅ | string | 眼睛风格：豆豆眼 / 线条眼 / 大眼高光等 |
| `nose_mouth` | ✅ | string | 鼻子与嘴：小圆鼻 / 无鼻、w 嘴 / 嘟嘴等 |
| `palette` | ✅ | object | 主色 / 辅色 / 点缀色（建议 2–5 色，可附 HEX 或中文色名） |
| `signature_accessories` | ✅ | array of string | 标志性配饰：头巾 / 蝴蝶结 / 帽子 / 花等 |
| `body_proportions` | ⭕ | string | 身体比例：Q 版头身比、四肢样式 |
| `personality_keywords` | ⭕ | array of string | 性格关键词：软萌 / 委屈 / 元气 / 傲娇 |
| `texture` | ⭕ | string | 质感：铅笔手绘线稿 / 水彩 / 蜡笔颗粒 |
| `derivation_notes` | ⭕ | string | 推导说明：来源依据、置信度、`unknown` 原因 |

`source = "image"` 时，无法从参考图确定的字段必须显式写 `"unknown"` 并记入 `derivation_notes`（SPEC §4.1-4）；`source = "profile"` 时所有字段由档案文字推导。

### 3.2 `text`

| 字段 | 必填 | 说明 (Description) |
|---|---|---|
| `content` | ✅ | 文案原文（见 §2 约束） |
| `verbatim` | ✅ | boolean；`single_line` 必须为 `true` |
| `typography` | ⭕ | 见 §3.3 |

### 3.3 `text.typography`（可选，推荐）

| 字段 | 必填 | 说明 (Description) |
|---|---|---|
| `style` | ⭕ | 字体风格：圆体加粗 / 手写体 / 涂鸦体 |
| `alignment` | ⭕ | 对齐：横排居中 / 横排居左 / 竖排右侧… |
| `outline` | ⭕ | 描边：白色描边 / 深色描边… |
| `bubble` | ⭕ | 气泡样式：手帐虚线框 / 叹号气泡 / 便签条… |

### 3.4 `output` 与 `review_flags`

- `output`：四个字段均为 const，见 §2 表；机器校验逐值（**区分大小写**）比对。
- `review_flags`：可选对象，值必须为 boolean。合法字段名（SPEC §8.1）：
  `verbatim_preserved`、`text_baked`、`transparent`、`square_1to1`、`readable_at_small`、`no_watermark`、`no_trademark`。
  出现未列举字段名 → 校验失败；布尔真实性由人工/视觉校验兜底（SPEC §8.2）。

---

## 4. 机器校验规则 (Machine Validation Rules)

对**每个契约对象**（数组元素）逐项执行；对**一次运行**整体执行聚合规则。

1. **块定位**：`` ^```kss-prompt$ `` … 闭合 `` ^```$ ``。
2. **可解析**：块内 JSON 经 `JSON.parse` 成功；顶层为对象或数组。
3. **形态**：顶层数组 → 长度必须等于模式数量（`single_line` = 3，`theme` = 6）；顶层对象 → 视为 N = 1（本项目模式下不合法，除非将来定义 N=1 模式）。
4. **必填字段**：所有 ✅ 字段存在且类型/取值合法（enum / const **逐值、区分大小写**校验）。
5. **模式约束**：`mode = "single_line"` ⇒ `text.verbatim === true` 且 `text.content` 与用户输入逐字相等；`mode = "theme"` ⇒ 6 个 `text.content` 两两不同。
6. **运行内一致性**：同一次运行的所有契约——`format_version`、`style_anchor`、`character.feature_map`（深比较）、`output.*` 完全一致。
7. **单行区分度**：`mode = "single_line"` ⇒ 3 个契约的 `expression`、`pose_action`、`composition` 两两不同（`sticker_elements` 建议不同）。
8. **主题区分度**：`mode = "theme"` ⇒ 6 个契约的 `expression` / `pose_action` / `composition` 组合两两不同。
9. **review_flags**：若存在：字段名 ∈ §3.4 合法集合，值均为 boolean。
10. **示例校验**：`examples/` 下的示例契约按规则 1–9 校验；其中「用户输入」取 `examples/` 对应输入文件中声明的输入。

---

## 5. 完整示例：单行模式（3 变体）

> 输入（示例）：一句原样文案「我真的会谢」。角色：无参考图 → 回退文字档案 `character_profiles/my-melody.md`（`source: "profile"`）。
> 一次运行输出**一个** `kss-prompt` 块，内容为 **3 个契约对象的数组**：

```kss-prompt
[
  {
    "format_version": "1.0",
    "mode": "single_line",
    "character": {
      "source": "profile",
      "feature_map": {
        "head_shape": "圆润",
        "ears": "头巾遮耳，露出内耳",
        "eyes": "豆豆眼",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油粉", "辅色": "白色", "点缀": "草莓红"},
        "signature_accessories": ["红色头巾", "小蝴蝶结"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "委屈"],
        "texture": "铅笔手绘线稿",
        "derivation_notes": "取自 character_profiles/my-melody.md（示例文字档案）"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "委屈巴巴",
    "pose_action": "蹲在角落画圈圈",
    "composition": "居中全身特写，配手帐虚线框",
    "sticker_elements": ["星星", "小花"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边", "bubble": "手帐虚线框内横排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "single_line",
    "character": {
      "source": "profile",
      "feature_map": {
        "head_shape": "圆润",
        "ears": "头巾遮耳，露出内耳",
        "eyes": "豆豆眼",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油粉", "辅色": "白色", "点缀": "草莓红"},
        "signature_accessories": ["红色头巾", "小蝴蝶结"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "委屈"],
        "texture": "铅笔手绘线稿",
        "derivation_notes": "取自 character_profiles/my-melody.md（示例文字档案）"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "无语翻白眼",
    "pose_action": "双手抱胸，侧身扭头",
    "composition": "半身斜角构图，头顶叹号气泡",
    "sticker_elements": ["闪电线", "涂鸦圈"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "竖排右侧", "outline": "白色描边", "bubble": "叹号气泡内竖排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "single_line",
    "character": {
      "source": "profile",
      "feature_map": {
        "head_shape": "圆润",
        "ears": "头巾遮耳，露出内耳",
        "eyes": "豆豆眼",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油粉", "辅色": "白色", "点缀": "草莓红"},
        "signature_accessories": ["红色头巾", "小蝴蝶结"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "委屈"],
        "texture": "铅笔手绘线稿",
        "derivation_notes": "取自 character_profiles/my-melody.md（示例文字档案）"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "无奈假笑",
    "pose_action": "举起双手耸肩",
    "composition": "居中大头特写，配贴纸气泡",
    "sticker_elements": ["云朵", "便签条"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "手写体", "alignment": "横排居中", "outline": "白色描边", "bubble": "贴纸气泡内横排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  }
]
```

3 个对象共享 `text.content`（「我真的会谢」逐字相等）与同一 `feature_map` / `style_anchor` / `output`；在 `expression`、`pose_action`、`composition`、`sticker_elements` 上互异。

---

## 6. 完整示例：主题模式（6 变体）

> 输入（示例）：主题「打工人」。角色：假设用户上传了 1 张参考图（`source: "image"`；图片未随仓库分发，`feature_map` 为演示形态，实际运行时由 SPEC §4.1 管线提取）。
> 一次运行输出**一个** `kss-prompt` 块，内容为 **6 个契约对象的数组**（文案、情绪、姿势、构图互不相同；`style_anchor` / `feature_map` / `output` 整套一致）：

```kss-prompt
[
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "长垂耳兔耳，内耳蜜桃粉",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "蜜桃粉", "点缀": "抹茶绿"},
        "signature_accessories": ["珍珠发夹", "小工牌"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "元气", "打工人"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "示例：假设用户上传 1 张参考图；字段为演示形态，实际运行时按 SPEC §4.1 提取并填写 unknown/置信度"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "元气满满",
    "pose_action": "握拳比心",
    "composition": "全身居中，手帐虚线框",
    "sticker_elements": ["星星", "小太阳"],
    "text": {
      "content": "上班第一天，元气满满",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边", "bubble": "手帐虚线框内横排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "长垂耳兔耳，内耳蜜桃粉",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "蜜桃粉", "点缀": "抹茶绿"},
        "signature_accessories": ["珍珠发夹", "小工牌"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "元气", "打工人"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "示例：假设用户上传 1 张参考图；字段为演示形态，实际运行时按 SPEC §4.1 提取并填写 unknown/置信度"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "心虚回头",
    "pose_action": "回头偷瞄，食指放唇边",
    "composition": "侧身斜角构图，便签条遮挡半脸",
    "sticker_elements": ["偷看眼睛", "便签条"],
    "text": {
      "content": "摸鱼被抓",
      "verbatim": true,
      "typography": {"style": "手写体", "alignment": "竖排右侧", "outline": "白色描边", "bubble": "便签条内竖排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "长垂耳兔耳，内耳蜜桃粉",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "蜜桃粉", "点缀": "抹茶绿"},
        "signature_accessories": ["珍珠发夹", "小工牌"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "元气", "打工人"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "示例：假设用户上传 1 张参考图；字段为演示形态，实际运行时按 SPEC §4.1 提取并填写 unknown/置信度"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "兴奋咧嘴",
    "pose_action": "奔跑起飞，背包甩起",
    "composition": "对角动态构图，速度线",
    "sticker_elements": ["云朵", "音符"],
    "text": {
      "content": "周五下班冲鸭",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排左倾", "outline": "白色描边", "bubble": "速度线旁横排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "长垂耳兔耳，内耳蜜桃粉",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "蜜桃粉", "点缀": "抹茶绿"},
        "signature_accessories": ["珍珠发夹", "小工牌"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "元气", "打工人"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "示例：假设用户上传 1 张参考图；字段为演示形态，实际运行时按 SPEC §4.1 提取并填写 unknown/置信度"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "疲惫眯眼",
    "pose_action": "双手捧大杯咖啡",
    "composition": "居中特写，蒸汽气泡",
    "sticker_elements": ["咖啡杯", "蒸汽"],
    "text": {
      "content": "咖啡续命",
      "verbatim": true,
      "typography": {"style": "手写体", "alignment": "横排居中", "outline": "白色描边", "bubble": "蒸汽气泡内横排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "长垂耳兔耳，内耳蜜桃粉",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "蜜桃粉", "点缀": "抹茶绿"},
        "signature_accessories": ["珍珠发夹", "小工牌"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "元气", "打工人"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "示例：假设用户上传 1 张参考图；字段为演示形态，实际运行时按 SPEC §4.1 提取并填写 unknown/置信度"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "无语死鱼眼",
    "pose_action": "双手叉腰叹气",
    "composition": "半身构图，头顶画饼涂鸦",
    "sticker_elements": ["饼状涂鸦", "闪电线"],
    "text": {
      "content": "老板画饼",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "竖排左侧", "outline": "白色描边", "bubble": "画饼涂鸦旁竖排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  },
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "长垂耳兔耳，内耳蜜桃粉",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "蜜桃粉", "点缀": "抹茶绿"},
        "signature_accessories": ["珍珠发夹", "小工牌"],
        "body_proportions": "Q 版 2 头身",
        "personality_keywords": ["软萌", "元气", "打工人"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "示例：假设用户上传 1 张参考图；字段为演示形态，实际运行时按 SPEC §4.1 提取并填写 unknown/置信度"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "开心眯眼笑",
    "pose_action": "转圈撒花",
    "composition": "全身旋转构图，花瓣飘落",
    "sticker_elements": ["花瓣", "金币"],
    "text": {
      "content": "工资到账",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边", "bubble": "花瓣间横排"}
    },
    "output": {"format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true},
    "review_flags": {
      "verbatim_preserved": true,
      "text_baked": true,
      "transparent": true,
      "square_1to1": true,
      "readable_at_small": true,
      "no_watermark": true,
      "no_trademark": true
    }
  }
]
```

6 个对象：`text.content` 两两不同、`expression` / `pose_action` / `composition` 组合两两不同；`feature_map`、`style_anchor`、`output` 六份**完全相同**（SPEC §6.3 规则 5 / 本文件规则 6）。

---

## 7. 字段等价性 (Field Equivalence)

- **任何 Markdown 提示词块**（无论 info string 是否为 `kss-prompt`）只要用于本技能生图，**必须携带与契约相同的语义字段**：`mode`、`character{source, feature_map}`、`style_anchor`、`expression`、`pose_action`、`composition`、`sticker_elements`、`text{content, verbatim}`、以及全部 `output` 硬约束（1:1、透明 PNG、文字烧录）。
- **原生工具提示词**（路径 ①）同样必须携带上述字段（SPEC §5.2）；机器校验只解析 `kss-prompt` JSON 块，但字段缺失会直接导致产出不满足硬约束。
- **唯一机器输出**：路径 ② 下 `kss-prompt` 块是唯一机器可校验输出；路径 ① 下不输出契约块。

---

## 8. 与 SPEC 的一致性说明 (Consistency with SPEC)

本文件以 SPEC §6 为基准，逐条对齐；SPEC 未规定或存在歧义处，**本文件为机器校验的权威**（按阶段指令：机器校验以本文件为准）。差异与澄清如下：

1. **补充——多份契约的 JSON 聚合形态**：SPEC §6.1 规定单行 3 份 / 主题 6 份契约，但未规定多份契约在单个 `kss-prompt` 块中的序列化形态。本文件补充：`N > 1` 时为**长度恰为 N 的 JSON 数组**，`N = 1` 时可为单对象（§1.2、§4-3）。SPEC §6.4 的单对象最小示例仍合法。**机器校验以本文件为准。**
2. **澄清——`output.format` 大小写**：SPEC §6.2 / §6.4 定义 const 为小写 `"png"`。本文件沿用小写 `"png"` 作为机器校验值（const 逐值、区分大小写）；人类可读写作「PNG」。无字段语义冲突。
3. **澄清——`theme` 模式的 `text.verbatim`**：SPEC §6.2 仅强制 `single_line ⇒ verbatim === true`。本文件补充：`theme` 模式下 `verbatim: true` 表示画面逐字呈现契约中自拟的 `text.content`（契约文本即权威文案），示例统一为 `true`。
4. **无其他偏差**：字段集合、类型、enum/const、`review_flags` 字段名与 SPEC §6.2 / §8.1 完全一致。

---

## 9. 版本与变更 (Versioning & Changes)

- 本文件定义 **Contract v1**（`format_version: "1.0"`）。
- **兼容规则**：后续版本只增不改字段语义；已发布字段的取值语义不得变更。
- **变更流程**：任何实现阶段发现本文件与 SPEC 冲突时，先按 SPEC §10 变更规则修改 SPEC，再同步本文件与实现；本文件自身修订须同步更新 §8 一致性说明与示例。
