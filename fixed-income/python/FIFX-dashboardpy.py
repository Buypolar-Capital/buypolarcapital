import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf

# ----------------------
# Page Setup
# ----------------------
st.set_page_config(page_title="BuyPolar Capital FI and FX", layout="wide")
st.title("📊 BPC Capital Dashboard")
st.header("💱 BuyPolar Capital – Fixed Income & FX Focus")

# ----------------------
# FX Portfolio Section
# ----------------------
st.subheader("🌍 FX Portfolio Performance")

fx_pairs = {
    "USDNOK=X": 0.4,
    "EURNOK=X": 0.3,
    "JPYUSD=X": 0.3,
}

fx_raw = yf.download(list(fx_pairs.keys()), start="2024-01-01", group_by="ticker", auto_adjust=True)

fx_data = pd.DataFrame()
for ticker in fx_pairs.keys():
    try:
        fx_data[ticker] = fx_raw[ticker]["Close"]
    except Exception:
        st.warning(f"⚠️ No data for {ticker}, skipping.")

fx_data.dropna(how="all", inplace=True)

if fx_data.empty:
    st.error("❌ No FX data retrieved. Please check ticker symbols or internet connection.")
    st.stop()

fx_norm = fx_data / fx_data.iloc[0]
fx_weights = pd.Series(fx_pairs)
fx_portfolio = (fx_norm * fx_weights).sum(axis=1)
fx_returns = fx_portfolio.pct_change().dropna()
fx_cum_returns = (1 + fx_returns).cumprod()

st.plotly_chart(px.line(fx_cum_returns, title="Cumulative FX Portfolio Return"), use_container_width=True)
st.subheader("💸 Daily FX PnL (%)")
st.dataframe((fx_returns * 100).to_frame(name="Daily PnL (%)"))

# ----------------------
# Real US Yield Curve Section
# ----------------------
st.header("🏛️ Real US Treasury Yields")

# Define Yahoo tickers for treasury yields
yield_tickers = {
    "3M": "^IRX",
    "5Y": "^FVX",
    "10Y": "^TNX",
    "30Y": "^TYX"
}

yields_dict = {}

for label, ticker in yield_tickers.items():
    try:
        data = yf.download(ticker, start="2024-01-01")["Close"]
        if not data.empty:
            yields_dict[label] = data
        else:
            st.warning(f"⚠️ No data returned for {label} ({ticker})")
    except Exception:
        st.warning(f"⚠️ Error retrieving {label} ({ticker})")

# Only proceed if we have data
if not yields_dict:
    st.error("❌ No yield data available. Try again later.")
    st.stop()

# Create DataFrame from valid yield series
yields_df = pd.DataFrame(yields_dict).dropna()

# Show latest yields
latest_yields = yields_df.iloc[-1]
st.subheader("📈 Current US Treasury Yields (%)")
st.dataframe(latest_yields.to_frame(name="Yield (%)"))

# Plot historical yields
st.subheader("📉 Yield History Over Time")
st.plotly_chart(px.line(yields_df, title="US Treasury Yields Over Time"), use_container_width=True)

# Plot yield curve snapshot
yc_snapshot = pd.DataFrame({
    "Maturity": latest_yields.index,
    "Yield": latest_yields.values
})
yc_snapshot["Maturity"] = pd.Categorical(yc_snapshot["Maturity"], categories=["3M", "5Y", "10Y", "30Y"], ordered=True)
yc_snapshot = yc_snapshot.sort_values("Maturity")

st.subheader("🔩 Yield Curve Snapshot")
fig_curve = px.line(yc_snapshot, x="Maturity", y="Yield", markers=True, title="US Treasury Yield Curve")
st.plotly_chart(fig_curve, use_container_width=True)
