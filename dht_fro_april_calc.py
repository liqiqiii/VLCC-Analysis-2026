#!/usr/bin/env python3
"""
DHT vs FRO: April 2026 Updated Calculation Engine
Updated prices, charter mix, fleet, $200K/$250K scenarios, Hormuz blended
"""
import json, os

D = '$'

# ============================================================
# UPDATED COMPANY DATA (April 8, 2026)
# ============================================================

DHT = {
    'name': 'DHT Holdings', 'price': 18.57, 'shares': 161.0, 'bv': 7.05,
    'payout_base': 0.95, 'net_debt': 360, 'equity': 1133,
    'vlccs': 24,  # 20 existing + 4 newbuilds (Antelope Jan, Addax Mar, Gazelle Mar, Impala Q2)
    'spot_pct': 0.75,  # UPDATED: shifting to 75% spot by Q2 2026 (was 54%)
    'tc_rate': 52000,   # UPDATED: weighted avg TC including new Opal $90K and Harrier $47.5K deals
    'breakeven': 25000,
    'ev': 3350,  # mktcap + net debt
    'fleet_age': 10,
    'newbuilds': 4,
    'tc_vessels': {  # individual TC deals
        'DHT Opal': {'rate': 90000, 'until': 'Q1 2027'},
        'DHT Harrier': {'rate': 47500, 'until': 'Q4 2030'},
        'DHT Leopard': {'rate': 49000, 'until': 'Q4 2027'},
        'DHT Tiger': {'rate': 45000, 'until': 'Q2 2026'},  # expiring soon!
        'DHT Osprey': {'rate': 48000, 'until': 'Q2 2027'},
        'DHT Gazelle': {'rate': 52000, 'until': 'Q1 2031'},  # new 5-7yr TC
    },
}

FRO = {
    'name': 'Frontline', 'price': 35.08, 'shares': 223.0, 'bv': 10.44,
    'payout_base': 0.85, 'net_debt': 2820, 'equity': 2325,
    'vlccs': 42,
    'suezmax': 21,
    'lr2': 18,
    'spot_pct_vlcc': 0.85,
    'spot_pct_suez': 0.85,
    'spot_pct_lr2': 0.80,
    'tc_rate_vlcc': 85000,
    'tc_rate_suez': 55000,
    'tc_rate_lr2': 45000,
    'be_vlcc': 25000,
    'be_suez': 23700,
    'be_lr2': 23800,
    'ev': 10643,
    'fleet_age': 8,
    'newbuilds': 9,
}

INSW = {  # benchmark comparison
    'name': 'Intl Seaways', 'price': 75.38, 'shares': 49.4, 'bv': 40.89,
    'payout_base': 0.87, 'net_debt': 250,
}

SUEZ_RATIO = 0.716
LR2_RATIO = 0.583
DAYS = 330

def calc_dht(vlcc_rate):
    spot_days = DHT['vlccs'] * DHT['spot_pct'] * DAYS
    tc_days = DHT['vlccs'] * (1 - DHT['spot_pct']) * DAYS
    profit = (vlcc_rate - DHT['breakeven']) * spot_days + (DHT['tc_rate'] - DHT['breakeven']) * tc_days
    eps = profit / (DHT['shares'] * 1e6)
    return profit, eps

def calc_fro(vlcc_rate):
    suez_rate = vlcc_rate * SUEZ_RATIO
    lr2_rate = vlcc_rate * LR2_RATIO
    v_profit = (vlcc_rate - FRO['be_vlcc']) * FRO['vlccs'] * FRO['spot_pct_vlcc'] * DAYS + \
               (FRO['tc_rate_vlcc'] - FRO['be_vlcc']) * FRO['vlccs'] * (1 - FRO['spot_pct_vlcc']) * DAYS
    s_profit = (suez_rate - FRO['be_suez']) * FRO['suezmax'] * FRO['spot_pct_suez'] * DAYS + \
               (FRO['tc_rate_suez'] - FRO['be_suez']) * FRO['suezmax'] * (1 - FRO['spot_pct_suez']) * DAYS
    l_profit = (lr2_rate - FRO['be_lr2']) * FRO['lr2'] * FRO['spot_pct_lr2'] * DAYS + \
               (FRO['tc_rate_lr2'] - FRO['be_lr2']) * FRO['lr2'] * (1 - FRO['spot_pct_lr2']) * DAYS
    profit = v_profit + s_profit + l_profit
    eps = profit / (FRO['shares'] * 1e6)
    return profit, eps, v_profit, s_profit, l_profit

# ============================================================
# GENERATE ALL TABLES
# ============================================================

rates = [75000, 90000, 100000, 120000, 150000, 200000, 250000]
dp = DHT['price']; fp = FRO['price']

print('=' * 120)
print('DHT vs FRO: APRIL 2026 UPDATED ANALYSIS')
print('=' * 120)
print()
print('UPDATED DATA vs MARCH REPORT:')
print(f"  DHT price: $19.40 -> ${dp} ({(dp/19.40-1)*100:+.1f}%)")
print(f"  FRO price: $38.10 -> ${fp} ({(fp/38.10-1)*100:+.1f}%)")
print(f"  DHT charter mix: 54% spot -> 75% spot (DHT shifting, Tiger TC expiring Q2)")
print(f"  DHT fleet: 24 VLCCs (4 newbuilds delivered Jan-Mar 2026)")
print(f"  DHT TC rate: $49,400 -> $52,000 (Opal $90K deal lifts avg)")
print(f"  Market: Baltic TD3C hit $445K/day all-time record (Hormuz crisis)")
print(f"  DHT MktCap: $3,130M -> ${dp*161:.0f}M | FRO MktCap: $8,500M -> ${fp*223:.0f}M")
print()

# TL;DR Table
print('TL;DR: QUAD-SCENARIO SUMMARY')
print('-' * 120)
hdr = f"{'Metric':<25s}"
for rate in [100000, 150000, 200000, 250000]:
    hdr += f" {'DHT@'+str(rate//1000)+'K':>12s} {'FRO@'+str(rate//1000)+'K':>12s}"
print(hdr)
print('-' * 120)

metrics_rows = []
for label, calc_fn in [
    ('EPS', lambda r: (calc_dht(r)[1], calc_fro(r)[1])),
    ('P/E', lambda r: (dp/calc_dht(r)[1], fp/calc_fro(r)[1])),
    ('P/B (trailing)', lambda r: (dp/DHT['bv'], fp/FRO['bv'])),
    ('Implied ROE', lambda r: (calc_dht(r)[1]/DHT['bv']*100, calc_fro(r)[1]/FRO['bv']*100)),
    ('Div Yield (95%/85%)', lambda r: (calc_dht(r)[1]*0.95/dp*100, calc_fro(r)[1]*0.85/fp*100)),
    ('TP @ 7x PE', lambda r: (calc_dht(r)[1]*7, calc_fro(r)[1]*7)),
    ('TP @ 5x PE', lambda r: (calc_dht(r)[1]*5, calc_fro(r)[1]*5)),
    ('Annual Profit (M)', lambda r: (calc_dht(r)[0]/1e6, calc_fro(r)[0]/1e6)),
]:
    row = f"  {label:<23s}"
    for rate in [100000, 150000, 200000, 250000]:
        d, f = calc_fn(rate)
        if 'EPS' == label:
            row += f" {D}{d:>10.2f} {D}{f:>10.2f}"
        elif 'P/E' in label:
            row += f" {d:>11.1f}x {f:>11.1f}x"
        elif 'P/B' in label:
            row += f" {d:>11.2f}x {f:>11.2f}x"
        elif 'ROE' in label:
            row += f" {d:>10.0f}% {f:>10.0f}%"
        elif 'Yield' in label:
            row += f" {d:>10.1f}% {f:>10.1f}%"
        elif 'TP' in label:
            du = (d/dp-1)*100; fu = (f/fp-1)*100
            row += f" {D}{d:>7.2f}({du:+.0f}%) {D}{f:>7.2f}({fu:+.0f}%)"
        elif 'Profit' in label:
            row += f" {D}{d:>9.0f}M {D}{f:>9.0f}M"
    print(row)

print()

# Full sensitivity
print('FULL EARNINGS SENSITIVITY (7 scenarios)')
print('-' * 100)
print(f"{'Rate':>10s} | {'DHT Profit':>12s} {'DHT EPS':>10s} {'DHT P/E':>8s} {'DHT DY':>8s} | {'FRO Profit':>12s} {'FRO EPS':>10s} {'FRO P/E':>8s} {'FRO DY':>8s}")
print('-' * 100)
for rate in rates:
    dp_r, de = calc_dht(rate)
    fp_r, fe = calc_fro(rate)[:2]
    dpe = dp/de; fpe = fp/fe
    ddy = de*0.95/dp*100; fdy = fe*0.85/fp*100
    print(f" {D}{rate//1000:>6d}K/d | {D}{dp_r/1e6:>9.0f}M {D}{de:>8.2f} {dpe:>7.1f}x {ddy:>6.1f}% | {D}{fp_r/1e6:>9.0f}M {D}{fe:>8.2f} {fpe:>7.1f}x {fdy:>6.1f}%")

# Hormuz blended
print()
print('HORMUZ BLENDED 2026 SCENARIOS')
print('-' * 100)
scenarios = [
    ('Hormuz opens May', {'Q1': (79000,90), 'Q2': (120000,91), 'Q3': (75000,92), 'Q4': (70000,92)}),
    ('Hormuz opens Aug', {'Q1': (79000,90), 'Q2': (200000,91), 'Q3': (120000,92), 'Q4': (80000,92)}),
    ('Hormuz closed all year', {'Q1': (79000,90), 'Q2': (250000,91), 'Q3': (200000,92), 'Q4': (150000,92)}),
]
for label, qs in scenarios:
    td = sum(q[1] for q in qs.values())
    wr = sum(q[0]*q[1] for q in qs.values()) / td
    dp_r, de = calc_dht(wr)
    fp_r, fe = calc_fro(wr)[:2]
    print(f"  {label:<25s} Blended {D}{wr/1000:.1f}K/d")
    print(f"    DHT: EPS {D}{de:.2f} | P/E {dp/de:.1f}x | DY {de*0.95/dp*100:.1f}% | TP@7x {D}{de*7:.2f} ({(de*7/dp-1)*100:+.0f}%) | Profit {D}{dp_r/1e6:.0f}M")
    print(f"    FRO: EPS {D}{fe:.2f} | P/E {fp/fe:.1f}x | DY {fe*0.85/fp*100:.1f}% | TP@7x {D}{fe*7:.2f} ({(fe*7/fp-1)*100:+.0f}%) | Profit {D}{fp_r/1e6:.0f}M")
    print()

# Operating leverage
print('OPERATING LEVERAGE (updated for 75% spot DHT)')
print('-' * 80)
print(f"{'Rate':>10s} | {'vs BE':>6s} | {'DHT Margin':>12s} {'FRO VLCC Margin':>16s}")
print('-' * 80)
for rate in [25000, 50000, 75000, 100000, 150000, 200000, 250000]:
    vs_be = rate / 25000
    d_margin = (rate - 25000) / rate * 100 if rate > 0 else 0
    f_margin = (rate - 25000) / rate * 100 if rate > 0 else 0
    print(f" {D}{rate//1000:>6d}K/d | {vs_be:>5.1f}x | {d_margin:>10.0f}% {f_margin:>14.0f}%")

# Charter strategy detail
print()
print('CHARTER STRATEGY UPDATE (April 2026)')
print('-' * 80)
print('DHT TC Fleet Employment:')
for vessel, info in DHT['tc_vessels'].items():
    print(f"  {vessel:<20s} {D}{info['rate']:>6,}/day  until {info['until']}")
print()
tc_floor = DHT['vlccs'] * (1-DHT['spot_pct']) * DAYS * (DHT['tc_rate'] - DHT['breakeven'])
fro_tc_floor = FRO['vlccs']*(1-FRO['spot_pct_vlcc'])*DAYS*(FRO['tc_rate_vlcc']-FRO['be_vlcc']) + \
               FRO['suezmax']*(1-FRO['spot_pct_suez'])*DAYS*(FRO['tc_rate_suez']-FRO['be_suez']) + \
               FRO['lr2']*(1-FRO['spot_pct_lr2'])*DAYS*(FRO['tc_rate_lr2']-FRO['be_lr2'])
print(f"  DHT TC earnings floor (spot=0): {D}{tc_floor/1e6:.0f}M/yr ({D}{tc_floor/161e6:.2f}/sh)")
print(f"  FRO TC earnings floor (spot=0): {D}{fro_tc_floor/1e6:.0f}M/yr ({D}{fro_tc_floor/223e6:.2f}/sh)")

# Valuation matrix
print()
print('VALUATION MATRIX (April 2026)')
print('-' * 80)
_, de100 = calc_dht(100000)
_, fe100 = calc_fro(100000)[:2]
_, de150 = calc_dht(150000)
_, fe150 = calc_fro(150000)[:2]

metrics = [
    ('Market Cap', f"{D}{dp*161:.0f}M", f"{D}{fp*223:.0f}M"),
    ('Enterprise Value', f"{D}{DHT['ev']:.0f}M", f"{D}{FRO['ev']:.0f}M"),
    ('P/B', f"{dp/DHT['bv']:.2f}x", f"{fp/FRO['bv']:.2f}x"),
    ('EV/EBITDA (est @100K)', f"{DHT['ev']/(de100*161+50):.1f}x", f"{FRO['ev']/(fe100*223+200):.1f}x"),
    ('P/E @ $100K', f"{dp/de100:.1f}x", f"{fp/fe100:.1f}x"),
    ('P/E @ $150K', f"{dp/de150:.1f}x", f"{fp/fe150:.1f}x"),
    ('FCF Yield @ $100K (est)', f"{de100*0.9/dp*100:.1f}%", f"{fe100*0.85/fp*100:.1f}%"),
    ('VLCC-eq fleet', '24.0', f"{42+21*SUEZ_RATIO+18*LR2_RATIO:.1f}"),
    ('MktCap/VLCC-eq', f"{D}{dp*161/24:.0f}M", f"{D}{fp*223/(42+21*SUEZ_RATIO+18*LR2_RATIO):.0f}M"),
    ('EV/VLCC-eq', f"{D}{DHT['ev']/24:.0f}M", f"{D}{FRO['ev']/(42+21*SUEZ_RATIO+18*LR2_RATIO):.0f}M"),
]
print(f"  {'Metric':<28s} {'DHT':>18s} {'FRO':>18s}")
print(f"  {'-'*64}")
for label, d_val, f_val in metrics:
    print(f"  {label:<28s} {d_val:>18s} {f_val:>18s}")

# FRO vs DHT segment breakdown at key rates
print()
print('FRO SEGMENT BREAKDOWN')
print('-' * 80)
print(f"{'Rate':>10s} | {'VLCC Profit':>14s} {'Suez Profit':>14s} {'LR2 Profit':>14s} {'Total':>14s}")
print('-' * 80)
for rate in [100000, 150000, 200000, 250000]:
    _, _, vp, sp, lp = calc_fro(rate)
    print(f" {D}{rate//1000:>6d}K/d | {D}{vp/1e6:>11.0f}M {D}{sp/1e6:>11.0f}M {D}{lp/1e6:>11.0f}M {D}{(vp+sp+lp)/1e6:>11.0f}M")

# Per $1K sensitivity
print()
print('RATE SENSITIVITY: per $1K VLCC rate increase')
d1, _ = calc_dht(100000); d2, _ = calc_dht(101000)
f1, _ = calc_fro(100000)[:2]; f2, _ = calc_fro(101000)[:2]
dht_per_1k = (d2 - d1) / 1e6
fro_per_1k = (f2 - f1) / 1e6 if isinstance(f2, (int,float)) else ((calc_fro(101000)[0] - calc_fro(100000)[0]) / 1e6)
print(f"  DHT: {D}{dht_per_1k:.1f}M profit / {D}{dht_per_1k/161:.4f} EPS per {D}1K rate increase")
# recalculate properly
d1p = calc_dht(100000)[0]; d2p = calc_dht(101000)[0]
f1p = calc_fro(100000)[0]; f2p = calc_fro(101000)[0]
print(f"  DHT: {D}{(d2p-d1p)/1e6:.1f}M / {D}{(d2p-d1p)/161e6:.4f} EPS per {D}1K")
print(f"  FRO: {D}{(f2p-f1p)/1e6:.1f}M / {D}{(f2p-f1p)/223e6:.4f} EPS per {D}1K")
print(f"  FRO captures {(f2p-f1p)/(d2p-d1p):.1f}x more per {D}1K rate increase")

# Save output data
output = {'rates': {}, 'hormuz': {}, 'meta': {
    'dht_price': dp, 'fro_price': fp, 'date': '2026-04-08',
    'dht_shares': 161, 'fro_shares': 223,
    'dht_bv': DHT['bv'], 'fro_bv': FRO['bv'],
    'dht_spot_pct': DHT['spot_pct'], 'fro_spot_pct': FRO['spot_pct_vlcc'],
}}
for rate in range(25000, 260000, 5000):
    dp_r, de = calc_dht(rate)
    fp_r, fe = calc_fro(rate)[:2]
    output['rates'][rate] = {
        'dht_profit_m': round(dp_r/1e6, 1), 'dht_eps': round(de, 4),
        'fro_profit_m': round(fp_r/1e6, 1), 'fro_eps': round(fe, 4),
    }

opath = os.path.join(os.path.dirname(__file__), 'dht_fro_april_data.json')
with open(opath, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nData saved to dht_fro_april_data.json")
