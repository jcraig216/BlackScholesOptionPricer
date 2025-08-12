import numpy as np
from scipy.stats import norm
from numpy import log, sqrt, exp

class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
        call_purchase_price: float = 0.0,
        put_purchase_price: float = 0.0,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.call_purchase_price = call_purchase_price
        self.put_purchase_price = put_purchase_price

    def calculate_prices(self):
        T = self.time_to_maturity
        K = self.strike
        S = self.current_price
        σ = self.volatility
        r = self.interest_rate
        call_cost = self.call_purchase_price
        put_cost = self.put_purchase_price

        rt_T = sqrt(T)
        d1 = (log(S / K) + (r + 0.5 * σ**2) * T) / (σ * rt_T)
        d2 = d1 - σ * rt_T
        discount = exp(-r * T)

        # Prices
        self.call_price = S * norm.cdf(d1) - K * discount * norm.cdf(d2)
        self.put_price = K * discount * norm.cdf(-d2) - S * norm.cdf(-d1)

        # Net P&L
        self.call_pnl = self.call_price - call_cost
        self.put_pnl = self.put_price - put_cost

        # Greeks
        nd1 = norm.pdf(d1)
        self.call_delta = norm.cdf(d1)
        self.put_delta = self.call_delta - 1

        self.call_gamma = self.put_gamma = nd1 / (S * σ * rt_T)

        self.call_vega = self.put_vega = S * nd1 * rt_T / 100  # per 1% vol
        self.call_theta = (-S * nd1 * σ / (2 * rt_T) - r * K * discount * norm.cdf(d2)) / 365
        self.put_theta = (-S * nd1 * σ / (2 * rt_T) + r * K * discount * norm.cdf(-d2)) / 365

        self.call_rho = K * T * discount * norm.cdf(d2) / 100
        self.put_rho = -K * T * discount * norm.cdf(-d2) / 100

        return self.call_price, self.put_price, self.call_pnl, self.put_pnl

    def get_call_pnl(self):
        return self.call_pnl

    def get_put_pnl(self):
        return self.put_pnl

    def get_call_price(self):
        return self.call_price

    def get_put_price(self):
        return self.put_price
