import os

def rf(p):
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()

def wf(p, c):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

# EN prompt log
en = rf('Prompt_Log_EN.md')
marker = '*This file will be updated as new prompts are added. Last updated: March 4, 2026.*'
p21 = """
## Prompt 21: Cyclical Stock Rules (Two-Cycle Backtrack)
**Date**: March 4, 2026

Create cyclical-stock-specific rules in the framework/ folder. Key additions:
- **CRule 1 (Two-Cycle Backtrack)**: For every cyclical stock, find the two most recent cycles, backtrack stock price vs commodity/rate correlation (R-squared, lead/lag), map current position to historical cycle anatomy, and predict where we are now.
- CRule 2-10: PE compression patterns, supply-demand duration, operating leverage multiplier, contrarian timing indicators, cross-cycle reference, earnings sensitivity matrix, exit strategy framework, inflation-adjusted comparison, shadow/grey market monitoring.

User's specific rule (CRule 1): "Find the two most recent cycles, do a backtrack of stock price vs raw material rate (e.g., tungsten price, VLCC rate). See the correlation, give basic analysis based on past cycles, predict where we are in the cycle now based on historical data."

---

"""
en = en.replace(marker, p21 + marker)
wf('Prompt_Log_EN.md', en)
print('EN:', 'Prompt 21' in rf('Prompt_Log_EN.md'))

# CN prompt log
cn = rf('Prompt_Log_CN.md')
mcn = '*\u672c\u6587\u4ef6\u5c06\u968f\u65b0\u63d0\u793a\u8bcd\u7684\u589e\u52a0\u800c\u66f4\u65b0\u3002\u6700\u540e\u66f4\u65b0\uff1a2026\u5e743\u67084\u65e5\u3002*'
p21cn = """
## \u63d0\u793a\u8bcd21\uff1a\u5468\u671f\u80a1\u89c4\u5219\uff08\u53cc\u5468\u671f\u56de\u6eaf\uff09
**\u65e5\u671f**\uff1a2026\u5e743\u67084\u65e5

\u5728framework/\u6587\u4ef6\u5939\u4e2d\u521b\u5efa\u5468\u671f\u80a1\u4e13\u9879\u89c4\u5219\u3002\u6838\u5fc3\u65b0\u589e\uff1a
- **\u5468\u671f\u89c4\u52191\uff08\u53cc\u5468\u671f\u56de\u6eaf\uff09**\uff1a\u5bf9\u6bcf\u53ea\u5468\u671f\u80a1\uff0c\u627e\u51fa\u6700\u8fd1\u4e24\u4e2a\u5b8c\u6574\u5468\u671f\uff0c\u56de\u6eaf\u80a1\u4ef7vs\u5927\u5b97\u4ef7\u683c/\u8d39\u7387\u7684\u76f8\u5173\u6027\uff08R\u00b2\u3001\u9886\u5148/\u6ede\u540e\uff09\uff0c\u5c06\u5f53\u524d\u4f4d\u7f6e\u6620\u5c04\u5230\u5386\u53f2\u5468\u671f\u89e3\u5256\u4e2d\uff0c\u9884\u6d4b\u6211\u4eec\u73b0\u5728\u5904\u4e8e\u54ea\u4e2a\u9636\u6bb5\u3002
- \u5468\u671f\u89c4\u52192-10\uff1aPE\u538b\u7f29\u6a21\u5f0f\u3001\u4f9b\u9700\u6301\u7eed\u65f6\u95f4\u3001\u7ecf\u8425\u6760\u6746\u500d\u589e\u5668\u3001\u9006\u5411\u65f6\u673a\u6307\u6807\u3001\u8de8\u5468\u671f\u53c2\u7167\u3001\u76c8\u5229\u654f\u611f\u6027\u77e9\u9635\u3001\u9000\u51fa\u7b56\u7565\u6846\u67b6\u3001\u901a\u80c0\u8c03\u6574\u3001\u5f71\u5b50\u5e02\u573a\u76d1\u63a7\u3002

\u7528\u6237\u7279\u5b9a\u89c4\u5219\uff08\u5468\u671f\u89c4\u52191\uff09\uff1a\"\u627e\u51fa\u6700\u8fd1\u4e24\u4e2a\u5468\u671f\uff0c\u56de\u6eaf\u80a1\u4ef7vs\u539f\u6750\u6599\u4ef7\u683c\uff08\u5982\u94a8\u4ef7\u683c\u3001VLCC\u8fd0\u8d39\uff09\u7684\u76f8\u5173\u6027\uff0c\u57fa\u4e8e\u5386\u53f2\u5468\u671f\u7ed9\u51fa\u57fa\u672c\u5206\u6790\uff0c\u9884\u6d4b\u6211\u4eec\u73b0\u5728\u5904\u4e8e\u5468\u671f\u7684\u54ea\u4e2a\u4f4d\u7f6e\u3002\"

---

"""
cn = cn.replace(mcn, p21cn + mcn)
wf('Prompt_Log_CN.md', cn)
print('CN:', '\u63d0\u793a\u8bcd21' in rf('Prompt_Log_CN.md'))
