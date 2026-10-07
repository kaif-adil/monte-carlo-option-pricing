import numpy as np
from gbm import simulate_terminal_price
from payoffs import call_payoff, put_payoff


def mc_price(S0, K, T, r, sigma, option="call", n_sims=100_000, seed=None):
    """
    Price a European option with Monte Carlo.
    Returns (price, standard_error).
    """
    ST = simulate_terminal_price(S0, r, sigma, T, n_sims, seed)

    if option == "call":
        payoffs = call_payoff(ST, K)
    elif option == "put":
        payoffs = put_payoff(ST, K)
    else:
        raise ValueError("option must be 'call' or 'put'")

    discount = np.exp(-r * T)                    # money later is worth less today
    price = discount * payoffs.mean()            # average payoff, discounted
    std_error = discount * payoffs.std(ddof=1) / np.sqrt(n_sims)
    return price, std_error