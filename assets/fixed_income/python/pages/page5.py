import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from arch import arch_model

st.set_page_config(page_title="📉 FX Volatility – GARCH, EGARCH, VaR", layout="wide")
st.title("📉 FX Volatility Modelling – GARCH, EGARCH & VaR")

# -------------------------------
# Load FX Data
# -------------------------------
st.subheader("💱 Load FX Data")

fx_ticker = st.selectbox("Select FX Pair", ["USDNOK=X", "EURNOK=X", "JPYUSD=X"])
data = yf.download(fx_ticker, start="2018-01-01", auto_adjust=True)[["Close"]].rename(columns={"Close": "price"})
data["return"] = 100 * data["price"].pct_change()
data.dropna(inplace=True)

st.line_chart(data["return"], use_container_width=True)

# -------------------------------
# Realized Volatility (Rolling STD)
# -------------------------------
st.subheader("📊 Realized Volatility (Rolling 30D Std Dev)")
data["realized_vol"] = data["return"].rolling(window=30).std()
st.line_chart(data["realized_vol"], use_container_width=True)
