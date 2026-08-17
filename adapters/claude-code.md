# Adapter — Anthropic Claude Code

> 对应 SPEC §5「生图能力协商」的宿主适配。接入与协商见本文件；规则本体见 `SKILL.md`；机器校验见 `docs/PROMPT_CONTRACT.md`。

## 1. 安装 (Install)

```bash
git clone https://github.com/anjiexu425-alt/kawaii-sticker-skill
mkdir -p ~/.claude/skills
cp -r kawaii-sticker-skill ~/.claude/skills/kawaii-sticker-skill
```

- 团队共享时，也可放到项目内 `.claude/skills/kawaii-sticker-skill/`。
- 目录内必须保留 `SKILL.md`：其 YAML frontmatter（`name` + `description`）是 Claude Code 技能发现与触发判定的元数据，**不要改动**。
- 重启会话后用触发语验证：`帮我给“我真的会谢”生成 3 张可爱贴纸`。

## 2. 能力协商 (Capability Table)

| 能力 | Claude Code 默认 | 说明 |
|---|---|---|
| 原生生图工具 | 通常**无** | Claude Code 默认不内置文生图工具；若通过 MCP 注入生图工具（如 fal / Replicate / 自建 Images MCP），按 SKILL.md §2.3 检测后走**路径 ①** |
| 图像理解（参考图） | ✅ | 用户以附件上传 1–3 张参考图，Claude 直接视觉解析 → 提取 `feature_map`（SKILL.md §6.1） |
| 契约输出（路径 ②） | ✅ | 无生图工具时输出 `kss-prompt` 契约块（本技能在 Claude Code 上的**默认路径**） |

## 3. 使用流程

1. 用户上传参考图（1–3 张）或直接给一句话 / 主题。
2. 按 SKILL.md §2 判定模式 → 角色锁定（参考图 `feature_map` 或 `character_profiles/` 兜底）。
3. 能力协商：未检测到原生图像工具 → **路径 ②**：输出 `kss-prompt` 契约块（3 或 6 个契约对象）。
4. 用户可把契约块交给任意支持该契约的生图能力（见 [generic-prompt.md](generic-prompt.md)）。

## 4. 注意事项

- 参考图必须是用户合法拥有的图片；遵守 SKILL.md §9 与 `NOTICE.md` 合规边界。
- 若用户期望会话内直接出图，建议在 Claude Code 中接入生图 MCP 工具——此时自动切换路径 ①（SKILL.md §2.3-2 双路径禁止，不会重复输出契约块）。
