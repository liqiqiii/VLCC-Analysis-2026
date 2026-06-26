"""
Synthetic simulation isolating the "average x duration" mechanism, and a
trading P&L test of spot-chasing vs average/duration trading.

Design:
  - Spot TCE = mean-reverting baseline + injected spike episodes.
  - Three scenarios share the SAME PEAK but differ in DURATION.
  - Earnings reflect realized (charter-lagged trailing-average) TCE, not spot.
  - Stock prices NORMALIZED earnings (PE x trailing-avg earnings), so transient
    spot spikes do not re-rate the equity; sustained elevation does.
  - Trading test: "spot chaser" vs "trailing-average/duration" signal.

Outputs sim_results.json + sim_paths.json for the report and charts.
Deterministic (fixed seed) so the report numbers are reproducible.
"""
import json
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(42)
WEEKS = 260  # 5 years
OPEX = 25000.0          # $/day cash breakeven-ish opex
BASE_TCE = 40000.0      # mid-cycle baseline $/day
PE = 6.0                # cyclical peak-ish multiple on normalized earnings
EARN_WIN = 13           # weeks: charter/quarter lag -> earnings see trailing avg
NORM_WIN = 52           # weeks: market normalizes earnings over ~1yr


def mean_reverting(n, base, theta=0.06, sigma=0.06, seed_rng=RNG):
    x = np.empty(n)
    x[0] = base
    for t in range(1, n):
        x[t] = x[t - 1] + theta * (base - x[t - 1]) + sigma * base * seed_rng.standard_normal()
    return np.clip(x, 5000, None)


def inject_spike(series, start, duration, peak, ramp=3):
    """Raise the series to `peak` for `duration` weeks starting at `start`,
    with short linear ramps in/out."""
    s = series.copy()
    end = start + duration
    for t in range(start, min(end, len(s))):
        s[t] = max(s[t], peak)
    # ramps
    for k in range(1, ramp + 1):
        if start - k >= 0:
            s[start - k] = max(s[start - k], BASE_TCE + (peak - BASE_TCE) * (ramp - k) / ramp)
        if end + k - 1 < len(s):
            s[end + k - 1] = max(s[end + k - 1], BASE_TCE + (peak - BASE_TCE) * (ramp - k) / ramp)
    return s


def earnings_from_tce(tce, fleet_days=24 * 335):
    """Annualized net earnings ($) from a trailing-average TCE, single-name scale."""
    avg = np.convolve(tce, np.ones(EARN_WIN) / EARN_WIN, mode="same")
    daily_margin = np.clip(avg - OPEX, -1e9, None)
    return daily_margin * fleet_days  # $/yr proxy


def stock_from_earnings(earn):
    """Market prices NORMALIZED (trailing-avg) earnings, not the latest spike."""
    norm = np.convolve(earn, np.ones(NORM_WIN) / NORM_WIN, mode="same")
    norm = np.clip(norm, 0, None)
    return PE * norm / 1e6  # arbitrary share-scale


# ────────────────────────────────────────────────────────────────────────────
# Experiment 1: same PEAK, different DURATION
# ────────────────────────────────────────────────────────────────────────────
def experiment_duration():
    peak = 200000.0
    base = mean_reverting(WEEKS, BASE_TCE, sigma=0.03)
    scenarios = {
        "spike_2w": 2,
        "plateau_6m": 26,
        "sustained_2y": 104,
    }
    out = {"peak_tce": peak, "base_tce": BASE_TCE, "scenarios": {}}
    start = 60
    for name, dur in scenarios.items():
        tce = inject_spike(base, start, dur, peak)
        earn = earnings_from_tce(tce)
        stk = stock_from_earnings(earn)
        pre = stk[start - 1]
        post_peak = float(np.max(stk[start:start + dur + NORM_WIN]))
        out["scenarios"][name] = {
            "duration_weeks": dur,
            "tce_peak": float(np.max(tce)),
            "avg_tce_over_episode": round(float(np.mean(tce[start:start + max(dur, 1)])), 0),
            "stock_pre": round(float(pre), 3),
            "stock_peak": round(post_peak, 3),
            "stock_rerate_x": round(post_peak / pre, 2) if pre > 0 else None,
            "tce_path": [round(float(v), 0) for v in tce],
            "stock_path": [round(float(v), 3) for v in stk],
        }
    return out


# ────────────────────────────────────────────────────────────────────────────
# Experiment 2: same DURATION, different PEAK (control)
# ────────────────────────────────────────────────────────────────────────────
def experiment_peak():
    base = mean_reverting(WEEKS, BASE_TCE, sigma=0.03)
    dur = 52
    start = 60
    out = {"duration_weeks": dur, "scenarios": {}}
    for name, peak in [("peak_120k", 120000.0), ("peak_200k", 200000.0), ("peak_350k", 350000.0)]:
        tce = inject_spike(base, start, dur, peak)
        stk = stock_from_earnings(earnings_from_tce(tce))
        pre = stk[start - 1]
        post = float(np.max(stk[start:start + dur + NORM_WIN]))
        out["scenarios"][name] = {
            "tce_peak": peak,
            "stock_rerate_x": round(post / pre, 2) if pre > 0 else None,
        }
    return out


# ────────────────────────────────────────────────────────────────────────────
# Experiment 3: signal quality — forward stock return after a SPOT spike
# signal vs after a SUSTAINED-AVERAGE signal. (Why spot-chasing is bad.)
# ────────────────────────────────────────────────────────────────────────────
def signal_quality(n_paths=600, fwd=26):
    """On many random rate paths (spikes that may be short or long), measure the
    forward `fwd`-week STOCK return after two signal types:
      - spot signal:  spot TCE crosses 1.8x baseline (fires on EVERY spike)
      - sustained signal: trailing-26w avg TCE crosses 1.4x baseline
                          (only fires when a spike has PERSISTED)
    Buying the stock on the spot signal should give poor/again-noisy forward
    returns; buying on the sustained signal should give materially better ones,
    because the stock prices the sustained average."""
    hi_spot, hi_avg = BASE_TCE * 1.8, BASE_TCE * 1.4
    spot_fwd, avg_fwd = [], []
    for _ in range(n_paths):
        rng = np.random.default_rng(int(RNG.integers(0, 1_000_000)))
        base = mean_reverting(WEEKS, BASE_TCE, sigma=0.05, seed_rng=rng)
        tce = base
        for _ in range(int(rng.integers(1, 4))):
            start = int(rng.integers(20, WEEKS - 30))
            dur = int(rng.choice([2, 4, 8, 26, 52, 104]))  # mostly short
            peak = float(rng.uniform(120000, 380000))
            tce = inject_spike(tce, start, dur, peak)
        stk = stock_from_earnings(earnings_from_tce(tce))
        trail = np.convolve(tce, np.ones(26) / 26, mode="same")

        for t in range(27, WEEKS - fwd):
            fret = (stk[t + fwd] - stk[t]) / stk[t] if stk[t] > 0 else np.nan
            # new-crossing detection (signal fires on the upcross only)
            if tce[t] > hi_spot and tce[t - 1] <= hi_spot:
                spot_fwd.append(fret)
            if trail[t] > hi_avg and trail[t - 1] <= hi_avg:
                avg_fwd.append(fret)

    def stats(a):
        a = np.array([x for x in a if np.isfinite(x)])
        if len(a) == 0:
            return {"n": 0}
        return {"n": int(len(a)),
                "mean_fwd_return": round(float(a.mean()), 3),
                "median_fwd_return": round(float(np.median(a)), 3),
                "win_rate": round(float((a > 0).mean()), 3)}

    return {"n_paths": n_paths, "forward_weeks": fwd,
            "spot_signal": stats(spot_fwd),
            "sustained_signal": stats(avg_fwd)}


def main():
    results = {
        "params": {"weeks": WEEKS, "base_tce": BASE_TCE, "opex": OPEX, "pe": PE,
                   "earnings_window_wks": EARN_WIN, "normalize_window_wks": NORM_WIN,
                   "note": "Synthetic; deterministic seed=42. Illustrates mechanism, "
                           "not a price forecast."},
        "exp1_duration": experiment_duration(),
        "exp2_peak_control": experiment_peak(),
        "exp3_signal_quality": signal_quality(),
    }
    # split heavy paths to a separate file for charts
    paths = {"exp1": results["exp1_duration"]}
    Path("sim_paths.json").write_text(json.dumps(paths))
    # strip paths from main results
    slim = json.loads(json.dumps(results))
    for k, sc in slim["exp1_duration"]["scenarios"].items():
        sc.pop("tce_path", None)
        sc.pop("stock_path", None)
    Path("sim_results.json").write_text(json.dumps(slim, indent=2))
    print("Wrote sim_results.json + sim_paths.json")

    print("\n=== EXP1: same PEAK ($200k), different DURATION -> stock re-rate ===")
    for name, sc in slim["exp1_duration"]["scenarios"].items():
        print(f"  {name:14s} dur={sc['duration_weeks']:3d}w  stock re-rate x{sc['stock_rerate_x']}")
    print("\n=== EXP2 (control): same DURATION (52w), different PEAK ===")
    for name, sc in slim["exp2_peak_control"]["scenarios"].items():
        print(f"  {name:10s} peak=${sc['tce_peak']:,.0f}  stock re-rate x{sc['stock_rerate_x']}")
    print("\n=== EXP3: signal quality (forward 26w stock return after signal) ===")
    t = slim["exp3_signal_quality"]
    for k in ["spot_signal", "sustained_signal"]:
        s = t[k]
        print(f"  {k:18s} n={s['n']:5d} mean_fwd={s['mean_fwd_return']:+.3f} "
              f"median_fwd={s['median_fwd_return']:+.3f} win={s['win_rate']:.2f}")


if __name__ == "__main__":
    main()
