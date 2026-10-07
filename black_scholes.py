import numpy as np
from scipy.stats import norm


def bs_price(S0, K, T, r, sigma, option="call"):
    """
    Exact Black-Scholes price of a European option.

    d1, d2 are intermediate numbers; norm.cdf(x) gives the
    probability that a standard random variable is below x.
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option == "call":
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    else:
        raise ValueError("option must be 'call' or 'put'")