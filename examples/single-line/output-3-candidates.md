# 单行模式输出示例（无参考图）：3 张同文案候选

> 对应输入：`input.md`（`<!-- input: 我真的会谢 -->`，无参考图）。
> 本示例为**契约路径（路径 ②）**输出：假设宿主无原生生图工具，助手输出**恰好一个** `kss-prompt` 块，块内为 **3 个契约对象的 JSON 数组**（每张贴纸 1 个对象）。块格式定义见 `examples/README.md` §2 与 `docs/PROMPT_CONTRACT.md` §1.2 / §5。

## 一次运行输出（3 个候选，共享同一句文案）

- **文案**：三张**完全共享**「我真的会谢」（`text.content` 逐字、字节级相等，`verbatim: true`），画面中该文案恰好出现一次。
- **角色**：`source: "profile"`，`feature_map` 取自 `character_profiles/my-melody.md`（示例文字档案），三份**完全相同**（锁定）。
- **风格**：`style_anchor` 三份**相同**。
- **差异维度**：仅 `expression`、`pose_action`、`composition`、`sticker_elements` 三张互异。
- **输出硬约束**：`output` 三份**相同**（1:1、透明 PNG、文字烧录）。

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
        "derivation_notes": "取自 character_profiles/my-melody.md（示例文字档案，source=profile）"
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
        "derivation_notes": "取自 character_profiles/my-melody.md（示例文字档案，source=profile）"
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
        "derivation_notes": "取自 character_profiles/my-melody.md（示例文字档案，source=profile）"
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

## 校验要点 (Validator Notes)

- [ ] `kss-prompt` 块**恰好一个**；`JSON.parse` 成功；顶层为数组且长度**恰为 3**。
- [ ] 3 个对象的 `text.content` 全部与输入标记「我真的会谢」**逐字相等**（字节级），`text.verbatim` 全部为 `true`。
- [ ] 3 个对象的 `expression`、`pose_action`、`composition` **两两不同**（`sticker_elements` 亦不同）。
- [ ] 3 个对象的 `format_version`、`style_anchor`、`character.feature_map`（深比较）、`output.*` **完全相同**。
- [ ] `character.source` 全部为 `"profile"`；`feature_map` 字段完整（含可选字段 `body_proportions` 等）。
- [ ] 每个对象均含全部 ✅ 必填字段；enum/const 逐值、区分大小写合法；`review_flags` 字段名合法、值均为 boolean。
