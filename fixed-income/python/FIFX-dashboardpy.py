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
# FX Market Section
# ----------------------
st.subheader("🌍 FX Portfolio Performance")

fx_pairs = {
    "USDNOK=X": 0.4,
    "EURNOK=X": 0.3,
    "JPYUSD=X": 0.3,
}

# Download FX data
fx_raw = yf.download(list(fx_pairs.keys()), start="2024-01-01", group_by="ticker", auto_adjust=True)

# Extract 'Close' price from multi-index structure
fx_data = pd.DataFrame()
for ticker in fx_pairs.keys():
    try:
        fx_data[ticker] = fx_raw[ticker]["Close"]
    except KeyError:
        st.warning(f"⚠️ No data for {ticker}, skipping.")
        continue

fx_data.dropna(how="all", inplace=True)

if fx_data.empty:
    st.error("❌ No FX data retrieved. Please check ticker symbols or internet connection.")
    st.stop()

# Normalize and calculate portfolio
fx_norm = fx_data / fx_data.iloc[0]
fx_weights = pd.Series(fx_pairs)
fx_portfolio = (fx_norm * fx_weights).sum(axis=1)
fx_returns = fx_portfolio.pct_change().dropna()
fx_cum_returns = (1 + fx_returns).cumprod()

# Plot cumulative FX return
st.plotly_chart(px.line(fx_cum_returns, title="Cumulative FX Portfolio Return"), use_container_width=True)

# Show daily FX PnL
st.subheader("💸 Daily FX PnL (%)")
st.dataframe((fx_returns * 100).to_frame(name="Daily PnL (%)"))

# ----------------------
# Fixed Income Section
# ----------------------
st.header("🏦 Fixed Income – Yield Curve Snapshot")

# Mock data – replace later with OECD or FRED API
maturities = ["1Y", "2Y", "5Y", "10Y", "30Y"]
yields_today = [3.2, 3.4, 3.7, 3.9, 4.1]
yields_last_month = [2.9, 3.1, 3.5, 3.7, 3.9]

yields_df = pd.DataFrame({
    "Maturity": maturities * 2,
    "Yield": yields_today + yields_last_month,
    "Date": ["Today"] * len(maturities) + ["Last Month"] * len(maturities)
})

# Yield curve plot
fig_yield = px.line(yields_df, x="Maturity", y="Yield", color="Date",
                    markers=True, title="Yield Curve Comparison")
st.plotly_chart(fig_yield, use_container_width=True)

# Yield curve delta
st.subheader("📉 Yield Curve Change (bps)")
delta_yields = np.array(yields_today) - np.array(yields_last_month)
delta_df = pd.DataFrame({
    "Maturity": maturities,
    "Change (bps)": delta_yields * 100
})
st.dataframe(delta_df.set_index("Maturity"))
