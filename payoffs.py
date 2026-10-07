import numpy as np


def call_payoff(S, K):
    """Profit at expiry from the right to BUY at K. Never negative."""
    return np.maximum(S - K, 0)


def put_payoff(S, K):
    """Profit at expiry from the right to SELL at K. Never negative."""
    return np.maximum(K - S, 0)