# -*- coding: utf-8 -*-
"""
REBUILD NAV ON CURRENT SECOND-HAND VALUES.

The user challenged the vessel values behind §20/§21/§26 and was right.
Those sections used a 5-year-old VLCC at $151.1m (Signal Group, end-August
2026). The market has moved violently since.

PRIMARY SOURCE — Xclusiv Shipbrokers weekly report, 21 September 2026,
downloaded to filings/xclusiv_2026_09_21.pdf, verbatim:

  "Between 10 July and 18 September, five-year-old VLCC values increased from
   around USD 145 mills to USD 172 mills, or approximately 18.6%, while
   10-year-old tonnage rose from USD 115 mills to USD 152 mills, up around
   32%. Fifteen-year-old values increased from approximately USD 83.5 mills
   to USD 135 mills, a rise of almost 61%, while resale values moved from
   around USD 175 mills to USD 193 mills."

So the age curve as at 18 Sep 2026 is:
     resale   $193m
     5-year   $172m
     10-year  $152m
     15-year  $135m

DHT's fleet is valued VESSEL BY VESSEL using the build years in its own
FY2025 20-F per-vessel table. FRO is valued on its disclosed fleet
composition and average age.
"""

import io
import os
import re
import sys

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
NOW = 2026.72                                   # late September 2026

# ── the age curve, Xclusiv 18 Sep 2026 ───────────────────────────────────────
AGE_PTS = [0, 5, 10, 15]
VAL_PTS = [193.0, 172.0, 152.0, 135.0]
# beyond 15 years the report gives no point. Signal Group had 20-year-old at
# $71.1m at END-AUGUST, before the 15-year point rose 61%. Rather than
# extrapolate that stale figure, a CONSERVATIVE linear decline is used from
# $135m at 15 years to $85m at 20 and $45m at 25. Flagged as an assumption.
AGE_PTS += [20, 25]
VAL_PTS += [85.0, 45.0]


def vlcc_value(age):
    return float(np.interp(max(age, 0), AGE_PTS, VAL_PTS))


print("=" * 100)
print("NAV REBUILT ON CURRENT SECOND-HAND VALUES (Xclusiv, 18 Sep 2026)")
print("=" * 100)
print(f"\n  Age curve used:  " +
      " · ".join(f"{a}yr ${v:.0f}m" for a, v in zip(AGE_PTS, VAL_PTS)))
print("  (0-15yr is quoted directly by the broker; 20 and 25yr are a")
print("   conservative assumption, flagged — see the note in §27.)")
print(f"\n  ⚠️ What §20/§21/§26 used instead: a 5-year-old at $151.1m")
print(f"     (Signal Group, END-AUGUST). The 5-year point is now $172m,")
print(f"     so those sections were {172/151.1-1:+.1%} stale on the key input.")

# ══════════════════════ DHT — vessel by vessel ═══════════════════════════════
t = open(os.path.join(HERE, "filings", "DHT_FY2025.txt"), encoding="utf-8").read()
m = re.search(r"fleet information[^.]{0,140}?charter[- ]?free fair market values as of\s+"
              r"December 31,\s*(\d{4})", t, re.I)
seg = t[m.end(): m.end() + 14000]
ROW = re.compile(r"([A-Z][A-Za-z0-9.\-'/ ]{2,40}?)\s+(19\d\d|20\d\d)\s+"
                 r"(VLCC|Aframax|Suezmax|LR2|Panamax)\s+"
                 r"(?:[A-Z][a-z]{2}\.?\s*)?(?:19\d\d|20\d\d)?\s*"
                 r"([\d,]{3,})\s+([\d,]{3,})")
ships = []
for nm_, built, typ, carry, fmv in ROW.findall(seg):
    v = int(fmv.replace(",", ""))
    if 5_000 <= v <= 400_000:
        ships.append(dict(name=nm_.strip(), built=int(built), typ=typ,
                          dec25_fmv=v / 1000.0))
d = pd.DataFrame(ships)
d["age"] = NOW - d["built"]
d["now_val"] = d["age"].apply(vlcc_value)
print("\n" + "-" * 100)
print(f"DHT — {len(d)} vessels from its FY2025 20-F table, revalued by age")
print("-" * 100)
print(f"  {'vessel':<22}{'built':>7}{'age':>6}{'Dec-25 FMV':>12}{'now':>9}{'chg':>8}")
for _, r in d.sort_values("built", ascending=False).iterrows():
    print(f"  {r['name'][:21]:<22}{r['built']:>7}{r['age']:>6.1f}"
          f"{r['dec25_fmv']:>12.1f}{r['now_val']:>9.1f}"
          f"{(r['now_val']/r['dec25_fmv']-1)*100:>7.0f}%")
dht_fleet_now = d["now_val"].sum()
dht_fleet_dec25 = d["dec25_fmv"].sum()
print(f"\n  TOTAL  Dec-2025 ${dht_fleet_dec25:,.0f}m  ->  NOW ${dht_fleet_now:,.0f}m "
      f"({dht_fleet_now/dht_fleet_dec25-1:+.0%})")
print(f"  average age {d['age'].mean():.1f} years")

# ══════════════════════ FRO — by segment ═════════════════════════════════════
# Frontline Q2-2026: 40 VLCC / 19 Suezmax / 18 LR2, average fleet age 6.6 years
FRO_VLCC_AGE = 6.6
SUEZ_5YR = 103.8      # Signal Group, end-August 2026 — STALE, conservative
LR2_5YR = 70.0        # assumption, flagged
fro_vlcc_val = vlcc_value(FRO_VLCC_AGE)
print("\n" + "-" * 100)
print("FRO — by segment, from its Q2-2026 disclosed fleet")
print("-" * 100)
print(f"  {'segment':<12}{'ships':>7}{'$m/ship':>10}{'total $m':>12}  basis")
seg_rows = [("VLCC", 40, fro_vlcc_val, f"age {FRO_VLCC_AGE}yr on the Xclusiv curve"),
            ("Suezmax", 19, SUEZ_5YR, "Signal end-Aug 5yr — STALE, conservative"),
            ("LR2/Afra", 18, LR2_5YR, "assumption, flagged")]
fro_fleet_now = 0
for s, n, v, basis in seg_rows:
    fro_fleet_now += n * v
    print(f"  {s:<12}{n:>7}{v:>10.1f}{n*v:>12,.0f}  {basis}")
print(f"  {'TOTAL':<12}{77:>7}{'':>10}{fro_fleet_now:>12,.0f}")
print(f"\n  vs the ${8875:,}m used in §20/§21/§26: {fro_fleet_now/8875-1:+.0%}")

# ══════════════════════ recompute P/NAV ══════════════════════════════════════
CO = {
    "DHT": dict(net_debt=273.1, shares=161.236, price=23.27,
                old_fleet=2583.0, new_fleet=dht_fleet_now),
    "FRO": dict(net_debt=2113.4, shares=222.623, price=51.42,
                old_fleet=8875.0, new_fleet=fro_fleet_now),
}
print("\n" + "=" * 100)
print("⭐ P/NAV RECOMPUTED")
print("=" * 100)
print(f"  {'':<6}{'fleet OLD':>11}{'fleet NOW':>11}{'NAVPS old':>11}{'NAVPS now':>11}"
      f"{'P/NAV old':>11}{'P/NAV now':>11}")
out = []
for t_, c in CO.items():
    n_old = (c["old_fleet"] - c["net_debt"]) / c["shares"]
    n_new = (c["new_fleet"] - c["net_debt"]) / c["shares"]
    print(f"  {t_:<6}{c['old_fleet']:>11,.0f}{c['new_fleet']:>11,.0f}"
          f"{n_old:>11.2f}{n_new:>11.2f}{c['price']/n_old:>11.2f}{c['price']/n_new:>11.2f}")
    out.append(dict(ticker=t_, fleet_old=round(c["old_fleet"]),
                    fleet_now=round(c["new_fleet"]), navps_old=round(n_old, 2),
                    navps_now=round(n_new, 2), pnav_old=round(c["price"]/n_old, 2),
                    pnav_now=round(c["price"]/n_new, 2)))
res = pd.DataFrame(out)
res.to_csv(os.path.join(DATA, "s27_nav_current_values.csv"), index=False)
d.to_csv(os.path.join(DATA, "s27_dht_vessels.csv"), index=False)

print(f"""
  >> THE USER WAS RIGHT. On current second-hand values:
     DHT falls from {res.pnav_old[0]:.2f}x to {res.pnav_now[0]:.2f}x
     FRO falls from {res.pnav_old[1]:.2f}x to {res.pnav_now[1]:.2f}x""")

# ══════════════════════ sensitivity on the two weak inputs ═══════════════════
print("\n" + "-" * 100)
print("SENSITIVITY — the two inputs still most likely to be TOO LOW")
print("-" * 100)
print("  (1) DHT VESSEL COUNT. The FY2025 table parsed gives "
      f"{len(d)} vessels, but §17")
print("      records 23 in the water today. Missing ships understate NAV.")
print(f"      {'vessels':<10}{'fleet $m':>11}{'NAVPS':>9}{'P/NAV':>9}")
avg_now = d["now_val"].mean()
for n in (len(d), 22, 23, 24):
    f_ = dht_fleet_now + (n - len(d)) * avg_now
    nv = (f_ - CO["DHT"]["net_debt"]) / CO["DHT"]["shares"]
    star = "  <- §17's count" if n == 23 else ""
    print(f"      {n:<10}{f_:>11,.0f}{nv:>9.2f}{CO['DHT']['price']/nv:>9.2f}{star}")

print("\n  (2) FRO's NON-VLCC TONNAGE. Suezmax is carried at Signal's END-AUGUST")
print("      5-year value of $103.8m and LR2 at an assumed $70m. Both predate")
print("      the September surge that lifted VLCCs 19-61%.")
print(f"      {'Suezmax $m':<13}{'LR2 $m':>9}{'fleet $m':>11}{'NAVPS':>9}{'P/NAV':>9}")
for sx, lr in [(103.8, 70.0), (120.0, 80.0), (135.0, 90.0)]:
    f_ = 40 * fro_vlcc_val + 19 * sx + 18 * lr
    nv = (f_ - CO["FRO"]["net_debt"]) / CO["FRO"]["shares"]
    tag = "  <- as used above" if sx == 103.8 else ""
    print(f"      {sx:<13.1f}{lr:>9.1f}{f_:>11,.0f}{nv:>9.2f}"
          f"{CO['FRO']['price']/nv:>9.2f}{tag}")

print("\n  >> BOTH adjustments push P/NAV DOWN FURTHER. The figures published")
print("     below therefore use the CONSERVATIVE end of each range, and the")
print("     true multiple is more likely below them than above.")

print("\n" + "-" * 100)
print("WHAT THIS DOES TO §26's CONCLUSION")
print("-" * 100)
HIST = {"DHT": (1.04, 1.45), "FRO": (0.99, 1.45)}
print(f"  {'':<6}{'hist mean':>11}{'hist max':>10}{'OLD today':>11}{'NEW today':>11}"
      f"{'vs mean':>10}{'vs max':>9}")
for t_, (mu, mx) in HIST.items():
    nv = float(res[res.ticker == t_].pnav_now.iloc[0])
    print(f"  {t_:<6}{mu:>11.2f}{mx:>10.2f}{float(res[res.ticker==t_].pnav_old.iloc[0]):>11.2f}"
          f"{nv:>11.2f}{(nv/mu-1)*100:>9.0f}%{(nv/mx-1)*100:>8.0f}%")
print("""
  >> §26 said today was ABOVE EVERY OBSERVATION in the record. On the
     corrected vessel values that is NO LONGER TRUE for DHT, and only
     marginally true for FRO. The §26 conclusion is WITHDRAWN as stated
     and replaced below.""")
print("\nDone.")
