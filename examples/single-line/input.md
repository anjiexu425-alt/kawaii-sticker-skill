# 单行模式输入示例（无参考图）：一句原样文案

<!-- input: 我真的会谢 -->

> 本文件是**机器可读的输入声明**：`<!-- input: ... -->` 标记中的内容即本次运行的用户输入原文（约定见 `examples/README.md` §3）。校验器须断言：输出契约中所有 `text.content` 与该标记**逐字、字节级相等**（PROMPT_CONTRACT §4 规则 5/10）。

## 用户请求 (User Request)

> 帮我做贴纸：**「我真的会谢」**

用户只给了一句原样文案，**没有上传任何参考图**。

## 运行前解析（本示例的判定过程）

1. **模式判定 → 单行模式（single_line）**
   - 用户输入是被引号包裹的一句短口语话术 → 按 SPEC §3.1 优先级 1 判定为单行模式。
   - 判定依据写入契约 `mode: "single_line"`。
2. **角色解析 → 无参考图 → 回退角色档案（profile fallback）**
   - 用户未提供参考图 → 按 SPEC §4.2 加载 `character_profiles/pangdun.md`（本技能默认原创档案「胖墩」）。
   - 档案为纯文字（不含任何官方素材）；由档案解析出 `feature_map`，`character.source = "profile"`。
   - 角色在本次运行内**锁定（locked）**：3 张候选共享同一份 `feature_map`。
3. **文案锁定 → 逐字保留（verbatim）**
   - 「我真的会谢」原样存为 `text.content`，`text.verbatim = true`；此后**任何环节不得增删改一个字符**（SPEC §3.2-1）。
4. **能力协商 → 路径 ②（契约输出）**
   - 本示例假设宿主**无原生生图工具** → 输出一个 `kss-prompt` 块（见 `output-3-candidates.md`），块内为 3 个契约对象的数组（SPEC §5.3）。

## 校验要点 (Validator Notes)

- [ ] 机器标记 `<!-- input: 我真的会谢 -->` 存在且可解析。
- [ ] 对应输出文件 `output-3-candidates.md` 的 `kss-prompt` 块解析为**长度恰为 3 的数组**。
- [ ] 3 个对象的 `text.content` 全部与「我真的会谢」**逐字相等**；`text.verbatim` 全部为 `true`。
- [ ] 3 个对象的 `character.source` 全部为 `"profile"`；`feature_map` 深比较完全相同（同档案、同锁定）。
