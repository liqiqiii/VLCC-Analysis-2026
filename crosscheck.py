#!/usr/bin/env python3
"""Cross-check: Booking Rate vs Charter Type Split"""

D = '$'

print('='*80)
print('CROSS-CHECK: Booking Rate vs Charter Type Split')
print('='*80)
print()

# === DHT ===
print('--- DHT Holdings ---')
print()
total_days_dht = 24 * 90  # ~2,160
tc_days = 797
total_booked_66pct = int(total_days_dht * 0.66)
spot_booked = total_booked_66pct - tc_days
spot_total = total_days_dht - tc_days
spot_booked_pct = spot_booked / spot_total * 100

print(f'Total available days (24 x 90): {total_days_dht}')
print(f'TC days (100% locked): {tc_days} at {D}43,300/day')
print(f'TC share of total: {tc_days/total_days_dht*100:.1f}%')
print(f'Total booked at 66%: {total_booked_66pct} days')
print(f'Spot days booked (derived): {spot_booked}')
print(f'Total spot days: {spot_total}')
print(f'Spot booking rate: {spot_booked_pct:.0f}% (reported: 45%)')
print(f'Open/unfixed: {total_days_dht - total_booked_66pct} days = 34%')
print()

# Later update
later_spot_booked = int(spot_total * 0.76)
later_total_booked = tc_days + later_spot_booked
later_pct = later_total_booked / total_days_dht * 100
print(f'LATER UPDATE: 76% of spot booked at {D}78,900/day')
print(f'Spot booked: {later_spot_booked}')
print(f'Total booked: {later_total_booked}/{total_days_dht} = {later_pct:.0f}%')
print(f'Open/unfixed: {total_days_dht - later_total_booked} days = {100-later_pct:.0f}%')
print()

print('STRATEGY SHIFT: DHT targeting ~75% spot by Q2 2026')
print(f'Q4 2025 charter type: 54% spot / 46% TC')
print(f'Q2 2026 target:       75% spot / 25% TC')
print()

# === FRO ===
print('--- Frontline (FRO) ---')
print()
segments = [
    ('VLCC', 42, 0.92, 107100),
    ('Suezmax', 21, 0.83, 76700),
    ('LR2', 18, 0.67, 62400),
]
total_fleet_days = 0
total_booked_days = 0
for name, ships, pct, rate in segments:
    days = ships * 90
    booked = int(days * pct)
    total_fleet_days += days
    total_booked_days += booked
    print(f'{name:10s}: {ships} ships x 90d = {days:5d} days, '
          f'{pct*100:.0f}% booked ({booked}) at {D}{rate:,}/day')

fleet_pct = total_booked_days / total_fleet_days * 100
print(f'Fleet total: {total_fleet_days} days, {total_booked_days} booked = {fleet_pct:.1f}%')
print(f'Open/unfixed: {total_fleet_days - total_booked_days} days = {100-fleet_pct:.1f}%')
print()

print('FRO VLCC TC coverage by quarter (structural):')
print('  Q1 2026:  8% TC / 92% spot market')
print('  Q2 2026: 24% TC / 76% spot market')
print('  Q3 2026: 24% TC / 76% spot market')
print('  Q4 2026: 23% TC / 77% spot market')
print()

# === RECONCILIATION ===
print('='*80)
print('RECONCILIATION')
print('='*80)
print()
print('User source:     DHT 66% locked / 34% open')
print('                 FRO 92% locked / 8% open (VLCC only)')
print()
print('My report used:  DHT 54% spot / 46% TC   (charter TYPE)')
print('                 FRO 83% spot / 17% TC   (charter TYPE)')
print()
print('THESE MEASURE DIFFERENT THINGS:')
print()
print('Metric 1: BOOKING RATE = % of Q1 days already contracted')
print('  Includes TC days + already-fixed spot + FFA')
print('  = near-term visibility (this quarter)')
print(f'  DHT: 66% (Jan 14) -> ~{later_pct:.0f}% (later update)')
print(f'  FRO: VLCC 92% | Fleet-wide {fleet_pct:.0f}%')
print()
print('Metric 2: CHARTER TYPE = % of fleet on spot vs TC market')
print('  = structural multi-year rate sensitivity')
print('  DHT: 54% spot / 46% TC (Q4 2025) -> 75/25 (Q2 2026)')
print('  FRO: 83% spot / 17% TC (fleet-wide)')
print()
print('BOTH are correct. User numbers = Q1 2026 booking snapshot.')
print('My model = structural charter type mix for cycle sensitivity.')
print()

print('='*80)
print('CRITICAL MISSING FACTOR: DHT STRATEGY SHIFT!')
print('='*80)
print()
print('DHT is moving FROM 54% spot TO 75% spot by Q2 2026.')
print('This means:')
print('  - My model used STALE charter mix (Q4 2025)')
print('  - Forward-looking, DHT is becoming MORE like FRO')
print('  - By Q2, DHT will be 75% spot / 25% TC')
print('  - This INCREASES DHTs rate sensitivity significantly')
print()

# Recalculate with Q2 2026 target
print('CORRECTED MODEL: DHT at 75% spot / 25% TC (Q2 2026 target)')
print('-'*60)
for rate in [50000, 75000, 107000, 120000, 150000, 200000]:
    old_profit = (rate - 25000) * 24 * 0.54 * 365 + (49400 - 25000) * 24 * 0.46 * 365
    new_profit = (rate - 25000) * 24 * 0.75 * 365 + (49400 - 25000) * 24 * 0.25 * 365
    old_eps = old_profit / 161e6
    new_eps = new_profit / 161e6
    delta = (new_eps - old_eps) / old_eps * 100
    print(f'VLCC {D}{rate//1000}K: Old EPS {D}{old_eps:.2f} -> New EPS {D}{new_eps:.2f} ({delta:+.1f}%)')

print()
print('Per {0}1K rate increase:'.format(D))
old_per_1k = (24 * 0.54 * 365) / 1e6
new_per_1k = (24 * 0.75 * 365) / 1e6
print(f'  Old (54% spot): {D}{old_per_1k:.1f}M/1K -> {D}{old_per_1k*1000/161:.3f}/sh')
print(f'  New (75% spot): {D}{new_per_1k:.1f}M/1K -> {D}{new_per_1k*1000/161:.3f}/sh')
print(f'  Increase: +{(new_per_1k/old_per_1k-1)*100:.0f}%')
