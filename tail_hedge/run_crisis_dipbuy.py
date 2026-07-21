"""
Crisis dip-buy evidence for the sectors report Section 7.
Computes, from committed daily adjusted closes, the crisis drawdown depth and the
forward returns from buying at the 2009 and 2020 market bottoms — for quality
survivors (JPM, AXP, XLF) vs a casualty (Citigroup C, pulled live).
Writes: data/results_crisis_dipbuy.csv
"""
import os, math
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "data")

def load(fn):
    df = pd.read_csv(os.path.join(DATA, fn)); df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")["AdjClose"].astype(float)

series = {"JPM": load("jpm_daily_1998_2024.csv"), "AXP": load("axp_daily_1998_2024.csv"),
          "XLF": load("xlf_daily_1998_2024.csv")}
# casualty: Citigroup, pulled live (not committed)
try:
    import yfinance as yf
    c = yf.download("C", start="2006-01-01", end="2024-12-31", interval="1d", progress=False, auto_adjust=True)["Close"].dropna().iloc[:, 0]
    c.index = pd.to_datetime(c.index).tz_localize(None)
    series["C (Citi, casualty)"] = c
except Exception as e:
    print("Citi pull failed:", e)

def nearest(s, date):
    idx = s.index[s.index >= pd.Timestamp(date)]
    return idx[0] if len(idx) else None

def ret_from(s, d0, months):
    i0 = nearest(s, d0)
    if i0 is None: return None
    tgt = i0 + pd.DateOffset(months=months)
    idx = s.index[s.index >= tgt]
    if not len(idx):  # use last available
        return round(s.iloc[-1] / s.loc[i0] - 1, 3)
    return round(s.loc[idx[0]] / s.loc[i0] - 1, 3)

rows = []
for name, s in series.items():
    # 2008-09 crisis drawdown (peak 2007-2009 to trough) and dip-buy from 2009-03-09
    seg = s[(s.index >= "2007-01-01") & (s.index <= "2009-12-31")]
    dd0809 = round((seg / seg.cummax() - 1).min(), 3) if len(seg) else None
    r09_1y = ret_from(s, "2009-03-09", 12); r09_3y = ret_from(s, "2009-03-09", 36)
    r09_5y = ret_from(s, "2009-03-09", 60); r09_end = ret_from(s, "2009-03-09", 999)
    # 2020 crisis
    seg20 = s[(s.index >= "2020-01-01") & (s.index <= "2020-12-31")]
    dd20 = round((seg20 / seg20.cummax() - 1).min(), 3) if len(seg20) else None
    r20_1y = ret_from(s, "2020-03-23", 12); r20_2y = ret_from(s, "2020-03-23", 24)
    # did it regain its 2007 pre-crisis peak? (level vs 2007 high)
    pre = s[(s.index >= "2007-01-01") & (s.index <= "2007-12-31")]
    peak07 = pre.max() if len(pre) else np.nan
    regained = "yes" if (len(s) and s.iloc[-1] >= peak07) else "no"
    rows.append({"asset": name, "DD_2008_09": dd0809, "buy_2009bottom_+1y": r09_1y,
                 "+3y": r09_3y, "+5y": r09_5y, "+to2024": r09_end,
                 "DD_2020": dd20, "buy_2020bottom_+1y": r20_1y, "+2y": r20_2y,
                 "regained_2007_peak_by_2024": regained})
    print(name, "| 2008-09 DD", dd0809, "| 2009 bottom +1y", r09_1y, "+to2024", r09_end,
          "| 2020 DD", dd20, "+1y", r20_1y, "| regained 07 peak:", regained)
pd.DataFrame(rows).to_csv(os.path.join(DATA, "results_crisis_dipbuy.csv"), index=False)
print("\nWrote results_crisis_dipbuy.csv")
