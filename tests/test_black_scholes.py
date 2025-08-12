import math
import importlib

# Import the renamed module
bs = importlib.import_module("black_scholes")

# Helper: try to resolve call/put functions under common names
def _resolve(name_candidates):
    for n in name_candidates:
        fn = getattr(bs, n, None)
        if callable(fn):
            return fn
    raise AttributeError(f"Could not find any of: {name_candidates}")

bs_call = _resolve(["bs_call", "call_price", "BS_CALL", "call"])
bs_put  = _resolve(["bs_put",  "put_price",  "BS_PUT",  "put"])

def test_put_call_parity():
    S, K, r, sigma, T = 100, 100, 0.05, 0.2, 1.0
    c = bs_call(S, K, r, sigma, T)
    p = bs_put(S, K, r, sigma, T)
    lhs = c - p
    rhs = S - K * math.exp(-r * T)
    assert abs(lhs - rhs) < 1e-8

def test_known_value_call_loose_band():
    # Zero-rate sanity: known configuration should be ~8.0
    S, K, r, sigma, T = 100, 100, 0.0, 0.2, 1.0
    c = bs_call(S, K, r, sigma, T)
    assert 7.9 < c < 8.1
