import numpy as np
import matplotlib.pyplot as plt
from black_scholes import bs_price
from monte_carlo import mc_price

S0, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
exact = bs_price(S0, K, T, r, sigma, "call")

sim_counts = [1_000, 3_000, 10_000, 30_000, 100_000, 300_000, 1_000_000]
repeats = 20  # repeat each size 20 times and average, so the curve is smooth

avg_errors = []
for n in sim_counts:
    errors = []
    for i in range(repeats):
        price, _ = mc_price(S0, K, T, r, sigma, "call", n_sims=n, seed=i)
        errors.append(abs(price - exact))
    avg_errors.append(np.mean(errors))
    print(f"n = {n:>9,} | avg error = {avg_errors[-1]:.4f}")

# Reference line: error should shrink like 1/sqrt(n)
ref = avg_errors[0] * np.sqrt(sim_counts[0] / np.array(sim_counts))

plt.figure(figsize=(7, 4.5))
plt.loglog(sim_counts, avg_errors, "o-", label="Monte Carlo error")
plt.loglog(sim_counts, ref, "--", label="1/sqrt(n) reference")
plt.xlabel("Number of simulations")
plt.ylabel("Average |MC price - Black-Scholes price|")
plt.title("Monte Carlo convergence (European call)")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("convergence.png", dpi=150)
plt.show()