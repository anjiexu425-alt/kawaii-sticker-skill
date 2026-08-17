# 主题模式输出示例：「打工人」6 张一套（1 套 = 6 份契约）

> 对应输入：`input.md`（`<!-- input: 打工人 -->` + 1 张参考图，文字描述）。
> 本示例为**契约路径（路径 ②）**输出：**恰好一个** `kss-prompt` 块，块内为 **6 个契约对象的 JSON 数组**（每张贴纸 1 个对象）。块格式定义见 `examples/README.md` §2 与 `docs/PROMPT_CONTRACT.md` §1.2 / §6。

## 一次运行输出（6 张一套）

- **文案（助手自拟）**：6 句围绕「打工人」、**两两不同**的短文案；每句逐字呈现于对应贴纸（`verbatim: true` 表示画面逐字呈现契约 `text.content`，PROMPT_CONTRACT §8-3）。
- **情绪 / 姿势 / 构图**：6 张的 `expression` / `pose_action` / `composition` 组合**两两不同**，彼此可区分。
- **一致性（整套像同一套）**：6 张共享**同一** `style_anchor`、**同一** `character.feature_map`（锁定）、**同一** `output` 硬约束，并建议统一配色倾向、描边粗细与字体风格（SPEC §3.3-5）。
- **角色**：`source: "image"`，`feature_map` 由参考图推导并锁定。

```kss-prompt
[
  {
    "format_version": "1.0",
    "mode": "theme",
    "character": {
      "source": "image",
      "feature_map": {
        "head_shape": "圆润梨形，头大身短",
        "ears": "长垂耳，垂在脸两侧；外侧奶白，内侧浅灰米带灰褐斑点",
        "eyes": "大深棕黑圆眼，水润高光，视线有方向",
        "nose_mouth": "小深棕三角鼻，小巧嘴型（默认微张露粉舌）",
        "palette": {"主色": "奶油白/暖象牙白 #faf0e2", "辅色": "浅灰米（内耳）", "点缀": "灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（长耳/身侧/尾巴）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气", "打工人"],
        "texture": "柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、低饱和",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 提取（用户原创资产）；斑点分布跨贴纸保持稳定；实际运行时按 SPEC §4.1 处理 unknown"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
        "head_shape": "圆润梨形，头大身短",
        "ears": "长垂耳，垂在脸两侧；外侧奶白，内侧浅灰米带灰褐斑点",
        "eyes": "大深棕黑圆眼，水润高光，视线有方向",
        "nose_mouth": "小深棕三角鼻，小巧嘴型（默认微张露粉舌）",
        "palette": {"主色": "奶油白/暖象牙白 #faf0e2", "辅色": "浅灰米（内耳）", "点缀": "灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（长耳/身侧/尾巴）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气", "打工人"],
        "texture": "柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、低饱和",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 提取（用户原创资产）；斑点分布跨贴纸保持稳定；实际运行时按 SPEC §4.1 处理 unknown"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
        "head_shape": "圆润梨形，头大身短",
        "ears": "长垂耳，垂在脸两侧；外侧奶白，内侧浅灰米带灰褐斑点",
        "eyes": "大深棕黑圆眼，水润高光，视线有方向",
        "nose_mouth": "小深棕三角鼻，小巧嘴型（默认微张露粉舌）",
        "palette": {"主色": "奶油白/暖象牙白 #faf0e2", "辅色": "浅灰米（内耳）", "点缀": "灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（长耳/身侧/尾巴）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气", "打工人"],
        "texture": "柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、低饱和",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 提取（用户原创资产）；斑点分布跨贴纸保持稳定；实际运行时按 SPEC §4.1 处理 unknown"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
        "head_shape": "圆润梨形，头大身短",
        "ears": "长垂耳，垂在脸两侧；外侧奶白，内侧浅灰米带灰褐斑点",
        "eyes": "大深棕黑圆眼，水润高光，视线有方向",
        "nose_mouth": "小深棕三角鼻，小巧嘴型（默认微张露粉舌）",
        "palette": {"主色": "奶油白/暖象牙白 #faf0e2", "辅色": "浅灰米（内耳）", "点缀": "灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（长耳/身侧/尾巴）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气", "打工人"],
        "texture": "柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、低饱和",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 提取（用户原创资产）；斑点分布跨贴纸保持稳定；实际运行时按 SPEC §4.1 处理 unknown"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
        "head_shape": "圆润梨形，头大身短",
        "ears": "长垂耳，垂在脸两侧；外侧奶白，内侧浅灰米带灰褐斑点",
        "eyes": "大深棕黑圆眼，水润高光，视线有方向",
        "nose_mouth": "小深棕三角鼻，小巧嘴型（默认微张露粉舌）",
        "palette": {"主色": "奶油白/暖象牙白 #faf0e2", "辅色": "浅灰米（内耳）", "点缀": "灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（长耳/身侧/尾巴）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气", "打工人"],
        "texture": "柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、低饱和",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 提取（用户原创资产）；斑点分布跨贴纸保持稳定；实际运行时按 SPEC §4.1 处理 unknown"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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
        "head_shape": "圆润梨形，头大身短",
        "ears": "长垂耳，垂在脸两侧；外侧奶白，内侧浅灰米带灰褐斑点",
        "eyes": "大深棕黑圆眼，水润高光，视线有方向",
        "nose_mouth": "小深棕三角鼻，小巧嘴型（默认微张露粉舌）",
        "palette": {"主色": "奶油白/暖象牙白 #faf0e2", "辅色": "浅灰米（内耳）", "点缀": "灰褐斑点、深棕黑眼、粉腮红"},
        "signature_accessories": ["头顶翘呆毛", "大蓬松长尾（向右弯曲）", "灰褐斑点（长耳/身侧/尾巴）"],
        "body_proportions": "小巧胖乎乎梨形，头大身短，小短手小短脚",
        "personality_keywords": ["软萌", "单纯", "活泼", "憨憨有灵气", "打工人"],
        "texture": "柔软铅笔/细线稿、轻微手绘纹理、细腻绒毛、低饱和",
        "derivation_notes": "由参考图 character_profiles/pangdun.png 提取（用户原创资产）；斑点分布跨贴纸保持稳定；实际运行时按 SPEC §4.1 处理 unknown"
      }
    },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
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

## 校验要点 (Validator Notes)

- [ ] `kss-prompt` 块**恰好一个**；`JSON.parse` 成功；数组长度**恰为 6**。
- [ ] `mode` 全部为 `"theme"`；6 个 `text.content` **两两不同**（助手自拟、口语化、有梗）。
- [ ] 6 个对象的 `expression` / `pose_action` / `composition` 组合**两两不同**。
- [ ] 6 个对象的 `format_version`、`style_anchor`、`character.feature_map`（深比较）、`output.*` **完全相同**（整套一致性，SPEC §3.3-5 / PROMPT_CONTRACT §4 规则 6）。
- [ ] `character.source` 全部为 `"image"`；`review_flags` 字段名合法、值均为 boolean。
- [ ] 人工检查（SPEC §8.2）：6 张文案与情绪彼此不同、整套风格统一（配色倾向 / 描边粗细 / 字体风格）。
