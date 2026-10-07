from monte_carlo import mc_price

S0, K, T, r = 100, 100, 1, 0.05

for sigma in [0.1, 0.2, 0.4]:
    c, c_se = mc_price(S0, K, T, r, sigma, "call", seed=42)
    p, p_se = mc_price(S0, K, T, r, sigma, "put", seed=42)
    print(f"sigma={sigma:.1f} | call = {c:6.3f} (+/- {1.96*c_se:.3f}) | put = {p:6.3f} (+/- {1.96*p_se:.3f})")