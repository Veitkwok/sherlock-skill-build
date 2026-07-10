# 系统级 Skill 审计方法论

> 用于检验多 skill 协同系统的完整性和闭环。适配自 darwin-skill 的 8 维评估框架。
> 本次审计记录：第一轮 2026-06-27 · finance-master v4.2 · 33 个 SKILL.md · 8 项发现全修复。第二轮 2026-06-28 · v4.3 · 29 个 SKILL.md · 3 项发现全修复。

## 审计核心工作流（Plan → Execute → Fix）

### Phase 0: Plan（先出 plan，用户确认后执行）

这是 finance-master 用户的核心工作流偏好——**永远不要直接动手**。

```
1. 分析任务 → 设计测试 prompt（覆盖所有主要路径）
2. 展示 plan：测试 prompt 列表 + 预期路径 + 审计范围
3. 用户确认/调整 → 进入执行
```

### Phase 1: 路径追踪审计

**Step 1: 设计测试 Prompt（5 个）**
覆盖所有主要意图路径，至少包含：
- 1 个标准路径（happy path）："深度分析 AAPL"
- 1 个多 skill 联动路径（链式调用）："找 Serenity 风格高风险美股"
- 1 个安全优先路径（否决/杀猪盘）："朋友推荐稳赚"
- 1 个单维度工具路径："NVDA 期权大单信号"
- 1 个复杂真实场景（含追问）："RKLB 跌了40%为什么 + 两周走势"

**Step 2: 逐路径追踪**
对每个测试 prompt，从入口 skill 开始逐层追踪：
```
入口 skill → 大脑 skill → 子 skill(s) → 输出
```
每个阶段检查：
- 触发词是否匹配
- 路由决策是否正确
- 子 skill 是否就绪（文件存在 + 可读）
- handoff 是否有显式协议（链式调用时）

**Step 3: 全局扫描**
- 搜索所有 SKILL.md 中的死链（引用不存在的文件）
- 搜索被移除但仍在引用的内容（HK/CN 残留等）
- 检查命名空间一致性
- 统计孤儿 skill（没有任何 skill 引用它）

**Step 4: 分类与修复**
- 🔴 致命 (2): 入口漏检、关键链断裂、架构冲突
- 🟡 薄弱 (5): 隐式 handoff、协议孤立、工具错配、能力缺口、死链虚引
- 🟢 通过 (1): 正常运转

### Phase 2: 修复执行（逐项 plan → 确认 → patch）

每个发现的修复流程：
```
1. 出简明 plan（改哪个文件、改什么、为什么）
2. 用户确认 → 执行 patch
3. 验证（检查修复后的文件残留）
```

## 评估维度（系统级 · darwin 适配）

| # | 维度 | 权重 | 检查内容 |
|---|------|------|---------|
| 1 | 入口检测 | 10 | 所有测试 prompt 是否被入口层正确捕获 |
| 2 | 路由准确性 | 15 | 大脑层是否正确分发到子 skill |
| 3 | 子 skill 就绪度 | 15 | 所有被路由到的子 skill 是否真实存在且可读 |
| 4 | 链式完整性 | 15 | 多 skill 联动时，handoff 是否有显式协议 |
| 5 | 安全与否决 | 10 | 安全类 skill 是否优先加载，否决条件是否覆盖 |
| 6 | 输出规范 | 10 | 各级输出格式是否明确 |
| 7 | 死代码与孤儿 | 15 | 死链、虚引、弃用内容、独立无用的 skill |
| 8 | 一致性与命名 | 10 | 命名空间是否统一，skill 间是否有矛盾 |

## 本次审计记录 · 第二轮（2026-06-28 · finance-master v4.3 · Darwin 综合评判 S 级）

| ID | 类型 | 发现 | 修复方式 |
|----|------|------|---------|
| G9 | 🟡 | 4 个 C 类 skill（generative-ui, skill-creator, hyperliquid-reader, yc-reader）与美股分析无关 | 删除。29 个 skill 保留 |
| G10 | 🟡 | §9 决策树仅覆盖 51% 子 skill（16/31） | 重写 §9 v2.1：模式感知 + 兜底路由 + investor-panel 显式路由 → 100% 覆盖 |
| G11 | 🟡 | investor-panel 和 lhb-analyzer 仍引用 Python 脚本（孤儿路由） | 重写 SKILL.md v4.0 agent 驱动版 |

## 本次审计记录 · 第一轮（2026-06-27 · finance-master v4.2）

| ID | 类型 | 发现 | 修复方式 |
|----|------|------|---------|
| G1 | 🔴 | finance-master 入口触发列表过窄（白名单 vs 语义检测：P3 可能漏检） | 三层触发逻辑（代码格式 + 语义意图 + 对话上下文） |
| G2 | 🔴 | sherlock-finance §4/§7/§9/frontmatter 含 HK/CN/A 股残留 | §4 弃用、§7 重写美股版、§9 去港股分支、frontmatter 清理 |
| G3 | 🟡 | x-advanced-research → serenity-skill 无显式 handoff 协议 | serenity-skill 新增 "Integration with x-advanced-research" 段 |
| G4 | 🟡 | options-payoff 路由不加载 §5 期权信号协议 | §9 期权分支追加 "+ 参考 §5 期权信号协议" |
| G5 | 🟡 | 缺少 1-4 周中期技术展望协议（P5 自由发挥风险） | 新增 §13 短期走势研判协议（1-4 周） |
| G6 | 🟡 | sherlock-finance §12 Step5 引用已删除的 hsbc-trade25-fees.md | 改写为通用费率说明 |
| G7 | 🟡 | x-advanced-research SKILL.md 引用不存在的 reference 文件 | 修正为实际存在的 4 个文件名 |
| G8 | 🟢 | 16/16 子 skill 文件存在且可读 | 无需修复 |

## 可复用模式（跨会话）

### 双模式 Skill 设计
为同时兼容 Hermes (MCP 工具) 和 Grok 网页版 (web+X search) 的 skill，在头部加入环境检测段：
- "如果你能访问 mcp_longbridge_* → Hermes 模式"
- "如果不能但能 web search → Grok 模式"
- 数据获取表做成双列（Hermes / Grok）
- 方法论完全一致，只有数据获取方式不同

### Skill 提纯模式
将来自上游的 script-heavy skill 转为纯方法论 skill：
1. 保留 SKILL.md（重写为纯分析指令）+ references/（方法论文档）
2. 删除 scripts/（Python 脚本）、assets/（HTML/SVG）、personas/（YAML 配置）
3. 将 YAML persona 浓缩为 Markdown 速查表（LLM 直接读取）
4. 数据获取从脚本执行改为 Hermes MCP 工具或 Grok web+X search

## 使用建议

每次 finance-master 发生架构变更（新增 skill、修改路由、更新大脑协议）后，跑一次审计。保持 `<20 个待处理问题`。超过 20 个考虑重构而不是修。
