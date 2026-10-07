import numpy as np
import matplotlib.pyplot as plt
from gbm import simulate_terminal_price
from strategies import STRATEGIES, strategy_profit, S0, T, r, sigma

# 1) Profit diagrams: profit vs final stock price
grid = np.linspace(50, 160, 400)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
for ax, (name, legs) in zip(axes, STRATEGIES.items()):
    profit, cost = strategy_profit(legs, grid)
    ax.plot(grid, profit, color="black")
    ax.axhline(0, color="gray", lw=1)
    ax.fill_between(grid, profit, 0, where=profit >= 0, color="green", alpha=0.25)
    ax.fill_between(grid, profit, 0, where=profit < 0, color="red", alpha=0.25)
    ax.set_title(name, fontsize=10)
    ax.set_xlabel("Stock price at expiry")
    ax.grid(alpha=0.3)
axes[0].set_ylabel("Profit / loss")
plt.tight_layout()
plt.savefig("strategies.png", dpi=150)

# 2) Monte Carlo analysis: simulate 200,000 futures, test each strategy
ST = simulate_terminal_price(S0, r, sigma, T, n_sims=200_000, seed=42)

print(f"{'Strategy':45} {'Cost':>7} {'Avg P/L':>8} {'P(profit)':>10} {'Worst':>8} {'Best':>8}")
for name, legs in STRATEGIES.items():
    profit, cost = strategy_profit(legs, ST)
    print(f"{name:45} {cost:7.2f} {profit.mean():8.2f} "
          f"{(profit > 0).mean():10.1%} {profit.min():8.2f} {profit.max():8.2f}")

plt.show()