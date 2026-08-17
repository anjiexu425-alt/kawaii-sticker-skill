# adapters/ — 宿主适配与能力协商 (Host Adapters)

本目录说明各宿主如何安装本技能、以及 `SKILL.md` §2.3「能力协商」在各宿主的落点。规则本体以 `SKILL.md` / `docs/SPEC.md` §5 为准；机器校验以 `docs/PROMPT_CONTRACT.md` 为准。

## 能力矩阵 (Capability Matrix)

| 宿主 | 技能安装位置 | 原生生图工具（默认） | 推荐路径 | 文档 |
|---|---|---|---|---|
| Anthropic Claude Code | `~/.claude/skills/kawaii-sticker-skill/` | 通常无（可经 MCP 注入） | 路径 ② 契约输出 | [claude-code.md](claude-code.md) |
| OpenAI Codex | `~/.codex/skills/kawaii-sticker-skill/` | 视环境（OpenAI Images API） | 路径 ① / ② | [codex.md](codex.md) |
| DeepSeek Harness | `agent-presets/<preset>/skills/kawaii-sticker-skill/` | 视会话注册的工具 | 路径 ① / ② | [deepseek-harness.md](deepseek-harness.md) |
| 任意生图模型 | — | — | 路径 ② → 翻译为提示词 | [generic-prompt.md](generic-prompt.md) |

## 通用原则（SKILL.md §2.3）

- 检测到宿主有**原生图像生成工具** → 路径 ①：把契约字段内联为自然语言提示词直接调用，**不额外输出契约块**（双路径禁止）。
- 无原生工具（或调用失败降级）→ 路径 ②：输出**恰好一个** `kss-prompt` fenced code block，块内为符合 `docs/PROMPT_CONTRACT.md` 的 JSON 契约（单行模式 3 对象、主题模式 6 对象）。
- **绝不声称宿主不存在的工具**；没有任何生图能力时如实告知，不伪造图片。
