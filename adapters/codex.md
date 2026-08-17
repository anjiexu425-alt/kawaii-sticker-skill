# Adapter — OpenAI Codex

> 对应 SPEC §5「生图能力协商」的宿主适配。接入与协商见本文件；规则本体见 `SKILL.md`；机器校验见 `docs/PROMPT_CONTRACT.md`。

## 1. 安装 (Install)

```bash
git clone <repo-url> kawaii-sticker-skill
mkdir -p ~/.codex/skills
cp -r kawaii-sticker-skill ~/.codex/skills/kawaii-sticker-skill
```

- 团队共享时，也可放到项目内 `.codex/skills/kawaii-sticker-skill/`。
- `SKILL.md` 的 frontmatter（`name` + `description`）是技能发现与触发判定的元数据，**不要改动**。

## 2. 能力协商 (Capability Table)

| 能力 | Codex 默认 | 说明 |
|---|---|---|
| 原生生图工具 | 视环境 | 若会话具备 OpenAI Images API（`gpt-image-1` 等）调用能力，按 SKILL.md §2.3 检测后走**路径 ①** |
| 图像理解（参考图） | ✅ | 支持图片附件 → `feature_map` 提取（SKILL.md §6.1） |
| 契约输出（路径 ②） | ✅ | 无生图能力时输出 `kss-prompt` 契约块（默认兜底） |

## 3. 路径 ① 调用要点（Images API）

- 将每个契约对象的字段**内联**为自然语言提示词：角色 `feature_map` 全字段 → 风格锚点 `style_anchor` → 该张的 `expression` / `pose_action` / `composition` / `sticker_elements` → **逐字文案** `text.content`（要求恰好出现一次）→ 输出硬约束（1:1、PNG、透明背景、文字烧录、无水印）。
- 单行模式：3 张各调一次（同一 `feature_map` / `style_anchor` / 文案）；主题模式：6 张各调一次（文案互异、风格统一）。
- 透明背景：优先选择支持 alpha 输出的模型参数；不支持时用纯色底生成后去底（见 [generic-prompt.md](generic-prompt.md) §2 后处理）。
- 原生工具存在但调用失败 → 重试 1 次 → 仍失败自动降级路径 ②（SKILL.md §2.3-4）。

## 4. 注意事项

- 不输出伪造图片；无任何生图能力时如实告知并输出契约块。
- 参考图必须为用户合法拥有的图片（SKILL.md §9 / `NOTICE.md`）。
