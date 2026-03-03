#!/usr/bin/env python3
"""Generate charts for charter strategy comparison"""
import json
import os

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'matplotlib', '-q'])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

outdir = r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026\charts'
os.makedirs(outdir, exist_ok=True)

with open(r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026\chart_data.json') as f:
    data = json.load(f)

rates = [d['vlcc_rate']/1000 for d in data]
dht_profit = [d['dht_profit_m'] for d in data]
fro_profit = [d['fro_profit_m'] for d in data]
dht_eps = [d['dht_eps'] for d in data]
fro_eps = [d['fro_eps'] for d in data]

# Chart style
plt.rcParams.update({
    'figure.figsize': (12, 7),
    'font.size': 11,
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# ============================================================
# Chart 1: Fleet Profit vs VLCC Rate
# ============================================================
fig, ax = plt.subplots()
ax.plot(rates, dht_profit, 'b-', linewidth=2.5, label='DHT (54% spot / 46% TC)')
ax.plot(rates, fro_profit, 'r-', linewidth=2.5, label='FRO (83% spot / 17% TC)')
ax.axvline(x=107.1, color='green', linestyle='--', alpha=0.7, label='Q1 2026 Rate ($107K)')
ax.axvline(x=25, color='gray', linestyle=':', alpha=0.5, label='Breakeven ($25K)')
ax.fill_between(rates, dht_profit, fro_profit, alpha=0.1, color='red')
ax.set_xlabel('VLCC Spot Rate ($K/day)')
ax.set_ylabel('Annual Fleet Profit ($M)')
ax.set_title('Fleet Profit Sensitivity to VLCC Rates\nDHT (hedged) vs FRO (spot-heavy)')
ax.legend(loc='upper left')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
ax.set_xlim(25, 250)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '01_profit_sensitivity.png'), dpi=150)
plt.close()

# ============================================================
# Chart 2: EPS Sensitivity
# ============================================================
fig, ax = plt.subplots()
ax.plot(rates, dht_eps, 'b-', linewidth=2.5, label='DHT EPS')
ax.plot(rates, fro_eps, 'r-', linewidth=2.5, label='FRO EPS')
ax.axvline(x=107.1, color='green', linestyle='--', alpha=0.7, label='Q1 2026 Rate')
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_xlabel('VLCC Spot Rate ($K/day)')
ax.set_ylabel('EPS ($/share)')
ax.set_title('EPS Sensitivity to VLCC Rates\nDHT vs FRO')
ax.legend(loc='upper left')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}'))
ax.set_xlim(25, 250)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '02_eps_sensitivity.png'), dpi=150)
plt.close()

# ============================================================
# Chart 3: Elasticity comparison (% profit change for +10% rate)
# ============================================================
base_rates_k = [40, 50, 60, 75, 85, 100, 107, 120, 150, 175, 200]
dht_elast = []
fro_elast = []

for br_k in base_rates_k:
    br = br_k * 1000
    # DHT
    days = 365
    dht_base = (br - 25000) * 24 * 0.54 * days + (49400 - 25000) * 24 * 0.46 * days
    dht_up = (br*1.1 - 25000) * 24 * 0.54 * days + (49400 - 25000) * 24 * 0.46 * days
    dht_e = (dht_up - dht_base) / dht_base * 100 if dht_base > 0 else 100
    dht_elast.append(dht_e)
    
    # FRO (simplified - VLCC dominant)
    suez_r = br * 0.716
    lr2_r = br * 0.583
    fro_base = ((br-25000)*42*0.85 + (85000-25000)*42*0.15 + (suez_r-23700)*21*0.85 + (55000-23700)*21*0.15 + (lr2_r-23800)*18*0.80 + (45000-23800)*18*0.20) * days
    suez_r2 = br*1.1*0.716
    lr2_r2 = br*1.1*0.583
    fro_up = ((br*1.1-25000)*42*0.85 + (85000-25000)*42*0.15 + (suez_r2-23700)*21*0.85 + (55000-23700)*21*0.15 + (lr2_r2-23800)*18*0.80 + (45000-23800)*18*0.20) * days
    fro_e = (fro_up - fro_base) / fro_base * 100 if fro_base > 0 else 100
    fro_elast.append(fro_e)

fig, ax = plt.subplots()
ax.bar([x-0.2 for x in range(len(base_rates_k))], dht_elast, 0.4, label='DHT', color='steelblue')
ax.bar([x+0.2 for x in range(len(base_rates_k))], fro_elast, 0.4, label='FRO', color='indianred')
ax.set_xticks(range(len(base_rates_k)))
ax.set_xticklabels([f'${r}K' for r in base_rates_k], rotation=45)
ax.set_ylabel('Profit Change (%)')
ax.set_xlabel('Base VLCC Rate')
ax.set_title('Earnings Elasticity: Profit Change from +10% Rate Increase\nFRO consistently captures more upside')
ax.legend()
ax.axhline(y=10, color='gray', linestyle=':', alpha=0.5, label='10% (proportional)')
plt.tight_layout()
plt.savefig(os.path.join(outdir, '03_elasticity_comparison.png'), dpi=150)
plt.close()

# ============================================================
# Chart 4: Profit ratio (FRO/DHT) at different rates
# ============================================================
ratios = [f/d if d > 0 else 0 for f, d in zip(fro_profit, dht_profit)]
fig, ax = plt.subplots()
ax.plot(rates, ratios, 'purple', linewidth=2.5)
ax.axvline(x=107.1, color='green', linestyle='--', alpha=0.7, label='Q1 2026')
ax.axhline(y=1, color='gray', linestyle=':', alpha=0.5)
ax.fill_between(rates, 1, ratios, where=[r>1 for r in ratios], alpha=0.2, color='red', label='FRO outearns')
ax.set_xlabel('VLCC Spot Rate ($K/day)')
ax.set_ylabel('FRO Profit / DHT Profit')
ax.set_title('Profit Ratio: FRO vs DHT at Different VLCC Rates\nHigher ratio = FRO benefits more from rate increases')
ax.legend()
ax.set_xlim(25, 250)
ax.set_ylim(0, 5)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '04_profit_ratio.png'), dpi=150)
plt.close()

# ============================================================
# Chart 5: Charter Mix Pie Charts
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# DHT
sizes_dht = [54, 46]
labels_dht = ['Spot (54%)', 'Time Charter (46%)']
colors_dht = ['#FF6B6B', '#4ECDC4']
ax1.pie(sizes_dht, labels=labels_dht, colors=colors_dht, autopct='%1.0f%%', startangle=90,
        textprops={'fontsize': 13}, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax1.set_title('DHT Holdings\nCharter Mix (VLCC Fleet)', fontsize=14, fontweight='bold')

# FRO
sizes_fro = [83, 17]
labels_fro = ['Spot (83%)', 'Time Charter (17%)']
colors_fro = ['#FF6B6B', '#4ECDC4']
ax2.pie(sizes_fro, labels=labels_fro, colors=colors_fro, autopct='%1.0f%%', startangle=90,
        textprops={'fontsize': 13}, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax2.set_title('Frontline (FRO)\nCharter Mix (Fleet-wide)', fontsize=14, fontweight='bold')

plt.suptitle('Spot vs Time Charter Exposure Comparison', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(outdir, '05_charter_mix_pies.png'), dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# Chart 6: Scenario Earnings Waterfall
# ============================================================
scenarios = ['Bear\n$40K', 'Q4 2025\n$74K', 'Q1 2026\n$107K', 'Bull\n$150K', 'Super Bull\n$200K', '2008 Peak\n$230K']
dht_scenarios = []
fro_scenarios = []
for rate in [40000, 74200, 107100, 150000, 200000, 230000]:
    days = 365
    dht_p = ((rate - 25000) * 24 * 0.54 + (49400 - 25000) * 24 * 0.46) * days / 1e6
    suez_r = rate * 0.716
    lr2_r = rate * 0.583
    fro_p = ((rate-25000)*42*0.85 + (85000-25000)*42*0.15 + (suez_r-23700)*21*0.85 + (55000-23700)*21*0.15 + (lr2_r-23800)*18*0.80 + (45000-23800)*18*0.20) * days / 1e6
    dht_scenarios.append(dht_p)
    fro_scenarios.append(fro_p)

x = range(len(scenarios))
fig, ax = plt.subplots(figsize=(13, 7))
bars1 = ax.bar([i-0.2 for i in x], dht_scenarios, 0.38, label='DHT', color='steelblue', edgecolor='white')
bars2 = ax.bar([i+0.2 for i in x], fro_scenarios, 0.38, label='FRO', color='indianred', edgecolor='white')

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
            f'${bar.get_height():,.0f}M', ha='center', va='bottom', fontsize=9, color='steelblue')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
            f'${bar.get_height():,.0f}M', ha='center', va='bottom', fontsize=9, color='indianred')

ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.set_ylabel('Annual Fleet Profit ($M)')
ax.set_title('DHT vs FRO: Fleet Profit Across Rate Scenarios\nAccounting for Charter Mix (Spot + TC)', fontsize=13)
ax.legend(fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
plt.tight_layout()
plt.savefig(os.path.join(outdir, '06_scenario_comparison.png'), dpi=150)
plt.close()

print(f'Generated 6 charts in {outdir}')
for f in sorted(os.listdir(outdir)):
    print(f'  {f}')
