# Adapter — DeepSeek Harness

> 对应 SPEC §5「生图能力协商」的宿主适配。接入与协商见本文件；规则本体见 `SKILL.md`；机器校验见 `docs/PROMPT_CONTRACT.md`。

## 1. Skill 目录约定（已核实 Harness 实现）

DeepSeek Harness 通过 **agent-presets** 组合条目发现技能，每个技能目录约定为：

```
<agent-presets 根>/<preset>/skills/<skill-name>/SKILL.md
```

- **内置 preset**：随 Harness 安装自带，如 `<dsh-install>/config/agent-presets/<preset>/skills/`（已内置 cordis 等 preset 的技能，如 `cordis-plugin-development`）。
- **用户级**：Harness 的 profile 通过 `cordis.patch.yml`（`$DSH_HOME/cordis.patch.yml` 或 profile 目录）以补丁层组合 `agent-presets` 条目；把技能目录放进对应 preset 的 `skills/` 下即可被技能目录发现与加载。
- `SKILL.md` 的 YAML frontmatter（`name` + `description`）即技能的**发现与触发元数据**，保持原样。

安装示例（以用户 preset 为例，路径以你的 profile 布局为准）：

```bash
git clone <repo-url> kawaii-sticker-skill
mkdir -p ~/.config/dsh/agent-presets/<preset>/skills
cp -r kawaii-sticker-skill ~/.config/dsh/agent-presets/<preset>/skills/kawaii-sticker-skill
```

## 2. 能力协商 (Capability Table)

| 能力 | Harness 默认 | 说明 |
|---|---|---|
| 原生生图工具 | 视会话注册的工具 | 用 SKILL.md §2.3 正则检测会话工具列表，有则**路径 ①** |
| 图像理解（参考图） | ✅ | 可解析用户上传的 1–3 张参考图 → `feature_map`（SKILL.md §6.1） |
| 契约输出（路径 ②） | ✅ | 无生图工具时输出 `kss-prompt` 契约块（默认兜底） |

## 3. 验证

新会话中触发：`帮我按“打工人”出一套 6 张可爱贴纸`，应得到 6 个契约对象的 `kss-prompt` 块（或原生工具调用，取决于会话工具）。

## 4. 注意事项

- 参考图必须为用户合法拥有的图片（SKILL.md §9 / `NOTICE.md`）。
- 技能目录名与 `SKILL.md` 中 `name` 建议保持一致（`kawaii-sticker-skill`），便于目录间切换与多 preset 复用。
