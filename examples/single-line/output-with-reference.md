# 单行模式输出示例（带参考图）：3 张同文案候选（feature_map 由参考图推导）

> 对应输入：`input-with-reference.md`（`<!-- input: 我真的会谢 -->` + 1 张参考图，文字描述）。
> 本示例为**契约路径（路径 ②）**输出：**恰好一个** `kss-prompt` 块，块内为 **3 个契约对象的 JSON 数组**。
> 与 `output-3-candidates.md`（profile 回退）对比：本示例的 `feature_map` 由参考图推导（SPEC §4.1），可见不同（像素统计配色、内耳色值、斑点分布记录 vs 档案版描述）。

## 一次运行输出（3 个候选，共享同一句文案）

- **文案**：三张共享「我真的会谢」（逐字、字节级相等，`verbatim: true`），画面中恰好出现一次。
- **角色**：`source: "image"`；`feature_map` 从参考图提取并**锁定**，三份完全相同。
- **风格**：`style_anchor` 三份相同（手绘绘本 × 日系萌系）。
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
        "head_shape": "圆润梨形，头大身短（与档案一致）",
        "ears": "长垂耳垂至肩下；外侧奶白 #faf0e2，内侧浅灰米 #d9cfc2 带灰褐斑点",
        "eyes": "大深棕黑圆眼，星形小高光，视线偏右上方，有灵气",
        "nose_mouth": "小深棕三角鼻，微张嘴露粉舌",
        "palette": {"主色": "#faf0e2 暖象牙白", "辅色": "#d9cfc2 浅灰米（内耳）", "点缀": "#8a7a6b 灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（左耳 3 处/身侧 2 处/尾巴 2 处，不规则）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气"],
        "texture": "手绘绘本 × 日系萌系：柔软铅笔线稿、细腻绒毛质感",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 逐项提取（SPEC §4.1，用户原创资产）；配色经像素统计（主体 #faf0e2）；斑点分布为观察记录，跨贴纸须保持稳定"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
    "expression": "元气爆棚",
    "pose_action": "举起双手比耶",
    "composition": "居中大头特写，头顶草莓涂鸦气泡",
    "sticker_elements": ["星星", "闪光星星"],
    "text": {
      "content": "我真的会谢",
      "verbatim": true,
      "typography": {"style": "圆体加粗", "alignment": "横排居中", "outline": "白色描边", "bubble": "气泡内横排"}
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
        "head_shape": "圆润梨形，头大身短（与档案一致）",
        "ears": "长垂耳垂至肩下；外侧奶白 #faf0e2，内侧浅灰米 #d9cfc2 带灰褐斑点",
        "eyes": "大深棕黑圆眼，星形小高光，视线偏右上方，有灵气",
        "nose_mouth": "小深棕三角鼻，微张嘴露粉舌",
        "palette": {"主色": "#faf0e2 暖象牙白", "辅色": "#d9cfc2 浅灰米（内耳）", "点缀": "#8a7a6b 灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（左耳 3 处/身侧 2 处/尾巴 2 处，不规则）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气"],
        "texture": "手绘绘本 × 日系萌系：柔软铅笔线稿、细腻绒毛质感",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 逐项提取（SPEC §4.1，用户原创资产）；配色经像素统计（主体 #faf0e2）；斑点分布为观察记录，跨贴纸须保持稳定"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
        "head_shape": "圆润梨形，头大身短（与档案一致）",
        "ears": "长垂耳垂至肩下；外侧奶白 #faf0e2，内侧浅灰米 #d9cfc2 带灰褐斑点",
        "eyes": "大深棕黑圆眼，星形小高光，视线偏右上方，有灵气",
        "nose_mouth": "小深棕三角鼻，微张嘴露粉舌",
        "palette": {"主色": "#faf0e2 暖象牙白", "辅色": "#d9cfc2 浅灰米（内耳）", "点缀": "#8a7a6b 灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（左耳 3 处/身侧 2 处/尾巴 2 处，不规则）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气"],
        "texture": "手绘绘本 × 日系萌系：柔软铅笔线稿、细腻绒毛质感",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 逐项提取（SPEC §4.1，用户原创资产）；配色经像素统计（主体 #faf0e2）；斑点分布为观察记录，跨贴纸须保持稳定"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
- [ ] `character.source` 全部为 `"image"`；`feature_map` 与 `output-3-candidates.md`（profile 版）**可见不同**（体现参考图特征：像素统计配色、内耳色值、斑点分布）。
- [ ] 无法从参考图确定的字段显式 `unknown` 且 `derivation_notes` 说明原因（SPEC §4.1-4 不确定性处理）。
