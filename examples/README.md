# Examples — 示例总览与块格式约定 (Conventions)

> 本目录是 **Prompt Contract v1 的示例集**：展示两种模式（单行 / 主题）在「宿主**没有**原生生图工具」时的标准输出形态。权威字段表与机器校验规则见 `docs/PROMPT_CONTRACT.md`；本文件只约定示例文件的**组织方式**与**块的精确格式**，使解析器（parser）能够读取、校验示例。

| 元数据 | 值 |
|---|---|
| 文档 | `examples/README.md` |
| 对应规格 | `docs/SPEC.md` §6 / `docs/PROMPT_CONTRACT.md` §1–§4 |
| 语言 | 中文为主，英文术语为辅（English keywords） |
| 验收入口 | SPEC M5（示例契约全部通过 §6.3 机器校验） |

## 1. 目录导航 (Index)

| 文件 | 内容 | 角色来源 |
|---|---|---|
| `single-line/input.md` | 单行模式输入：「我真的会谢」，**无参考图** | profile 回退（`character_profiles/my-melody.md`） |
| `single-line/output-3-candidates.md` | 单行模式输出：**1 个 `kss-prompt` 块**，内含 **3 个契约对象** | `source: "profile"` |
| `single-line/input-with-reference.md` | 单行模式输入：「我真的会谢」+ **1 张参考图**（文字描述，不嵌图） | image 特征图管线 |
| `single-line/output-with-reference.md` | 单行模式输出：3 个契约对象，`feature_map` 由参考图推导 | `source: "image"` |
| `theme/input.md` | 主题模式输入：「打工人」+ 1 张参考图（文字描述） | image 特征图管线 |
| `theme/output-6-pack.md` | 主题模式输出：1 个 `kss-prompt` 块，内含 **6 个契约对象** | `source: "image"` |

> 角色来源两种形态（`profile` / `image`）与两种模式（`single_line` / `theme`）在此示例集中均有覆盖；仓库中的示例契约**不含任何官方素材**（SPEC §1.3 / NOTICE.md）。

## 2. 输出块精确格式 (Exact Block Format)

每次运行（一次用户请求）在契约路径下输出**恰好一个** fenced code block——这就是本目录所说的 **STANDARDIZED PROMPT BLOCK**：

````text
```kss-prompt
<JSON 内容>
```
````

解析器（parser）按以下规则读取，**全部可机器校验（machine-checkable）**：

1. **块定位**：起始行精确为 `` ```kss-prompt ``（info string 固定为 `kss-prompt`，正则 `` ^```kss-prompt$ ``）；闭合行精确为 `` ``` ``（正则 `` ^```$ ``）。块外的一切自然语言说明**不是**机器输出。
2. **块内内容**：严格 JSON（RFC 8259），`JSON.parse` 必须成功。块内**不允许**注释、尾逗号、非 JSON 内容。
3. **聚合形态**：
   - 单行模式（`mode: "single_line"`）→ JSON **数组**，长度**恰好为 3**，每个元素是一个契约对象（对应 1 张贴纸）。
   - 主题模式（`mode: "theme"`）→ JSON **数组**，长度**恰好为 6**。
   - 数组长度与 `mode` 不符 → 校验失败（PROMPT_CONTRACT §4 规则 3）。
4. **对象字段**：每个契约对象携带完整字段集（✅ 必填，⭕ 可选）：
   - `format_version`（const `"1.0"`）、`mode`（enum `single_line`|`theme`）
   - `character.source`（enum `image`|`profile`）、`character.feature_map`（SPEC §4.3 字段集）
   - `style_anchor`、`expression`、`pose_action`、`composition`（string）
   - `sticker_elements`（⭕ array of string）
   - `text.content`、`text.verbatim`（boolean）、`text.typography`（⭕ object）
   - `output.format`（const `"png"`）、`output.background`（const `"transparent"`）、`output.aspect_ratio`（const `"1:1"`）、`output.text_baked`（const `true`）
   - `review_flags`（⭕ object of boolean，字段名 ∈ SPEC §8.1 合法集合）
5. **同一次运行的一致性（deep-compare）**：数组内所有对象的 `format_version`、`style_anchor`、`character.feature_map`、`output.*` 必须**完全相同**（SPEC §6.3 规则 5）。
6. **模式内约束**：
   - `single_line`：`text.verbatim === true`；`text.content` 与用户输入**逐字相等**；3 个对象的 `expression`、`pose_action`、`composition` **两两不同**（`sticker_elements` 建议不同）。
   - `theme`：6 个 `text.content` **两两不同**；6 个对象的 `expression`/`pose_action`/`composition` 组合**两两不同**。

## 3. 输入文件的机器约定 (Input Marker Convention)

为使校验器能核对「`text.content` 与用户输入逐字相等」（PROMPT_CONTRACT §4 规则 5/10），每个 `input*.md` 文件在开头声明一条**机器可读标记**：

```html
<!-- input: 我真的会谢 -->
```

- 解析规则：匹配 `<!-- input: (.*) -->`，捕获内容即为本次运行的用户输入原文。
- 单行模式：该内容必须与输出契约中所有 `text.content` **逐字、字节级相等**（含标点、空格）。
- 主题模式：该内容为**主题词**，输出契约的 6 句文案由助手自拟，不要求与主题词相等，但必须两两不同。

有参考图时，输入文件另加一条标记声明图片数量与文字描述（不嵌入真实图片）：

```html
<!-- reference: 1, text-described (详见正文描述，不嵌入图片) -->
```

## 4. 校验要点 (Validator Notes)

- 对每个 `output*.md`：**只**解析 `kss-prompt` 块 → `JSON.parse` → 按 §2 规则 4–6 逐项断言；任何一项不满足即失败。
- `review_flags` 若存在：字段名 ∈ `{verbatim_preserved, text_baked, transparent, square_1to1, readable_at_small, no_watermark, no_trademark}`，值均为 boolean；布尔真实性由人工/视觉检查兜底（SPEC §8.2）。
- 示例契约全部预期 **通过** 校验；它们是 `tests/validate_examples.py`（tests 阶段）的黄金样本（golden fixtures）。

## 5. 阅读顺序 (Reading Order)

1. 先读两种 `input*.md`，理解模式判定与角色来源；
2. 再读对应 `output*.md`，对照 `docs/PROMPT_CONTRACT.md` §5/§6 的完整示例核对格式；
3. 对比 `output-3-candidates.md` 与 `output-with-reference.md` 的 `feature_map`，观察「档案推导」与「参考图推导」的差异（SPEC §4.2 vs §4.1）。
