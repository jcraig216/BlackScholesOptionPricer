# Black-Scholes Options Pricing & P&L Visualizer

Interactive **Streamlit** app for exploring European call/put prices and strategy **P&L** under the Black–Scholes model. Adjust spot, volatility, time to expiry, strike, and risk-free rate to see how inputs move option value and profit/loss.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blackscholesoptionpricer-jackcraig.streamlit.app)

**Live demo:** https://blackscholesoptionpricer-jackcraig.streamlit.app  
**Tech:** Python · Streamlit · NumPy · pandas · Plotly

---

## Features
- **Pricing:** Computes theoretical prices for European calls/puts (Black–Scholes).
- **Visualization:** Heatmaps for **Option Value** and **P&L** across spot and volatility.
- **Two tabs:**  
  1) **Fair Value** — price surfaces.  
  2) **Profit & Loss** — enter your trade prices to see net P&L.
- **Greeks toggle:** Show Δ, Γ, Θ, Vega, Rho on the main metric cards.
- **Interactive controls:** Sliders/inputs for S, σ, T, K, r; adjustable grid resolution.
- **Download CSV:** Export the current heatmap data for calls/puts.

---

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
