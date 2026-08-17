# Kawaii Sticker Skill（可爱贴纸技能）

> 一个**通用、开源**的 AI Skill：把它安装进 Codex / Claude Code / DeepSeek Harness 等 AI 助手后，助手会按「手绘绘本 × 日系萌系」画风，为你的**原创角色**生成**聊天贴纸 / 表情包**（内置默认原创角色「胖墩」，可公开商用）。
>
> **这不是网站 / Web App**：无服务器、无后端、无部署——它只是一套随取随用的「指令 + 资产包」。
>
> 🌸 通用设计：默认角色为**原创**「胖墩」（`character_profiles/pangdun.md` + 参考图）；任何角色都能通过参考图或文字档案接入。

## 特性 (Features)

| 能力 | 说明 |
|---|---|
| **单句模式** | 用户给一句话（如「我真的会谢」），**文案逐字保留**，生成 **3 张**同文案候选贴纸，差异在表情 / 动作 / 构图 / 贴纸装饰 |
| **主题模式** | 用户给一个主题（如「打工人」），AI 自拟文案，生成 **1 套 6 张**：文案 / 情绪 / 动作 / 构图互异、风格统一 |
| **角色参考机制** | 上传 1–3 张参考图 → 提取结构化 `feature_map` 锁定角色；无图时回退 `character_profiles/` 文字档案 |
| **宿主无关生图** | 宿主有原生生图工具 → 直接调用；否则输出**机器可校验的标准化 Prompt Contract**（`kss-prompt` JSON 块），可喂给任意生图模型 |
| **视觉硬约束** | 1:1 方图、透明背景 PNG、文字烧录进画面、画风遵循角色档案（默认手绘绘本 × 日系萌系）、无水印、无商标 |
| **合规通用** | MIT 许可；仓库**不含任何官方版权图片**（详见 `NOTICE.md`） |

## 快速开始 (Quick Start)

1. 获取本仓库：

   ```bash
   git clone https://github.com/anjiexu425-alt/kawaii-sticker-skill
   ```

2. 按你的宿主安装（详见 [adapters/](adapters/)）：

   | 宿主 | 安装位置 |
   |---|---|
   | Claude Code | `~/.claude/skills/kawaii-sticker-skill/` |
   | Codex | `~/.codex/skills/kawaii-sticker-skill/` |
   | DeepSeek Harness | `agent-presets/<preset>/skills/kawaii-sticker-skill/` |

3. 在会话中直接使用（无需额外配置）：

   - 单句模式：`帮我给“我真的会谢”生成 3 张可爱贴纸`
   - 主题模式：`帮我按“打工人”出一套 6 张表情包`
   - 验证生效：输入一句**模糊请求**（如「帮胖墩做表情包」），若助手**先询问模式**（单句 3 张 / 主题 6 张）再产出，说明技能已正确加载并遵循模式确认规则。

## 使用示例 (Usage Examples)

见 [examples/](examples/)：

| 示例 | 文件 |
|---|---|
| 单句模式输入（无参考图） | `examples/single-line/input.md` |
| 单句模式输出：3 张同文案候选 | `examples/single-line/output-3-candidates.md` |
| 单句模式输入（带 1 张参考图） | `examples/single-line/input-with-reference.md` |
| 单句模式输出：参考图锁定角色 | `examples/single-line/output-with-reference.md` |
| 主题模式输入（打工人） | `examples/theme/input.md` |
| 主题模式输出：1 套 6 张 | `examples/theme/output-6-pack.md` |

输出形态（无原生工具时，路径 ②）是一个 `kss-prompt` fenced block，内含 JSON 契约数组，例如：

````markdown
```kss-prompt
[
  {
    "format_version": "1.0",
    "mode": "single_line",
    "character": { "source": "profile", "feature_map": { "head_shape": "圆润", "...": "..." } },
    "style_anchor": "手绘绘本 × 日系萌系 (hand-drawn picture-book × Japanese kawaii: soft pencil/light linework, gentle hand-drawn texture, fine fluffy fur, soft low-saturation palette)",
    "expression": "委屈巴巴",
    "pose_action": "蹲在角落画圈圈",
    "composition": "居中全身特写，配手绘虚线框",
    "sticker_elements": ["星星", "小花"],
    "text": { "content": "我真的会谢", "verbatim": true, "typography": { "style": "圆体加粗" } },
    "output": { "format": "png", "background": "transparent", "aspect_ratio": "1:1", "text_baked": true },
    "review_flags": { "verbatim_preserved": true, "transparent": true, "square_1to1": true }
  }
]
```
````

完整字段规范见 [docs/PROMPT_CONTRACT.md](docs/PROMPT_CONTRACT.md)；跨模型翻译提示词见 [adapters/generic-prompt.md](adapters/generic-prompt.md)。

## 仓库结构 (Repository Structure)

```
kawaii-sticker-skill/
├── SKILL.md                     # 技能入口指令（frontmatter: name + description）
├── README.md                    # 本文件
├── LICENSE                      # MIT
├── NOTICE.md                    # 第三方 IP 声明（不含官方素材）
├── .github/workflows/ci.yml     # CI：运行测试套件
├── docs/                        # SPEC · PROMPT_CONTRACT · STRUCTURE
│   ├── SPEC.md                  #   权威规格说明书
│   ├── PROMPT_CONTRACT.md       #   机器可校验的提示词契约规范 v1
│   └── STRUCTURE.md             #   目录结构与文件归属
├── character_profiles/          # 文字版角色档案（通用、可扩展）
│   ├── README.md                #   档案使用与新增指南
│   ├── _template.md             #   新增角色模板
│   ├── pangdun.md               #   默认原创角色「胖墩」档案
│   └── pangdun.png              #   胖墩原创参考图（用户自有资产）
├── adapters/                    # 各宿主接入与能力协商
│   ├── README.md                #   能力矩阵
│   ├── claude-code.md
│   ├── codex.md
│   ├── deepseek-harness.md
│   └── generic-prompt.md        #   任意生图模型的翻译指南
├── examples/                    # 示例输入 / 输出
│   ├── README.md                #   示例约定与块格式
│   ├── single-line/             #   单句模式（3 候选）
│   └── theme/                   #   主题模式（6 张套组）
└── tests/                       # 测试（纯 stdlib Python，零依赖）
    ├── validate_structure.py    #   结构 + frontmatter + 无图片二进制校验
    ├── validate_examples.py     #   示例契约的机器校验（文案逐字、数量、一致性）
    ├── run_tests.sh             #   一键运行
    ├── test_checklist.md        #   人工/agent 验收清单
    └── fixtures/                #   样例输入与 feature_map
```

## 测试 (Testing)

```bash
bash tests/run_tests.sh
```

- **零依赖**：纯 Python 3 标准库。
- 校验内容：必需文件齐全、`SKILL.md` frontmatter 合法、仓库无图片二进制；示例契约的文案逐字相等（单句模式 3 张相同）、主题模式 6 张文案/情绪互异、全部契约字段完整且风格/角色一致。
- CI（`.github/workflows/ci.yml`）会在每次 push/PR 自动运行。

## 文档索引 (Docs)

| 文档 | 内容 |
|---|---|
| [docs/SPEC.md](docs/SPEC.md) | 权威规格：模式、流程、角色参考、能力协商、验收标准 |
| [docs/PROMPT_CONTRACT.md](docs/PROMPT_CONTRACT.md) | 提示词契约 v1：字段表、序列化、机器校验规则、完整示例 |
| [docs/STRUCTURE.md](docs/STRUCTURE.md) | 目录结构与文件归属 |

## 许可与知识产权 (License & IP)

- 代码与文档：**MIT License**（见 [LICENSE](LICENSE)）。
- 本仓库**不含**任何第三方受版权保护的官方角色图片、Logo、商标、水印；默认角色「胖墩」为**用户原创设计**（`character_profiles/pangdun.md` + `pangdun.png`），可公开商用。详见 [NOTICE.md](NOTICE.md)。

## 贡献 (Contributing)

- 新增角色：复制 `character_profiles/_template.md` 填写即可（见 [character_profiles/README.md](character_profiles/README.md)）。
- 新增宿主：在 `adapters/` 增加一个 `.md` 并更新能力矩阵。
- 修改规则：以 `docs/SPEC.md` 为准，保持 `SKILL.md` 与 `docs/PROMPT_CONTRACT.md` 一致，并跑通 `tests/`。
