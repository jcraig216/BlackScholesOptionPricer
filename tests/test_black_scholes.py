#tests/test_black_scholes.py
import math
from black_scholes import BlackScholes

def price_call_put(S, K, r, sigma, T):
    bs = BlackScholes(
        time_to_maturity=T,
        strike=K,
        current_price=S,
        volatility=sigma,
        interest_rate=r,
        call_purchase_price=0.0,
        put_purchase_price=0.0,
    )
    call_price, put_price, _, _ = bs.calculate_prices()
    return call_price, put_price

def test_put_call_parity():
    S, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    c, p = price_call_put(S, K, r, sigma, T)
    lhs = c - p
    rhs = S - K * math.exp(-r * T)
    assert abs(lhs - rhs) < 1e-8

def test_known_value_call_zero_rate():
    # Common sanity config: r=0, sigma=0.2, T=1, S=K=100 → call ≈ 7.9656
    S, K, r, sigma, T = 100, 100, 0.0, 0.20, 1.0
    c, _ = price_call_put(S, K, r, sigma, T)
    assert 7.9 < c < 8.1
