"""
BDTI vs DHT vs FRO — Correlation Chart
Combines:
  - BDTI (Baltic Dirty Tanker Index) from GitHub CSV + Investing.com scrape
  - DHT & FRO stock prices from Yahoo Finance
Uses dual y-axes: BDTI index (left), stock price USD (right)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import yfinance as yf
import json
from datetime import datetime
from pathlib import Path

# ─── CONFIG ──────────────────────────────────────────────────────────────────
CHART_START = "2020-01-01"
OUTPUT_DIR = Path("charts")
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── 1. Load BDTI from GitHub CSV ───────────────────────────────────────────
print("Loading BDTI from GitHub CSV...")
bdti_gh = pd.read_csv(
    "https://raw.githubusercontent.com/Aftikharmnz/Baltic/main/Baltic%20Dirty%20Tanker%20Historical%20Data.csv"
)
bdti_gh["Date"] = pd.to_datetime(bdti_gh["Date"], format="mixed")
bdti_gh = bdti_gh[["Date", "Price"]].rename(columns={"Price": "BDTI"})
bdti_gh = bdti_gh.sort_values("Date").reset_index(drop=True)
print(f"  GitHub CSV: {len(bdti_gh)} rows, {bdti_gh['Date'].iloc[0].date()} to {bdti_gh['Date'].iloc[-1].date()}")

# ─── 2. Load BDTI from Investing.com scrape ─────────────────────────────────
bdti_scrape = None
scrape_file = Path("bdti_scraped_data.json")
if scrape_file.exists():
    print("Loading BDTI from investing.com scrape...")
    with open(scrape_file) as f:
        raw = json.load(f)
    
    # Deduplicate by date
    seen_dates = set()
    clean_rows = []
    for row in raw:
        dt = row.get("rowDateTimestamp", "")
        if dt and dt not in seen_dates:
            seen_dates.add(dt)
            clean_rows.append({
                "Date": pd.to_datetime(dt),
                "BDTI": float(row["last_closeRaw"]),
            })
    
    if clean_rows:
        bdti_scrape = pd.DataFrame(clean_rows)
        bdti_scrape["Date"] = pd.to_datetime(bdti_scrape["Date"]).dt.tz_localize(None)
        bdti_scrape = bdti_scrape.sort_values("Date").reset_index(drop=True)
        print(f"  Scrape: {len(bdti_scrape)} rows, {bdti_scrape['Date'].iloc[0].date()} to {bdti_scrape['Date'].iloc[-1].date()}")

# ─── 3. Combine BDTI sources ────────────────────────────────────────────────
print("Combining BDTI data...")
if bdti_scrape is not None:
    bdti = pd.concat([bdti_gh, bdti_scrape], ignore_index=True)
    bdti = bdti.drop_duplicates(subset="Date").sort_values("Date").reset_index(drop=True)
else:
    bdti = bdti_gh.copy()

print(f"  Combined BDTI: {len(bdti)} rows, {bdti['Date'].iloc[0].date()} to {bdti['Date'].iloc[-1].date()}")

# ─── 4. Fetch DHT + FRO from Yahoo Finance ──────────────────────────────────
print("Fetching DHT from Yahoo Finance...")
dht_raw = yf.download("DHT", start=CHART_START, progress=False)
dht = pd.DataFrame({
    "Date": dht_raw.index.get_level_values(0),
    "DHT": dht_raw["Close"].values.flatten(),
})
dht["Date"] = pd.to_datetime(dht["Date"]).dt.tz_localize(None)
print(f"  DHT: {len(dht)} rows, {dht['Date'].iloc[0].date()} to {dht['Date'].iloc[-1].date()}")

print("Fetching FRO from Yahoo Finance...")
fro_raw = yf.download("FRO", start=CHART_START, progress=False)
fro = pd.DataFrame({
    "Date": fro_raw.index.get_level_values(0),
    "FRO": fro_raw["Close"].values.flatten(),
})
fro["Date"] = pd.to_datetime(fro["Date"]).dt.tz_localize(None)
print(f"  FRO: {len(fro)} rows, {fro['Date'].iloc[0].date()} to {fro['Date'].iloc[-1].date()}")

# ─── 5. Build the chart ─────────────────────────────────────────────────────
print("\nBuilding chart...")

fig, ax1 = plt.subplots(figsize=(18, 9))

# Dark background for financial chart look
fig.patch.set_facecolor("#1a1a2e")
ax1.set_facecolor("#16213e")

# Left axis: BDTI
color_bdti = "#00d4ff"
ax1.plot(bdti["Date"], bdti["BDTI"], color=color_bdti, linewidth=1.8, alpha=0.9, label="BDTI (Baltic Dirty Tanker Index)")
ax1.fill_between(bdti["Date"], bdti["BDTI"], alpha=0.15, color=color_bdti)
ax1.set_ylabel("BDTI Index", color=color_bdti, fontsize=13, fontweight="bold")
ax1.tick_params(axis="y", labelcolor=color_bdti, labelsize=11)
ax1.set_ylim(bottom=0)

# Right axis: Stock prices
ax2 = ax1.twinx()
color_dht = "#ff6b6b"
color_fro = "#ffd93d"

ax2.plot(dht["Date"], dht["DHT"], color=color_dht, linewidth=1.8, alpha=0.9, label="DHT Holdings ($)")
ax2.plot(fro["Date"], fro["FRO"], color=color_fro, linewidth=1.8, alpha=0.9, label="Frontline FRO ($)")
ax2.set_ylabel("Stock Price (USD)", color="#ffffff", fontsize=13, fontweight="bold")
ax2.tick_params(axis="y", labelcolor="#ffffff", labelsize=11)

# X axis
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=10, color="#cccccc")
ax1.tick_params(axis="x", colors="#cccccc")

# Grid
ax1.grid(True, alpha=0.2, color="#4a4a6a")
ax1.set_axisbelow(True)

# Title
fig.suptitle(
    "Baltic Dirty Tanker Index (BDTI) vs DHT Holdings & Frontline (FRO)",
    fontsize=16, fontweight="bold", color="#ffffff", y=0.97
)
ax1.set_title(
    "TD3C (MEG→China VLCC route) is the largest component of BDTI\n"
    f"BDTI data: {bdti['Date'].iloc[0].strftime('%b %Y')}–{bdti['Date'].iloc[-1].strftime('%b %Y')}  |  "
    f"Stock data: {dht['Date'].iloc[0].strftime('%b %Y')}–{dht['Date'].iloc[-1].strftime('%b %Y')}",
    fontsize=10, color="#888888", pad=10
)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
legend = ax1.legend(
    lines1 + lines2, labels1 + labels2,
    loc="upper left", fontsize=11,
    facecolor="#1a1a2e", edgecolor="#4a4a6a",
    labelcolor="#ffffff"
)

# Mark key events
events = [
    ("2020-03-15", "COVID Storage\nSpike", "#ff9f43"),
    ("2022-02-24", "Russia-Ukraine\nWar", "#ee5a24"),
    ("2024-10-01", "Q4 2024\nSeasonal Peak", "#6ab04c"),
]
for date_str, label, color in events:
    dt = pd.to_datetime(date_str)
    if bdti["Date"].iloc[0] <= dt <= dht["Date"].iloc[-1]:
        ax1.axvline(x=dt, color=color, linestyle="--", alpha=0.5, linewidth=1)
        ylim = ax1.get_ylim()
        ax1.text(dt, ylim[1] * 0.92, label, color=color, fontsize=8, ha="center",
                fontweight="bold", alpha=0.8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#1a1a2e", edgecolor=color, alpha=0.7))

# Add current prices annotation
dht_last = float(dht["DHT"].iloc[-1])
fro_last = float(fro["FRO"].iloc[-1])
bdti_last = float(bdti["BDTI"].iloc[-1])
bdti_last_date = bdti["Date"].iloc[-1].strftime("%b %d")

price_text = (
    f"Latest Prices:\n"
    f"  DHT: ${dht_last:.2f}\n"
    f"  FRO: ${fro_last:.2f}\n"
    f"  BDTI: {bdti_last:.0f} ({bdti_last_date})"
)
ax1.text(0.98, 0.05, price_text, transform=ax1.transAxes,
         fontsize=10, color="#ffffff", fontfamily="monospace",
         verticalalignment="bottom", horizontalalignment="right",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#1a1a2e", edgecolor="#4a4a6a", alpha=0.9))

# Note about data gap
if bdti["Date"].iloc[-1] < dht["Date"].iloc[-1]:
    gap_start = bdti["Date"].iloc[-1]
    ax1.axvspan(gap_start, dht["Date"].iloc[-1], alpha=0.08, color="#ff6b6b")
    mid_gap = gap_start + (dht["Date"].iloc[-1] - gap_start) / 2
    ylim = ax1.get_ylim()
    ax1.text(mid_gap, ylim[1] * 0.5, "BDTI data\nnot available\n(paywalled)",
             color="#ff6b6b", fontsize=9, ha="center", alpha=0.6, fontstyle="italic")

plt.tight_layout()

output_path = OUTPUT_DIR / "bdti_vs_dht_fro.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"\nChart saved to: {output_path}")
print(f"  Size: {output_path.stat().st_size / 1024:.0f} KB")

# ─── 6. Print correlation stats for overlapping period ───────────────────────
print("\n" + "=" * 60)
print("CORRELATION ANALYSIS (overlapping period)")
print("=" * 60)

# Merge on date
merged = bdti.merge(dht, on="Date", how="inner").merge(fro, on="Date", how="inner")
print(f"Overlapping days: {len(merged)}")
if len(merged) > 30:
    corr_dht = merged["BDTI"].corr(merged["DHT"])
    corr_fro = merged["BDTI"].corr(merged["FRO"])
    print(f"BDTI vs DHT correlation: {corr_dht:.3f}")
    print(f"BDTI vs FRO correlation: {corr_fro:.3f}")
    
    # Rolling correlation
    merged_sorted = merged.sort_values("Date")
    roll_60 = merged_sorted["BDTI"].rolling(60).corr(merged_sorted["DHT"])
    print(f"60-day rolling corr (DHT) range: {roll_60.min():.3f} to {roll_60.max():.3f}")
