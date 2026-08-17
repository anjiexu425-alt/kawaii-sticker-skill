# character_profiles/ — 文字版角色档案 (Character Profiles)

角色档案是**纯文字**的角色特征描述（Markdown，**无图片素材**），用于用户没有参考图时的角色锁定兜底（SPEC §4.2–§4.3 / SKILL.md §6.3）。本仓库是**通用**的：新增角色只需新增一个 `.md`，无需改任何代码。

## 现有档案

| 档案 | 说明 |
|---|---|
| `pangdun.md` | **默认原创角色**「胖墩」：文字档案 + 用户原创参考图 `pangdun.png`（可公开商用） |
| `my-melody.md` | 美乐蒂手绘 / 手帐风**文字风格示例**（非默认、非官方素材，见 `NOTICE.md`） |
| `_template.md` | 新增角色的填空模板 |

## 如何使用（助手侧）

无参考图时，助手按 SKILL.md §2.2 选择档案：用户指定档案名 > 默认档案（`pangdun.md`，原创角色「胖墩」）> 仓库首个可用档案；随后把档案解析为 `character.feature_map`（结构见 `docs/PROMPT_CONTRACT.md` §3.1），并在本次运行内**锁定**。

## 如何新增角色

1. 复制 `_template.md` 为 `character_profiles/<角色名>.md`。
2. 填写：角色概述、视觉特征表、贴纸化建议、`feature_map` 对照表。
3. 必填字段：`head_shape` / `ears` / `eyes` / `nose_mouth` / `palette` / `signature_accessories`；其余（`body_proportions` / `personality_keywords` / `texture` / `derivation_notes`）推荐填写。
4. 规则：
   - **文字为主**：档案必须含文字描述；**用户原创**参考图（如 `pangdun.png`）可放在本目录（仓库图片白名单，`tests/` 校验例外）。
   - **不侵权**：不得使用受版权保护的官方形象、商标、Logo 及其图片素材（`NOTICE.md`）；第三方风格仅可作文字描述参考。
   - 与 `docs/PROMPT_CONTRACT.md` §3.1 字段保持一致，保证机器可解析。
