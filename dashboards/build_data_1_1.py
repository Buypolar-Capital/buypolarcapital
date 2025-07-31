import yfinance as yf
import pandas as pd
import os

# Define assets to track
tickers = ["AAPL", "TSLA", "MSFT", "NVDA", "GOOG"]
output_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(output_dir, exist_ok=True)

# Download latest data
data = yf.download(tickers, period="2d")['Close']
print(data.columns)


# Calculate returns and volatility
returns = (data.iloc[-1] / data.iloc[-2] - 1) * 100
vol = data.pct_change().std() * 100

leaderboard_df = pd.DataFrame({
    "ticker": returns.index,
    "ret": returns.values.round(2),
    "vol": vol.values.round(2)
})

# Summary
summary_df = pd.DataFrame([{
    "num_tickers": len(tickers),
    "top_ticker": leaderboard_df.sort_values(by='ret', ascending=False).iloc[0]['ticker'],
    "commentary": "Auto-generated summary. Customize this with an LLM or your own analysis."
}])

# Save
leaderboard_df.to_csv(os.path.join(output_dir, "leaderboard.csv"), index=False, sep=";")
summary_df.to_csv(os.path.join(output_dir, "summary.csv"), index=False, sep=";")

print("✅ Data built and saved!")
