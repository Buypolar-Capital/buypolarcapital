import os
import pandas as pd
import yfinance as yf

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "shel_intraday_utc.csv")

# Download data
shel_us = yf.download("SHEL", period="1d", interval="1m", prepost=True)
shel_eu = yf.download("SHEL.L", period="1d", interval="1m")

print("US data shape:", shel_us.shape)
print("EU data shape:", shel_eu.shape)

# Check if either is empty
if shel_us.empty:
    raise ValueError("❌ shel_us (SHEL - NYSE) returned empty DataFrame!")
if shel_eu.empty:
    raise ValueError("❌ shel_eu (SHEL.L - London) returned empty DataFrame!")

# Convert index to UTC
shel_us.index = shel_us.index.tz_convert("UTC")
shel_eu.index = shel_eu.index.tz_convert("UTC")

# Extract just the series (not wrapped inside a DataFrame)
shel_us_close = shel_us["Close"]
if isinstance(shel_us_close, pd.DataFrame):
    shel_us_close = shel_us_close.iloc[:, 0]

shel_eu_close = shel_eu["Close"]
if isinstance(shel_eu_close, pd.DataFrame):
    shel_eu_close = shel_eu_close.iloc[:, 0]

# Confirm they are Series
print("US Close type:", type(shel_us_close))
print("EU Close type:", type(shel_eu_close))

# Combine into one DataFrame
df = pd.DataFrame({
    "shel_us": shel_us_close,
    "shel_eu": shel_eu_close
}).dropna()

# Save
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
df.to_csv(DATA_PATH)
print(f"✅ Saved intraday data to {DATA_PATH}")
