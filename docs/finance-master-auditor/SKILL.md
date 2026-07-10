---
name: finance-master-auditor
description: finance-master 同步审计员。Hermes cron job 专用——检测上游 GitHub 仓库更新、按审计决策树执行同步策略（AUTO/PATCH/NOTIFY/IMPORT/SKIP）、管理版本号、推送 Telegram 报告。不可用于 Grok 网页版（含 Python 脚本）。
version: 1.2.0
author: Veit Kwok
license: MIT
metadata:
  hermes:
    tags: [finance, devops, sync, audit, cron]
    trigger_keywords:
      - 同步
      - 更新skill
      - 检查上游
      - 审计
---

# Finance Master Auditor · 同步审计员 v1.2

> 你是 finance-master 的**运维守护者**。你的职责不是分析股票，而是**监控上游更新、审计变更、管理版本**。

---

## 触发方式与模式

此 skill 支持两种运行模式：

| 模式 | 触发 | 行为 |
|------|------|------|
| **Cron 自动** | cron job `2cd20c6abb1f` 每 14 天 | 读 diff 报告 → 按决策树自动执行 → Telegram 报告 |
| **手动审计** | `skill_view(name='finance-master-auditor')` 或用户说"审计" | **先呈现审计 plan → 等待用户确认 → 再执行** |

**手动模式铁律**：绝不在同一轮中 plan + execute。先展示分析结果、分类（🔴/🟡/🟢）、修复方案。用户说"确认"后才动手。

---

## 工作流程

### Step 1 · 运行检测器

```bash
cd ~/.hermes/skills/finance-master-auditor/scripts && python3 skill-watchdog.py
```

读取输出的 `diff_report_path`。

### Step 2 · 读审计手册

```
read_file ~/.hermes/skills/finance-master-auditor/references/sync-audit-guide.md
```

### Step 3 · 分析 diff 报告

读 `~/.hermes/data/skill-watch-diff.json`。

- 所有 repo `status: unchanged` → 回复"无变更"，结束。
- 有 changes → 按 sync-audit-guide.md §2 决策树逐项处理。

### Step 4 · 执行审计决策

对每个变更 skill，按策略执行：

| 策略 | 操作 |
|------|------|
| **AUTO** | 直接覆盖 + 轻量提纯（删 plugin.json） |
| **PATCH** | 覆盖 + 按指南 §3.2 重应用补丁 + 验证 |
| **NOTIFY** | 不修改 → 列出变更概要 → Telegram 通知 |
| **IMPORT** | 评估新 skill 相关性 → 提纯 → 加入 finance-skills/ |
| **SKIP** | 本地创建 skill，跳过 |

### Step 4.5 · 提纯审计（必须追加）

执行 sync-audit-guide.md **§8 导入后提纯与死链审计**：
- Step 1: 文件类型清理（删 .py/.json/.yaml）
- Step 2: 有价值格式转换（JSON/Python → .md）
- Step 3: 死链检查（scripts/, .cache/, stage1() 等）
- Step 4: 弃用声明（保留方法论但标明脚本已删）
- Step 5: SKILL.md 重写判断
- Step 6: 空目录清理

### Step 5 · 版本管理

读了 `~/.hermes/skills/finance-master/VERSION`。

执行了 AUTO/PATCH/IMPORT → PATCH +1。

**不修改**的本地 skill（sherlock-finance, x-advanced-research, finance-master/SKILL.md）→ 版本不动。

### Step 6 · 报告

按 sync-audit-guide.md §7 模板，Telegram 推送审计报告。

---

## 关键文件索引

| 文件 | 用途 |
|------|------|
| `scripts/skill-watchdog.py` | 上游检测器 · git fetch → diff JSON |
| `references/sync-audit-guide.md` | 审计决策手册 · 决策树 + 已知修改模式 + 提纯模板 |
| `references/skill-purification-guide.md` | 提纯规则详述 |
| `references/skill-registry.yaml` | 29 个 skill 注册表 |
| `references/system-audit-methodology.md` | 系统审计方法论（darwin 框架适配 · 两轮审计记录） |
| `~/.hermes/config/skill-watch.json` | 上游仓库配置（3 个 repo） |
| `~/.hermes/data/skill-watch-diff.json` | watchdog 输出的 diff 报告 |
| `~/.hermes/data/skill-watch-state.json` | 上次同步的 SHA 记录 |
| `~/.hermes/skills/finance-master/VERSION` | 被管理的版本号 |

---

## 架构位置

```
~/.hermes/skills/
├── finance-master/          ← 纯 skill 内容（可导出到 Grok）
│   ├── SKILL.md             薄层入口
│   ├── VERSION               被本 auditor 管理 ←
│   ├── sherlock-finance/     ★ 大脑 v2.1
│   ├── x-advanced-research/  X 编排器
│   ├── finance-skills/       21 工具
│   ├── UZI-Skill/            4 提纯
│   └── serenity-skill/      供应链瓶颈
│
└── finance-master-auditor/  ← 运维层（Hermes 专用）
    ├── SKILL.md              本文件
    ├── VERSION               v1.2.0
    ├── scripts/
    │   └── skill-watchdog.py
    └── references/
        ├── sync-audit-guide.md
        ├── skill-purification-guide.md
        ├── skill-registry.yaml
        └── system-audit-methodology.md
```

---

*v1.2.0 · 第二轮审计后更新 · 同步至 finance-master v4.3 状态*
