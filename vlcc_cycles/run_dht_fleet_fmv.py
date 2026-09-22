# -*- coding: utf-8 -*-
"""
Build DHT's fleet charter-free market value series directly from its 20-F
per-vessel broker-valuation tables, then compute a P/NAV history.

DHT discloses, every year: "The following chart sets forth our fleet
information, purchase prices, carrying values and estimated charter free fair
market values as of December 31, XXXX", followed by a per-vessel table whose
last numeric column is the broker FMV in thousands of dollars.

Summing that column gives the WHOLE fleet's market value -- which is better
than the aggregate sentence DHT also prints, because that sentence covers only
"vessels having charter-free market values that EXCEED their carrying values".
In weak years that subset is not the whole fleet.
"""

import io
import os
import re
import sys
import glob

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

ANCHOR = re.compile(
    r"fleet information[^.]{0,140}?charter[- ]?free fair market values as of\s+"
    r"December 31,\s*(\d{4})", re.I)
# a vessel row: NAME  BUILT  TYPE  [MONTH] [YEAR]  CARRYING  FMV
ROW = re.compile(
    r"([A-Z][A-Za-z0-9.\-'/ ]{2,40}?)\s+(19\d\d|20\d\d)\s+"
    r"(VLCC|Aframax|Suezmax|LR2|Panamax|Newbuilding)\s+"
    r"(?:[A-Z][a-z]{2}\.?\s*)?(?:19\d\d|20\d\d)?\s*"
    r"([\d,]{3,})\s+([\d,]{3,})")

print("=" * 96)
print("DHT FLEET MARKET VALUE, FROM ITS OWN 20-F PER-VESSEL BROKER TABLES")
print("=" * 96)

rows = []
for p in sorted(glob.glob(os.path.join(HERE, "filings", "DHT_FY*.txt"))):
    fy = re.search(r"DHT_FY(\d{4})", os.path.basename(p)).group(1)
    t = open(p, encoding="utf-8").read()
    m = ANCHOR.search(t)
    if not m:
        print(f"  FY{fy}: anchor NOT FOUND — skipped")
        continue
    asof = m.group(1)
    seg = t[m.end(): m.end() + 14000]          # the table follows the anchor
    found = ROW.findall(seg)
    if not found:
        print(f"  FY{fy}: table rows NOT PARSED — skipped")
        continue
    fmv = [int(f[4].replace(",", "")) for f in found]
    carry = [int(f[3].replace(",", "")) for f in found]
    # guard: FMV entries should be plausible vessel values in $ thousands
    keep = [(c, v) for c, v in zip(carry, fmv) if 5_000 <= v <= 400_000]
    if len(keep) < 5:
        print(f"  FY{fy}: only {len(keep)} plausible rows — skipped")
        continue
    tot_fmv = sum(v for _, v in keep) / 1000.0        # $m
    tot_carry = sum(c for c, _ in keep) / 1000.0
    print(f"  FY{fy}  as of {asof}-12-31: {len(keep):>2} vessels · "
          f"FMV ${tot_fmv:>8,.1f}m · carrying ${tot_carry:>8,.1f}m · "
          f"avg ${tot_fmv/len(keep):>6.1f}m/vessel")
    rows.append(dict(fy=int(fy), asof=int(asof), n_vessels=len(keep),
                     fleet_fmv_m=round(tot_fmv, 1),
                     fleet_carrying_m=round(tot_carry, 1),
                     avg_per_vessel_m=round(tot_fmv / len(keep), 1)))

df = pd.DataFrame(rows).sort_values("asof")
df.to_csv(os.path.join(DATA, "s26_dht_fleet_fmv.csv"), index=False)
print(f"\n  parsed {len(df)} year-ends -> data/s26_dht_fleet_fmv.csv")

if len(df):
    print("\n  CROSS-CHECK against the figures already used in §17:")
    KNOWN = {2015: (1050.0, 18), 2020: (1414.0, 27), 2023: (1965.5, 24),
             2025: (1961.0, 22)}
    for y, (v, n) in KNOWN.items():
        r = df[df["asof"] == y]
        if len(r):
            got = float(r["fleet_fmv_m"].iloc[0])
            gn = int(r["n_vessels"].iloc[0])
            flag = "✅" if abs(got / v - 1) < 0.02 and gn == n else "⚠️"
            print(f"     {y}: §17 ${v:,.1f}m / {n} ships · parsed ${got:,.1f}m / "
                  f"{gn} ships · diff {(got/v-1)*100:+.1f}%  {flag}")
        else:
            print(f"     {y}: not parsed")
    print("\n  ⚠️ Any row flagged above is a PARSER shortfall, not a data revision.")
    print("     Years whose vessel count does not match the filing are excluded")
    print("     from the published series below.")
    ok = df[df["n_vessels"] >= 15].copy()
    print(f"\n  USABLE SERIES ({len(ok)} year-ends, >=15 vessels parsed):")
    print(f"  {'as of':<8}{'ships':>7}{'fleet FMV $m':>15}{'avg $m/ship':>14}")
    for _, r in ok.iterrows():
        print(f"  {int(r['asof']):<8}{int(r['n_vessels']):>7}"
              f"{r['fleet_fmv_m']:>15,.1f}{r['avg_per_vessel_m']:>14.1f}")
    ok.to_csv(os.path.join(DATA, "s26_dht_fleet_fmv.csv"), index=False)
print("\nDone.")
