import numpy as np


def simulate_terminal_price(S0, r, sigma, T, n_sims, seed=None):
    """
    Simulate n_sims possible stock prices at time T using
    Geometric Brownian Motion.

    S0    : price today
    r     : risk-free interest rate (0.05 = 5%)
    sigma : volatility (0.2 = 20% per year)
    T     : years until expiry
    """
    rng = np.random.default_rng(seed)       # random number generator
    Z = rng.standard_normal(n_sims)         # random "luck" for each future
    drift = (r - 0.5 * sigma**2) * T        # steady growth part
    shock = sigma * np.sqrt(T) * Z          # random jump part
    return S0 * np.exp(drift + shock)