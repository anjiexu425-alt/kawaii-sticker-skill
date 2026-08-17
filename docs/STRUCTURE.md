# Kawaii Sticker Skill — 仓库结构说明 (STRUCTURE)

> 本文件是仓库的**结构地图（structure map）**：说明每个目录与文件的职责、以及由哪个阶段（phase）负责产出。**内容层面的权威规格是 `docs/SPEC.md`**；本文件只管辖「文件放哪里、由谁写」。布局（layout）冲突以本文件为准，内容（content）冲突以 SPEC.md 为准。

| 元数据 | 值 |
|---|---|
| 文档 | `docs/STRUCTURE.md` |
| 版本 | 1.0（Phase: repo-structure） |
| 状态 | 生效（authoritative for layout） |
| 语言 | 中文为主，英文术语为辅（English keywords） |
| 适用范围 | 仓库布局、目录职责、各阶段产出物所有权 |

## 目录 (TOC)

1. [目标目录树](#1-目标目录树)
2. [目录职责速览](#2-目录职责速览)
3. [阶段所有权表](#3-阶段所有权表)
4. [约定与规则](#4-约定与规则)
5. [与 SPEC 的关系](#5-与-spec-的关系)

---

## 1. 目标目录树

> 图例：`【主流程】` = 主流程阶段拥有（定稿或 WIP 占位，勿改）；`【spec】` = 已完成；`【本阶段】` = repo-structure；其余为后续阶段。每个文件后为该文件的**一行职责说明**。

```text
Kawaii Sticker Skill/
├── SKILL.md
│       助手入口指令：YAML frontmatter（name/description）+ 双模式流程实现（SPEC §3–§5）【skill】
├── README.md
│       项目总览：安装 / 使用 / 两种模式 / IP 声明入口（当前为 WIP 占位，最终版由主流程写入）【主流程】
├── LICENSE
│       MIT 许可证（已存在，勿改）【主流程】
├── NOTICE.md
│       第三方 IP 声明：不含官方素材、参考图权利责任边界（已存在，勿改）【主流程】
├── .gitignore
│       忽略规则：Python / OS / 编辑器产物（已存在，勿改）【主流程】
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       │        CI：push/PR 时执行 bash tests/run_tests.sh，退出码须为 0（SPEC M8；已存在，勿改）【主流程】
│       └── .gitkeep
│               占位：保证目录被 git 跟踪【本阶段】
│
├── docs/
│   ├── SPEC.md
│   │        权威规格：模式 / 用户流程 / 特征图 / 能力协商 / 契约字段 / 硬约束 / 验收标准（已存在）【spec】
│   ├── PROMPT_CONTRACT.md
│   │        Prompt Contract v1 详解：字段表、最小示例、机器校验规范（SPEC §6 的展开）【prompt-contract】
│   ├── STRUCTURE.md
│   │        本文件：仓库结构地图与阶段所有权【repo-structure / 本阶段】
│   └── .gitkeep
│           占位【本阶段】
│
├── character_profiles/
│   ├── README.md
│   │        档案目录说明：如何新增角色档案、档案选择规则（SPEC §4.2）【characters】
│   ├── _template.md
│   │        角色档案模板：按 SPEC §4.3 特征图字段设计的可填写模板【characters】
│   ├── pangdun.md
│   │        默认原创角色档案：胖墩（手绘绘本 × 日系萌系画风）；可公开商用（SPEC §4.2）【characters】
│   ├── pangdun.png
│   │        胖墩用户原创参考图（用户自有资产；仓库图片白名单仅限本目录）【characters】
│   └── .gitkeep
│           占位【本阶段】
│
├── adapters/
│   ├── README.md
│   │        适配器总览：各宿主能力协商表导航（当前为 WIP 占位，最终版由主流程写入）【主流程】
│   ├── claude-code.md
│   │        Anthropic Claude Code 宿主：能力检测表 + 接入与回退说明【adapters】
│   ├── codex.md
│   │        OpenAI Codex 宿主：能力检测表 + 接入与回退说明【adapters】
│   ├── deepseek-harness.md
│   │        DeepSeek Harness 宿主：能力检测表 + 接入与回退说明【adapters】
│   ├── generic-prompt.md
│   │        通用路径：如何将 Prompt Contract 交给任意生图能力（SPEC §5.3 路径 ②）【adapters】
│   └── .gitkeep
│           占位【本阶段】
│
├── examples/
│   ├── README.md
│   │        示例总览：两种模式的输入 / 输出示例导航与阅读顺序【examples】
│   ├── single-line/
│   │   ├── input.md
│   │   │        单行模式输入示例：一句须原样保留的文案（如「我真的会谢」，无参考图）【examples】
│   │   ├── input-with-reference.md
│   │   │        单行模式输入示例（带参考图）：原样文案 + 1 张参考图的文字描述（SPEC §4.1 特征图管线）【examples】
│   │   ├── output-3-candidates.md
│   │   │        单行模式输出示例（无参考图）：3 张同文案候选 + 3 份合法契约（须通过 SPEC §6.3 校验，M5）【examples】
│   │   ├── output-with-reference.md
│   │   │        单行模式输出示例（带参考图）：3 张同文案候选 + 由参考图推导 feature_map 的 3 份契约【examples】
│   │   └── .gitkeep
│   │           占位【本阶段】
│   └── theme/
│       ├── input.md
│       │        主题模式输入示例：一个主题词（如「打工人」）+ 1 张参考图的文字描述【examples】
│       ├── output-6-pack.md
│       │        主题模式输出示例：6 张一套 + 6 份合法契约（须通过 SPEC §6.3 校验，M5）【examples】
│       └── .gitkeep
│             占位【本阶段】
│
└── tests/
    ├── README.md
    │        测试总览：运行方式、校验器清单、与 SPEC §8.1 的对应关系【tests】
    ├── run_tests.sh
    │        测试入口脚本：CI 直接调用（SPEC M8），全部通过则退出码 0【tests】
    ├── validate_structure.py
    │        结构校验器：SPEC M1–M4（frontmatter 存在性 / 必需文件 / 档案纯文字 / 无官方素材）【tests】
    ├── validate_examples.py
    │        契约校验器：按 SPEC §6.3 规则 1–6 校验 examples/ 契约（SPEC M5–M6）【tests】
    ├── test_checklist.md
    │        人工检查清单：SPEC §8.2 落地为可勾选步骤（面向每套生成的贴纸）【tests】
    └── fixtures/
        ├── .gitkeep
        │       占位【本阶段】
        └── （原创测试夹具：契约样本 / 示例图，必须为原创，SPEC M4 / §7 🔧 可机检项）【tests】
```

## 2. 目录职责速览

| 目录 | 职责 | 阶段 |
|---|---|---|
| 仓库根 `/` | 入口与元数据：`SKILL.md`、`README.md`、`LICENSE`、`NOTICE.md`、`.gitignore` | 各阶段（见 §3） |
| `.github/workflows/` | CI 流水线：调用 `bash tests/run_tests.sh` | 主流程（已存在） |
| `docs/` | 规格类文档：SPEC（权威）、PROMPT_CONTRACT、STRUCTURE | spec + 后续 |
| `character_profiles/` | 文字版角色档案：通用、可扩展（新增角色 = 新增一个 `.md`） | characters |
| `adapters/` | 各宿主能力协商表与接入说明（对应 SPEC §5.1 检测规则） | 主流程(README) + adapters |
| `examples/` | 两种模式的输入 / 输出示例（契约须通过 §6.3 校验） | examples |
| `tests/` | 可运行校验器 + 原创 fixtures + 人工检查清单（实现 SPEC §8.1） | tests |

## 3. 阶段所有权表

| 阶段 phase | 产出文件 |
|---|---|
| main（主流程，已定稿） | `README.md`、`LICENSE`、`NOTICE.md`、`.gitignore`、`.github/workflows/ci.yml`、`adapters/README.md`（已定稿；任何阶段勿改） |
| spec（已完成） | `docs/SPEC.md` |
| repo-structure（本阶段） | `docs/STRUCTURE.md`、各目录 `.gitkeep` 占位 |
| skill | `SKILL.md` |
| prompt-contract | `docs/PROMPT_CONTRACT.md` |
| characters | `character_profiles/README.md`、`character_profiles/_template.md`、`character_profiles/pangdun.md`、`character_profiles/pangdun.png`（用户原创） |
| adapters | `adapters/claude-code.md`、`adapters/codex.md`、`adapters/deepseek-harness.md`、`adapters/generic-prompt.md` |
| examples | `examples/README.md`、`examples/single-line/input.md`、`examples/single-line/input-with-reference.md`、`examples/single-line/output-3-candidates.md`、`examples/single-line/output-with-reference.md`、`examples/theme/input.md`、`examples/theme/output-6-pack.md` |
| tests | `tests/README.md`、`tests/run_tests.sh`、`tests/validate_structure.py`、`tests/validate_examples.py`、`tests/test_checklist.md`、`tests/fixtures/` 内容 |

## 4. 约定与规则

1. **`.gitkeep` 仅作占位**：保证空目录进入 git；对应目录写入正式文件后即可删除，无需保留。
2. **主流程文件不可改**：§3 中 main 阶段拥有的文件任何阶段不得修改；如确需变更，先与主流程协商，并同步回改 SPEC / STRUCTURE。
3. **地图与仓库必须一致**：新增、重命名或删除任何文件/目录 → 同步更新本文件；`tests/validate_structure.py` 将按本文件与 SPEC §8.1 检查关键文件存在性。
4. **内容冲突仲裁**：`docs/SPEC.md` 是内容层面唯一仲裁源（SPEC §10）；本文件只仲裁布局与所有权。
5. **资产纪律**：所有新增文件须为 UTF-8 纯文本；仓库不引入任何官方 / 第三方图片素材（SPEC §1.3、NOTICE.md）；`tests/fixtures/` 内图片必须为原创。
6. **阶段顺序依赖**：`SKILL.md`（skill）引用 `docs/PROMPT_CONTRACT.md` 与 `character_profiles/`；`examples/` 与 `tests/` 依赖契约文档定稿；CI（`ci.yml`）依赖 `tests/run_tests.sh` 落地后转绿。

## 5. 与 SPEC 的关系

- **内容权威**：`docs/SPEC.md` —— 决定「做什么、怎么做、算不算合格」。
- **布局权威**：本文件 —— 决定「文件放哪里、由谁写」。
- **冲突处理**：先改 SPEC，再同步本文件与实现（SPEC §10 变更规则）；本文件自身变更遵循 §4-3。
