import numpy as np
from payoffs import call_payoff, put_payoff
from black_scholes import bs_price

S0, T, r, sigma = 100, 1.0, 0.05, 0.2

# A strategy = list of legs: (kind, strike, quantity)
# quantity +1 = buy, -1 = sell (short)
STRATEGIES = {
    "Straddle (buy call + put, K=100)": [
        ("call", 100, +1), ("put", 100, +1)],
    "Bull call spread (buy K=100, sell K=120)": [
        ("call", 100, +1), ("call", 120, -1)],
    "Covered call (own stock, sell K=110)": [
        ("stock", None, +1), ("call", 110, -1)],
}


def leg_payoff(kind, K, ST):
    if kind == "call":
        return call_payoff(ST, K)
    if kind == "put":
        return put_payoff(ST, K)
    return ST                                   # owning the stock itself


def leg_price(kind, K):
    if kind == "stock":
        return S0
    return bs_price(S0, K, T, r, sigma, kind)


def strategy_profit(legs, ST):
    """Total payoff at expiry minus what you paid upfront (net cost)."""
    payoff = sum(q * leg_payoff(k, K, ST) for k, K, q in legs)
    cost = sum(q * leg_price(k, K) for k, K, q in legs)
    return payoff - cost, cost