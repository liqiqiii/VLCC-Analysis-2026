# tail_hedge/ — Tail-Hedging & Convexity: 50-Year Backtest

Empirical test of the Taleb/Spitznagel tail-hedging (convexity) thesis on **50 years
of real S&P 500 total return (1974-08 → 2024-07)**, using Robert Shiller's monthly
*Real Total Return Price* (dividends reinvested, CPI-adjusted). A companion study
([`report_vlcc_en.md`](report_vlcc_en.md)) applies the same logic to **VLCC equities
(DHT/FRO)** with a **win-rate-vs-VRP / break-even-VRP framework**.

## Contents

| File | What |
|---|---|
| [`summary_en.md`](summary_en.md) / [`summary_cn.md`](summary_cn.md) | **Cheat-sheet: 7-asset cross-asset decision table (topic hub)** |
| [`report_en.md`](report_en.md) / [`report_cn.md`](report_cn.md) | S&P study (EN/CN) — GitHub Pages |
| [`report_vlcc_en.md`](report_vlcc_en.md) / [`report_vlcc_cn.md`](report_vlcc_cn.md) | **VLCC (DHT/FRO) study + win-rate-vs-VRP framework (EN/CN)** |
| [`report_sectors_en.md`](report_sectors_en.md) / [`report_sectors_cn.md`](report_sectors_cn.md) | **Financials (XLF) & Technology (XLK) study — hold-vs-hedge suitability (EN/CN)** |
| [`run_backtest.py`](run_backtest.py) | Reproducible monthly backtest; regenerates the monthly CSVs in `data/` |
| [`run_backtest_daily.py`](run_backtest_daily.py) | **Daily** path-dependent backtest: ladder, lagged-redeploy control, and Universa-style variant (§7 of the report) |
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
| `data/results_daily_universa_core.csv` | **Daily**: Universa-style variant (F) core-fraction sensitivity + 2020 outcome |
| `data/results_daily_crash_episodes.csv` | **Daily**: crash-window returns + trough drawdowns (Buy&Hold / D / F) |
| [`run_backtest_vlcc.py`](run_backtest_vlcc.py) | **VLCC** convexity backtest (DHT/FRO) + win-rate-vs-VRP + break-even VRP |
| `data/{dht,fro}_daily_2005_2024.csv` | DHT/FRO daily adjusted close (yfinance) |
| `data/results_vlcc_profile.csv` | VLCC vs S&P vol / drawdown profile |
| `data/results_vlcc_hedge_grid.csv` | DHT/FRO strike × tenor × VRP: CAGR / maxDD |
| `data/results_vlcc_winrate_vrp.csv` | per-VRP win-rate, expectancy, payoff ratio, CAGR delta |
| `data/results_vlcc_breakeven_vrp.csv` | expectancy & CAGR break-even VRP (DHT 67% / FRO 0% / S&P 0%) |
| `data/results_vlcc_reliability.csv` | annual underlying return vs hedge P&L (convexity / lumpiness) |
| [`run_backtest_vlcc_windows.py`](run_backtest_vlcc_windows.py) | sub-window break-even VRP robustness + LIVE option paid-VRP calibration |
| `data/results_vlcc_breakeven_windows.csv` | break-even VRP by window (DHT 67% full → 0% in 2013+/2019+) |
| `data/results_vlcc_paid_vrp.csv` | live DHT/FRO ~30%-OTM put IV → paid VRP (DHT ≈33%, FRO ≈26–31%) |
| [`run_backtest_sectors.py`](run_backtest_sectors.py) | Financials (XLF) & Technology (XLK) convexity backtest + break-even spectrum |
| `data/{xlf,xlk}_daily_1998_2024.csv` | XLF/XLK daily adjusted close (yfinance) |
| `data/results_sector_profile.csv` | XLF/XLK/S&P vol / maxDD / CAGR |
| `data/results_sector_breakeven_windows.csv` | sector break-even VRP by window (XLK 27% full → 0% post-2010) |
| `data/results_sector_winrate_vrp.csv` | per-VRP win-rate, payoff, CAGR delta (XLF/XLK/S&P) |
| `data/results_sector_hedge_grid.csv` | XLF/XLK strike × tenor × VRP |
| `data/results_sector_reliability.csv` | annual underlying vs hedge P&L |
| `data/results_sector_paid_vrp.csv` | live XLK ≈24% paid VRP (XLF LEAPS puts too thin) |
| `data/results_breakeven_spectrum.csv` | S&P/XLF/XLK/DHT/FRO break-even VRP side by side |
| [`run_backtest_stocks.py`](run_backtest_stocks.py) | JPM/AXP quality-name backtest (§6 of sector report) |
| `data/{jpm,axp}_daily_1998_2024.csv` | JPM/AXP daily adjusted close (yfinance) |
| `data/results_stock_profile.csv` | JPM/AXP vol / maxDD / CAGR |
| `data/results_stock_breakeven_windows.csv` | JPM/AXP break-even VRP by window (all ~0%) |
| `data/results_stock_winrate_vrp.csv` | per-VRP win-rate / CAGR delta (JPM/AXP) |
| `data/results_stock_hedge_grid.csv` | JPM/AXP strike × VRP grid |
| `data/results_stock_paid_vrp.csv` | live JPM/AXP put paid VRP (~100%!) |
| `data/results_breakeven_spectrum_full.csv` | full spectrum incl JPM/AXP |

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
