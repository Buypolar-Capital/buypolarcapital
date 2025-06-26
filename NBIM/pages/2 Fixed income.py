import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.load_data import load_fixed_income_data

st.set_page_config(layout="wide")
st.title("🏦 Fixed Income Overview")

# Load fixed income data
df = load_fixed_income_data()

# Display top-level summary
st.markdown("Simulated top 10 fixed income issuers (government and institutional)")

# Plot loop
for name in df.columns:
    st.markdown(f"### {name}")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[name],
        mode="lines",
        name=name,
        line=dict(width=2)
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=20, b=20),
        xaxis_title="Date",
        yaxis_title="Simulated Bond Price"
    )

    st.plotly_chart(fig, use_container_width=True)

    change_pct = 100 * (df[name].iloc[-1] - df[name].iloc[0]) / df[name].iloc[0]
    st.metric(label="Change over period", value=f"{change_pct:.2f}%")
    st.markdown("---")
