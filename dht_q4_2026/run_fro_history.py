"""Build the 2007Q1-2009Q2 historical P/E tables from dated public inputs.

Default execution uses the committed daily-price snapshot without network access.
--refresh-prices replaces that snapshot from Yahoo and verifies its split factor.
This is an EPS-bridge study with explicit vintage limitations, not a backtest.
"""

import argparse
import csv
from datetime import date, datetime, timezone
from decimal import Decimal as D
from html import escape
import json
from pathlib import Path
from urllib.request import Request, urlopen


HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
CENT = D("0.01")
SPLIT_FACTOR = D("5")
PRICE_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/FRO"
    "?period1=1167609600&period2=1246406400&interval=1d&events=div%2Csplits"
)
SPLIT_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/FRO"
    "?period1=1451606400&period2=1767225600&interval=1mo&events=splits"
)


def fetch_chart(url):
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=45) as response:
        chart = json.load(response)["chart"]
    if chart.get("error") or not chart.get("result"):
        raise ValueError(f"Yahoo chart error: {chart.get('error')}")
    return chart["result"][0]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def refresh_prices():
    actions = fetch_chart(SPLIT_URL).get("events", {}).get("splits", {})
    splits = sorted(actions.values(), key=lambda item: item["date"])
    if len(splits) != 1 or splits[0]["splitRatio"] != "1:5":
        raise ValueError(f"Historical split assumption must be reviewed: {splits}")
    chart = fetch_chart(PRICE_URL)
    if chart["meta"]["currency"] != "USD":
        raise ValueError("Expected NYSE USD prices")
    quote = chart["indicators"]["quote"][0]
    prices = []
    for index, timestamp in enumerate(chart["timestamp"]):
        if quote["close"][index] is None or quote["high"][index] is None:
            raise ValueError(f"Missing daily quote at {timestamp}")
        day = datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat()
        close = D(str(quote["close"][index]))
        high = D(str(quote["high"][index]))
        low = D(str(quote["low"][index]))
        prices.append(
            {
                "date": day,
                "vendor_split_adjusted_close": str(close),
                "original_close": str((close / SPLIT_FACTOR).quantize(CENT)),
                "original_high": str((high / SPLIT_FACTOR).quantize(CENT)),
                "original_low": str((low / SPLIT_FACTOR).quantize(CENT)),
            }
        )
    validate_prices(prices)
    write_csv(DATA / "fro_daily_prices_2007_2009.csv", prices)
    metadata = {
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "Yahoo Finance chart API, NYSE FRO, USD",
        "price_url": PRICE_URL,
        "split_url": SPLIT_URL,
        "split_events": splits,
        "transformation": "Original price = split-only Close / 5. AdjClose is never used.",
        "rows": len(prices),
        "primary_check": "FY2008 annual-report NYSE quarterly high/low table; FY2009 H1 ranges.",
        "limitations": "Reconstructed cents-rounded prices; no trade-tape audit. Dividends and spin-off distributions are not added back.",
    }
    (DATA / "fro_price_provenance.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def validate_prices(prices):
    days = [row["date"] for row in prices]
    if not prices or days != sorted(set(days)):
        raise ValueError("Prices must be nonempty, unique and date-sorted")
    highs_lows = {
        "2007Q1": ("36.55", "29.35"),
        "2007Q2": ("47.94", "34.26"),
        "2007Q3": ("53.09", "38.25"),
        "2007Q4": ("51.06", "37.49"),
        "2008Q1": ("49.66", "34.00"),
        "2008Q2": ("72.36", "46.34"),
        "2008Q3": ("69.09", "43.25"),
        "2008Q4": ("47.50", "25.00"),
        "2009Q1": ("33.29", "15.78"),
        "2009Q2": ("28.59", "17.00"),
    }
    for quarter, (high, low) in highs_lows.items():
        subset = [
            row for row in prices
            if f"{row['date'][:4]}Q{(int(row['date'][5:7]) - 1) // 3 + 1}" == quarter
        ]
        if not subset:
            raise ValueError(f"No prices for {quarter}")
        actual_high = max(D(row["original_high"]) for row in subset)
        actual_low = min(D(row["original_low"]) for row in subset)
        if abs(actual_high - D(high)) > D("0.02") or abs(actual_low - D(low)) > D("0.02"):
            raise ValueError(
                f"Annual-report price range mismatch: {quarter} "
                f"{actual_high}/{actual_low} versus {high}/{low}"
            )


def render_chart(rows):
    width, height = 1100, 920
    left, right, plot_width = 85, 30, 985
    colors = ("#136f91", "#d46a24", "#7851a9")
    panels = [
        ("Original quarter-end share price (USD)", [("Price", "original_close")], 80),
        ("EPS denominators (USD per original share)",
         [("Period TTM bridge", "period_ttm_eps_bridge"),
          ("Reporting-lag approximation", "lag_ttm_eps_approx")], 12),
        ("Quarter-end P/E (x)",
         [("Period TTM (hindsight)", "period_ttm_pe_hindsight"),
          ("Reporting-lag approximation", "reporting_lag_pe_approx"),
          ("Same-year final EPS (hindsight)", "same_year_pe_hindsight")], 20),
    ]
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Frontline quarter-end prices and P/E, 2007Q1 to 2009Q2</title>',
        '<desc id="desc">Original prices are reconstructed from split-only Close divided by five. '
        'Period and same-year P/E use later earnings; the reporting-lag line is an approximation, '
        'not a fully versioned information-available backtest.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<g font-family="Arial, sans-serif" fill="#263238">',
        '<text x="40" y="32" font-size="22" font-weight="bold">Frontline: price, earnings and P/E are different clocks</text>',
        '<text x="40" y="56" font-size="13">Quarter-end observations; no dividend-adjusted prices; no annualized-quarter P/E</text>',
    ]
    for panel_index, (title, series, maximum) in enumerate(panels):
        top = 100 + panel_index * 270
        baseline, plot_height = top + 175, 170
        svg.append(f'<text x="40" y="{top - 20}" font-size="17" font-weight="bold">{escape(title)}</text>')
        for tick in range(5):
            value = maximum * tick / 4
            y = baseline - plot_height * tick / 4
            svg.append(f'<line x1="{left}" y1="{y}" x2="{width-right}" y2="{y}" stroke="#dde3e8"/>')
            svg.append(f'<text x="{left-12}" y="{y+4}" text-anchor="end" font-size="12">{value:g}</text>')
        if panel_index == 2:
            y = baseline - 2 / maximum * plot_height
            svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#b71c1c" stroke-dasharray="5 4"/>')
            svg.append(f'<text x="{left+3}" y="{y-5:.1f}" font-size="11" fill="#b71c1c">2x reference, not a trading rule</text>')
        for series_index, (label, key) in enumerate(series):
            color = colors[series_index]
            points = []
            for index, row in enumerate(rows):
                x = left + index * plot_width / (len(rows) - 1)
                y = baseline - float(row[key]) / maximum * plot_height
                points.append(f"{x:.1f},{y:.1f}")
                svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>')
            svg.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2.5"/>')
            legend_x = left + series_index * 320
            svg.append(f'<text x="{legend_x}" y="{baseline+52}" font-size="12" fill="{color}">{escape(label)}</text>')
        for index, row in enumerate(rows):
            x = left + index * plot_width / (len(rows) - 1)
            svg.append(f'<text x="{x:.1f}" y="{baseline+22}" text-anchor="middle" font-size="12">{row["quarter"]}</text>')
    svg.extend([
        '<text x="40" y="895" font-size="12">Sources: Frontline filings/releases and Yahoo split-only prices; vintage and rounding limitations in the bilingual report.</text>',
        '</g></svg>',
    ])
    return "\n".join(svg) + "\n"


def build(write_outputs=True):
    inputs = json.loads((DATA / "fro_earnings_2006_2009.json").read_text())
    with (DATA / "fro_daily_prices_2007_2009.csv").open(newline="") as handle:
        prices = list(csv.DictReader(handle))
    validate_prices(prices)
    rows = []
    for q in inputs["quarters"]:
        end = date.fromisoformat(q["period_end"])
        eligible = [p for p in prices if date.fromisoformat(p["date"]) <= end]
        p = eligible[-1]
        if (end - date.fromisoformat(p["date"])).days > 4:
            raise ValueError(f"Stale quarter-end quote for {q['quarter']}")
        price = D(p["original_close"])
        if q["quarter"].endswith("Q4"):
            ttm_eps = D(q["ytd_eps"])
        else:
            ttm_eps = D(q["prior_annual_eps"]) + D(q["ytd_eps"]) - D(q["prior_ytd_eps"])
        annual_eps = D(inputs["annual"][q["quarter"][:4]]["basic_eps"])
        lag_eps = D(q["lag_ttm_eps"])
        rows.append(
            {
                "quarter": q["quarter"],
                "price_date": p["date"],
                "original_close": f"{price:.2f}",
                "quarter_eps_initial": q["basic_eps"],
                "period_ttm_eps_bridge": f"{ttm_eps:.2f}",
                "period_ttm_pe_hindsight": f"{price / ttm_eps:.2f}",
                "lag_earnings_end": q["lag_earnings_end"],
                "lag_ttm_eps_approx": f"{lag_eps:.2f}",
                "reporting_lag_pe_approx": f"{price / lag_eps:.2f}",
                "same_year_final_eps": f"{annual_eps:.2f}",
                "same_year_pe_hindsight": f"{price / annual_eps:.2f}",
            }
        )
    if write_outputs:
        write_csv(DATA / "fro_quarterly_pe_2007_2009.csv", rows)
        charts = HERE / "charts"
        charts.mkdir(exist_ok=True)
        (charts / "fro_pe_2007_2009.svg").write_text(render_chart(rows), encoding="utf-8")
    print("| Quarter | Original close | EPS(TTM bridge) | Period TTM P/E* | Release-lag P/E** | Same-year final P/E* |")
    print("|---|---:|---:|---:|---:|---:|")
    for row in rows:
        print(
            f"| {row['quarter']} | ${row['original_close']} | ${row['period_ttm_eps_bridge']} "
            f"| {row['period_ttm_pe_hindsight']}x | {row['reporting_lag_pe_approx']}x "
            f"| {row['same_year_pe_hindsight']}x |"
        )
    high = max(prices, key=lambda p: D(p["original_high"]))
    close_high = max(prices, key=lambda p: D(p["original_close"]))
    print("\nIntraday peak:", high["date"], high["original_high"])
    print("Closing peak:", close_high["date"], close_high["original_close"])
    threshold_hits = [
        p for p in prices
        if "2008-11-28" <= p["date"] <= "2009-02-25"
        and D(p["original_close"]) / D("11.21") <= 2
    ]
    if threshold_hits:
        first = threshold_hits[0]
        print("First sub-2x close in the post-Q3-release/pre-FY-release subwindow:",
              first["date"], first["original_close"], "using the 11.21 EPS bridge")
    print("* Hindsight; ** approximate reporting-lag comparator, not a fully versioned as-of backtest.")
    return inputs, prices, rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-prices", action="store_true")
    args = parser.parse_args()
    if args.refresh_prices:
        refresh_prices()
    build()
