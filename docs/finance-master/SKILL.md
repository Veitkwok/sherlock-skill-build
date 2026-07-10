---
name: finance-master
description: 金融分析统一入口。检测到金融/股票相关请求时，自动加载 sherlock-finance 推理协议作为大脑，sherlock-finance 按协议选择决策树路由到对应子 skill（finance-skills 25个、UZI-Skill 4个、x-advanced-research、serenity-skill）。覆盖 34 个子 skill 的智能调度系统。
version: 4.2.0
author: Veit Kwok
license: MIT
metadata:
  hermes:
    tags: [finance, stocks, valuation, analysis, research, trading, orchestrator, router]
    related_skills: [sherlock-finance, UZI-Skill/deep-analysis, x-advanced-research, serenity-skill]
---

# Finance Master · 金融分析统一入口 v4.2

> 你的职责不是做分析，而是**检测金融请求 → 加载 sherlock-finance**。sherlock-finance 是大脑，它负责推理、路由、判断。

---

## 自动触发

当用户输入**出现金融意图信号**时，立即加载 sherlock-finance。

### 触发逻辑（三层匹配，任一命中即进入）

**L1 · 股票代码**
- 标准格式：`AAPL.US`, `TSLA`, `700.HK`, `RKLB` 等
- 裸 ticker：`NVDA`, `PLTR`, `ASTS` 等大写字母组合
- 你提到任何股票 → 进入

**L2 · 金融意图信号**
- 分析动作：分析、深度分析、估值、DCF、财报、帮我看看、看一下、了解、研究
- 判断动作：值得买、怎么样、怎么看、值不值、安全吗、能买吗
- 价格运动：为什么跌、为什么涨、走势、跌了、涨了、震荡、回调、反弹
- 技术工具：期权、目标价、PE、ROE、技术面、做空、持仓
- 信息源：X 上、Reddit、讨论、在说、有人提到、在推

**L3 · 对话上下文**
- 上一轮在分析某只股票 → 当前追问（"那现在呢""还会跌吗""目标价多少"）→ 继续加载

### 加载指令

```
skill_view(name='finance-master/sherlock-finance')
```

---

## 子 skill 池

sherlock-finance 的 §9 协议选择决策树会自动路由到以下子 skill：

| 命名空间 | Skill 数 | 来源 |
|----------|---------|------|
| `finance-master/finance-skills/` | 25 | himself65/finance-skills |
| `finance-master/UZI-Skill/` | 4 | wbh604/UZI-Skill (提纯版) |
| `finance-master/x-advanced-research/` | 1 | X/Twitter 研究元编排器 |
| `finance-master/serenity-skill/` | 1 | muxuuu/serenity-skill |
| `finance-master/sherlock-finance/` | 1 | 推理协议 (大脑) |

总计 32 个 SKILL.md。

---

## 自动化更新

Cron job `2cd20c6abb1f`：每 14 天检查三个上游 GitHub 仓库 → 自动拉取 + 提纯 + 版本更新 → Telegram 推送报告。

详见 `references/skill-purification-guide.md`（提纯规则 + persona 转换模式）。
审计方法见 `references/system-audit-methodology.md`（系统级多 prompt 路径追踪 + 8 维评估框架）。

---

## 架构设计

三层模型（v4.2 定型）：

```
finance-master/SKILL.md           ← L0 · 薄层入口
        │ 加载
        ▼
finance-master/sherlock-finance/  ← L1 · 大脑（五步消除引擎 + 协议选择决策树 §9）
        │ 路由到
        ▼
finance-master/{子 skill 池}      ← L2 · 32 个执行 skill
```

详见 `references/skill-purification-guide.md`。

---

*v4.2: 大脑从自制路由器切换为 sherlock-finance · x-advanced-research 独立为顶层 skill*
