# Black-Scholes Options Pricing & P&L Visualizer

Interactive **Streamlit** app for exploring European call/put prices and strategy **P&L** under the Black–Scholes model. Adjust spot, volatility, time to expiry, strike, and risk-free rate to see how inputs move option value and profit/loss.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blackscholesoptionpricer-jackcraig.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Live demo:** https://blackscholesoptionpricer-jackcraig.streamlit.app  
**Tech:** Python · Streamlit · NumPy · pandas · Plotly

---

## Features
- **Pricing (Black–Scholes):** Computes theoretical prices for European calls/puts.
- **Visualization:** Plotly heatmaps for **Option Value** and **P&L** across spot (S) and volatility (σ).
- **Two tabs:**  
  1) **Fair Value** — price surfaces.  
  2) **Profit & Loss** — enter your trade prices to see net P&L.
- **Greeks toggle:** Show Δ (Delta), Γ (Gamma), Θ (Theta), Vega, Rho on the main metric cards.
- **Controls:** Sidebar inputs for \(S\), \(σ\), \(T\), \(K\), \(r\); adjustable grid resolution; min/max ranges for spot & vol.
- **Download CSV:** Export the current heatmap data (call/put) for both tabs.
- **Chart help:** “How to read this chart” expander + optional cell value labels.
- **Performance:** Caches heatmap computations for snappier updates.

---

## Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

---

## Requirements
```text
streamlit
numpy
pandas
plotly
```

---

## How it works

This app implements the **Black–Scholes** model for *European* options.

**Pricing formulas**

C = S·N(d₁) − K·e^(−rT)·N(d₂)  

P = K·e^(−rT)·N(−d₂) − S·N(−d₁)

with

d₁ = [ln(S/K) + (r + 0.5·σ²)·T] / [σ·√T]  

d₂ = d₁ − σ·√T

- \( S \) — spot price  
- \( K \) — strike price  
- \( r \) — risk-free interest rate  
- \( T \) — time to expiry (in years)  
- \( σ \) — annualized volatility  
- \( N(x) \) — standard normal cumulative distribution function (CDF), computed via `math.erf`

**P&L**
- Reported P&L is the **model price minus your purchase price** (per contract), shown for calls and puts.

**Greeks (displayed on the main cards)**
- **Delta (Δ):** sensitivity to \(S\)  
- **Gamma (Γ):** sensitivity of Delta to \(S\)  
- **Theta (Θ):** **annualized** time decay (per year)  
- **Vega:** sensitivity to \( σ \) (**per vol unit**; for per-1% vol, divide by 100)  
- **Rho:** sensitivity to \(r\), reported **per 1% change in \(r\)**

**Edge cases**
- For very small \(T\) or \( σ \), prices safely fall back to **intrinsic value**; Greeks use simple, well-behaved defaults.

**Assumptions**
- European exercise, frictionless markets, constant \(r\) and \( σ \); dividends not modeled.

---

## Project Structure
```text
.
├─ streamlit_app.py        # UI: controls, tabs, charts, downloads
├─ black_scholes.py        # pricing + Greeks (pure Python)
├─ tests/
│  └─ test_black_scholes.py
├─ requirements.txt
├─ .gitignore
└─ README.md
```

---

## Tests

```bash
pip install pytest
pytest -q
```

Includes:
- Put-call parity sanity check
- Known-value call price check (e.g. r=0, σ=0.2, T=1, S=K=100 ≈ 8.0)

---

## Acknowledgments
This app was inspired by other public Black–Scholes calculators, including  
[Prudhvi Reddy’s Streamlit demo](https://blackschole.streamlit.app).  
All code and design decisions in this repository are my own implementation.

---

## License

MIT - see LICENSE for details
