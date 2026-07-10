# Skill Sync Audit Guide

> 面向 cron job 中的 LLM 审计师。当 watchdog 检测到上游 GitHub 仓库有更新时，审计师读此手册后执行决策。

---

## §1 三个上游仓库

| 仓库 | URL | 对应本地路径 |
|------|-----|------------|
| himself65/finance-skills | github.com/himself65/finance-skills | `finance-master/finance-skills/` (21 skills) |
| wbh604/UZI-Skill | github.com/wbh604/UZI-Skill | `finance-master/UZI-Skill/` (4 skills) |
| muxuuu/serenity-skill | github.com/muxuuu/serenity-skill | `finance-master/serenity-skill/` (1 skill) |

---

## §2 审计决策树

watchdog 生成 diff 报告 JSON 后，审计师读取它，按以下树逐项处理：

```
对每个出现在 diff 中的 skill：
│
├── 该 skill 在 finance-master 中已存在？
│   │
│   ├── 是 → 已存在 skill
│   │   ├── 读本地版本 + 读上游版本（SKILL.md 全文）
│   │   ├── 判断修改深度（见 §3）
│   │   │   ├── 深度 < 20%（基本未改）：AUTO
│   │   │   ├── 深度 20-50%（轻量修改）：PATCH
│   │   │   └── 深度 > 50%（大量修改）：NOTIFY
│   │   └── 按对应策略执行（见 §4）
│   │
│   └── 否 → 上游新增 skill
│       ├── 读上游 SKILL.md
│       ├── 评估与美股/金融分析的相关性（见 §5）
│       │   ├── 相关：IMPORT — 提纯后加入 finance-master
│       │   └── 不相关：SKIP — 记录日志
│       └── 报告
│
└── 本地有但上游没有？（被上游删除）
    └── 不自动删除。NOTIFY — 列出被上游删除的 skill，询问处置。
```

---

## §3 已知本地修改模式（审计师参考）

### 3.1 深度重写（差异度 > 50% · 策略: NOTIFY）

这些 skill 被完全重写。上游更新时**绝不自动合并**。

| Skill | 上游来源 | 本地改动 |
|-------|---------|---------|
| **deep-analysis** | `wbh604/UZI-Skill/skills/deep-analysis/` | SKILL.md 完全重写 (54KB → 15KB · v3.9.1 → v4.0 · 双模式版)；删除 `scripts/` (198 文件)；删除 `personas/` (51 YAML)；删除 `assets/` (71 文件)；删除 `run.py`；删除 `requirements.txt`；新增 `references/investor-frameworks.md` (36 位美股大师速查表)；所有 Python fetcher/HTML 生成/Playwright 自动化已移除 |
| **sherlock-finance** | `~/.hermes/skills/sherlock-finance/` (本地创建后移入) | SKILL.md 完全重写 (v1.1 → v2.1 · 美股专精)；删除 `references/hsbc-trade25-fees.md`；§4 港股协议已弃用；§7 跨市场信号重写为美股版；§9 v2.1 决策树（新增模式感知 + 兜底路由 + investor-panel 显式路由 + 安全优先）；新增 §13 短期走势研判协议 |
| **finance-master/SKILL.md** | 本地创建 | 三层触发逻辑；从自制路由器改为 sherlock-finance 委托模式 |

### 3.2 轻量修改（差异度 20-50% · 策略: PATCH）

这些 skill 有局部修改。上游更新时**重新应用补丁**。

| Skill | 上游来源 | 本地改动 | 补丁描述 |
|-------|---------|---------|---------|
| **serenity-skill** | `muxuuu/serenity-skill/` | SKILL.md 在 "The answer should feel like..." 后插入 `## Integration with x-advanced-research` 段（~20 行）；删除 `scripts/` (3 py)；`bottleneck-scorecard.json` → `references/bottleneck-scoring.md` | 在 `The answer should feel like` 之后插入 handoff 协议段；覆盖后删除 .py/.json/.yaml |
| **investor-panel** | `wbh604/UZI-Skill/skills/investor-panel/` | SKILL.md 重写为 v4.0 agent 驱动版（移除 `scripts/lib/`、`.cache/` 引用）；删除 `assets/` | 覆盖后重写 SKILL.md + 删除非 .md 文件 |
| **lhb-analyzer** | `wbh604/UZI-Skill/skills/lhb-analyzer/` | SKILL.md 重写为 v4.0 agent 驱动版（移除 `scripts/fetch_lhb.py`）；删除 `assets/` | 覆盖后重写 SKILL.md + 删除非 .md 文件 |
| **company-valuation** | `himself65/finance-skills/plugins/market-analysis/skills/company-valuation/` | 删除 `plugin.json`（Hermes 不需要） | 覆盖后删除 plugin.json |
| **全部 21 个 finance-skills** | `himself65/finance-skills/plugins/*/skills/*/` | 删除每个 skill 下的 `plugin.json` 或 `README.md`（提纯）；已删除 4 个无关 skill（generative-ui, skill-creator, hyperliquid-reader, yc-reader——见 §3.3） | 覆盖后删除 plugin.json + README.md（如存在） |

### 3.3 已删除 / 无上游（策略: SKIP / N/A）

| Skill | 上游来源 | 状态 | 说明 |
|-------|---------|------|------|
| **trap-detector** | `wbh604/UZI-Skill/skills/trap-detector/` | 基本无修改 | 仅删除 `assets/` |
| **generative-ui** | `himself65/finance-skills/` | ❌ 已删除 | Claude 专用 UI 生成，与美股分析无关 |
| **skill-creator** | `himself65/finance-skills/` | ❌ 已删除 | 通用 Hermes skill 创建工具，非金融分析 |
| **hyperliquid-reader** | `himself65/finance-skills/` | ❌ 已删除 | 加密 perp DEX，非美股。依赖 opencli 插件 |
| **yc-reader** | `himself65/finance-skills/` | ❌ 已删除 | YC 创业公司查询，边缘用途。opencli 依赖 |

### 3.4 本地创建（无上游 · 策略: SKIP）

| Skill | 说明 |
|-------|------|
| `x-advanced-research/` | 从用户 zip 创建，无上游仓库 |
| `VERSION` | 本地版本号 |
| `references/skill-registry.yaml` | 本地注册表 |
| `references/skill-purification-guide.md` | 本地提纯文档 |

---

## §4 执行策略

### AUTO（直接覆盖）

```
1. 备份当前版本（cp -r skill_dir skill_dir.bak）
2. 用上游版本覆盖
3. 重新应用轻量提纯：删除 plugin.json / README.md / .DS_Store / __pycache__
4. 删除备份
5. 日志记录
```

### PATCH（拉取 → 重新应用补丁）

```
1. 备份当前版本
2. 用上游版本覆盖
3. 重新应用已知补丁（按 §3.2 中的补丁描述）
4. 重新应用轻量提纯
5. 对比 patch 后的版本是否与预期一致（检查关键段落是否存在）
6. 一致 → 删除备份；不一致 → 恢复备份 + NOTIFY
7. 日志记录
```

### NOTIFY（仅通知）

```
1. 生成变更摘要：
   - 上游改了哪些文件
   - 本地有哪些自定义修改
   - 建议：手动 review 后决定是否合并
2. 不自动修改任何文件
3. Telegram 推送变更摘要
```

### IMPORT（导入新 skill）

```
1. 读上游 SKILL.md → 评估相关性（见 §5）
2. 若相关：
   - 复制到 finance-master/finance-skills/<name>/
   - 提纯：删除 plugin.json
   - 如果来自 UZI-Skill：删除 scripts/ + assets/ + personas/ + run.py（深度提纯）
3. 若不相关：跳过
4. 报告新增
```

---

## §5 新 Skill 评估标准

新 skill 是否应该加入 finance-master？

**必须同时满足**：
- 与金融/投资分析相关（关键词：stock, equity, option, valuation, earnings, sentiment, portfolio, market, trading, finance, 股票, 美股, 估值, 财报, 期权）
- 与美股兼容（不依赖 A 股/港股独有市场机制）
- 功能层面有用（提供新的分析维度或数据源）

**明确排除**：
- 仅限 A 股/港股/加密货币的 skill
- 纯 UI/前端展示类（与泛金融无关）
- 与已有 21 个 finance-skills 中某个功能完全重复

**灰色地带**（需要人工判断）：
- 加密货币相关但涉及美股标的（如比特币 ETF 分析）→ 可导入
- 宏观数据工具（如 CPI/NFP 追踪）→ 可导入，放入 data-providers 类

---

## §6 提纯模板

### 深度提纯（来自 UZI-Skill）

```
适用：从 wbh604/UZI-Skill 导入的任何 skill
操作：
  1. 复制 SKILL.md（不修改内容——审计师不做重写，只做删除）
  2. 保留 references/（方法论参考）
  3. 删除 scripts/（所有 Python 脚本——Hermes 用 MCP，不执行脚本）
  4. 删除 personas/（YAML persona 定义——已浓缩为 references/investor-frameworks.md）
  5. 删除 assets/（HTML 模板、SVG 头像等）
  6. 删除 run.py, requirements.txt
```

### 轻量提纯（来自 himself65/finance-skills）

```
适用：从 himself65/finance-skills 导入的任何 skill
操作：
  1. 复制全部文件
  2. 删除 plugin.json（Hermes 不使用）
  3. 保留 README.md（如存在，有助于理解 skill）
  4. 删除 .DS_Store, __pycache__
```

---

## §7 审计报告格式

审计完成后的 Telegram 报告模板：

```
📦 finance-master 同步审计 · {date}

📥 上游变化:
  finance-skills: {old_sha} → {new_sha}
  UZI-Skill: {old_sha} → {new_sha}
  serenity-skill: {old_sha} → {new_sha}

📋 处理结果:
  ✅ AUTO    (2) company-valuation, yfinance-data
  🔧 PATCH   (1) serenity-skill → 重新应用 handoff 补丁 ✓
  🔔 NOTIFY  (1) UZI-Skill/deep-analysis · 上游有更新，本地改动过大，需手动 review
  ➕ IMPORT   (1) 新增 skill: stock-screener (评估: 美股相关 ✓)
  ⏭️ SKIP    (1) 新 skill: crypto-defi-scanner (评估: 无关美股 ✗)

📊 当前版本: 4.2.0 → 4.2.1 (PATCH)
📊 总 skill 数: 29 → 29（无变化）
```

---

## §8 导入后提纯与死链审计

审计师在执行 AUTO/PATCH/IMPORT 操作后，**必须追加以下 6 步提纯审计**。

### Step 1 · 文件类型清理

扫描新导入或覆盖的 skill 目录，删除所有非 `.md` 且非 `LICENSE` 的文件：

| 删除 | 示例 |
|------|------|
| `.py` | `scripts/*.py`, `run.py`, `validate_skill.py` |
| `.json` | `bottleneck-scorecard.json` |
| `.yaml` / `.yml` | `agents/openai.yaml` |
| `requirements.txt` | Python 依赖声明 |
| `.DS_Store` | macOS 系统文件 |

### Step 2 · 有价值格式转换

如果 `.json` 或 `.py` 文件包含**方法论数据**（评分公式、权重、阈值、对照表），先提取 → 转换为 `.md` → 再删除原件。

**已知转换模式**：

| 原件 | 转换为 | 转换内容 |
|------|--------|---------|
| `assets/bottleneck-scorecard.json` + `scripts/serenity_scorecard.py` | `references/bottleneck-scoring.md` | 8 因子权重 + 8 扣分项 + 评分公式 + Verdict 阈值 |
| `agents/*.yaml` | ❌ 不转换 | OpenAI GPT 配置，在 Hermes/Grok 中无用 |

### Step 3 · 死链检查

搜索所有 `.md` 文件中是否引用**已删除的路径**：

**搜索模式**（任一命中即为死链）：
```
scripts/        run.py          requirements.txt
personas/       assets/         .cache/
assemble_report  render_share   render_war
inline_assets   playwright      stage1()
stage2()        run_real_test   fetch_*.py
```

**豁免规则**（不算死链）：
- 弃用声明正文中的引用（`> ⚠️ 弃用声明...` 段落内）
- `stage1_growth`、`stage2_growth` 等 DCF 参数名（不含括号）
- SKILL.md 中自述性质的 `无脚本/无HTML/已删除`
- `Bloomberg` 作为新闻来源引用

### Step 4 · 弃用声明

对保留的原版 reference 文件：如果内容引用旧脚本路径但方法论本身仍有效 → 在文件第一个 `# ` 标题后插入弃用声明：

```markdown
> ⚠️ **弃用声明**：本文档描述原版 Python 脚本工作流（`scripts/`、`run.py`、`.cache/`、Playwright、HTML 报告等）。在 finance-master 中，所有脚本已删除，分析由 Agent 通过 Hermes MCP 工具链或 Grok web/X search 直接执行。本文档中的方法论（维度定义、参数标准、评分逻辑）仍有效，但执行方式已从「运行 Python 脚本」变为「Agent 直接推理 + 工具调用」。
```

### Step 5 · SKILL.md 重写判断

如果 SKILL.md 本身包含以下模式 → 标记为"需重写"，NOTIFY 用户：
- `scripts/` + `python` 命令
- `pip install`
- `from lib.xxx import`
- `.cache/{ticker}/` 路径依赖

重写模板参考 `investor-panel/SKILL.md` v4.0 和 `lhb-analyzer/SKILL.md` v4.0——输入从 JSON 文件变为 Agent 已掌握的结构化数据，数据获取从脚本调用变为 web search/MCP 工具。

### Step 6 · 空目录清理

删除所有空目录（`rmdir`）。

### 审计报告追加

在 Telegram 报告末尾追加提纯审计段：

```
🧹 提纯审计:
  ✅ 清理: 删除了 X 个 .py / Y 个 .json / Z 个空目录
  📝 转换: bottleneck-scorecard.json → bottleneck-scoring.md
  ⚠️  死链: 发现 N 处 · 已加弃用声明覆盖
  🔧 重写: 0 个 SKILL.md 需重写
```
