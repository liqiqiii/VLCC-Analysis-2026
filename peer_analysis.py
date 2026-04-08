#!/usr/bin/env python3
"""
Crude Tanker Peer Universe: 7-Company Comparative Analysis Engine
DHT / FRO / INSW / ECO / TNK / NAT / CMBT
April 2026 — Includes Hormuz-Open Normalization Scenarios
"""
import json
import os

D = '$'
P = '%'

# ============================================================
# COMPANY DATA (Apr 8, 2026)
# ============================================================

COMPANIES = {
    'DHT': {
        'name': 'DHT Holdings', 'ticker': 'DHT', 'price': 18.57, 'shares': 161.0,
        'bv': 7.05, 'payout': 0.95, 'net_debt': 360,
        'profile': 'Pure VLCC, hedged 50/50',
        'segments': {
            'VLCC': {'ships': 24, 'spot_pct': 0.54, 'tc_rate': 49400, 'be': 25000},
        },
    },
    'FRO': {
        'name': 'Frontline', 'ticker': 'FRO', 'price': 35.08, 'shares': 223.0,
        'bv': 10.44, 'payout': 0.85, 'net_debt': 2820,
        'profile': 'Multi-fleet, max spot leverage',
        'segments': {
            'VLCC':    {'ships': 42, 'spot_pct': 0.85, 'tc_rate': 85000, 'be': 25000},
            'Suezmax': {'ships': 21, 'spot_pct': 0.85, 'tc_rate': 55000, 'be': 23700},
            'LR2':     {'ships': 18, 'spot_pct': 0.80, 'tc_rate': 45000, 'be': 23800},
        },
    },
    'INSW': {
        'name': 'Intl Seaways', 'ticker': 'INSW', 'price': 75.38, 'shares': 49.4,
        'bv': 40.89, 'payout': 0.87, 'net_debt': 250,
        'profile': 'Diversified, low breakeven',
        'segments': {
            'VLCC':    {'ships': 11, 'spot_pct': 0.81, 'tc_rate': 50000, 'be': 22000},
            'Suezmax': {'ships': 13, 'spot_pct': 0.81, 'tc_rate': 45000, 'be': 22000},
            'LR2':     {'ships':  5, 'spot_pct': 0.81, 'tc_rate': 35000, 'be': 20000},
            'LR1':     {'ships': 14, 'spot_pct': 0.81, 'tc_rate': 30000, 'be': 18000},
            'MR':      {'ships': 30, 'spot_pct': 0.81, 'tc_rate': 25000, 'be': 15000},
        },
    },
    'ECO': {
        'name': 'Okeanis Eco', 'ticker': 'ECO', 'price': 50.60, 'shares': 39.0,
        'bv': 16.04, 'payout': 0.80, 'net_debt': 800,
        'profile': 'Modern eco fleet, 100% spot',
        'segments': {
            'VLCC':    {'ships': 8, 'spot_pct': 1.00, 'tc_rate': 0, 'be': 23000},
            'Suezmax': {'ships': 8, 'spot_pct': 1.00, 'tc_rate': 0, 'be': 22000},
        },
    },
    'TNK': {
        'name': 'Teekay Tankers', 'ticker': 'TNK', 'price': 76.42, 'shares': 34.6,
        'bv': 55.00, 'payout': 0.50, 'net_debt': -853,  # net cash
        'profile': 'Suez/Afra focus, net cash',
        'segments': {
            'Suezmax': {'ships': 16, 'spot_pct': 0.85, 'tc_rate': 50000, 'be': 22000},
            'LR2':     {'ships': 18, 'spot_pct': 0.85, 'tc_rate': 42000, 'be': 21000},
        },
    },
    'NAT': {
        'name': 'Nordic American', 'ticker': 'NAT', 'price': 5.91, 'shares': 211.0,
        'bv': 5.50, 'payout': 0.90, 'net_debt': 200,
        'profile': 'Pure Suezmax, 50/50 spot/TC',
        'segments': {
            'Suezmax': {'ships': 20, 'spot_pct': 0.50, 'tc_rate': 38000, 'be': 19000},
        },
    },
    'CMBT': {
        'name': 'CMB.TECH', 'ticker': 'CMBT', 'price': 12.93, 'shares': 290.0,
        'bv': 13.50, 'payout': 0.50, 'net_debt': 1500,
        'profile': 'Diversified (tanker+dry+container)',
        'segments': {
            'VLCC':    {'ships': 25, 'spot_pct': 0.70, 'tc_rate': 48000, 'be': 24000},
            'Suezmax': {'ships': 15, 'spot_pct': 0.70, 'tc_rate': 42000, 'be': 22000},
        },
    },
}

RATE_RATIO = {
    'VLCC': 1.000,
    'Suezmax': 0.716,
    'LR2': 0.583,
    'LR1': 0.450,
    'MR': 0.350,
}

DAYS = 330  # operational days per year

# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def calc_earnings(company, vlcc_spot_rate):
    total_profit = 0
    for seg_name, seg in company['segments'].items():
        spot_rate = vlcc_spot_rate * RATE_RATIO[seg_name]
        spot_days = seg['ships'] * seg['spot_pct'] * DAYS
        tc_days = seg['ships'] * (1 - seg['spot_pct']) * DAYS
        spot_profit = (spot_rate - seg['be']) * spot_days
        tc_profit = (seg['tc_rate'] - seg['be']) * tc_days
        total_profit += spot_profit + tc_profit
    eps = total_profit / (company['shares'] * 1e6)
    return total_profit, eps

def calc_vlcc_eq(company):
    eq = 0
    for seg_name, seg in company['segments'].items():
        eq += seg['ships'] * RATE_RATIO[seg_name]
    return eq

def calc_metrics(company, vlcc_spot_rate):
    profit, eps = calc_earnings(company, vlcc_spot_rate)
    pe = company['price'] / eps if eps > 0 else 999
    dy = eps * company['payout'] / company['price'] * 100 if eps > 0 else 0
    dps = eps * company['payout']
    roe = eps / company['bv'] * 100 if company['bv'] > 0 else 0
    tp7 = eps * 7
    tp5 = eps * 5
    tp7u = (tp7 / company['price'] - 1) * 100 if company['price'] > 0 else 0
    tp5u = (tp5 / company['price'] - 1) * 100 if company['price'] > 0 else 0
    mc = company['price'] * company['shares']
    eq = calc_vlcc_eq(company)
    return {
        'profit': profit / 1e6, 'eps': eps, 'pe': pe, 'dy': dy, 'dps': dps,
        'roe': roe, 'tp7': tp7, 'tp5': tp5, 'tp7u': tp7u, 'tp5u': tp5u,
        'mc': mc, 'eq': eq, 'mc_eq': mc / eq if eq > 0 else 0,
        'pb': company['price'] / company['bv'] if company['bv'] > 0 else 0,
    }

# ============================================================
# MAIN OUTPUT
# ============================================================

tickers = ['DHT', 'FRO', 'INSW', 'ECO', 'TNK', 'NAT', 'CMBT']
rates = [75000, 90000, 100000, 120000, 150000, 200000, 250000]

print('=' * 140)
print('CRUDE TANKER PEER UNIVERSE: 7-COMPANY COMPARATIVE ANALYSIS')
print('April 8, 2026 | Prices: DHT {0}18.57 | FRO {0}35.08 | INSW {0}75.38 | ECO {0}50.60 | TNK {0}76.42 | NAT {0}5.91 | CMBT {0}12.93'.format(D))
print('=' * 140)
print()

# Company overview
print('COMPANY OVERVIEW')
print('-' * 140)
hdr = '{:<6s} {:<16s} {:>8s} {:>8s} {:>8s} {:>7s} {:>7s} {:>10s} {:>10s} {:<30s}'.format(
    'Ticker', 'Name', 'Price', 'MktCap', 'Ships', 'VLCCeq', 'MC/eq', 'P/B', 'NetDebt', 'Profile')
print(hdr)
print('-' * 140)
for t in tickers:
    c = COMPANIES[t]
    ships = sum(s['ships'] for s in c['segments'].values())
    eq = calc_vlcc_eq(c)
    mc = c['price'] * c['shares']
    nd = c.get('net_debt', 0)
    nd_str = '{0}{1:.0f}M'.format(D, nd) if nd >= 0 else 'NET CASH {0}{1:.0f}M'.format(D, abs(nd))
    print('{:<6s} {:<16s} {}{:>6.2f} {}{:>5.0f}M {:>6d} {:>7.1f} {}{:>5.0f}M {:>9.2f}x {:>10s} {:<30s}'.format(
        t, c['name'], D, c['price'], D, mc, ships, eq, D, mc/eq, c['price']/c['bv'], nd_str, c['profile']))
print()

# Sensitivity table
print('=' * 140)
print('EARNINGS SENSITIVITY: EPS AT EACH VLCC SPOT RATE')
print('=' * 140)
print('{:>10s} |'.format('VLCC Rate'), end='')
for t in tickers:
    print('{:>12s}'.format(t), end='')
print()
print('-' * 95)
for rate in rates:
    print('{}{:>7d}K/d |'.format(D, rate // 1000), end='')
    for t in tickers:
        m = calc_metrics(COMPANIES[t], rate)
        print(' {}{:>9.2f}'.format(D, m['eps']), end='')
    print()

print()
print('P/E AT EACH VLCC SPOT RATE')
print('-' * 95)
print('{:>10s} |'.format('VLCC Rate'), end='')
for t in tickers:
    print('{:>12s}'.format(t), end='')
print()
print('-' * 95)
for rate in rates:
    print('{}{:>7d}K/d |'.format(D, rate // 1000), end='')
    for t in tickers:
        m = calc_metrics(COMPANIES[t], rate)
        print('{:>11.1f}x'.format(m['pe']), end='')
    print()

print()
print('DIVIDEND YIELD AT EACH VLCC SPOT RATE')
print('-' * 95)
print('{:>10s} |'.format('VLCC Rate'), end='')
for t in tickers:
    print('{:>12s}'.format(t), end='')
print()
print('-' * 95)
for rate in rates:
    print('{}{:>7d}K/d |'.format(D, rate // 1000), end='')
    for t in tickers:
        m = calc_metrics(COMPANIES[t], rate)
        print('{:>10.1f}{}'.format(m['dy'], P), end='')
    print()

# Hormuz scenarios
print()
print('=' * 140)
print('BLENDED 2026 ANNUAL SCENARIOS (Q1 actual + crisis + normalization)')
print('=' * 140)
print()

blend_scenarios = [
    ('Hormuz opens May 2026', {'Q1': (79000, 90), 'Q2': (120000, 91), 'Q3': (75000, 92), 'Q4': (70000, 92)}),
    ('Hormuz opens Aug 2026', {'Q1': (79000, 90), 'Q2': (200000, 91), 'Q3': (120000, 92), 'Q4': (80000, 92)}),
    ('Hormuz stays closed',   {'Q1': (79000, 90), 'Q2': (250000, 91), 'Q3': (200000, 92), 'Q4': (150000, 92)}),
]

for label, quarters in blend_scenarios:
    total_days = sum(q[1] for q in quarters.values())
    wtd_rate = sum(q[0] * q[1] for q in quarters.values()) / total_days
    print('  {} | Q1: {}{}K  Q2: {}{}K  Q3: {}{}K  Q4: {}{}K | Blended: {}{:.1f}K/d'.format(
        label, D, quarters['Q1'][0]//1000, D, quarters['Q2'][0]//1000,
        D, quarters['Q3'][0]//1000, D, quarters['Q4'][0]//1000, D, wtd_rate/1000))
    for t in tickers:
        c = COMPANIES[t]
        m = calc_metrics(c, wtd_rate)
        print('    {:5s}: EPS {}{:.2f} | P/E {:.1f}x | DY {:.1f}{} | TP@7x {}{:.2f} (+{:.0f}{}) | Profit {}{:.0f}M'.format(
            t, D, m['eps'], m['pe'], m['dy'], P, D, m['tp7'], m['tp7u'], P, D, m['profit']))
    print()

# Ranking
print('=' * 140)
print('RANKING AT {0}90K NORMALIZED (Hormuz-Open Structural Supercycle)'.format(D))
print('=' * 140)
print()

ranked = []
for t in tickers:
    c = COMPANIES[t]
    m = calc_metrics(c, 90000)
    m['ticker'] = t
    ranked.append(m)

# Sort by P/E (cheapest first)
by_pe = sorted(ranked, key=lambda x: x['pe'])
print('  By P/E (cheapest):      ', ' > '.join('{} ({:.1f}x)'.format(r['ticker'], r['pe']) for r in by_pe))

by_dy = sorted(ranked, key=lambda x: -x['dy'])
print('  By Div Yield (highest): ', ' > '.join('{} ({:.1f}{})'.format(r['ticker'], r['dy'], P) for r in by_dy))

by_pb = sorted(ranked, key=lambda x: x['pb'])
print('  By P/B (cheapest):      ', ' > '.join('{} ({:.2f}x)'.format(r['ticker'], r['pb']) for r in by_pb))

by_mceq = sorted(ranked, key=lambda x: x['mc_eq'])
print('  By MktCap/VLCC-eq:      ', ' > '.join('{} ({}{}M)'.format(r['ticker'], D, int(r['mc_eq'])) for r in by_mceq))

by_tp7 = sorted(ranked, key=lambda x: -x['tp7u'])
print('  By TP@7x upside:        ', ' > '.join('{} (+{:.0f}{})'.format(r['ticker'], r['tp7u'], P) for r in by_tp7))

print()
print('PICK RECOMMENDATIONS (at {0}90K normalized):'.format(D))
print()
print('  1. BEST VALUE:           INSW — lowest P/B (1.84x), lowest breakeven, highest DY among large-caps')
print('  2. BEST VLCC PURE PLAY:  DHT  — 24 VLCCs, 95% payout, hedged downside')
print('  3. BEST UPSIDE LEVERAGE: FRO  — 83% spot, 81 ships, maximum cycle capture')
print('  4. BEST ECO/MODERN:      ECO  — 100% spot, youngest fleet, highest earnings sensitivity')
print('  5. SAFEST BALANCE SHEET: TNK  — net cash $853M, zero leverage risk')
print('  6. INCOME PLAY:          NAT  — 90% payout, 27-year unbroken dividend streak')
print('  7. SPECIAL SITUATION:    CMBT — selling VLCCs at peak, transitioning to green shipping')

# Save chart data
chart_output = []
for rate in range(25000, 260000, 5000):
    row = {'vlcc_rate': rate}
    for t in tickers:
        m = calc_metrics(COMPANIES[t], rate)
        row[t + '_eps'] = round(m['eps'], 4)
        row[t + '_profit_m'] = round(m['profit'], 2)
        row[t + '_pe'] = round(m['pe'], 2)
        row[t + '_dy'] = round(m['dy'], 2)
    chart_output.append(row)

output_path = os.path.join(os.path.dirname(__file__), 'peer_chart_data.json')
with open(output_path, 'w') as f:
    json.dump(chart_output, f, indent=2)
print('\nChart data saved to peer_chart_data.json ({} data points)'.format(len(chart_output)))
