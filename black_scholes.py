# black_scholes.py
# Simple Black–Scholes pricer for European options (calls & puts) with basic Greeks.
# Designed to be easy to read and plug into your Streamlit app.

from dataclasses import dataclass, field
from math import erf, exp, log, pi, sqrt
from typing import Tuple

_EPS = 1e-12  # small number to avoid divide-by-zero


def _norm_pdf(x: float) -> float:
    return (1.0 / sqrt(2.0 * pi)) * exp(-0.5 * x * x)


def _norm_cdf(x: float) -> float:
    # Standard normal CDF using error function (keeps us SciPy-free)
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


@dataclass
class BlackScholes:
    # Inputs (annualized rates/vol)
    time_to_maturity: float   # T (years)
    strike: float             # K
    current_price: float      # S
    volatility: float         # sigma (e.g., 0.20 = 20%)
    interest_rate: float      # r (continuous)
    call_purchase_price: float = 0.0
    put_purchase_price: float = 0.0

    # Outputs (filled by calculate_prices)
    call_price: float = field(default=0.0, init=False)
    put_price: float = field(default=0.0, init=False)
    call_pnl: float = field(default=0.0, init=False)
    put_pnl: float = field(default=0.0, init=False)

    # Basic Greeks (filled by calculate_prices)
    call_delta: float = field(default=0.0, init=False)
    put_delta: float = field(default=0.0, init=False)
    call_gamma: float = field(default=0.0, init=False)
    put_gamma: float = field(default=0.0, init=False)
    call_theta: float = field(default=0.0, init=False)  # annualized
    put_theta: float = field(default=0.0, init=False)   # annualized
    call_vega: float = field(default=0.0, init=False)   # per vol unit
    put_vega: float = field(default=0.0, init=False)    # per vol unit
    call_rho: float = field(default=0.0, init=False)    # per 1% change in r
    put_rho: float = field(default=0.0, init=False)     # per 1% change in r

    def calculate_prices(self) -> Tuple[float, float, float, float]:
        """
        Returns (call_price, put_price, call_pnl, put_pnl).
        Also fills in the Greek attributes above.
        """
        S = max(self.current_price, _EPS)
        K = max(self.strike, _EPS)
        r = float(self.interest_rate)
        sigma = max(self.volatility, 0.0)
        T = max(self.time_to_maturity, 0.0)

        # Easy branch: at expiry or ~zero vol -> intrinsic values; Greeks are simple/default.
        if T < _EPS or sigma < _EPS:
            call = max(S - K, 0.0)
            put = max(K - S, 0.0)

            self.call_price, self.put_price = call, put
            self.call_pnl = call - self.call_purchase_price
            self.put_pnl = put - self.put_purchase_price

            # Simple deltas; use 0.5/-0.5 at-the-money
            if S > K:
                self.call_delta, self.put_delta = 1.0, -1.0
            elif S < K:
                self.call_delta, self.put_delta = 0.0, 0.0
            else:
                self.call_delta, self.put_delta = 0.5, -0.5

            self.call_gamma = self.put_gamma = 0.0
            self.call_theta = self.put_theta = 0.0
            self.call_vega = self.put_vega = 0.0
            self.call_rho = self.put_rho = 0.0

            return self.call_price, self.put_price, self.call_pnl, self.put_pnl

        # Regular Black–Scholes
        den = max(sigma, _EPS) * sqrt(T)
        d1 = (log(S / K) + (r + 0.5 * sigma * sigma) * T) / den
        d2 = d1 - den

        Nd1 = _norm_cdf(d1)
        Nd2 = _norm_cdf(d2)
        Nmd1 = _norm_cdf(-d1)
        Nmd2 = _norm_cdf(-d2)
        nd1 = _norm_pdf(d1)
        disc = exp(-r * T)

        # Prices
        call = S * Nd1 - K * disc * Nd2
        put = K * disc * Nmd2 - S * Nmd1
        self.call_price, self.put_price = call, put

        # P&L vs what you paid
        self.call_pnl = call - self.call_purchase_price
        self.put_pnl = put - self.put_purchase_price

        # Greeks (basic forms)
        self.call_delta = Nd1
        self.put_delta = Nd1 - 1.0

        gamma = nd1 / (S * den)
        self.call_gamma = gamma
        self.put_gamma = gamma

        vega = S * nd1 * sqrt(T)        # per vol unit (e.g., per 0.01 vol -> vega/100)
        self.call_vega = vega
        self.put_vega = vega

        theta_common = -(S * nd1 * sigma) / (2.0 * sqrt(T))  # annualized
        self.call_theta = theta_common - r * K * disc * Nd2
        self.put_theta = theta_common + r * K * disc * Nmd2

        # Rho scaled to "per 1% change in r"
        self.call_rho = 0.01 * (K * T * disc * Nd2)
        self.put_rho  = 0.01 * (-K * T * disc * Nmd2)

        return self.call_price, self.put_price, self.call_pnl, self.put_pnl


# Simple helpers if you want function-style access
def bs_call(S: float, K: float, r: float, sigma: float, T: float) -> float:
    return BlackScholes(T, K, S, sigma, r).calculate_prices()[0]


def bs_put(S: float, K: float, r: float, sigma: float, T: float) -> float:
    return BlackScholes(T, K, S, sigma, r).calculate_prices()[1]
