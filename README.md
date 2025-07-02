# Black-Scholes Options Pricing & PnL Visualizer

This repository provides an interactive Black-Scholes Pricing Model that calculates and visualizes European call and put option prices. Built using Streamlit, this tool helps users explore how option prices and profit/loss change based on volatility, spot price, and time to maturity.

## Features

1. Options Pricing Visualization

   * Calculates theoretical prices for Call and Put options using the Black-Scholes model
   * Visualizes prices and profit/loss using heatmaps
   * Dual-tab interface: one for theoretical value, one for user-based P\&L

2. Interactive Dashboard

   * Real-time updates as parameters are changed
   * Accepts custom inputs for Spot Price, Volatility, Strike Price, Time to Maturity, Risk-Free Rate
   * Allows users to enter their own call and put purchase prices to view net gains/losses

3. Customizable Parameters

   * Set min/max ranges for spot price and volatility to customize heatmap axes
   * Toggle between theoretical pricing view and P\&L view

## Dependencies

* Python 3.10+
* Streamlit
* NumPy, SciPy
* Matplotlib, Seaborn

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run streamlit_app.py
```

## License

MIT License — feel free to use, modify, or share this project.
