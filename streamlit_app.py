import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from BlackScholes import BlackScholes

#######################
# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

# Function to generate heatmaps
# ... your existing imports and BlackScholes class definition ...


# Sidebar for User Inputs
# Sidebar for User Inputs
with st.sidebar:
    st.title("Black-Scholes Options Model")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/jack-craig-65a2082a9/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Jack Craig`</a>', unsafe_allow_html=True)

    # Toggle to show Greeks
    show_greeks = st.checkbox("Show Greeks (Δ, Γ, Θ, Vega, Rho)", value=False)

    # Market parameters
    with st.expander("Market Parameters", expanded=False):
        current_price = st.number_input("Current Asset Price", value=100.0)
        strike = st.number_input("Strike Price", value=100.0)
        time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0, min_value=0.01)
        volatility = st.number_input("Volatility (σ)", value=0.2, min_value=0.01)
        interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

    # Purchase prices
    with st.expander("Your Option Purchase Prices", expanded=False):
        call_purchase_price = st.number_input("Call Option Purchase Price", value=0.0, min_value=0.0, step=0.01)
        put_purchase_price = st.number_input("Put Option Purchase Price", value=0.0, min_value=0.0, step=0.01)

    # Heatmap settings
    with st.expander("Heatmap Parameters", expanded=False):
        spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price * 0.8, step=0.01)
        spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price * 1.2, step=0.01)
        vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01)
        vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01)

        spot_range = np.linspace(spot_min, spot_max, 10)
        vol_range = np.linspace(vol_min, vol_max, 10)




def plot_heatmap(bs_model, spot_range, vol_range, strike, call_purchase_price, put_purchase_price, mode='pnl'):
    call_values = np.zeros((len(vol_range), len(spot_range)))
    put_values = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate,
                call_purchase_price=call_purchase_price,
                put_purchase_price=put_purchase_price
            )
            call_price, put_price, call_pnl, put_pnl = bs_temp.calculate_prices()

            if mode == 'pnl':
                call_values[i, j] = call_pnl
                put_values[i, j] = put_pnl
            else:
                call_values[i, j] = call_price
                put_values[i, j] = put_price

    # Create DataFrames for CSV export
    call_df = pd.DataFrame(call_values, index=np.round(vol_range, 2), columns=np.round(spot_range, 2))
    put_df = pd.DataFrame(put_values, index=np.round(vol_range, 2), columns=np.round(spot_range, 2))

    # Plotly heatmaps
    call_fig = go.Figure(data=go.Heatmap(
    z=call_df.values,
    x=call_df.columns,
    y=call_df.index,
    text=np.round(call_df.values, 2),
    texttemplate="%{text}",
    colorscale='RdYlGn',
    colorbar=dict(title="Call")
    ))
    call_fig.update_layout(
        title='Call Heatmap',
        xaxis_title='Spot Price',
        yaxis_title='Volatility',
        margin=dict(l=50, r=50, t=50, b=50)
    )

    put_fig = go.Figure(data=go.Heatmap(
    z=put_df.values,
    x=put_df.columns,
    y=put_df.index,
    text=np.round(put_df.values, 2),
    texttemplate="%{text}",
    colorscale='RdYlGn',
    colorbar=dict(title="Put")
    ))
    put_fig.update_layout(
        title='Put Heatmap',
        xaxis_title='Spot Price',
        yaxis_title='Volatility',
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return call_fig, put_fig, call_df, put_df

# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Call and Put values using updated BlackScholes class
bs_model = BlackScholes(
    time_to_maturity,
    strike,
    current_price,
    volatility,
    interest_rate,
    call_purchase_price,
    put_purchase_price
)
call_price, put_price, call_gain, put_gain = bs_model.calculate_prices()

# Prepare optional Greeks HTML
call_greeks_html = ""
put_greeks_html = ""

if show_greeks:
    call_greeks_html = (
    f'<div class="metric-label">Δ (Delta)</div><div class="metric-value">{bs_model.call_delta:.3f}</div>'
    f'<div class="metric-label">Γ (Gamma)</div><div class="metric-value">{bs_model.call_gamma:.3f}</div>'
)
    put_greeks_html = (
    f'<div class="metric-label">Δ (Delta)</div><div class="metric-value">{bs_model.put_delta:.3f}</div>'
    f'<div class="metric-label">Γ (Gamma)</div><div class="metric-value">{bs_model.put_gamma:.3f}</div>'
)


# Display Call and Put Values in colored metric cards
col1, col2 = st.columns([1, 1])

# CALL display block
# CALL display block
with col1:
    if show_greeks:
        st.markdown(f"""
            <div class="metric-container metric-call">
                <div>
                    <div class="metric-label">CALL Value</div>
                    <div class="metric-value">${call_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${call_gain:.2f}</div>
                    <div class="metric-label">Δ (Delta)</div>
                    <div class="metric-value">{bs_model.call_delta:.3f}</div>
                    <div class="metric-label">Γ (Gamma)</div>
                    <div class="metric-value">{bs_model.call_gamma:.3f}</div>
                    <div class="metric-label">Θ (Theta)</div>
                    <div class="metric-value">{bs_model.call_theta:.3f}</div>
                    <div class="metric-label">Vega</div>
                    <div class="metric-value">{bs_model.call_vega:.3f}</div>
                    <div class="metric-label">Rho</div>
                    <div class="metric-value">{bs_model.call_rho:.3f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="metric-container metric-call">
                <div>
                    <div class="metric-label">CALL Value</div>
                    <div class="metric-value">${call_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${call_gain:.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


# PUT display block
with col2:
    if show_greeks:
        st.markdown(f"""
            <div class="metric-container metric-put">
                <div>
                    <div class="metric-label">PUT Value</div>
                    <div class="metric-value">${put_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${put_gain:.2f}</div>
                    <div class="metric-label">Δ (Delta)</div>
                    <div class="metric-value">{bs_model.put_delta:.3f}</div>
                    <div class="metric-label">Γ (Gamma)</div>
                    <div class="metric-value">{bs_model.put_gamma:.3f}</div>
                    <div class="metric-label">Θ (Theta)</div>
                    <div class="metric-value">{bs_model.put_theta:.3f}</div>
                    <div class="metric-label">Vega</div>
                    <div class="metric-value">{bs_model.put_vega:.3f}</div>
                    <div class="metric-label">Rho</div>
                    <div class="metric-value">{bs_model.put_rho:.3f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="metric-container metric-put">
                <div>
                    <div class="metric-label">PUT Value</div>
                    <div class="metric-value">${put_price:.2f}</div>
                    <div class="metric-label">Net Gain</div>
                    <div class="metric-value">${put_gain:.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


# Heatmap Section
st.markdown("")
st.title("Options Price - Interactive Heatmap")
st.info("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'.")

# Generate heatmaps for both modes
tab1, tab2 = st.tabs(["Fair Value", "Profit & Loss"])

with tab1:
    st.subheader("Fair Value Heatmaps")
    fair_fig_call, fair_fig_put, fair_df_call, fair_df_put = plot_heatmap(
        bs_model, spot_range, vol_range, strike,
        call_purchase_price, put_purchase_price, mode='fair_value'
    )
    st.plotly_chart(fair_fig_call, use_container_width=True, key="fair_call_chart")
    st.download_button("Download Fair Value Call CSV", fair_df_call.to_csv().encode(), "fair_call.csv", "text/csv")
    st.plotly_chart(fair_fig_put, use_container_width=True, key="fair_put_chart")
    st.download_button("Download Fair Value Put CSV", fair_df_put.to_csv().encode(), "fair_put.csv", "text/csv")

with tab2:
    st.subheader("P&L Heatmaps")
    pnl_fig_call, pnl_fig_put, pnl_df_call, pnl_df_put = plot_heatmap(
        bs_model, spot_range, vol_range, strike,
        call_purchase_price, put_purchase_price, mode='pnl'
    )
    st.plotly_chart(pnl_fig_call, use_container_width=True, key="pnl_call_chart")
    st.download_button("Download P&L Call CSV", pnl_df_call.to_csv().encode(), "pnl_call.csv", "text/csv")
    st.plotly_chart(pnl_fig_put, use_container_width=True, key="pnl_put_chart")
    st.download_button("Download P&L Put CSV", pnl_df_put.to_csv().encode(), "pnl_put.csv", "text/csv")
