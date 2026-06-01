---
layout: default
title: AI 究竟革命了什么？—— 资本开支 vs 收入的现实检查 (2026年6月1日)
---

# AI 究竟革命了什么？
## 1.2 万亿美元资本开支已经投入。真实产出在哪？
### 2026 年 6 月 1 日 —— 行业分析

> **用户的问题（转述）**：大部分 AI 投资来自 Mag7 的传统云/广告利润。最大赢家是 Nvidia 和它的供应商（SK 海力士、三星、美光 —— 现在都是万亿美元公司）。但实际 AI 使用规模仍然相当有限。AI 究竟革命了什么？

> **TL;DR ——简短诚实的回答**：
> - **是的** —— 你对财务结构的判断基本正确。"卖铲子"赢家（Nvidia + 内存 + 元器件）拿走了大部分已实现利润；终端 AI 收入仍然远小于资本开支。
> - **但是** 差距正在快速缩小。AI 原生软件 ARR 从 ~$15B（2025 年初）增长到 **~$1,500-2,000 亿年化（2026 年中）**，每年增长 100-300%。
> - **诚实的"已革命"清单很短**：**软件工程**是唯一一个被**大规模转型**的知识工作类别（2,000 万+ Copilot 用户，50%+ 生产力提升，经统计验证）。**广告**（Meta）和**客户服务**是**实质性改善**但未被转型。其他都是**有限 ROI 的辅助**（按 McKinsey 2025，只有 6% 的企业报告 5%+ 的 EBIT 影响）。
> - **数学差距**：2026 年超大规模厂商资本开支 ~$700B vs AI 软件收入 ~$150-200B = 每年 $500B 差距。越来越多由**债务**资助（2026 新增行业债务 $230B+）。自由现金流崩盘（亚马逊 -95%）。**这在 3 年路径上是不可持续的** —— 要么收入扩展到匹配资本开支（Anthropic 30 倍增长持续），要么资本开支放缓且内存/Nvidia 利润池萎缩。
> - **我的诚实看法**：我们正处于基础设施建设的 2-3 年内，需要 5-7 年的收入扩展才能合理化。**软件工程证明了革命是可能的。** 它在 2026-2028 年是否扩展到其他知识工作是万亿美元问题。

---

## ⚠️ 协议提示

应用 `.github/copilot-instructions.md` 顶部**两步研究协议**。第一节 = 事实基础。第二节 = 回答"被革命了什么"的第一步草稿。第三节 = 第二步审稿。第四节 = 诚实综合 + 开放讨论。

---

# 第一节 ——事实基础

## 1.1 流入的资本开支（支出端）

按年度的超大规模厂商 AI 基础设施资本开支：

| 年份 | 总计 ($B) | 微软 | 谷歌 | 亚马逊 | Meta |
|------|----------|------|------|--------|------|
| 2024 | ~$197B | ~$70-80B | ~$70-80B | ~$75B | ~$40B |
| 2025 | $300-380B | $80B | $75-93B | $125B | $60-65B |
| **2026** | **$700B+** | **$180-190B** | **$180-190B** | **$180-200B** | **高达 $145B** |

**2024-2026 累计：~1.2 万亿美元**，仅来自 4 家公司，加上 Oracle，加上纯基础设施（CoreWeave、Crusoe 等）。

**关键财务信号**（来自 CreditSights、Allianz、Futurum）：
- **资本开支/收入比：45-57%** —— 公用-工业级，对科技业前所未有
- **自由现金流崩盘**：亚马逊 -95% 至 $1.2B；Alphabet 预计 -90%
- **债务融资**：仅 2026 年新增行业债务 $230-240B
- ~60% 的资本开支现在是**非芯片**基础设施（电力、冷却、土地、网络）

## 1.2 卖铲子获取的利润

### Nvidia
- FY2026 收入跟踪 ~$200B+，净利润 ~$100B+
- 捕获 AI 价值链的大部分利润

### 内存（SK 海力士 + 三星 + 美光）—— 现在都 $1T+ 市值

| 公司 | Q1 2026 收入 | 运营利润率 | HBM 份额 | 市值 |
|------|--------------|----------|---------|------|
| **SK 海力士** | ₩52.6T ($38B) —— +198% YoY | **72%（纪录）** | **50-59%** | **$1.06T** |
| **三星（DS）** | ₩81.7T ($60B+) | 65%+ | ~22% | $1T+ |
| **美光** | $23.86B (FQ2'26)；预测 Q3 ~$33.5B | 毛利 81% | ~21% | $1T+ |

- HBM 现在 ~**AI GPU 物料清单的 50%+**
- 2026 年 HBM 产能全部售罄；紧张持续到 2028
- 合并内存收入 2026 年化：**~$300B+**

### 元器件（PCB、MLCC、网络、光学、电源）
- 估计合并收入：$150-200B+ 年化
- 主要赢家：Broadcom、Arista（网络）、Vertiv（冷却）、Lite-On（电源）、村田（MLCC）、Yageo、Unimicron（PCB）

**供应商总价值链捕获**：**~$650-750B 年化创造价值**（收入，非利润）—— 大致匹配 2026 年超大规模厂商资本开支的供给侧。

## 1.3 终端客户产生的收入（需求端）

### 纯 AI 软件 ARR（2026 年中）

| 公司 | 2025/1 ARR | 2025/12 ARR | 2026 年中 ARR | 增长 |
|------|-----------|-------------|--------------|------|
| **OpenAI** | ~$13B | ~$25B | **~$33B**（Q2'26） | ~2.5x |
| **Anthropic** | ~$1B | ~$9B | **~$45B**（2026/5） | **15 个月内 30x** —— 超越 OpenAI |
| **合计** | ~$14B | ~$34B | **~$78B** | ~5.5x |

- Anthropic Q2 2026：首次盈利季（$559M）
- OpenAI：ChatGPT 9 亿周活跃用户；预计 2026 年亏损 $14B
- 70% 的财富 100 企业是 Anthropic 客户
- Claude Code 推出 6 个月内达到 $1B ARR
- Anthropic 80% 收入来自企业

### 超大规模厂商堆栈内嵌的 AI 收入

| 产品 | 付费用户 / 收入 | 备注 |
|------|---------------|------|
| **Microsoft Copilot** | **1500 万付费席位**，$30/用户/月 | 仅此 ~$5.4B ARR；加上 Azure OpenAI |
| **Google Gemini Enterprise** | 捆绑在 Workspace；具体席位数未披露 | 重大但不透明 |
| **AWS Bedrock** | 基础设施（无席位数）；基础模型服务 ~$10B+ ARR | 多模型平台 |
| **Meta AI 驱动广告** | Q4 2025 广告收入 $58B (+24% YoY)；Advantage+ $60B+ ARR；AI 归因 $1B+ 快速 ARR | 巨大：AI 直接贡献几个百分点的广告抬升 |

**估计 2026 年中 AI 软件 + AI 驱动收入：$150-200B 年化**

### 数学差距

| 指标 | 数值 |
|------|------|
| 2026 超大规模厂商资本开支 | ~**$700B** |
| 2026 AI 软件收入（广义） | ~**$150-200B** |
| **差距** | **~$500B 年度** |
| 差距资金来源 | 债务（+$230B 2026）+ FCF 缓冲 + 现有现金 |

**资本开支/AI 收入比：~3.5-4.7x。** 即使收入到 2028 年三倍（$450-600B），也只是赶上 2026 年的水平 —— 而 2027/2028 的资本开支预测更高。

## 1.4 生产力现实（"它有效吗"端）

McKinsey 2025 + BCG 2026 + 多项调查：

| 指标 | 结果 |
|------|------|
| 至少在一项业务功能中使用 AI 的组织 | **88%** |
| 在企业范围内扩展 | 33% |
| 报告任何可测 EBIT 影响 | **39%** |
| "AI 高绩效者"（5%+ EBIT 来自 AI） | **6%** |
| 早期采用者生产力提升 | 15-22% |
| BCG 测量的特定任务收益 | 30-90% |
| 顶级表现者 ROI 倍数 | 5-10x |

**翻译**：革命对 6% 存在。对中位数公司，AI 是一个 15-22% 的生产力工具，对底线影响有限 —— 比 1980 年代的电子表格好，但不在资本开支暗示的规模上。

---

# 第二节 ——第一步草稿答案

## 核心结论（回答"AI 究竟革命了什么？"）

**一个知识工作类别已经被大规模革命：软件工程**。两个相邻类别 —— 广告和客户服务 —— 是**实质改善但未转型**。其他一切（法律、医疗临床、制造、教育、一般知识工作）处于**试点到辅助阶段**，为 6% 的"AI 高绩效者"产生温和生产力收益，其他 94% 是噪音。用户描述的财务结构是正确的：~$1.2T 累计资本开支在 2024-2026 流入，首先被 Nvidia（~$100B+ 净利润）捕获，然后是内存（~$300B+ 收入，各 $1T 市值），然后是元器件供应商（~$150B+ 收入）。终端客户 AI 收入是 $150-200B 年化 —— 真实数字快速增长（纯 AI 公司 100-300%/年），但**比 2026 资本开支小 3-4 倍**。2026-2028 窗口将揭示收入是否扩展到匹配资本开支（合理化供应商超级周期）或差距扩大（触发资本开支回撤和内存/Nvidia 利润池压缩）。**目前证据指向部分验证，非完全合理化** —— 编程是革命是可能的概念验证；广度问题未解决。

## 3 个支持点（革命在它真实的地方是真实的）

**S1. 软件工程已经大规模可证地被转型。**
- 2,000 万+ GitHub Copilot 用户；90% 的财富 100；50,000+ 组织
- 任务完成快 51-55%（受控研究）
- 每个开发者每周节省 3.6 小时
- 日常 AI 用户合并 60% 更多 PR
- 企业试点中 PR 时间从 9.6 天削减到 2.4 天
- 加上 Cursor、Claude Code（6 个月 $1B ARR）、Codeium 等 —— 整个新子行业
- **这是 AI 作为生产力革命的最清晰例子**，由发表研究验证。
→ **论点 → 证据**：GitHub 研究、JetBrains 2026 开发者调查、Accenture-Microsoft 企业研究；特定统计警告：AI 共同撰写的 PR 比纯人类 PR 多 1.7 倍问题（质量抵消）。

**S2. AI 原生软件收入以前所未有的速度增长。**
- Anthropic ARR：$1B（2025/1）→ $45B（2026/5）= **17 个月 30 倍**，企业软件历史最快上升
- OpenAI ARR：18 个月 $13B → $33B（2.5x）
- 1,000+ Anthropic 企业客户每年 $1M+（从 2026/2 的 500 增加）
- 70% 的财富 100 是 Anthropic 客户
- Claude Code 推出 6 个月达到 $1B ARR
- **如果这种增长速度持续，2-3 年内扩展到匹配资本开支**
→ **论点 → 证据**：Anthropic IPO 文件/二级市场；OpenAI 收入新闻；交叉核对企业合同签约；风险：2027 年 ARR 增长放缓将失效。

**S3. 现有服务获得大规模 AI 驱动的增量收益。**
- Meta Q1 2026 收入 +33% YoY；Advantage+ AI 广告 $60B+ ARR；新归因模型 = 24% 转化抬升
- Meta WhatsApp 付费消息 $2B ARR
- Google AI Overviews 改变搜索体验
- AWS Bedrock 基础模型 API 服务 ~$10B+ ARR
- **现有商业模式改善是真实可测的**，即使它们不显示为独立形式的"AI 收入"
→ **论点 → 证据**：Meta 10-Q；AdExchanger 报道；Google Cloud 公告；风险：很难将"AI 抬升"与有机增长分离。

## 2 个反对点（革命未广泛到来）

**O1. 中位企业看到温和到零影响；只有 6% 是"AI 高绩效者"。**
- McKinsey 2025：88% 使用 AI，但只有 **6% 报告 5%+ EBIT 影响**
- 39% 报告任何可测 EBIT 影响 —— 意味着 **61% 看不到底线差异**
- BCG："大多数企业以小试点目标太低"；只有 6% 重新设计了工作流
- **资本开支论点要求 94% 赶上 6%**，不只是温和生产力收益
- 生产力收益在微软、Accenture、Goldman 等公司可见；在中位 S&P 500 EBIT 利润率不可见
→ **论点 → 证据**：McKinsey State of AI 2025；BCG 2026 智能体报告；风险：2026-2027 可能是 94% 赶上的拐点。

**O2. 资本开支与收入比率前所未有且部分循环。**
- $700B 资本开支 vs $150-200B 收入 = 2026 年 **3.5-4.7x 差距**
- 债务资助：2026 行业债务 +$230B
- 自由现金流崩盘：亚马逊 -95%，Alphabet 预计 -90%
- **循环融资**：OpenAI 是 Azure 最大客户之一；Google Cloud 有 $460B AI 积压；许多 AI 初创公司最大费用是支付给超大规模厂商的云
- 资本开支/收入 45-57% 看起来更像公用事业或电信 —— ROE 低的部门
- **历史类比**：电信 2000-2002（类似的资本开支/收入比），铁路 1880 年代

## 明示的未知项

1. **Anthropic 30x 收入增长在 2027 是否会持续或饱和？**
2. **94% 企业是否会赶上 6%？**
3. **生产力收益是否会显示在宏观统计（TFP、人均 GDP）？**
4. **当前 LLM 架构是否到达扩展极限？**
5. **超大规模厂商 2026 资本开支是否真会达到 $700B+，还是会随差距扩大而回撤？**
6. **编程革命：是否泛化到其他知识工作，还是软件特殊？**

---

# 第三节 ——第二步严格审稿

## 3.1 仍需核验的事实

| # | 论断 | 最佳一手源 |
|---|------|----------|
| 1 | "Anthropic ARR $45B 2026/5" | Anthropic IR / 二级市场文件 |
| 2 | "OpenAI ARR $33B Q2 2026" | OpenAI 收入新闻 / SoftBank 报道 |
| 3 | "超大规模厂商 2026 资本开支 $700B+" | MSFT/GOOGL/AMZN/META 最新 Q1 2026 电话会 |
| 4 | "内存公司都 $1T+" | Bloomberg 市场数据 |
| 5 | "微软 1500 万付费 Copilot 席位" | Microsoft Ignite / Q1'26 财报 |
| 6 | "Meta Advantage+ $60B ARR" | Meta Q4 2025 / Q1 2026 纪要 |
| 7 | "McKinsey 6% AI 高绩效者" | McKinsey State of AI 2025 PDF 直接 |
| 8 | "GitHub Copilot 2000 万用户" | GitHub Universe 2025/2026 |
| 9 | "亚马逊 FCF -95%" | 亚马逊 Q1 2026 10-Q |
| 10 | "$230B 行业债务 2026" | CreditSights 科技债务跟踪 |

## 3.2 论证跳步

1. **"软件工程 = 革命；其他 = 辅助"** —— 二元框架；现实是光谱。客户服务正在被实质性重组（如 Salesforce、Klarna 显著的人员变化）。可论证客户服务也是"被革命"。
2. **"3.5-4.7x 数学差距不可持续"** —— 假设需要 5-7 年摊销才能合理化。如果 GPU/资产寿命延长或收入按 100%/年复合，差距可能缩小。
3. **"Anthropic 30x 增长扩展到革命"** —— 从 17 个月期间外推，包括编程工具发布。可能是一次性企业捕获，非持续。
4. **"资本开支-收入比看起来像电信/公用事业"** —— 类比不完美；AI 基础设施同时具有网络（商品）和战略（认知）特性。
5. **"只有 6% 高绩效者 = 主要是炒作"** —— 同样的 6% 统计在 2005-2010 年早期 SaaS 采用是真的，到 2020 变得普遍。拐点动态可能重复。

## 3.3 缺失反例

1. **编程可能不会泛化**：代码有独特属性（结构化、可验证、模块化、句法约束）。AI 对代码有效不一定意味它对法律简报、财务分析或运营管理有效。
2. **"94% 落后者"可能包括 AI 怀疑行业**（制造、政府、农业）—— 它们就是不会由 AI 引领。
3. **生产力收益可能被雇主捕获**，不创造新收入。
4. **能源瓶颈**：超大规模厂商资本开支现在受电力可用性约束，不是芯片可用性。
5. **AGI / 扩展定律不确定性**：如果 AI 能力到达平台期（GPT-6 没有比 GPT-5 显著更好），整个收入论点弱化。
6. **计算价格下降**：GPU 寿命、模型效率和推理 token 成本都在每年改善 2-4x。

## 3.4 最该补的一手来源

1. McKinsey State of AI 2025 PDF（直接，非摘要）
2. BCG AI 成熟度调查 2026（完整报告）
3. Anthropic 最新融资文件 / IPO S-1
4. OpenAI 收入确认数字（SoftBank / 微软交叉核对）
5. 超大规模厂商 Q1 2026 财报电话会议纪要（资本开支指引）
6. GitHub Octoverse 2026
7. 美联储 TFP / 生产力数据 2024-2026
8. SemiAnalysis HBM 市场报告
9. Allianz / CreditSights AI 资本开支可持续性论文
10. 独立学术研究编程工具生产力（CACM 文章）

## 3.5 仍属推测的句子

| # | 陈述 | 状态 |
|---|------|------|
| 1 | "2026-2028 窗口将揭示收入是否扩展到资本开支" | **条件预测** |
| 2 | "Anthropic 30x 增长，如果持续，2-3 年内扩展到资本开支" | **线性外推** |
| 3 | "只有 6% AI 高绩效者意味革命未广泛到来" | **解释性主张** |
| 4 | "资本开支-收入比不可持续" | **取决于摊销期 + 增长率假设** |
| 5 | "编程可能不泛化到其他知识工作" | **未测试假设** |
| 6 | "软件工程是唯一被完全革命的类别" | **模式识别；可争议截止点** |
| 7 | "Meta AI 抬升 = 广告收入的几个百分点" | **从披露指标估计** |
| 8 | "$1.2T 累计资本开支" | **从单独披露求和** |
| 9 | "亚马逊自由现金流 -95%" | **季度数字；可能恢复** |
| 10 | "2027 是拐点" | **主观预测** |

---

# 第四节 ——诚实综合 + 开放讨论

## 数据实际告诉我们什么

**多头案（最强表述）**：
- 收入正在以前所未有的速度扩展（Anthropic 17 个月 30 倍 —— 没有 SaaS 公司做过）
- 编程工具革命证明技术可以转型知识工作 —— 这是广度问题，不是能力问题
- Meta $60B+ AI 驱动广告 ARR 显示超大规模厂商在自己业务内回收 AI 投资，不只是卖给初创公司
- 内存/Nvidia 利润率只有 AI 能力到达平台期时才看起来泡沫；如果继续扩展，供应商寡头垄断可能持续 5-10 年
- 2026 年中 6% 企业是"AI 高绩效者"看起来像 2008 年 6% 是"SaaS 原生" —— 早期周期，非终态
- AI 基础设施有 5-7 年摊销；比较 1 年资本开支与 1 年收入低估真实经济

**空头案（最强表述）**：
- $1.2T 累计资本开支 vs $150-200B 年化收入 = 没有从这里 5x 收入增长，数学不通
- 由债务越来越多地资助；FCF 崩盘
- 循环融资（OpenAI → 微软 → Azure → ...）抬高表面收入
- 94% 企业未受益意味着 AI 可能更像 CRM（有用工具）而非电力（通用转型）
- 宏观生产力统计还未显示 AI 红利（鉴于投资规模，这是担忧）
- 编程工具成功不泛化：代码是独特结构化的
- 历史类比（电信 2000-02、铁路 1880 年代）结局不好，尽管真实长期效用

**我的诚实综合**：

用户的框架 —— *"万亿美元内存公司 + Nvidia 拿走利润；实际 AI 使用有限"* —— 捕获了 2026 年中的**资产负债表真相**，但低估了**增长导数**。纯 AI 收入增长（100-300%/年）与过去科技泡沫结构性不同（电信 2001、互联网 2000 都是收入增长在资本开支之前放缓）。这里，**2026 年中收入增长仍在加速**。话虽如此，**数学差距作为 3 年路径确实不可持续** —— 如果收入到 2028 年没有从这里 3-5x，预期资本开支回撤和供应商股票倍数压缩。

**最重要的单一问题**：*AI 编程模式（真正 50% 生产力收益、广泛采用）是否到 2028 年在 2-3 个其他主要知识工作类别复制？* 如果是 —— 完全革命，资本开支合理，供应商寡头持久。如果否 —— 部分革命像互联网（真实但比炒作窄），资本开支回撤，供应商倍数压缩但底层技术持续。

**多空概率（主观）**：55% 多头，35% 中间，10% 空头。Anthropic 30x 增长是反对空头案的最大单一论据 —— 这种速度不会发生在虚假革命中。

## 我会和你辩论的

1. **你说"AI 实际使用规模仍然相当有限"** —— 我会反驳。9 亿周活 ChatGPT 用户 + 2000 万 Copilot 席位 + 70% F100 用 Anthropic = **使用不有限**。**有限**的是**广泛企业 EBIT 影响**（只有 6% 看到 >5%）。使用 ≠ 经济转型。也许你想表达的区别是"转型"？
2. **你将价值捕获归因于 Mag7 → Nvidia → 内存/元器件 —— 正确，但你可能低估 Meta AI 广告贡献**。Meta 的 $60B+ Advantage+ ARR 和 24% YoY 广告增长是 AI 价值，*不显示为单独 AI 收入* —— 它显示为核心业务收入抬升。同样的更微妙地发生在 Google 和亚马逊。
3. **你暗示这是单向循环** —— 但 Anthropic 刚有第一个盈利季并达到 $45B ARR。那不是超大规模厂商补贴；那是 70% 财富 100 的真实客户付款。循环论据在 2023-2024 强；正在快速弱化。
4. **我 100% 同意你的地方**：万亿美元内存市值相对于"被革命"足迹看起来拉伸。如果我必须做空什么，那将是在资本开支适度的下一个迹象时做空内存 —— 历史上价值链最周期性的部分。

## 我会发现真正不确定的开放问题

- Anthropic 增长是编程驱动的（可饱和）还是通用知识工作驱动的（持久）？
- Microsoft Copilot 1500 万付费席位到 2027 年是增长到 1 亿+ 还是停滞？
- Meta AI 广告护城河是巩固（变得不可替代）还是商品化（每个广告网络采用类似技术）？
- H100/B200 实际寿命是 3 年还是 6+？对资本开支摊销数学很重要。
- 物理 AI（机器人、自动驾驶）2026-2028 是否会加速以增加另一个计算需求向量？

---

## 一手来源

### 资本开支
1. Visual Capitalist — *The Rise of AI Hyperscaler Spending*: https://www.visualcapitalist.com/the-rise-of-ai-hyperscaler-spending/
2. CNBC — *Google, Meta, Amazon, Microsoft spending on AI*: https://www.cnbc.com/2025/10/31/tech-ai-google-meta-amazon-microsoft-spend.html
3. CNBC — *Tech AI spending approaches $700 billion in 2026*: https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html
4. Allianz Research — *AI capex cycle*: https://www.allianz.com/content/dam/onemarketing/azcom/Allianz_com/economic-research/publications/specials/en/2026/march/2026_03_25_AI.pdf
5. CreditSights — *Hyperscaler Capex 2026*: https://know.creditsights.com/insights/technology-hyperscaler-capex-2026-estimates/

### 内存 / HBM 万亿美元俱乐部
6. Morningstar — *SK Hynix, Micron Trillion-Dollar Club*: https://www.morningstar.com/news/dow-jones/202605271274/sk-hynix-micron-join-trillion-dollar-club-update
7. US News — *SK Hynix Joins $1 Trillion Club*: https://money.usnews.com/investing/news/articles/2026-05-26/sk-hynix-joins-1-trillion-club-after-samsung-micron-on-ai-chip-boom
8. CurrentAffair — *HBM Memory Chip Supercycle 2026*: https://www.currentaffair.today/blog/finance-9/hbm-memory-chip-supercycle-2026-how-sk-hynix-micron-and-samsung-formed-the-newest-1-trillion-club-747

### AI 软件收入
9. OpenTools — *Anthropic Revenue Hits $45B ARR*: https://opentools.ai/news/anthropic-revenue-surpasses-openai
10. IDLEN — *Anthropic Passes OpenAI October 2026 IPO*: https://www.idlen.io/news/anthropic-overtakes-openai-30-billion-revenue-april-2026/

### 生产力 / ROI
11. McKinsey — *State of AI 2025 PDF*: https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/the%20state%20of%20ai/november%202025/the-state-of-ai-2025-agents-innovation_cmyk-v1.pdf
12. BCG via n5r — *AI Agents Deliver 30-90% ROI Gains*: https://n5r.com/en-us/blog/bcg-ai-agents-mcp-a2a-enterprise-roi-agent-economy

### 编程工具革命
13. GitHub — *Quantifying Copilot impact with Accenture*: https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/
14. JetBrains — *Which AI Coding Tools Do Developers Use* (2026/4): https://blog.jetbrains.com/research/2026/04/which-ai-coding-tools-do-developers-actually-use-at-work/

### Meta AI 广告
15. PPC Land — *Meta's ad business hits record $58B*: https://ppc.land/metas-ad-business-hits-record-58b-as-ai-drives-conversion-gains/
16. Facebook About — *2026: AI Drives Performance*: https://about.fb.com/news/2026/01/2026-ai-drives-performance/

### 泡沫 / 循环融资
17. AI2.Work — *Hyperscalers Pledge $725B While Revenue Lags*: https://ai2.work/blog/hyperscalers-pledge-725b-in-ai-capex-while-revenue-returns-lag-behind
18. Cresset — *2026 Outlook: Is AI a Bubble?*: https://cressetcapital.com/articles/market-update/market-update-12-17-25-2026-outlook-is-ai-a-bubble/

### Microsoft Copilot 采用
19. Stackmatix — *Copilot Adoption 2026*: https://www.stackmatix.com/blog/copilot-market-adoption-trends
20. EPC Group — *Copilot vs Gemini Enterprise 2026*: https://www.epcgroup.net/microsoft-copilot-vs-google-gemini-enterprise-comparison

---

*应用两步研究协议。**不构成投资建议**。个人观点：当前 AI 资本开支超级周期被 2026-2028 收入扩展合理化的概率为 55% 多头 / 35% 中间 / 10% 空头。在新数据上保持开放。*

---

*English version: [report_en](report_en)*
