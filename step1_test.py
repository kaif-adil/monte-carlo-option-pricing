import numpy as np
from gbm import simulate_terminal_price
from payoffs import call_payoff, put_payoff

S0, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

ST = simulate_terminal_price(S0, r, sigma, T, n_sims=100_000, seed=42)

print("First 5 simulated prices:", np.round(ST[:5], 2))
print("Average simulated price :", round(ST.mean(), 2))
print("Expected (S0*e^(rT))    :", round(S0 * np.exp(r * T), 2))
print("Avg call payoff         :", round(call_payoff(ST, K).mean(), 2))
print("Avg put payoff          :", round(put_payoff(ST, K).mean(), 2))