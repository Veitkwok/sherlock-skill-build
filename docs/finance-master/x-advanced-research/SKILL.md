---
name: x-advanced-research
description: Meta-orchestrator and intelligent router for advanced real-time X/Twitter research with Grok's native tools. When user mentions X/Twitter research, monitoring, trend analysis, profile deep dive, thread analysis, high-engagement content scraping, sentiment tracking, voice/style extraction, competitor/niche signals, content inspiration from X, or similar tasks, automatically performs semantic intent analysis, selects optimal tool combinations (x_keyword_search with advanced operators, x_semantic_search, x_thread_fetch, x_user_search), applies smart filters (engagement thresholds, time windows, trusted accounts, negation), chains multiple calls for depth (broad → targeted → thread/profile), and delivers structured outputs with citations, key quotes, metrics, insights, and actionable takeaways. Supports user's key accounts for prioritized analysis. Compatible with Grok web (native tools) and other agents via tool wrappers. Prioritizes quality, recency, relevance, and safety (avoid spam/low-signal sources).
---

# x-advanced-research v1.0.0

**x-advanced-research** 是一个面向 Grok（尤其是网页版）的 **X/Twitter 高级研究元编排器**（Meta-Orchestrator / Intelligent Router）。它本身不直接执行单一搜索，而是根据用户查询的语义意图，智能路由到最优的工具组合、过滤策略和调用链路，最终产出结构化、专业级的研究输出。

目标：让 Grok 充分发挥其原生实时 X 数据优势，实现“像专业研究员一样”使用 X 工具——不再是大海捞针，而是精准、深度、结构化的研究。

## 核心架构：三层路由模型（参考 finance-master 设计）

### Layer 0 · 元 Skill 路由器（本文件 SKILL.md）
- 接收用户输入 → 语义分析 + 触发词匹配 → 输出需要执行的工具策略 / 调用链路 / 子模块
- 关键流程：意图分类 → 安全/质量扫描 → 工具选择与参数规划 → 链式调用规划 → 输出格式规范

### Layer 1 · 规则引擎（嵌入本文件 + references/）
- **触发词规则**：覆盖常见 X 研究场景（详见下文“常见场景与触发”）
- **组合引擎**：定义多工具组合规则（例如“监控主题 + 关键账号 + 高互动” → semantic + keyword with from: + min_faves + thread fetch）
- **冲突仲裁**：优先级规则（质量优先、安全优先、深度优先、时效优先）
- **过滤与优化规则**：engagement 阈值、时间窗口、账号白名单、否定词、去重、信号质量评估

### Layer 2 · 能力模块池（references/ 中的模块化方法论）
- 不是独立子 skill 文件，而是按需加载的参考模块（search-strategies.md、output-templates.md、key-accounts.md、serenity-high-risk-movers.md）
- 未来可扩展为独立子目录（如 profile-dive/、trend-monitor/），但当前以 references 为主，保持轻量高效

## 常见场景与触发规则（Layer 1 核心）

当用户查询包含以下意图时自动触发并路由：

**1. 实时趋势 / 主题监控（Trend & Monitoring）**
- 触发词：监控、实时跟踪、最新讨论、趋势、sentiment on [topic]、过去X小时/天人们在说
- 路由策略：x_semantic_search（broad）+ x_keyword_search（with since:/until: + min_faves:/min_views: + -filter:replies） → 结构化总结（正面/负面/中性信号、关键帖子、趋势演变）

**2. Profile / 账号深度分析（Account Deep Dive）**
- 触发词：分析 @handle 的帖子、抓取高互动内容、提取风格/voice、该账号最近在说什么、niche leader 内容
- 路由策略：x_user_search（确认账号） → x_keyword_search from:@handle min_faves:1000（或自定义阈值） → x_thread_fetch（高价值线程） → voice/style extraction + 关键洞察

**3. Thread / 长帖深度处理（Thread Analysis & Transformation）**
- 触发词：分析这个 thread、把 thread 转成课程/总结/结构化笔记、thread 洞察
- 路由策略：x_thread_fetch → 交互式或结构化输出（模块化拆解、关键原则、应用场景、引用原帖）

**4. 高互动内容抓取 / 内容灵感（High-Engagement Scraping & Inspiration）**
- 触发词：抓取 likes>1000 的帖子、niche 高质量内容、competitor 热门帖、灵感来源、hooks/angles
- 路由策略：x_keyword_search（高级 operators + min_faves + 时间过滤） → 提取 hooks、tone、angles、structure → 输出 style guide 或内容模板

**5. 情感 / 舆情跟踪（Sentiment & Signal Tracking）**
- 触发词：sentiment、情绪、舆情、正面/负面信号、社区反应
- 路由策略：semantic + keyword 组合 → 量化 sentiment 分布 + 代表性引用 + 演变趋势

**6. 供应链 / 瓶颈 /  niche 信号研究（Specialized Signals，参考 serenity 风格）**
- 触发词：供应链、瓶颈、卡脖子、单一供应商、产能、行业信号
- 路由策略：semantic search on topic + 针对性 keyword（from:行业专家账号） + 链式分析

**7. 高风险快速增值美股 / Serenity 风格大涨标的捕捉（用户核心场景）**
- 触发词：高风险快速增值、可能大涨的美股、AI 供应链瓶颈机会、Serenity 风格、catalyst driven movers、小资金高 beta 标的、asymmetric upside
- 路由策略：**Serenity 最高优先**（@aleabitoreddit Top #1）+ 其他重点账号 → 识别 bottleneck / catalyst ticker → 链式 X 深挖 + 明确推荐交叉验证 https://analysissite.vercel.app/、https://serenity.bemix.cc/、https://antseer.ai/skill/3544、https://www.redditalpha.xyz/en/dashboard/ → 输出 High-Risk Mover Alert 结构化报告（参考 references/serenity-high-risk-movers.md）
- 特别强调：不对称回报、风险校准、与 finance-master deep-analysis 联动

**8. 组合研究任务（Complex Multi-step）**
- 示例：“监控 AI 代理趋势 + 重点看 @关键账号 + 提取高互动内容做内容灵感”
- 路由：并行/顺序组合上述策略，自动规划调用链

**用户关键账号支持**（已更新 references/key-accounts.md）
- @aleabitoreddit 为 **Top #1 Priority**（Serenity Core，AI 供应链瓶颈研究核心来源）
- 其他 20 个账号均为 High 优先级
- 路由时自动优先采样这些账号的高互动内容、在 profile 分析和 ticker 识别中提升权重
- 特别在“高风险快速增值美股”场景中，Serenity 信号权重最高

## 智能路由与链式调用逻辑

**基础原则**：
- **广度优先 → 深度优先**：先 semantic 或 broad keyword 发现信号 → 再 targeted keyword / thread fetch 深挖
- **质量优先**：优先高 engagement（min_faves / min_views）、可信账号、原创帖；自动过滤低信号（replies-heavy、spam）
- **时效 + 相关性平衡**：默认 since:最近合理窗口；需要历史时显式指定
- **高级 Operators 智能使用**：min_faves:、min_views:、from:、-from:、since:/until:、filter:images / -filter:replies、"exact phrase"、OR/AND 组合
- **去重与去噪**：结果中自动去重 URL，优先引用原文

**典型调用链示例**（模型应自动规划）：
1. 用户：“分析 AI 编码代理最近的讨论”
   → x_semantic_search "AI coding agents" (limit 10-20)
   → 识别高价值主题/账号
   → x_keyword_search "AI coding agents OR agents coding" min_faves:500 since:2026-06-01 -filter:replies
   → 对 top 帖子/线程执行 x_thread_fetch
   → 结构化输出（趋势、关键观点、引用、sentiment）

2. 用户：“抓取 @handle 高互动帖子做风格分析”
   → x_keyword_search from:@handle min_faves:1000 (或用户指定阈值)
   → 提取 hooks/tone/angles → 输出可复用 style guide

**输出结构化要求**（强制执行，参考 output-templates.md）：
- 始终包含：Post URLs / citations、关键引用（带原文链接）、engagement metrics（likes/views/reposts）、时间戳
- 洞察层：趋势总结、信号强度、正面/负面/中性分布、 actionable takeaways
- 可视化友好： bullet points、表格（如果适用）、分模块
- 质量标注：来源可信度、潜在偏差说明

## 冲突仲裁与优先级规则

- **质量与安全优先**：低信号/ spam / 明显推广内容自动降权或过滤；优先用户 key accounts 和高 engagement
- **深度优先于广度**：thread/profile 深挖优先于纯 broad search
- **时效优先于历史**：实时监控类任务优先最近窗口
- **用户意图优先**：明确指定“只看 @xxx”时严格限制 from:
- **并行加载**：多个互补策略可并行（如 semantic + targeted keyword）

## 双模式数据获取说明

- **Grok 网页版（主要模式）**：完全依赖原生 X 工具（x_keyword_search、x_semantic_search、x_thread_fetch 等）。模型内置知识 + 实时搜索结果校准。输出以洞察和引用为主，数字为区间估计时会说明。
- **其他 Agent 环境（如 Hermes）**：可通过工具包装器调用类似 X search 能力，或 fallback 到 web_search + X 公开数据。核心分析框架和路由逻辑完全一致。

## 文件结构

```
x-advanced-research/
├── SKILL.md                  # 元路由器 + 核心规则
├── VERSION                   # 版本号（当前 1.0.0）
├── references/
│   ├── search-strategies.md  # 高级搜索策略、operators 使用指南、过滤最佳实践
│   ├── output-templates.md   # 结构化输出模板（趋势报告、High-Risk Mover 等）
│   ├── key-accounts.md       # 用户重点关注账号列表（含优先级、研究重点）
│   └── serenity-high-risk-movers.md  # Serenity 风格高风险快涨标的捕捉流程
└── (未来扩展) scripts/ 或子目录（如 trend-monitor/）
```

## 版本管理与迭代

- 当前版本：1.0.0
- 升级规则：PATCH（小优化）、MINOR（新增场景/模块）、MAJOR（架构重写）
- 强烈推荐结合 darwin-skill 进行持续优化（结构评分 + 实测效果验证）
- 更新后通过测试 prompt 验证路由准确性和输出质量

## 关键设计决策（与 finance-master 对齐）

1. **为什么做成一个智能路由器而不是多个独立 skill？**  
   X 工具本身强大，但“怎么用、什么时候链式、如何过滤、输出什么结构”需要统一方法论。路由器让系统自动匹配复杂意图，避免用户手动选工具。

2. **为什么用 references/ 而不是 30 个子 skill 文件？**  
   当前聚焦 X 核心能力增强，模块化参考文件更轻量、易维护。未来如需独立子 skill（如独立 trend-monitor skill），可按 finance-master 模式拆分。

3. **为什么强调链式调用和结构化输出？**  
   单一搜索往往信息碎片化。链式 + 结构化能产出“可直接用于决策或内容生成”的专业输出，最大化 Grok X 能力的价值。

4. **用户关键账号的重要性**：  
   将在 references/key-accounts.md 中维护（你后续提供列表后我帮填充）。路由时自动提升这些账号的权重或默认采样，实现“个性化 X 研究大脑”。

5. **与现有 skills 兼容**：  
   可与 wenai-script-generator、stella 等组合使用（例如：先用 x-advanced-research 拉实时 X 灵感 → 再用 wenai 生成故事）。

---

**使用方式**：
- 直接在对话中描述 X 相关研究任务即可触发（例如：“用 x-advanced-research 监控 AI 代理趋势并提取高互动内容” 或直接描述任务）。
- Slash command 支持：`/x-advanced-research [任务描述]`
- 首次使用建议提供你的重点 X 账号列表，我会帮你更新 references/key-accounts.md。

这个 skill 将持续迭代。需要我现在创建 references/ 下的核心文件（search-strategies.md、output-templates.md 等）吗？或者你先提供重点关注的 X 博主列表，我一起填充？

准备好后，我们可以用 darwin-skill 对它进行基线评估和优化。