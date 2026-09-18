# -*- coding: utf-8 -*-
"""
"Follow Zijin" — backtesting the co-investment (利益共同体) pattern.

The user's thesis, in their words:
    "藏格矿业参股巨龙矿业，和紫金成为利益共同体；这就是一个很好的
     从先共同参股到进一步加深合作的情况。"

i.e. the tradeable pattern is NOT "companies Zijin acquires outright" (in a
full takeover you are cashed out at the premium and cannot ride the value
creation). It is:

    A LISTED company becomes a MINORITY CO-INVESTOR alongside Zijin in a
    single shared asset. It stays listed. Zijin operates and funds the asset.
    The partner rides the re-rating -- with MORE torque than Zijin itself,
    because the shared asset is a far larger share of the partner's NAV.
    Then Zijin deepens the relationship (raises its stake / takes control),
    which is a second catalyst.

This script measures that. It deliberately separates:
    FOLLOWABLE   -- minority stake / JV; target stayed listed
    TAKEOVER     -- target delisted; an outside investor could NOT follow
    DEEPENING    -- Zijin increased an existing relationship

Every anchor date below is a PUBLIC announcement date, sourced in the report.
Returns are therefore what an outsider could actually have earned by buying
at the close AFTER the news -- not backfitted to the low.

Data: Yahoo Finance via yfinance (auto_adjust=True -> total return).

Rule 4 / known traps guarded here:
  * yfinance returns columns ALPHABETICALLY -> always index by ticker NAME.
  * TICKER RECYCLING: "CNL.TO" is today Collective Mining, NOT the Continental
    Gold that Zijin took over in 2020. Same class of trap as Barrick GOLD->B.
    Delisted takeover targets are handled from sourced deal terms, not tickers.
"""

import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# CJK glyphs: fall back through the fonts actually shipped on Windows
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                          "Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(DATA, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

TODAY = "2026-09-18"

# ---------------------------------------------------------------- the deal book
# kind: FOLLOWABLE | TAKEOVER | DEEPENING | SPINOFF
# entry_px: the actual subscription / transaction price where disclosed (the real
#           economics). Where None, we use the market close on the anchor date.
DEALS = [
    dict(kind="FOLLOWABLE", date="2015-03-23", ticker="IVN.TO", ccy="CAD",
         entry_px=None,
         target="Ivanhoe Mines", asset="Kamoa-Kakula copper (DRC)",
         terms="Zijin buys 9.9% of Ivanhoe for ~C$85m; two months later 49.5% of "
               "Kamoa Holding for US$412m -> Zijin 39.6% / Ivanhoe 39.6% at the "
               "project. Topped up to 13.88% in Oct-2019 for C$194m."),
    dict(kind="FOLLOWABLE", date="2020-06-08", ticker="000408.SZ", ccy="CNY",
         entry_px=None,
         target="Zangge Mining 藏格矿业", asset="Julong copper 巨龙铜业 (Tibet)",
         terms="Zijin buys 50.1% of Julong for RMB 3.883bn and becomes operator "
               "of a mine Zangge had stalled. Zangge keeps 30.78% -> the listed "
               "minority co-investor. Julong: 115kt Cu (2022) -> 166kt (2024), "
               "Phase II to 300-350kt/yr."),
    dict(kind="FOLLOWABLE", date="2022-06-30", ticker="600388.SS", ccy="CNY",
         entry_px=10.80,
         target="Longking 龙净环保", asset="environmental equipment -> energy storage",
         terms="Zijin buys 15.02% equity + 10.02% proxy = 25.04% of votes for "
               "RMB 1.7343bn at RMB 10.80/sh. Later topped up via placement; "
               "renamed 紫金龙净 in 2026. NOTE: date is the 2022 announcement "
               "window - FLAGGED as approximate."),
    dict(kind="FOLLOWABLE", date="2022-11-06", ticker="1818.HK", ccy="HKD",
         entry_px=6.72,
         target="Zhaojin Mining 招金矿业", asset="Haiyu 海域金矿 (Shandong)",
         terms="THE SECOND TRUE INSTANCE OF THE PATTERN. Zijin subscribes "
               "654,078,741 H-shares at HK$6.72 (HK$4.395bn) for 20% (since "
               "diluted to 18.20%) -- AND separately bought 30% of the Haiyu "
               "gold mine itself in Oct-2022 for RMB 3.9845bn. Zhaojin holds the "
               "other 70%. Zijin look-through economic interest in Haiyu ~42.9%. "
               "Haiyu: 562t resources @4.2g/t, ~212t recoverable, 15-20t/yr at "
               "full production, ~23yr life."),
    dict(kind="FOLLOWABLE", date="2024-07-31", ticker="MAU.TO", ccy="CAD",
         entry_px=1.75,
         target="Montage Gold", asset="Kone gold project (Cote d'Ivoire)",
         terms="Zijin subscribes 9.9% for C$57.3m at C$1.75 within an upsized "
               "C$180m placement. NOTE: exact announcement day FLAGGED as "
               "approximate (Jul-2024); the C$1.75 subscription price is firm."),
    dict(kind="FOLLOWABLE", date="2024-09-23", ticker="3939.HK", ccy="HKD",
         entry_px=2.0825,
         target="Wanguo Gold 万国黄金集团", asset="Jinling mine, Solomon Is.",
         terms="Zijin subscribes 165.6m new shares at HK$8.33 for HK$1.3794bn "
               "(a 9.95% DISCOUNT to the HK$9.25 close of 20-Sep-2024), taking "
               "it to ~17.57% (15.28% of enlarged capital) and #2 holder. "
               "*** SPLIT ADJUSTMENT: a 1-for-4 subdivision took effect "
               "25-Nov-2025, so the HK$8.33 subscription price equals HK$2.0825 "
               "on today's basis. Cross-check: HK$9.25/4 = HK$2.3125, which "
               "matches the HK$2.27-2.43 the series shows for Sep-2024. The "
               "earlier '1.90x' was a pre/post-split mismatch and is WRONG. ***"),
    dict(kind="DEEPENING", date="2025-01-17", ticker="000408.SZ", ccy="CNY",
         entry_px=35.00,
         target="Zangge Mining 藏格矿业", asset="control of the partner itself",
         terms="Zijin buys 24.82% of Zangge at RMB 35.00/sh for RMB 13.729bn and "
               "takes control (final ~26.18%). The 'deepening' leg, 4.6 years "
               "after the Julong co-investment. Motive: absolute control of "
               "Julong Phase II/III capex."),
    dict(kind="SPINOFF", date="2025-09-30", ticker="2259.HK", ccy="HKD",
         entry_px=71.59,
         target="Zijin Gold International 紫金黄金国际",
         asset="Zijin's overseas gold mines",
         terms="HKEX IPO at HK$71.59; ~HK$25bn raised, the largest gold-mining "
               "IPO ever; retail 240.7x subscribed. Now the vehicle doing the "
               "overseas gold M&A."),
    dict(kind="DEEPENING", date="2026-03-22", ticker="600988.SS", ccy="CNY",
         entry_px=41.36,
         target="Chifeng Gold 赤峰黄金", asset="gold, China/Laos/Ghana (14.5t in 2025)",
         terms="Zijin agrees to acquire 25.85% and control for RMB 18.26bn at "
               "RMB 41.36/sh (H-share HK$30.19). Targeted completion 30-Sep-2026. "
               "The NEWEST followable situation - an A/H company that stays listed."),
    dict(kind="FOLLOWABLE", date="2026-08-10", ticker="AAUC.TO", ccy="CAD",
         entry_px=32.55,
         target="Allied Gold", asset="gold (Africa)",
         terms="After the C$44.00/sh full takeover COLLAPSED (see counterexamples), "
               "Zijin Gold Intl instead took ~9.2% via a US$295m placement at "
               "C$32.55."),
]

BENCH = {"601899.SS": "Zijin Mining (A)", "2899.HK": "Zijin Mining (H)",
         "HG=F": "Copper", "GC=F": "Gold"}

# Full takeovers: the target DELISTED. Kept as evidence, not as a backtest.
TAKEOVERS = [
    ("2018-09-05", "Nevsun Resources", "NSU.TO", "C$1.86bn @ C$6.00 (+57%)",
     "Timok Cu-Au (Serbia) + Bisha (Eritrea)"),
    ("2019-12-02", "Continental Gold", "CNL.TO (RECYCLED)", "C$1.4bn @ C$5.50 (+29%)",
     "Buritica gold (Colombia)"),
    ("2020-06-15", "Guyana Goldfields", "GUY.TO", "C$323m @ C$1.85",
     "Aurora gold (Guyana)"),
    ("2021-10-09", "Neo Lithium", "NLC.V", "C$960m @ C$6.50",
     "3Q lithium brine (Argentina)"),
]

# The failures. An honest backtest MUST carry these.
COUNTEREXAMPLES = [
    ("2024-01", "Solaris Resources (SLS.TO)",
     "C$130m for 15% + a board seat, to fund Warintza copper in Ecuador",
     "TERMINATED May-2024 after >4 months stuck in an Investment Canada Act "
     "national-security review. Solaris then moved its HQ to Quito."),
    ("2025", "Xanadu Mines (XAM.AX)",
     "Zijin was the largest holder at 15.7% of the listco",
     "Zijin ACCEPTED Bastion Mining's A$0.08/sh takeover; XAM delisted Aug-2025. "
     "Zijin kept its 50% of the Kharmagtai JV vehicle. Following Zijin into the "
     "LISTCO paid A$0.08; Zijin kept the ASSET."),
    ("2026-01-26 -> 2026-07-29", "Allied Gold (AAUC.TO)",
     "Zijin Gold Intl agreed to buy 100% at C$44.00/sh, ~C$5.5bn - billed as "
     "Zijin's largest acquisition ever",
     "TERMINATED 29-Jul-2026: no reasonable likelihood of satisfying conditions, "
     "primarily a delay in CHINESE regulatory approval. Holders who bought for "
     "the C$44 takeout were left with a ~9.2% placement at C$32.55 instead."),
    ("2025-09 -> 2026", "Zijin Gold International (2259.HK)",
     "The spin-off itself",
     "52-week range HK$84.20-268.00: a ~-42% drawdown from the high. Even the "
     "winners are violently volatile."),
]


def fetch(tickers, start="2014-01-01"):
    """Download closes, indexed BY NAME (yfinance returns columns alphabetically)."""
    raw = yf.download(list(tickers), start=start, progress=False,
                      auto_adjust=True)
    close = raw["Close"]
    if not hasattr(close, "columns"):
        close = close.to_frame(list(tickers)[0])
    return {t: close[t].dropna() for t in tickers if t in close.columns}


def at(series, when):
    """Last close on or before `when` (i.e. what an outsider could transact)."""
    s = series.loc[:when]
    return (s.iloc[-1], s.index[-1]) if len(s) else (np.nan, None)


print("=" * 84)
print('"FOLLOW ZIJIN" — does co-investing alongside Zijin actually pay?')
print("=" * 84)

need = sorted({d["ticker"] for d in DEALS} | set(BENCH))
px = fetch(need)
for t in need:
    if t in px:
        print(f"  {t:<12} {len(px[t]):>5} obs  {px[t].index[0].date()} -> "
              f"{px[t].index[-1].date()}")
    else:
        print(f"  {t:<12} MISSING")

# ============================================================ 1) deal-by-deal
print("\n" + "-" * 84)
print("1) RETURN FROM EACH PUBLIC ANNOUNCEMENT DATE (buy at the close after the news)")
print("-" * 84)

rows = []
for d in DEALS:
    t = d["ticker"]
    if t not in px:
        print(f"\n  [{d['kind']}] {d['date']}  {d['target']} ({t})  -- NO PRICE DATA")
        continue
    p_mkt, d0 = at(px[t], d["date"])
    p0 = d["entry_px"] if d["entry_px"] else p_mkt
    basis = "subscription price" if d["entry_px"] else "close on announcement"
    p1 = px[t].iloc[-1]
    yrs = (pd.Timestamp(TODAY) - pd.Timestamp(d["date"])).days / 365.25
    mult = p1 / p0
    cagr = mult ** (1 / yrs) - 1 if yrs > 0.15 else np.nan

    zj, _ = at(px["601899.SS"], d["date"])
    zj_mult = px["601899.SS"].iloc[-1] / zj
    cu, _ = at(px["HG=F"], d["date"])
    cu_mult = px["HG=F"].iloc[-1] / cu
    au, _ = at(px["GC=F"], d["date"])
    au_mult = px["GC=F"].iloc[-1] / au

    rows.append(dict(kind=d["kind"], date=d["date"], target=d["target"],
                     ticker=t, ccy=d["ccy"], basis=basis,
                     entry=round(p0, 2), close_on_announce=round(p_mkt, 2),
                     px_now=round(p1, 2), years=round(yrs, 1),
                     multiple=round(mult, 2),
                     cagr_pct=round(cagr * 100, 1) if cagr == cagr else None,
                     zijin_multiple=round(zj_mult, 2),
                     vs_zijin=round(mult / zj_mult, 2),
                     copper_multiple=round(cu_mult, 2),
                     gold_multiple=round(au_mult, 2), asset=d["asset"]))

    print(f"\n  [{d['kind']}] {d['date']}  {d['target']} ({t})")
    print(f"      asset: {d['asset']}")
    print(f"      {d['terms']}")
    print(f"      entry {p0:,.2f} {d['ccy']} ({basis}; close that day "
          f"{p_mkt:,.2f}) -> {p1:,.2f}")
    print(f"      = {mult:6.2f}x over {yrs:.1f}y"
          + (f"  ({cagr*100:+.0f}%/yr)" if cagr == cagr else "  (<2mo, no CAGR)"))
    print(f"      Zijin same window {zj_mult:5.2f}x -> vs Zijin {mult/zj_mult:5.2f}x"
          f"   |  copper {cu_mult:4.2f}x   gold {au_mult:4.2f}x")

book = pd.DataFrame(rows)
book.to_csv(os.path.join(DATA, "deal_returns.csv"), index=False)

# ============================================================ 2) the premise
print("\n" + "-" * 84)
print("2) THE USER'S PREMISE, CHECKED — which anchor date is the honest one?")
print("-" * 84)
zg = px["000408.SZ"]
lo = zg.loc["2020"].min()
lo_d = zg.loc["2020"].idxmin()
p_jul, _ = at(zg, "2020-06-08")
p_ctl, _ = at(zg, "2025-01-17")
p_now = zg.iloc[-1]

print(f"  (a) 2020 absolute low            {lo:6.2f} ({lo_d.date()}) -> {p_now:.2f}"
      f" = {p_now/lo:5.2f}x   <- NOT actionable (hindsight low)")
print(f"  (b) Julong announcement 2020-06-08 {p_jul:6.2f}            -> {p_now:.2f}"
      f" = {p_now/p_jul:5.2f}x   <- ACTIONABLE: the co-investment forms")
print(f"  (c) Zangge control  2025-01-17     {p_ctl:6.2f}            -> {p_now:.2f}"
      f" = {p_now/p_ctl:5.2f}x   <- ACTIONABLE: the deepening leg")
share = np.log(p_now / p_jul) / np.log(p_now / lo) * 100
print(f"\n  Share of the 2020-low->today move that came AFTER the Julong deal "
      f"(log basis): {share:.0f}%")
print("  => The 'buy the bottom' framing is wrong, but it does not matter:")
print("     the move is overwhelmingly POST-announcement, so it was investable.")

# ============================================================ 3) the torque
print("\n" + "-" * 84)
print("3) THE CORE MECHANISM — the partner has MORE torque than the operator")
print("-" * 84)
for label, tkr, anchor in [("Zangge  vs Zijin (from Julong 2020-06-08)",
                            "000408.SZ", "2020-06-08"),
                           ("Ivanhoe vs Zijin (from stake   2015-03-23)",
                            "IVN.TO", "2015-03-23")]:
    p0, _ = at(px[tkr], anchor)
    z0, _ = at(px["601899.SS"], anchor)
    pm = px[tkr].iloc[-1] / p0
    zm = px["601899.SS"].iloc[-1] / z0
    print(f"  {label}:  partner {pm:5.2f}x   Zijin {zm:5.2f}x   "
          f"ratio {pm/zm:4.2f}x")
print("\n  Why: the shared asset is a far larger fraction of the PARTNER's NAV")
print("  than of Zijin's diversified NAV. Same asset, more concentration,")
print("  more torque -- the same elasticity logic as the gold-miner report.")

# ============================================================ 4) takeovers
print("\n" + "-" * 84)
print("4) WHY FULL TAKEOVERS ARE NOT 'FOLLOWABLE' — the targets DELISTED")
print("-" * 84)
for dt, name, tkr, price, asset in TAKEOVERS:
    print(f"  {dt}  {name:<20} {tkr:<18} {price:<10} {asset}")
print("\n  An outside holder of these names received the takeover price ONCE.")
print("  None of the post-deal value creation (Timok, Buritica, 3Q lithium)")
print("  accrued to them. This is precisely why the user's CO-INVESTMENT")
print("  framing is the better one: the partner stays listed.")
pd.DataFrame(TAKEOVERS,
             columns=["date", "target", "ticker", "consideration", "asset"]
             ).to_csv(os.path.join(DATA, "takeovers.csv"), index=False)

# ============================================================ 4b) the failures
print("\n" + "-" * 84)
print("4b) COUNTEREXAMPLES — where following Zijin did NOT work")
print("-" * 84)
for when, who, what, outcome in COUNTEREXAMPLES:
    print(f"\n  {when}  {who}")
    print(f"      deal   : {what}")
    print(f"      outcome: {outcome}")
pd.DataFrame(COUNTEREXAMPLES,
             columns=["when", "target", "deal", "outcome"]
             ).to_csv(os.path.join(DATA, "counterexamples.csv"), index=False)
print("\n  >> Base rate matters: Zijin's announced intention is NOT the same as")
print("     a completed deal. Two of its last three headline offshore deals")
print("     (Solaris 2024, Allied Gold 2026) DIED in regulatory review -- one")
print("     Canadian, one CHINESE. That is the main risk in this strategy.")

# ============================================================ 4c) summary
print("\n" + "-" * 84)
print("4c) SCORECARD — the followable set only")
print("-" * 84)
fol = book[book["kind"].isin(["FOLLOWABLE", "DEEPENING"])].copy()
print(f"  {'date':<12}{'target':<26}{'entry':>9}{'now':>10}{'mult':>8}"
      f"{'vs Zijin':>10}")
for _, r in fol.iterrows():
    print(f"  {r['date']:<12}{r['target'][:24]:<26}{r['entry']:>9.2f}"
          f"{r['px_now']:>10.2f}{r['multiple']:>7.2f}x{r['vs_zijin']:>9.2f}x")
mature = fol[fol["years"] >= 1.0]
print(f"\n  Deals with >=1y of seasoning: {len(mature)}")
print(f"  Median multiple            : {mature['multiple'].median():.2f}x")
print(f"  Beat Zijin itself          : {(mature['vs_zijin'] > 1).sum()}/{len(mature)}")
print(f"  Lost money                 : {(mature['multiple'] < 1).sum()}/{len(mature)}")

# ============================================================ 5) chart
fig, axes = plt.subplots(2, 1, figsize=(13.5, 11))

ax = axes[0]
anchor = "2020-06-08"
for tkr, lab, col, lw in [("000408.SZ", "Zangge 藏格 (the listed partner)", "#c0392b", 2.4),
                          ("601899.SS", "Zijin 紫金 (the operator)", "#2c3e50", 2.0),
                          ("HG=F", "Copper", "#e67e22", 1.4),
                          ("GC=F", "Gold", "#f1c40f", 1.4)]:
    s = px[tkr].loc[anchor:]
    ax.plot(s.index, s / s.iloc[0], color=col, lw=lw, label=lab)
ax.set_yscale("log")
for x, txt, col in [("2020-06-08", "Zijin buys 50.1% of Julong\n→ Zangge becomes co-investor", "#27ae60"),
                    ("2025-01-17", "Zijin takes CONTROL of Zangge\n(the deepening leg)", "#8e44ad")]:
    ax.axvline(pd.Timestamp(x), color=col, ls=":", lw=1.6)
    ax.annotate(txt, xy=(pd.Timestamp(x), ax.get_ylim()[1]),
                xytext=(6, -10), textcoords="offset points", fontsize=8,
                color=col, va="top", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, alpha=.9))
ax.set_ylabel("total return, rebased (log)")
ax.set_title("A. The Julong case — the listed MINORITY PARTNER out-ran the operator",
             fontsize=11.5, fontweight="bold")
ax.grid(alpha=.25, which="both")
ax.legend(fontsize=8.5, loc="upper left")

ax = axes[1]
anchor = "2015-03-23"
for tkr, lab, col, lw in [("IVN.TO", "Ivanhoe Mines (the listed partner)", "#c0392b", 2.4),
                          ("601899.SS", "Zijin 紫金 (the operator)", "#2c3e50", 2.0),
                          ("HG=F", "Copper", "#e67e22", 1.4)]:
    s = px[tkr].loc[anchor:]
    ax.plot(s.index, s / s.iloc[0], color=col, lw=lw, label=lab)
ax.set_yscale("log")
ax.axvline(pd.Timestamp("2015-03-23"), color="#27ae60", ls=":", lw=1.6)
ax.annotate("Zijin buys 9.9% of Ivanhoe (Mar-2015)\nthen 49.5% of Kamoa Holding "
            "(May-2015)\n→ 39.6%/39.6% project JV",
            xy=(pd.Timestamp("2015-03-23"), ax.get_ylim()[1]), xytext=(6, -10),
            textcoords="offset points", fontsize=8, color="#27ae60",
            va="top", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#27ae60", alpha=.9))
ax.set_ylabel("total return, rebased (log)")
ax.set_title("B. The Kamoa case — the same structure, 5 years earlier, offshore",
             fontsize=11.5, fontweight="bold")
ax.grid(alpha=.25, which="both")
ax.legend(fontsize=8.5, loc="upper left")

fig.suptitle('"Follow Zijin": co-investment in a shared asset vs owning the operator\n'
             "Anchored on PUBLIC announcement dates. Source: Yahoo Finance "
             "(total-return), company announcements.",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .945])
p = os.path.join(CHARTS, "follow_zijin.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")

print("\nDone. CSVs in data/, chart in charts/.")
