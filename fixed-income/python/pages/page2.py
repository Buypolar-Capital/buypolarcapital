import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

# ----------------------
# Page Config
# ----------------------
st.title("📉 BPC Capital Dashboard – Signals & Strategy")

# ----------------------
# Yield Curve Slope Tracking
# ----------------------
st.header("📐 Yield Curve Slope Analysis")

yield_tickers = {
    "3M": "^IRX",
    "5Y": "^FVX",
    "10Y": "^TNX",
    "30Y": "^TYX"
}

yields_data = {}

for label, ticker in yield_tickers.items():
    try:
        data = yf.download(ticker, start="2024-01-01", auto_adjust=True)
        if isinstance(data, pd.DataFrame) and "Close" in data.columns:
            close_series = data["Close"].dropna()
            if not close_series.empty:
                yields_data[label] = close_series
            else:
                st.warning(f"⚠️ No usable 'Close' data for {label} ({ticker})")
        else:
            st.warning(f"⚠️ No data for {label} ({ticker})")
    except Exception as e:
        st.warning(f"⚠️ Failed to download {label} ({ticker}): {e}")

# ✅ Only proceed if we have at least two full Series
if len(yields_data) < 2:
    st.error("❌ Not enough yield data for slope analysis")
    st.stop()

# 👇 This will now work safely
yields_df = pd.concat(yields_data.values(), axis=1)
yields_df.columns = yields_data.keys()
yields_df.dropna(inplace=True)


# Calculate spreads
spreads = pd.DataFrame()
if all(x in yields_df.columns for x in ["3M", "10Y"]):
    spreads["3M10Y"] = yields_df["10Y"] - yields_df["3M"]
if all(x in yields_df.columns for x in ["5Y", "30Y"]):
    spreads["5Y30Y"] = yields_df["30Y"] - yields_df["5Y"]

st.subheader("🧮 Yield Spreads Over Time")
st.plotly_chart(px.line(spreads, title="Yield Curve Slopes (bps)"), use_container_width=True)

# Highlight inversion periods
latest_spreads = spreads.iloc[-1]
for label, value in latest_spreads.items():
    st.metric(label=f"Latest {label} Spread", value=f"{value:.2f} bps", delta=value)

# ----------------------
# FX Z-Score Signal Tracking
# ----------------------
st.header("💡 FX Z-Score Signals")

fx_pairs = ["USDNOK=X", "EURNOK=X", "JPYUSD=X"]
fx_raw = yf.download(fx_pairs, start="2024-01-01", group_by="ticker", auto_adjust=True)

fx_data = pd.DataFrame()
for ticker in fx_pairs:
    try:
        fx_data[ticker] = fx_raw[ticker].get("Close", pd.Series(dtype=float))
    except:
        st.warning(f"⚠️ Failed to load {ticker}")

fx_data.dropna(inplace=True)

# Calculate z-scores
zscore_df = (fx_data - fx_data.rolling(window=20).mean()) / fx_data.rolling(window=20).std()

st.subheader("📈 FX Z-Score (20-Day Rolling)")
st.plotly_chart(px.line(zscore_df, title="Z-Scores of Selected FX Pairs"), use_container_width=True)

# Signal table
st.subheader("🔔 FX Signal Table (Threshold ±1.5)")
signal_df = zscore_df.iloc[-1].to_frame(name="Z-Score")
signal_df["Signal"] = signal_df["Z-Score"].apply(
    lambda z: "Buy" if z < -1.5 else ("Sell" if z > 1.5 else "Hold")
)
st.dataframe(signal_df)

st.caption("Note: Z-score signals are for exploratory purposes only.")
