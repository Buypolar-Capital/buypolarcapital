import os
import pandas as pd
import yfinance as yf

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "shel_intraday_utc.csv")

print("⏳ Downloading 5m data for last 30 days...")
shel_us = yf.download("SHEL", period="30d", interval="5m", prepost=True)
shel_eu = yf.download("SHEL.L", period="30d", interval="5m")

# Check shapes
print("✔️ SHEL (NYSE) shape:", shel_us.shape)
print("✔️ SHEL.L (LSE) shape:", shel_eu.shape)

# Timezone setup
shel_us.index = shel_us.index.tz_convert("UTC") if shel_us.index.tzinfo else shel_us.index.tz_localize("UTC")
shel_eu.index = shel_eu.index.tz_convert("UTC") if shel_eu.index.tzinfo else shel_eu.index.tz_localize("UTC")

# Unwrap the inner columns
shel_us_close = shel_us["Close"].iloc[:, 0] if isinstance(shel_us["Close"], pd.DataFrame) else shel_us["Close"]
shel_eu_close = shel_eu["Close"].iloc[:, 0] if isinstance(shel_eu["Close"], pd.DataFrame) else shel_eu["Close"]

print("🔍 SHEL (NYSE) Close sample:\n", shel_us_close.head())
print("🔍 SHEL.L (LSE) Close sample:\n", shel_eu_close.head())

# Combine and align
df = pd.DataFrame({
    "shel_us": shel_us_close,
    "shel_eu": shel_eu_close
}).dropna()

# Save
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
df.to_csv(DATA_PATH)
print(f"✅ Saved to {DATA_PATH}")
