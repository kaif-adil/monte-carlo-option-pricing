import pandas as pd
import matplotlib.pyplot as plt
from black_scholes import bs_price
from monte_carlo import mc_price

# Base case: the "default" knob positions
BASE = dict(S0=100, K=100, T=1.0, r=0.05, sigma=0.2)


def sweep(param, values, option="call", n_sims=200_000):
    """Change ONE input across `values`, keep the rest at BASE.
    Price with both methods and return a DataFrame."""
    rows = []
    for v in values:
        inputs = {**BASE, param: v}           # copy BASE, override one knob
        bs = bs_price(inputs["S0"], inputs["K"], inputs["T"],
                      inputs["r"], inputs["sigma"], option)
        mc, se = mc_price(inputs["S0"], inputs["K"], inputs["T"],
                          inputs["r"], inputs["sigma"], option,
                          n_sims=n_sims, seed=42)
        rows.append({"param": param, "value": v, "option": option,
                     "bs_price": bs, "mc_price": mc, "mc_ci95": 1.96 * se})
    return pd.DataFrame(rows)


experiments = {
    "sigma": [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50],
    "K":     [80, 90, 100, 110, 120],
    "T":     [0.25, 0.5, 1.0, 1.5, 2.0],
}
labels = {"sigma": "Volatility (sigma)", "K": "Strike price (K)",
          "T": "Time to expiry (years)"}

# Run everything for calls and puts into one big table
results = pd.concat(
    [sweep(p, vals, opt) for p, vals in experiments.items()
     for opt in ["call", "put"]],
    ignore_index=True,
)
results.to_csv("sensitivity_results.csv", index=False)
print(results.round(3).to_string())

# Plot: top row = calls, bottom row = puts, one column per knob
fig, axes = plt.subplots(2, 3, figsize=(13, 7))
for row, opt in enumerate(["call", "put"]):
    for col, p in enumerate(experiments):
        d = results[(results.param == p) & (results.option == opt)]
        ax = axes[row, col]
        ax.plot(d.value, d.bs_price, "-", label="Black-Scholes")
        ax.errorbar(d.value, d.mc_price, yerr=d.mc_ci95, fmt="o",
                    capsize=3, label="Monte Carlo (95% CI)")
        ax.set_xlabel(labels[p])
        ax.set_ylabel(f"{opt.capitalize()} price")
        ax.grid(alpha=0.3)
        if row == 0 and col == 0:
            ax.legend()
fig.suptitle("Option price sensitivity: Monte Carlo vs Black-Scholes")
plt.tight_layout()
plt.savefig("sensitivity.png", dpi=150)
plt.show()