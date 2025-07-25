

from ga_core import run_ga
from fitness_function import data, apply_indicators, backtest_and_metrics
from ga_config import PARAM_RANGES
from pprint import pprint


print("GA Parameter Ranges:")
pprint(PARAM_RANGES)

print("Running Genetic Algorithm... (This may take time)")
best_chromosome, best_fitness = run_ga()

print("\n Best Chromosome:")
for key, val in zip(PARAM_RANGES.keys(), best_chromosome):
    print(f"{key}: {val}")

print(f"\n Fitness Score: {round(best_fitness, 2)}")

df = data.copy()
df = apply_indicators(df.copy(), best_chromosome)
stats = backtest_and_metrics(df, best_chromosome)

print("\n Final In-Sample Backtest Stats:")
for k in ['cagr', 'sharpe', 'max_drawdown', 'num_trades', 'win_rate', 'net_profit']:
    val = stats[k]
    if isinstance(val, float):
        print(f"{k.title()}: {round(val, 2)}")
    else:
        print(f"{k.title()}: {val}")

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))
plt.plot(stats['equity_curve'], label="Equity Curve", color='darkblue')
plt.title(" Equity Curve of Best Strategy")
plt.xlabel("Trades")
plt.ylabel("Equity (₹)")
plt.legend()
plt.grid(True)
plt.show()
