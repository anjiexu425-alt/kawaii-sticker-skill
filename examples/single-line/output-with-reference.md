# 单行模式输出示例（带参考图）：3 张同文案候选（feature_map 由参考图推导）

> 对应输入：`input-with-reference.md`（`<!-- input: 我真的会谢 -->` + 1 张参考图，文字描述）。
> 本示例为**契约路径（路径 ②）**输出：**恰好一个** `kss-prompt` 块，块内为 **3 个契约对象的 JSON 数组**。
> 与 `output-3-candidates.md`（profile 回退）对比：本示例的 `feature_map` 由参考图推导（SPEC §4.1），可见不同（大眼高光 vs 豆豆眼；草莓小发夹 vs 小蝴蝶结；主色奶油白 vs 奶油粉；`body_proportions` 为 `unknown`）。

## 一次运行输出（3 个候选，共享同一句文案）

- **文案**：三张共享「我真的会谢」（逐字、字节级相等，`verbatim: true`），画面中恰好出现一次。
- **角色**：`source: "image"`；`feature_map` 从参考图提取并**锁定**，三份完全相同。
- **风格**：`style_anchor` 三份相同。
- **差异维度**：`expression`、`pose_action`、`composition`、`sticker_elements` 三张互异。
- **输出硬约束**：`output` 三份相同（1:1、透明 PNG、文字烧录）。

```kss-prompt
[
  {
    "format_version": "1.0",
    "mode": "single_line",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "红色连帽头巾遮耳，露出蜜桃粉内耳",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "头巾红", "点缀": "草莓红"},
        "signature_accessories": ["红色连帽头巾", "草莓小发夹"],
        "body_proportions": "unknown（参考图为头部特写，无法确定身体比例）",
        "personality_keywords": ["软萌", "元气"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "由参考图逐项提取（SPEC §4.1）：头巾红色约 #E8505B；草莓发夹位于头巾右侧；大眼高光明显；仅头部特写故 body_proportions 记为 unknown"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "元气爆棚",
    "pose_action": "举起双手比耶",
    "composition": "居中大头特写，头顶草莓涂鸦气泡",
    "sticker_elements": ["草莓", "闪光星星"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边", "bubble": "草莓气泡内横排"}
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
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "红色连帽头巾遮耳，露出蜜桃粉内耳",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "头巾红", "点缀": "草莓红"},
        "signature_accessories": ["红色连帽头巾", "草莓小发夹"],
        "body_proportions": "unknown（参考图为头部特写，无法确定身体比例）",
        "personality_keywords": ["软萌", "元气"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "由参考图逐项提取（SPEC §4.1）：头巾红色约 #E8505B；草莓发夹位于头巾右侧；大眼高光明显；仅头部特写故 body_proportions 记为 unknown"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "得意挑眉",
    "pose_action": "双手叉腰昂头",
    "composition": "半身侧倾构图，身后洒落音符",
    "sticker_elements": ["音符", "涂鸦圈"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "手写体", "alignment": "竖排右侧", "outline": "白色描边", "bubble": "音符旁竖排"}
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
      "source": "image",
      "feature_map": {
        "head_shape": "圆润，奶油白",
        "ears": "红色连帽头巾遮耳，露出蜜桃粉内耳",
        "eyes": "大眼高光，圆溜溜",
        "nose_mouth": "小圆鼻，w 嘴",
        "palette": {"主色": "奶油白", "辅色": "头巾红", "点缀": "草莓红"},
        "signature_accessories": ["红色连帽头巾", "草莓小发夹"],
        "body_proportions": "unknown（参考图为头部特写，无法确定身体比例）",
        "personality_keywords": ["软萌", "元气"],
        "texture": "铅笔手绘线稿，粉彩平涂",
        "derivation_notes": "由参考图逐项提取（SPEC §4.1）：头巾红色约 #E8505B；草莓发夹位于头巾右侧；大眼高光明显；仅头部特写故 body_proportions 记为 unknown"
      }
    },
    "style_anchor": "美乐蒂手绘 / 手帐风 (My Melody-style hand-drawn, journal/diary aesthetic)",
    "expression": "抿嘴害羞",
    "pose_action": "双手捧脸低头",
    "composition": "三分身斜角构图，脸颊贴纸遮半脸",
    "sticker_elements": ["小花", "爱心"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边", "bubble": "爱心气泡内横排"}
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

- [ ] `kss-prompt` 块**恰好一个**；`JSON.parse` 成功；数组长度**恰为 3**。
- [ ] 3 个对象 `text.content` 全部与输入「我真的会谢」**逐字相等**、`verbatim: true`。
- [ ] 3 个对象 `expression`、`pose_action`、`composition` **两两不同**。
- [ ] 3 个对象 `format_version`、`style_anchor`、`character.feature_map`（深比较）、`output.*` **完全相同**（锁定 + 一致性）。
- [ ] `character.source` 全部为 `"image"`；`feature_map` 与 `output-3-candidates.md`（profile 版）**可见不同**（体现参考图特征）。
- [ ] `body_proportions` 为 `unknown` 且 `derivation_notes` 说明原因（SPEC §4.1-4 不确定性处理）。
