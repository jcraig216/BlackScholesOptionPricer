# Black-Scholes Options Pricing & P&L Visualizer

Interactive **Streamlit** app for exploring European call/put prices and strategy **P&L** under the Black–Scholes model. Adjust spot, volatility, time to expiry, strike, and risk-free rate to build intuition for how inputs move option value and profit/loss.

**Live demo:** https://blackscholesoptionpricer-jackcraig.streamlit.app  
**Tech:** Python · Streamlit · NumPy · pandas · SciPy · Plotly

---

## Features

- **Pricing:** Computes theoretical prices for European calls/puts via Black–Scholes.
- **Visualization:** Heatmaps/plots for option value and **P&L** across spot, vol, and time.
- **Two tabs:**
  1) **Theoretical Value** — price surfaces & sensitivities visualization.  
  2) **User P&L** — input your paid prices to see net gains/losses.
- **Interactive controls:** Sliders/inputs for spot, volatility, strike, time to maturity, risk-free rate.
- **Custom ranges:** Set min/max for axes to focus on regions of interest.

---

## Quickstart

```bash
# 1) Install dependencies
pip install -r requirements.txt

# 2) Run the app
streamlit run streamlit_app.py
