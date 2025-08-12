import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from black_scholes import BlackScholes



# Page configuration & styles
# -----------------------------
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for metric cards
st.markdown(
    """
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    width: auto;
    margin: 0 auto;
}
.metric-call {
    background-color: #90ee90; /* light green */
    color: black;
    margin-right: 10px;
    border-radius: 10px;
}
.metric-put {
    background-color: #ffcccb; /* light red */
    color: black;
    border-radius: 10px;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}
.metric-label {
    font-size: 1rem;
    margin-bottom: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)



# Sidebar — user inputs
# -----------------------------
with st.sidebar:
    st.title("Black-Scholes Options Model")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/jack-craig-65a2082a9/"
    st.markdown(
        f'<a href="{linkedin_url}" target="_blank" style="text-decoration:none;color:inherit;">'
        f'<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" '
        f'style="vertical-align:middle;margin-right:10px;">`Jack Craig`</a>',
        unsafe_allow_html=True,
    )

    show_greeks = st.checkbox("Show Greeks (Δ, Γ, Θ, Vega, Rho)", value=False)

    # Market parameters
    with st.expander("Market Parameters", expanded=False):
        current_price = st.number_input("Current Asset Price", value=100.0, min_value=0.01)
        strike = st.number_input("Strike Price (K)", value=100.0, min_value=0.01)
        time_to_maturity = st.number_input("Time to Maturity (Years, T)", value=1.0, min_value=0.01)
        volatility = st.number_input("Volatility (σ)", value=0.20, min_value=0.01, max_value=5.0)
        interest_rate = st.number_input("Risk-Free Interest Rate (r)", value=0.05, step=0.005, format="%.3f")

    # Purchase prices
    with st.expander("Your Option Purchase Prices", expanded=False):
        call_purchase_price = st.number_input(
            "Call Option Purchase Price", value=0.0, min_value=0.0, step=0.01
        )
        put_purchase_price = st.number_input(
            "Put Option Purchase Price", value=0.0, min_value=0.0, step=0.01
        )

    # Heatmap settings
    with st.expander("Heatmap Parameters", expanded=False):
        spot_min = st.number_input("Min Spot Price", min_value=0.01, value=current_price * 0.80, step=0.01)
        spot_max = st.number_input("Max Spot Price", min_value=0.01, value=current_price * 1.20, step=0.01)
        vol_min = st.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.00, value=max(0.01, volatility * 0.50), step=0.01)
        vol_max = st.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.00, value=min(1.00, volatility * 1.50), step=0.01)
        grid_points = st.slider("Grid resolution (per axis)", min_value=10, max_value=60, value=25, step=1)



# Input guards & ranges
# -----------------------------
if spot_min >= spot_max:
    st.warning("Max Spot must be greater than Min Spot. Adjusting automatically.")
    spot_max = spot_min * 1.01

if vol_min >= vol_max:
    st.warning("Max Volatility must be greater than Min Volatility. Adjusting automatically.")
    vol_max = min(vol_min + 0.01, 1.00)

spot_range = np.linspace(spot_min, spot_max, grid_points)
vol_range = np.linspace(vol_min, vol_max, grid_points)



# Helpers
# -----------------------------
@st.cache_data(show_spinner=False)
def compute_grids(
    time_to_maturity: float,
    interest_rate: float,
    strike: float,
    call_purchase_price: float,
    put_purchase_price: float,
    spot_range: np.ndarray,
    vol_range: np.ndarray,
    mode: str,
):
    """
    Compute price or P&L grids over spot and vol ranges.
    mode in {"fair_value", "pnl"}
    """
    call_values = np.zeros((len(vol_range), len(spot_range)))
    put_values = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=interest_rate,
                call_purchase_price=call_purchase_price,
                put_purchase_price=put_purchase_price,
            )
            call_price, put_price, call_pnl, put_pnl = bs_temp.calculate_prices()
            if mode == "pnl":
                call_values[i, j] = call_pnl
                put_values[i, j] = put_pnl
            else:
                call_values[i, j] = call_price
                put_values[i, j] = put_price

    call_df = pd.DataFrame(call_values, index=np.round(vol_range, 3), columns=np.round(spot_range, 2))
    put_df = pd.DataFrame(put_values, index=np.round(vol_range, 3), columns=np.round(spot_range, 2))
    return call_df, put_df


def make_heatmap(df: pd.DataFrame, title: str, show_values: bool, colorbar_title: str):
    text_vals = np.round(df.values, 2) if show_values else None
    text_tpl = "%{text}" if show_values else None
    fig = go.Figure(
        data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            text=text_vals,
            texttemplate=text_tpl,
            colorscale="RdYlGn",
            colorbar=dict(title=colorbar_title),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Spot Price (S)",
        yaxis_title="Volatility (σ)",
        margin=dict(l=50, r=50, t=50, b=50),
    )
    return fig


# Safe attribute getter for Greeks (so UI doesn't crash if class lacks one)
def get_attr(obj, name, default=None):
    return getattr(obj, name, default)



# Main content
# -----------------------------
st.title("Option Value & P&L — Interactive Heatmaps")

# Inputs table
input_df = pd.DataFrame(
    {
        "Current Asset Price (S)": [current_price],
        "Strike (K)": [strike],
        "Time to Maturity (T, yrs)": [time_to_maturity],
        "Volatility (σ)": [volatility],
        "Risk-Free Rate (r)": [interest_rate],
    }
)
st.dataframe(input_df, use_container_width=True)

# Base model at the chosen point
bs_model = BlackScholes(
    time_to_maturity=time_to_maturity,
    strike=strike,
    current_price=current_price,
    volatility=volatility,
    interest_rate=interest_rate,
    call_purchase_price=call_purchase_price,
    put_purchase_price=put_purchase_price,
)

call_price, put_price, call_gain, put_gain = bs_model.calculate_prices()

# Metric cards
col1, col2 = st.columns([1, 1])

with col1:
    if show_greeks:
        st.markdown(
            f"""
            <div class="metric-container metric-call">
                <div>
                    <div class="metric-label">CALL Value</div>
                    <div class="metric-value">${call_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${call_gain:.2f}</div>
                    <div class="metric-label">Δ (Delta)</div>
                    <div class="metric-value">{get_attr(bs_model, "call_delta", float("nan")):.3f}</div>
                    <div class="metric-label">Γ (Gamma)</div>
                    <div class="metric-value">{get_attr(bs_model, "call_gamma", float("nan")):.3f}</div>
                    <div class="metric-label">Θ (Theta)</div>
                    <div class="metric-value">{get_attr(bs_model, "call_theta", float("nan")):.3f}</div>
                    <div class="metric-label">Vega</div>
                    <div class="metric-value">{get_attr(bs_model, "call_vega", float("nan")):.3f}</div>
                    <div class="metric-label">Rho</div>
                    <div class="metric-value">{get_attr(bs_model, "call_rho", float("nan")):.3f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="metric-container metric-call">
                <div>
                    <div class="metric-label">CALL Value</div>
                    <div class="metric-value">${call_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${call_gain:.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col2:
    if show_greeks:
        st.markdown(
            f"""
            <div class="metric-container metric-put">
                <div>
                    <div class="metric-label">PUT Value</div>
                    <div class="metric-value">${put_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${put_gain:.2f}</div>
                    <div class="metric-label">Δ (Delta)</div>
                    <div class="metric-value">{get_attr(bs_model, "put_delta", float("nan")):.3f}</div>
                    <div class="metric-label">Γ (Gamma)</div>
                    <div class="metric-value">{get_attr(bs_model, "put_gamma", float("nan")):.3f}</div>
                    <div class="metric-label">Θ (Theta)</div>
                    <div class="metric-value">{get_attr(bs_model, "put_theta", float("nan")):.3f}</div>
                    <div class="metric-label">Vega</div>
                    <div class="metric-value">{get_attr(bs_model, "put_vega", float("nan")):.3f}</div>
                    <div class="metric-label">Rho</div>
                    <div class="metric-value">{get_attr(bs_model, "put_rho", float("nan")):.3f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="metric-container metric-put">
                <div>
                    <div class="metric-label">PUT Value</div>
                    <div class="metric-value">${put_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${put_gain:.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
with st.expander("How to read this chart"):
    st.markdown(
        "- **Spot (x-axis)** and **Volatility (y-axis)** drive the heatmap.\n"
        "- **Strike (K)**, **rate (r)**, and **time (T)** are fixed by the controls above.\n"
        "- Adjust the axis ranges and grid resolution to zoom into relevant scenarios."
    )

# Global toggle for cell labels on heatmaps
show_values = st.checkbox("Show heatmap cell values", value=False)

# Tabs for Fair Value vs P&L
tab1, tab2 = st.tabs(["Fair Value", "Profit & Loss"])

with tab1:
    st.subheader("Fair Value Heatmaps")
    fair_call_df, fair_put_df = compute_grids(
        time_to_maturity,
        interest_rate,
        strike,
        call_purchase_price,
        put_purchase_price,
        spot_range,
        vol_range,
        mode="fair_value",
    )
    fair_call_fig = make_heatmap(fair_call_df, "Call — Fair Value", show_values, "Call")
    fair_put_fig = make_heatmap(fair_put_df, "Put — Fair Value", show_values, "Put")

    st.plotly_chart(fair_call_fig, use_container_width=True, key="fair_call_chart")
    st.download_button(
        "Download Fair Value (Call) CSV",
        fair_call_df.to_csv().encode(),
        "fair_value_call.csv",
        "text/csv",
    )
    st.plotly_chart(fair_put_fig, use_container_width=True, key="fair_put_chart")
    st.download_button(
        "Download Fair Value (Put) CSV",
        fair_put_df.to_csv().encode(),
        "fair_value_put.csv",
        "text/csv",
    )

with tab2:
    st.subheader("P&L Heatmaps")
    pnl_call_df, pnl_put_df = compute_grids(
        time_to_maturity,
        interest_rate,
        strike,
        call_purchase_price,
        put_purchase_price,
        spot_range,
        vol_range,
        mode="pnl",
    )
    pnl_call_fig = make_heatmap(pnl_call_df, "Call — P&L", show_values, "Call P&L")
    pnl_put_fig = make_heatmap(pnl_put_df, "Put — P&L", show_values, "Put P&L")

    st.plotly_chart(pnl_call_fig, use_container_width=True, key="pnl_call_chart")
    st.download_button(
        "Download P&L (Call) CSV",
        pnl_call_df.to_csv().encode(),
        "pnl_call.csv",
        "text/csv",
    )
    st.plotly_chart(pnl_put_fig, use_container_width=True, key="pnl_put_chart")
    st.download_button(
        "Download P&L (Put) CSV",
        pnl_put_df.to_csv().encode(),
        "pnl_put.csv",
        "text/csv",
    )
