from black_scholes import bs_price
from monte_carlo import mc_price

S0, K, T, r = 100, 100, 1, 0.05

print(f"{'sigma':>5} {'type':>5} {'BS (exact)':>11} {'MC':>8} {'MC +/-':>8} {'diff':>8}")
for sigma in [0.1, 0.2, 0.4]:
    for opt in ["call", "put"]:
        bs = bs_price(S0, K, T, r, sigma, opt)
        mc, se = mc_price(S0, K, T, r, sigma, opt, seed=42)
        print(f"{sigma:>5.1f} {opt:>5} {bs:>11.3f} {mc:>8.3f} {1.96*se:>8.3f} {mc-bs:>8.3f}")