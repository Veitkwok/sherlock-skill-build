# Skill Purification Methodology

> 从 Python 脚本密集型 skill 提取纯方法论，适配标准化 AI Agent 环境（Hermes/Grok 网页版）。

## 核心原则

提纯目标：保留分析方法论和推理框架，剥离执行层（脚本、自动化、报告生成）。让 AI agent 用自己的推理能力 + 标准工具（MCP/web search/X search）完成分析，输出纯文本/Markdown。

## 提纯层次

### L1 · 文件清理（机械层）

删除而非保留的：

| 删除内容 | 原因 |
|----------|------|
| `scripts/`（所有 Python 文件） | Hermes 用 MCP 工具链，Grok 用 web/X search，均不执行 Python |
| `assets/`（HTML 模板/SVG/PNG） | 输出已改为 Markdown，不需要视觉资产 |
| `run.py`, `requirements.txt` | 无 Python 环境可执行 |
| `personas/`（YAML 数据文件） | LLM 不解析 YAML——需转为 Markdown（见 L2） |
| `plugin.json` | Hermes 不使用 Claude Code plugin 格式 |

保留的：

| 保留内容 | 原因 |
|----------|------|
| `SKILL.md` | 核心方法论（待改写——见 L2） |
| `references/` | 方法论参考文档（LLM 可直接阅读） |
| `LICENSE` | 许可证 |

### L2 · SKILL.md 改写（结构层）

原始 skill 通常专为某个平台设计（如 Claude Code 的多 agent 并行、Python 脚本编排）。改写目标：

1. **移除平台特定指令**：删除所有 `cd scripts && python ...`、`spawn sub-agent`、`Playwright MCP` 等依赖
2. **移除不适用市场的硬性门控**：如 A 股/港股专属协议、中文名纠错、ETF 引导
3. **改为通用工具描述**：把"调用 mcp_longbridge_quote"改为"获取实时股价（用你的平台提供的工具）"
4. **双模式支持**：Hermes 模式（MCP）+ Grok 模式（web+X search）各给数据获取路径
5. **输出格式统一**：HTML → Markdown，删除社交分享卡/战报/PNG 生成指令
6. **收缩投资者集合**：65 人（含 A 股游资）→ 36 人（纯美股）

### L3 · Persona 转换（方法论保留层）

原始 YAML persona 文件是 Python 脚本的输入数据。转换为 LLM 可读的 Markdown 速查表：

**转换逻辑**：
- 从 N 个 YAML 中筛选目标市场相关投资者（如美股只保留 36/65）
- 每个投资者从 40-80 行 YAML 浓缩为 10-15 行 Markdown
- 保留：核心指标、否决条件、语言风格、经典话术、典型持仓、信号倾向
- 删除：Python lambda 表达式、特征字段名、规则引擎配置
- 分组：按投资流派组织（价值派/成长派/宏观/技术/量化/科技领袖）

**输出文件**：`references/investor-frameworks.md`（约 16KB，LLM 一次性读完全部 36 人）

### L4 · 链式整合（系统层）

当多个子 skill 需要串联时（如 x-advanced-research → serenity-skill → deep-analysis），添加显式 handoff 协议：

```markdown
## Integration with {upstream-skill}

When this skill receives input from {upstream-skill}:
- Accept {input format}
- Apply {workflow} to each item
- Output to {downstream-skill}: {output format}
```

无此协议时，chain 依赖 agent 常识——断链风险。

### L5 · 评分/计算转换（代码→方法论）

当 skill 包含 Python 评分脚本 + JSON 模板时，提取公式和权重，转为 agent 直接计算的 Markdown：

**模式识别**：Python 脚本里有 `WEIGHTS = {...}`、`score()` 函数、`verdict` 阈值 → 这是有价值的评分方法论。

**转换步骤**：
1. 从 `.py` 提取：权重表、评分公式、verdict 阈值
2. 从 `.json` 提取：因子定义、扣分项、evidence 结构
3. 合并为一份 `references/<name>-scoring.md`
4. 每个因子附带：0 分 vs 5 分的含义对照（agent 可自行评分）
5. 写明公式（agent 手算或用内置计算能力）
6. 删除 `.py` + `.json` 文件
7. 清理 `scripts/` 空目录

**关键原则**：不是「删掉脚本失去功能」，而是「把脚本里的方法论提炼出来，让 agent 自己执行评分逻辑」。agent 的推理能力 > Python 脚本的机械计算。

## 实战案例：serenity-skill 评分脚本转换

| 指标 | 转换前 | 转换后 |
|------|--------|--------|
| 评分引擎 | `scripts/serenity_scorecard.py` (201 行 Python) | `references/bottleneck-scoring.md` |
| 评分模板 | `assets/bottleneck-scorecard.json` (JSON 占位) | 融入 bottleneck-scoring.md |
| 验证脚本 | `scripts/validate_skill.py` (59 行) | 删除（Hermes 自行校验） |
| 平台配置 | `agents/openai.yaml` | 删除（非通用格式） |
| 文件类型 | 16 .md + 1 LICENSE + 3 .py + 1 .json + 1 .yaml | 16 .md + 1 LICENSE |
| 空目录 | agents/, scripts/ | 无 |

转换要点：Python 的 `WEIGHTS` dict + `score()` 函数 → 8 因子加权表 + 公式 + Verdict 阈值。每个因子附带 0 分 vs 5 分的含义对照，agent 按表手算即可。

## 实战案例：UZI-Skill deep-analysis 提纯

| 指标 | 提纯前 | 提纯后 |
|------|--------|--------|
| 文件数 | ~270（含 198 scripts + 51 personas + 71 assets） | 19（SKILL.md + 18 references） |
| SKILL.md 大小 | 54 KB (1,082 行) | 15 KB (300 行) |
| 投资者覆盖 | 65 人（含 28 A 股/港股） | 36 人（纯美股） |
| Persona 格式 | 51 YAML 文件 | 1 个 investor-frameworks.md |
| 输出格式 | Bloomberg 风格 HTML + 社交分享卡 + 战报 PNG | Markdown 分析报告 |
| 数据获取 | Python fetcher × 22 + Playwright | Hermes MCP / Grok web+X search |
| 平台兼容 | 仅 Claude Code | Hermes + Grok 网页版双模式 |
| 版本 | v3.9.1 | v4.0.0（MAJOR bump） |

## 自动化提纯（watchdog pipeline）

watchdog 检测到上游更新后，审计师按 `sync-audit-guide.md` 判断修改深度：

- **AUTO**（差异 < 20%）：覆盖 → 轻量提纯（删 plugin.json/.DS_Store）
- **PATCH**（差异 20-50%）：覆盖 → 重新应用已知补丁（如 serenity handoff 协议）
- **NOTIFY**（差异 > 50%）：仅通知——人工 review，不自动合并

审计师角色：读 diff 报告 → 按决策树逐 skill 判断 → 执行或通知 → Telegram 推送审计报告。
