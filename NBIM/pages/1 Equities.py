import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.load_data import load_equity_data

st.set_page_config(layout="wide")
st.title("📈 Equities Overview")

# Load data
df = load_equity_data()

# Define readable names
companies = {
    "Apple Inc (USA)": "AAPL",
    "Taiwan Semiconductor (Taiwan)": "TSM",
    "SAP SE (Germany)": "SAP",
    "ASML Holding (Netherlands)": "ASML",
    "Novo Nordisk (Denmark)": "NVO",
    "Tencent Holdings (China)": "0700.HK",
    "Nestlé SA (Switzerland)": "NESN.SW",
    "LVMH (France)": "MC.PA",
    "Toyota (Japan)": "7203.T",
    "Samsung Electronics (South Korea)": "005930.KS"
}

# Plot loop
for name in df.columns:
    series = df[name].dropna()

    if series.empty:
        st.warning(f"⚠️ No data available for {name} — skipping.")
        continue

    st.markdown(f"### {name}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=series.index,
        y=series.values,
        mode="lines",
        name=name,
        line=dict(width=2)
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=20, b=20),
        xaxis_title="Date",
        yaxis_title="Price (Local Currency)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Compute change only if we have at least two points
    if len(series) > 1:
        change_pct = 100 * (series.iloc[-1] - series.iloc[0]) / series.iloc[0]
        st.metric(label="30-day change", value=f"{change_pct:.2f}%")
    else:
        st.info("ℹ️ Not enough data to compute % change.")

    st.markdown("---")
