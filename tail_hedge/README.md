# tail_hedge/ — Tail-Hedging & Convexity: 50-Year Backtest

Empirical test of the Taleb/Spitznagel tail-hedging (convexity) thesis on **50 years
of real S&P 500 total return (1974-08 → 2024-07)**, using Robert Shiller's monthly
*Real Total Return Price* (dividends reinvested, CPI-adjusted).

## Contents

| File | What |
|---|---|
| [`report_en.md`](report_en.md) | Full write-up (EN) — GitHub Page |
| [`report_cn.md`](report_cn.md) | 中文版 — GitHub Page |
| [`run_backtest.py`](run_backtest.py) | Reproducible monthly backtest; regenerates the monthly CSVs in `data/` |
| [`run_backtest_daily.py`](run_backtest_daily.py) | **Daily** path-dependent backtest of the monetize-ladder (§7 of the report) |
| `data/shiller_real_tr_monthly_1974_2024.csv` | Derived monthly input series (Date, RealTRP, ret) |
| `data/sp500_daily_close_1974_2024.csv` | Daily ^GSPC close 1974-2024 (Yahoo/yfinance) — input for the daily test |
| `data/results_baseline_barbell.csv` | Buy&Hold + cash-barbell (AQR "just de-risk") |
| `data/results_monthly_put_hedge.csv` | Rolling 1-month OTM put, BS-priced (strike × VRP grid) |
| `data/results_leaps_put_hedge.csv` | Rolling 12-month (LEAPS) put grid — the long-dated design |
| `data/results_equal_drawdown.csv` | Hedge vs cash barbell tuned to equal max drawdown |
| `data/results_tail_shape.csv` | Skew / kurtosis / worst-month (left-tail clipping) |
| `data/results_crash_episodes.csv` | Convex payoff across the 5 major crashes (monthly) |
| `data/results_daily_ladder.csv` | **Daily**: Buy&Hold vs passive vs ladder→cash vs ladder→equity (lagged E & immediate D) |
| `data/results_daily_redeploy_lag.csv` | **Daily**: dip-timing control — CAGR by redeploy lag (0/5/20/60/120d/cash) |
| `data/results_daily_crash_episodes.csv` | **Daily**: crash-window returns + trough drawdowns (reveals the 2020 failure mode) |

## Reproduce

```
cd tail_hedge
python run_backtest.py
```

Requires `pandas` (+ `xlrd` only if re-parsing the raw Shiller `.xls`). The committed
derived CSV makes the run reproducible without re-downloading.

## Headline finding

Convex tail-hedging **raises the geometric return and slashes tail risk when protection
is cheap and long-dated**, but at realistic option pricing it costs ~0.4–1.4%/yr of CAGR
— it is disciplined *ruin-insurance that complements Kelly*, not standalone alpha.
**Price (the vol-risk-premium), tenor/strike, and disciplined monetization decide everything.**

> Caveat: Shiller monthly prices are month-averages → fast crashes (1987, 2020) are
> smoothed → hedge value here is **conservative**. Gross of tax/transaction costs.
> Education/analysis, not investment advice.
