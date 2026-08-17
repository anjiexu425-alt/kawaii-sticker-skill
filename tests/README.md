# Tests — 测试总览 (Test Suite)

> 本目录实现 SPEC §8.1 的**机器可测验收项（M1–M8）**：结构校验器（`validate_structure.py`）、示例契约校验器（`validate_examples.py`）、人工检查清单（`test_checklist.md`）与可运行 fixtures。CI 入口为 `bash tests/run_tests.sh`（SPEC M8 / `.github/workflows/ci.yml`）。

| 元数据 | 值 |
|---|---|
| 文档 | `tests/README.md` |
| 对应规格 | SPEC §8.1（M1–M8）/ PROMPT_CONTRACT §4 / examples/README.md |
| 运行环境 | Python 3（**stdlib only，无任何第三方依赖**）+ bash |
| 语言 | 中文为主，英文术语为辅 |

## 1. 如何运行 (How to Run)

从**仓库根目录**执行（不需要安装任何第三方包）：

```bash
bash tests/run_tests.sh          # 一键运行全部（CI 同款入口）
# 或逐个运行：
python3 tests/validate_structure.py   # 结构校验（SPEC M1–M4）
python3 tests/validate_examples.py    # 示例契约校验（SPEC M5–M6）
```

要求：`python3` ≥ 3.8（仅用标准库；CI 使用 3.12）；`bash` 可用。Windows 用户可用 Git Bash / WSL 运行 `run_tests.sh`，或直接用 `python3` 运行两个校验器。

## 2. 校验器清单 (Validator List)

### 2.1 `validate_structure.py` — 结构校验（SPEC M1–M4）

| 检查 | 说明 | SPEC |
|---|---|---|
| 必需文件存在 | 20 个关键文件（入口、文档、档案、示例、本测试）逐一存在 | M1/M2/M3 |
| SKILL.md frontmatter | 以 `---` 开头，块内含 `name` 与**非空** `description`（纯字符串解析，无 YAML 库） | M1 |
| 仓库无图片二进制 | 全树遍历：任何 `.png/.jpg/.jpeg/.gif/.webp/.bmp/.svg` 文件即失败 | M3/M4 |

### 2.2 `validate_examples.py` — 示例契约校验（SPEC M5–M6）

按 `examples/README.md` §2（块格式）与 §3（输入标记）解析，按 `docs/PROMPT_CONTRACT.md` §4 规则 1–9 校验：

| 检查 | 说明 |
|---|---|
| 块定位 | 每个 `output*.md` **恰好一个** `` ```kss-prompt `` 块（起始 `` ^```kss-prompt$ ``、闭合 `` ^```$ ``） |
| JSON 可解析 | 块内容 `JSON.parse` 成功，顶层为数组 |
| 数量 | 数组长度：`single_line` = 3，`theme` = 6 |
| 必填字段 | 每块含 `format_version`/`mode`/`character.feature_map`/`style_anchor`/`expression`/`pose_action`/`composition`/`sticker_elements`/`text`/`output` |
| enum/const | `format_version=="1.0"`；`mode` 与文件匹配；`character.source∈{image,profile}`；`output.format=="png"`、`background=="transparent"`、`aspect_ratio=="1:1"`、`text_baked==true`（区分大小写） |
| feature_map | 身份字段（head_shape/ears/eyes/nose_mouth/palette/signature_accessories）齐全且类型正确 |
| 文案逐字 | `single_line`：每块 `text.content` 与输入标记 `<!-- input: ... -->` **字节级相等**（标记须为「我真的会谢」），`verbatim===true` |
| 区分度 | `single_line`：expression/pose_action/composition 两两不同；`theme`：6 句文案两两不同、expression 两两不同、三元组两两不同 |
| 运行内一致性 | 同一文件内所有块共享同一 `style_anchor`、同一 `feature_map`（深比较）、同一 `output`、同一 `format_version` |
| review_flags | 字段名 ∈ SPEC §8.1 合法集合，值均为 boolean |

### 2.3 `test_checklist.md` — 人工/代理验收清单（SPEC §8.2）

面向每套**实际生成**的贴纸的勾选清单：两种模式、有/无参考图、原生工具路径 vs 契约路径、SKILL.md §5 全部视觉硬约束、交付与合规。由人（或运行技能的助手）逐项勾选。

## 3. Fixtures（原创测试夹具）

| 文件 | 内容 | 用途 |
|---|---|---|
| `fixtures/single_line_input.txt` | `我真的会谢`（单行模式输入） | 单行模式手动复现的标准输入 |
| `fixtures/theme_input.txt` | `打工人`（主题模式输入） | 主题模式手动复现的标准输入 |
| `fixtures/sample_feature_map.json` | 合法 feature_map 示例（字段符合 PROMPT_CONTRACT §3.1） | 契约/提示词构建的参考样本 |

全部为**原创文本/JSON**，不含任何官方图片素材（SPEC M4 / NOTICE.md）。

## 4. 退出码 (Exit Codes)

| 程序 | 退出码 | 含义 |
|---|---|---|
| `validate_structure.py` | 0 | 全部通过 |
| | 1 | 任一检查失败（并打印对应 `FAIL:` 行） |
| `validate_examples.py` | 0 | 全部通过 |
| | 1 | 任一检查失败（并打印对应 `FAIL:` 行） |
| `run_tests.sh` | 0 | 两个校验器均通过（`ALL TESTS PASSED`） |
| | 1 | 任一校验器失败（`SOME TESTS FAILED`） |

CI（`.github/workflows/ci.yml`）直接调用 `bash tests/run_tests.sh`，退出码须为 0（SPEC M8）。
