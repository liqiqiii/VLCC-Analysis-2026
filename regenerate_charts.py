#!/usr/bin/env python3
"""Regenerate charts with corrected DHT 75% spot model"""
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

outdir = r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026\charts'
os.makedirs(outdir, exist_ok=True)

# Corrected parameters
DHT_SPOT = 0.75  # Q2 2026 target
DHT_TC = 0.25
DHT_SHIPS = 24
DHT_TC_RATE = 49400
DHT_BE = 25000
DHT_SHARES = 161e6

FRO_SHARES = 223e6

suez_ratio = 0.716
lr2_ratio = 0.583

def calc_dht(rate):
    days = 365
    spot = (rate - DHT_BE) * DHT_SHIPS * DHT_SPOT * days
    tc = (DHT_TC_RATE - DHT_BE) * DHT_SHIPS * DHT_TC * days
    return spot + tc

def calc_dht_old(rate):
    """Old 54% spot model for comparison"""
    days = 365
    spot = (rate - DHT_BE) * DHT_SHIPS * 0.54 * days
    tc = (DHT_TC_RATE - DHT_BE) * DHT_SHIPS * 0.46 * days
    return spot + tc

def calc_fro(rate):
    days = 365
    suez_r = rate * suez_ratio
    lr2_r = rate * lr2_ratio
    vlcc = (rate - 25000) * 42 * 0.85 + (85000 - 25000) * 42 * 0.15
    suez = (suez_r - 23700) * 21 * 0.85 + (55000 - 23700) * 21 * 0.15
    lr2 = (lr2_r - 23800) * 18 * 0.80 + (45000 - 23800) * 18 * 0.20
    return (vlcc + suez + lr2) * days

rates_k = list(range(25, 251, 2))
rates = [r * 1000 for r in rates_k]

dht_profit = [calc_dht(r) / 1e6 for r in rates]
dht_old_profit = [calc_dht_old(r) / 1e6 for r in rates]
fro_profit = [calc_fro(r) / 1e6 for r in rates]
dht_eps = [calc_dht(r) / DHT_SHARES for r in rates]
dht_old_eps = [calc_dht_old(r) / DHT_SHARES for r in rates]
fro_eps = [calc_fro(r) / FRO_SHARES for r in rates]

plt.rcParams.update({
    'figure.figsize': (12, 7),
    'font.size': 11,
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# ============================================================
# Chart 1: Profit Sensitivity (with old vs new DHT)
# ============================================================
fig, ax = plt.subplots()
ax.plot(rates_k, dht_old_profit, 'b--', linewidth=1.5, alpha=0.5, label='DHT OLD (54% spot)')
ax.plot(rates_k, dht_profit, 'b-', linewidth=2.5, label='DHT CORRECTED (75% spot)')
ax.plot(rates_k, fro_profit, 'r-', linewidth=2.5, label='FRO (83% spot)')
ax.axvline(x=107, color='green', linestyle='--', alpha=0.7, label='Q1 2026 Rate ($107K)')
ax.fill_between(rates_k, dht_profit, fro_profit, alpha=0.08, color='red')
ax.fill_between(rates_k, dht_old_profit, dht_profit, alpha=0.15, color='blue',
                label='DHT strategy shift gain')
ax.set_xlabel('VLCC Spot Rate ($K/day)')
ax.set_ylabel('Annual Fleet Profit ($M)')
ax.set_title('Fleet Profit Sensitivity: DHT Strategy Shift Impact\n'
             'DHT moving from 54% → 75% spot narrows gap with FRO')
ax.legend(loc='upper left', fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
ax.set_xlim(25, 250)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '01_profit_sensitivity.png'), dpi=150)
plt.close()

# ============================================================
# Chart 2: EPS Sensitivity (with old vs new)
# ============================================================
fig, ax = plt.subplots()
ax.plot(rates_k, dht_old_eps, 'b--', linewidth=1.5, alpha=0.5, label='DHT OLD (54% spot)')
ax.plot(rates_k, dht_eps, 'b-', linewidth=2.5, label='DHT CORRECTED (75% spot)')
ax.plot(rates_k, fro_eps, 'r-', linewidth=2.5, label='FRO EPS')
ax.axvline(x=107, color='green', linestyle='--', alpha=0.7, label='Q1 2026 Rate')
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_xlabel('VLCC Spot Rate ($K/day)')
ax.set_ylabel('EPS ($/share)')
ax.set_title('EPS Sensitivity: DHT Corrected vs FRO\n'
             'Gap narrows significantly with 75% spot')
ax.legend(loc='upper left')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}'))
ax.set_xlim(25, 250)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '02_eps_sensitivity.png'), dpi=150)
plt.close()

# ============================================================
# Chart 3: Elasticity (corrected)
# ============================================================
base_rates_k = [40, 50, 60, 75, 85, 100, 107, 120, 150, 175, 200]
dht_elast = []
fro_elast = []

for br_k in base_rates_k:
    br = br_k * 1000
    dht_b = calc_dht(br)
    dht_u = calc_dht(br * 1.10)
    fro_b = calc_fro(br)
    fro_u = calc_fro(br * 1.10)
    dht_e = (dht_u - dht_b) / dht_b * 100 if dht_b > 0 else 100
    fro_e = (fro_u - fro_b) / fro_b * 100 if fro_b > 0 else 100
    dht_elast.append(dht_e)
    fro_elast.append(fro_e)

fig, ax = plt.subplots()
x_pos = range(len(base_rates_k))
ax.bar([x-0.2 for x in x_pos], dht_elast, 0.4, label='DHT (75% spot)', color='steelblue')
ax.bar([x+0.2 for x in x_pos], fro_elast, 0.4, label='FRO (83% spot)', color='indianred')
ax.set_xticks(list(x_pos))
ax.set_xticklabels([f'${r}K' for r in base_rates_k], rotation=45)
ax.set_ylabel('Profit Change (%)')
ax.set_xlabel('Base VLCC Rate')
ax.set_title('Earnings Elasticity: +10% Rate Increase\n'
             'DHT now much closer to FRO (was 10.4% vs 12.4%, now 11.8% vs 12.4% at $100K)')
ax.legend()
ax.axhline(y=10, color='gray', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '03_elasticity_comparison.png'), dpi=150)
plt.close()

# ============================================================
# Chart 4: Profit ratio (corrected)
# ============================================================
ratios_new = [calc_fro(r) / calc_dht(r) if calc_dht(r) > 0 else 0 for r in rates]
ratios_old = [calc_fro(r) / calc_dht_old(r) if calc_dht_old(r) > 0 else 0 for r in rates]

fig, ax = plt.subplots()
ax.plot(rates_k, ratios_old, 'purple', linewidth=1.5, alpha=0.5, linestyle='--',
        label='Old model (54% spot): FRO/DHT')
ax.plot(rates_k, ratios_new, 'purple', linewidth=2.5,
        label='Corrected (75% spot): FRO/DHT')
ax.axvline(x=107, color='green', linestyle='--', alpha=0.7, label='Q1 2026')
ax.fill_between(rates_k, ratios_new, ratios_old, alpha=0.15, color='blue',
                label='DHT gains from strategy shift')
ax.set_xlabel('VLCC Spot Rate ($K/day)')
ax.set_ylabel('FRO Profit / DHT Profit')
ax.set_title('Profit Ratio: FRO vs DHT (Corrected)\n'
             'Ratio drops from ~3.7x to ~3.1x at current rates — gap narrowing')
ax.legend(fontsize=10)
ax.set_xlim(25, 250)
ax.set_ylim(0, 5)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '04_profit_ratio.png'), dpi=150)
plt.close()

# ============================================================
# Chart 5: Charter Mix Pies (CORRECTED)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

sizes_dht = [75, 25]
labels_dht = ['Spot (75%)\n→ was 54%', 'Time Charter (25%)\n→ was 46%']
colors_dht = ['#FF6B6B', '#4ECDC4']
ax1.pie(sizes_dht, labels=labels_dht, colors=colors_dht, autopct='%1.0f%%', startangle=90,
        textprops={'fontsize': 12}, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax1.set_title('DHT Holdings (Q2 2026 Target)\nCharter Mix — SHIFTED', fontsize=14, fontweight='bold')

sizes_fro = [83, 17]
labels_fro = ['Spot (83%)', 'Time Charter (17%)']
colors_fro = ['#FF6B6B', '#4ECDC4']
ax2.pie(sizes_fro, labels=labels_fro, colors=colors_fro, autopct='%1.0f%%', startangle=90,
        textprops={'fontsize': 12}, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax2.set_title('Frontline (FRO)\nCharter Mix (Fleet-wide)', fontsize=14, fontweight='bold')

plt.suptitle('DHT Strategy Shift: Converging with FRO', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '05_charter_mix_pies.png'), dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Chart 6: Scenario Comparison (corrected)
# ============================================================
scenarios = ['Bear\n$40K', 'Q4 2025\n$74K', 'Q1 2026\n$107K', 'Bull\n$150K', 'Super\n$200K', '2008\n$230K']
dht_sc = [calc_dht(r)/1e6 for r in [40000, 74200, 107100, 150000, 200000, 230000]]
dht_old_sc = [calc_dht_old(r)/1e6 for r in [40000, 74200, 107100, 150000, 200000, 230000]]
fro_sc = [calc_fro(r)/1e6 for r in [40000, 74200, 107100, 150000, 200000, 230000]]

x = range(len(scenarios))
fig, ax = plt.subplots(figsize=(14, 7))
w = 0.25
bars0 = ax.bar([i-w for i in x], dht_old_sc, w, label='DHT OLD (54%)', color='lightsteelblue',
               edgecolor='white', alpha=0.7)
bars1 = ax.bar([i for i in x], dht_sc, w, label='DHT CORRECTED (75%)', color='steelblue',
               edgecolor='white')
bars2 = ax.bar([i+w for i in x], fro_sc, w, label='FRO (83%)', color='indianred',
               edgecolor='white')

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
            f'${bar.get_height():,.0f}M', ha='center', va='bottom', fontsize=8, color='steelblue')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
            f'${bar.get_height():,.0f}M', ha='center', va='bottom', fontsize=8, color='indianred')

ax.set_xticks(list(x))
ax.set_xticklabels(scenarios)
ax.set_ylabel('Annual Fleet Profit ($M)')
ax.set_title('DHT vs FRO: Fleet Profit (CORRECTED for DHT Strategy Shift)\n'
             'Blue shaded area shows DHT gain from 54% → 75% spot', fontsize=13)
ax.legend(fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
plt.tight_layout()
plt.savefig(os.path.join(outdir, '06_scenario_comparison.png'), dpi=150)
plt.close()

# ============================================================
# Chart 7: NEW — Booking Rate vs Charter Type (visual explainer)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# DHT booking breakdown
categories = ['TC\n(100% locked)', 'Spot Fixed\n(booked)', 'Spot Open\n(unfixed)']
dht_vals = [797/2160*100, (1425-797)/2160*100, (2160-1425)/2160*100]  # Jan 14 snapshot
colors_booking = ['#4ECDC4', '#FFB347', '#FF6B6B']
bars = ax1.bar(categories, dht_vals, color=colors_booking, edgecolor='white', linewidth=2)
ax1.set_ylabel('% of Q1 Revenue Days')
ax1.set_title('DHT Q1 2026 Day Breakdown\n(Jan 14 snapshot: 66% locked)', fontsize=13, fontweight='bold')
for bar, val in zip(bars, dht_vals):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             f'{val:.0f}%', ha='center', va='bottom', fontsize=13, fontweight='bold')
ax1.set_ylim(0, 55)

# FRO VLCC booking breakdown
fro_vals = [8, 84, 8]  # ~8% TC, ~84% spot fixed, ~8% open
bars = ax2.bar(categories, fro_vals, color=colors_booking, edgecolor='white', linewidth=2)
ax2.set_ylabel('% of Q1 VLCC Days')
ax2.set_title('FRO VLCC Q1 2026 Day Breakdown\n(92% locked)', fontsize=13, fontweight='bold')
for bar, val in zip(bars, fro_vals):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             f'{val:.0f}%', ha='center', va='bottom', fontsize=13, fontweight='bold')
ax2.set_ylim(0, 100)

plt.suptitle('Booking Rate ≠ Charter Type: Both Have Low Near-Term Risk',
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '07_booking_rate_explainer.png'), dpi=150, bbox_inches='tight')
plt.close()

print(f'Generated 7 charts in {outdir}:')
for f in sorted(os.listdir(outdir)):
    if f.endswith('.png'):
        print(f'  {f}')
