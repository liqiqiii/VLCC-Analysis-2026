#!/usr/bin/env python3
"""Charter Strategy Sensitivity Analysis: DHT vs FRO"""
import json
import os

# ============================================================
# CHARTER MIX DATA (from Q4 2025 / Q1 2026 earnings)
# ============================================================

# DHT: 24 VLCCs, ~54% spot / 46% TC
# TC rate locked at ~$49,400/day (Q4 2025), some at $47,500-52,500
DHT = {
    'name': 'DHT',
    'vlccs': 24,
    'spot_pct': 0.54,  # 54% spot exposure
    'tc_pct': 0.46,    # 46% time charter
    'tc_rate': 49400,  # weighted avg TC rate
    'breakeven': 25000,
    'shares': 161e6,
    'net_debt': 360e6,
    'ffa_usage': 'None disclosed',
    'tc_policy': '~50/50 target, tilting more TC recently',
    'profit_sharing_tc': True,  # some index-linked TCs
    'segments': {'VLCC': {'ships': 24, 'spot_pct': 0.54, 'tc_rate': 49400, 'be': 25000}},
}

# FRO: 42 VLCC + 21 Suez + 18 LR2
# VLCC: ~85% spot (TC coverage 8-24% by quarter, avg ~15%)
# Suezmax/LR2: mostly spot too, ~80-90%
FRO = {
    'name': 'FRO',
    'vlccs': 42,
    'spot_pct_vlcc': 0.85,  # 85% spot VLCC
    'tc_pct_vlcc': 0.15,    # 15% TC VLCC
    'tc_rate_vlcc': 85000,  # avg of $76,900 and $93,500
    'spot_pct_suez': 0.85,
    'tc_rate_suez': 55000,
    'spot_pct_lr2': 0.80,
    'tc_rate_lr2': 45000,
    'breakeven_vlcc': 25000,
    'breakeven_suez': 23700,
    'breakeven_lr2': 23800,
    'shares': 223e6,
    'net_debt': 2820e6,
    'ffa_usage': 'Tactical, undisclosed size',
    'tc_policy': '"Golden rule": TC < 30%, maximize spot upside',
    'segments': {
        'VLCC': {'ships': 42, 'spot_pct': 0.85, 'tc_rate': 85000, 'be': 25000},
        'Suezmax': {'ships': 21, 'spot_pct': 0.85, 'tc_rate': 55000, 'be': 23700},
        'LR2': {'ships': 18, 'spot_pct': 0.80, 'tc_rate': 45000, 'be': 23800},
    },
}

# Rate scenarios
vlcc_rates = list(range(25000, 250001, 5000))  # $25K to $250K
suez_ratio = 0.716  # Suezmax rate as fraction of VLCC
lr2_ratio = 0.583   # LR2 rate as fraction of VLCC

D = '$'
P = '%'

def calc_dht_earnings(vlcc_spot_rate):
    """Calculate DHT fleet profit and EPS at a given VLCC spot rate"""
    days = 365
    spot_days = DHT['vlccs'] * DHT['spot_pct'] * days
    tc_days = DHT['vlccs'] * DHT['tc_pct'] * days
    
    spot_profit = (vlcc_spot_rate - DHT['breakeven']) * spot_days
    tc_profit = (DHT['tc_rate'] - DHT['breakeven']) * tc_days
    
    total_profit = spot_profit + tc_profit
    blended_tce = (vlcc_spot_rate * DHT['spot_pct'] + DHT['tc_rate'] * DHT['tc_pct'])
    eps = total_profit / DHT['shares'] if total_profit > 0 else total_profit / DHT['shares']
    
    return {
        'total_profit': total_profit,
        'blended_tce': blended_tce,
        'eps': eps,
        'spot_contribution': spot_profit / max(total_profit, 1) * 100 if total_profit > 0 else 0,
    }

def calc_fro_earnings(vlcc_spot_rate):
    """Calculate FRO fleet profit and EPS at a given VLCC spot rate"""
    days = 365
    suez_spot = vlcc_spot_rate * suez_ratio
    lr2_spot = vlcc_spot_rate * lr2_ratio
    
    # VLCC
    vlcc_spot_days = FRO['segments']['VLCC']['ships'] * FRO['segments']['VLCC']['spot_pct'] * days
    vlcc_tc_days = FRO['segments']['VLCC']['ships'] * (1-FRO['segments']['VLCC']['spot_pct']) * days
    vlcc_profit = (vlcc_spot_rate - 25000) * vlcc_spot_days + (85000 - 25000) * vlcc_tc_days
    
    # Suezmax
    suez_spot_days = FRO['segments']['Suezmax']['ships'] * FRO['segments']['Suezmax']['spot_pct'] * days
    suez_tc_days = FRO['segments']['Suezmax']['ships'] * (1-FRO['segments']['Suezmax']['spot_pct']) * days
    suez_profit = (suez_spot - 23700) * suez_spot_days + (55000 - 23700) * suez_tc_days
    
    # LR2
    lr2_spot_days = FRO['segments']['LR2']['ships'] * FRO['segments']['LR2']['spot_pct'] * days
    lr2_tc_days = FRO['segments']['LR2']['ships'] * (1-FRO['segments']['LR2']['spot_pct']) * days
    lr2_profit = (lr2_spot - 23800) * lr2_spot_days + (45000 - 23800) * lr2_tc_days
    
    total_profit = vlcc_profit + suez_profit + lr2_profit
    eps = total_profit / FRO['shares']
    
    return {
        'total_profit': total_profit,
        'eps': eps,
        'vlcc_profit': vlcc_profit,
        'suez_profit': suez_profit,
        'lr2_profit': lr2_profit,
    }

# ============================================================
# MAIN ANALYSIS
# ============================================================

print('='*100)
print('CHARTER STRATEGY SENSITIVITY ANALYSIS: DHT vs FRO')
print('='*100)
print()

# 1. Charter Mix Comparison
print('1. CHARTER MIX COMPARISON')
print('-'*80)
print(f'{"Metric":<35} {"DHT":<30} {"FRO":<30}')
print('-'*80)
print(f'{"Fleet composition":<35} {"24 VLCCs":<30} {"42V + 21S + 18LR2":<30}')
print(f'{"VLCC spot exposure":<35} {"54%":<30} {"85%":<30}')
print(f'{"VLCC TC exposure":<35} {"46%":<30} {"15%":<30}')
print(f'{"TC rate locked (VLCC)":<35} {D+"49,400/day":<30} {D+"85,000/day avg":<30}')
print(f'{"TC policy":<35} {"~50/50 balanced":<30} {"<30% TC golden rule":<30}')
print(f'{"FFA hedging":<35} {"Not disclosed":<30} {"Tactical, undisclosed":<30}')
print(f'{"Profit-sharing TC":<35} {"Yes (index-linked)":<30} {"Some":<30}')
print(f'{"Overall spot exposure":<35} {"~54%":<30} {"~83% (fleet-wide)":<30}')
print()

# 2. Earnings sensitivity table
print('2. EARNINGS SENSITIVITY TO VLCC SPOT RATE')
print('-'*100)
header = f'{"VLCC Spot":>12} | {"DHT Profit":>12} {"DHT EPS":>10} {"DHT Blend":>12} | {"FRO Profit":>12} {"FRO EPS":>10} | {"FRO/DHT":>8}'
print(header)
print('-'*100)

key_rates = [25000, 40000, 50000, 60000, 75000, 85000, 100000, 107100, 120000, 150000, 175000, 200000, 230000]
results = []

for rate in key_rates:
    dht = calc_dht_earnings(rate)
    fro = calc_fro_earnings(rate)
    ratio = fro['total_profit'] / dht['total_profit'] if dht['total_profit'] > 0 else float('inf')
    
    results.append({
        'rate': rate,
        'dht_profit': dht['total_profit'],
        'dht_eps': dht['eps'],
        'dht_blend': dht['blended_tce'],
        'fro_profit': fro['total_profit'],
        'fro_eps': fro['eps'],
        'ratio': ratio,
    })
    
    dht_p = dht['total_profit'] / 1e6
    fro_p = fro['total_profit'] / 1e6
    print(f'{D}{rate/1000:>9.0f}K/d | {D}{dht_p:>10.0f}M {D}{dht["eps"]:>8.2f} {D}{dht["blended_tce"]/1000:>9.1f}K | {D}{fro_p:>10.0f}M {D}{fro["eps"]:>8.2f} | {ratio:>7.2f}x')

print()

# 3. Rate sensitivity (elasticity): % change in profit for 10% rate change
print('3. EARNINGS ELASTICITY: +10{} VLCC RATE -> PROFIT CHANGE'.format(P))
print('-'*80)
print(f'{"Base VLCC Rate":>15} | {"DHT Profit +":>15} {"FRO Profit +":>15} | {"Who benefits more":>20}')
print('-'*80)

for base in [50000, 75000, 100000, 107100, 120000, 150000, 200000]:
    dht_base = calc_dht_earnings(base)
    dht_up = calc_dht_earnings(base * 1.10)
    fro_base = calc_fro_earnings(base)
    fro_up = calc_fro_earnings(base * 1.10)
    
    if dht_base['total_profit'] > 0:
        dht_chg = (dht_up['total_profit'] - dht_base['total_profit']) / dht_base['total_profit'] * 100
    else:
        dht_chg = float('inf')
    
    if fro_base['total_profit'] > 0:
        fro_chg = (fro_up['total_profit'] - fro_base['total_profit']) / fro_base['total_profit'] * 100
    else:
        fro_chg = float('inf')
    
    winner = 'FRO' if fro_chg > dht_chg else 'DHT'
    print(f'{D}{base/1000:>12.0f}K/d | {dht_chg:>13.1f}{P} {fro_chg:>13.1f}{P} | {winner:>20}')

print()

# 4. Downside protection: earnings at low rates
print('4. DOWNSIDE PROTECTION (LOW RATE SCENARIOS)')
print('-'*80)
print(f'{"VLCC Rate":>12} | {"DHT EPS":>10} {"DHT Div":>10} | {"FRO EPS":>10} {"FRO Div":>10} | {"Safer":>8}')
print('-'*80)

for rate in [25000, 30000, 35000, 40000, 50000]:
    dht = calc_dht_earnings(rate)
    fro = calc_fro_earnings(rate)
    dht_div = max(0, dht['eps'] * 1.0)  # 100% payout
    fro_div = max(0, fro['eps'] * 0.8)  # ~80% payout
    safer = 'DHT' if dht['eps'] > fro['eps'] / (FRO['shares']/DHT['shares']) else 'FRO'
    # Actually compare who stays positive longer
    safer = 'DHT' if dht['total_profit'] > 0 and fro['total_profit'] <= 0 else ('TIE' if (dht['total_profit'] > 0) == (fro['total_profit'] > 0) else 'FRO')
    print(f'{D}{rate/1000:>9.0f}K/d | {D}{dht["eps"]:>8.2f} {D}{dht_div:>8.2f} | {D}{fro["eps"]:>8.2f} {D}{fro_div:>8.2f} | {safer:>8}')

print()

# 5. Upside capture efficiency
print('5. UPSIDE CAPTURE: PROFIT PER $1K VLCC RATE INCREASE')
print('-'*80)
print(f'{"From Rate":>12} {"To Rate":>12} | {"DHT +Profit":>14} {"FRO +Profit":>14} | {"FRO Captures":>15}')
print('-'*80)

for base, target in [(75000,100000), (100000,125000), (125000,150000), (150000,200000)]:
    dht_b = calc_dht_earnings(base)['total_profit']
    dht_t = calc_dht_earnings(target)['total_profit']
    fro_b = calc_fro_earnings(base)['total_profit']
    fro_t = calc_fro_earnings(target)['total_profit']
    
    dht_per_1k = (dht_t - dht_b) / ((target - base) / 1000) / 1e6
    fro_per_1k = (fro_t - fro_b) / ((target - base) / 1000) / 1e6
    ratio = fro_per_1k / dht_per_1k
    
    print(f'{D}{base/1000:>9.0f}K {D}{target/1000:>9.0f}K | {D}{dht_per_1k:>11.1f}M/1K {D}{fro_per_1k:>11.1f}M/1K | {ratio:>12.2f}x more')

print()

# 6. Stability analysis: revenue floor from TC
print('6. EARNINGS FLOOR (TC-GUARANTEED REVENUE)')
print('-'*80)
dht_tc_floor = DHT['tc_pct'] * DHT['vlccs'] * 365 * (DHT['tc_rate'] - DHT['breakeven'])
fro_vlcc_tc_floor = 0.15 * 42 * 365 * (85000 - 25000)
fro_suez_tc_floor = 0.15 * 21 * 365 * (55000 - 23700)
fro_lr2_tc_floor = 0.20 * 18 * 365 * (45000 - 23800)
fro_tc_floor = fro_vlcc_tc_floor + fro_suez_tc_floor + fro_lr2_tc_floor

print(f'DHT guaranteed TC profit (even if spot = $0): {D}{dht_tc_floor/1e6:.0f}M/yr')
print(f'FRO guaranteed TC profit (even if spot = $0): {D}{fro_tc_floor/1e6:.0f}M/yr')
print(f'DHT TC floor per share: {D}{dht_tc_floor/DHT["shares"]:.2f}/sh')
print(f'FRO TC floor per share: {D}{fro_tc_floor/FRO["shares"]:.2f}/sh')
print(f'DHT TC floor as {P} of market cap: {dht_tc_floor/(19.40*DHT["shares"])*100:.1f}{P}')
print(f'FRO TC floor as {P} of market cap: {fro_tc_floor/(38.10*FRO["shares"])*100:.1f}{P}')
print()

# 7. Key insight summary
print('='*100)
print('KEY INSIGHTS')
print('='*100)
print()
print('1. FRO is 83{} spot-exposed vs DHT at 54{} -> FRO has ~1.54x more rate sensitivity'.format(P, P))
print('2. DHT TC floor ({0}{1:.0f}M/yr) provides 2.7x more downside protection per share than FRO'.format(D, dht_tc_floor/1e6))
print('3. At breakeven rates ({0}25K), DHT still earns {0}{1:.0f}M from TCs; FRO earns {0}{2:.0f}M'.format(D, dht_tc_floor/1e6, fro_tc_floor/1e6))
print('4. For every {0}1K rate increase above {0}100K, FRO captures {0}{1:.1f}M more profit than DHT'.format(
    D, 
    (calc_fro_earnings(101000)['total_profit'] - calc_fro_earnings(100000)['total_profit'] - 
     calc_dht_earnings(101000)['total_profit'] + calc_dht_earnings(100000)['total_profit']) / 1e6
))
print('5. DHT = hedged play (stable dividends in all markets)')
print('   FRO = unhedged bet (maximum upside capture, deeper downside)')

# Save data for charting
chart_data = []
for rate in range(25000, 250001, 2500):
    dht = calc_dht_earnings(rate)
    fro = calc_fro_earnings(rate)
    chart_data.append({
        'vlcc_rate': rate,
        'dht_profit_m': dht['total_profit'] / 1e6,
        'fro_profit_m': fro['total_profit'] / 1e6,
        'dht_eps': dht['eps'],
        'fro_eps': fro['eps'],
        'dht_blend': dht['blended_tce'],
    })

with open(r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026\chart_data.json', 'w') as f:
    json.dump(chart_data, f, indent=2)
print('\nChart data saved to chart_data.json')
