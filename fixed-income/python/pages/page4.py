
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

try:
    from prophet import Prophet
    prophet_installed = True
except ImportError:
    prophet_installed = False

st.title("📈 FX Forecasting – ARIMA, ETS & Prophet")

# -------------------------------
# Load FX Data
# -------------------------------
st.subheader("💱 Load FX Data")

fx_ticker = st.selectbox("Select FX Pair", ["USDNOK=X", "EURNOK=X", "JPYUSD=X"])
raw = yf.download(fx_ticker, start="2018-01-01", auto_adjust=True)[["Close"]].dropna()
raw.columns = ["price"]


st.line_chart(raw, use_container_width=True)

# -------------------------------
# Forecast Parameters
# -------------------------------
st.subheader("⚙️ Forecast Settings")

horizon = st.slider("Forecast Horizon (days)", min_value=30, max_value=365, value=90, step=10)

# -------------------------------
# ARIMA Forecast
# -------------------------------
st.subheader("🔍 ARIMA Forecast")

arima_model = ARIMA(raw["price"], order=(5,1,0)).fit()
arima_forecast = arima_model.forecast(steps=horizon)
arima_df = pd.DataFrame({
    "Date": pd.date_range(start=raw.index[-1] + pd.Timedelta(days=1), periods=horizon),
    "ARIMA Forecast": arima_forecast
})

st.line_chart(arima_df.set_index("Date"), use_container_width=True)

# -------------------------------
# ETS (Holt-Winters)
# -------------------------------
st.subheader("📊 Exponential Smoothing (ETS) Forecast")

ets_model = ExponentialSmoothing(raw["price"], trend="add", seasonal=None).fit()
ets_forecast = ets_model.forecast(horizon)
ets_df = pd.DataFrame({
    "Date": pd.date_range(start=raw.index[-1] + pd.Timedelta(days=1), periods=horizon),
    "ETS Forecast": ets_forecast
})

st.line_chart(ets_df.set_index("Date"), use_container_width=True)

# -------------------------------
# Prophet Forecast
# -------------------------------
st.subheader("🔮 Prophet Forecast")

if prophet_installed:
    prophet_df = raw.reset_index().rename(columns={"Date": "ds", "price": "y"})
    model = Prophet()
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future)

    forecast_df = forecast[["ds", "yhat"]].set_index("ds").tail(horizon)
    forecast_df.columns = ["Prophet Forecast"]

    st.line_chart(forecast_df, use_container_width=True)
else:
    st.warning("⚠️ Prophet is not installed. Run `pip install prophet` to enable this forecast.")

# -------------------------------
# Combined Plot
# -------------------------------
st.subheader("🧵 Combined Forecast View")

combined_df = pd.concat([
    arima_df.set_index("Date").rename(columns={"ARIMA Forecast": "ARIMA"}),
    ets_df.set_index("Date").rename(columns={"ETS Forecast": "ETS"}),
], axis=1)

if prophet_installed:
    combined_df["Prophet"] = forecast_df["Prophet Forecast"]

fig = px.line(combined_df, title="📈 Forecast Comparison")
st.plotly_chart(fig, use_container_width=True)

st.caption("⚠️ Forecasts are for educational use only and not investment advice.")
