import os
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

os.makedirs("dashboard/plots", exist_ok=True)

def load_and_plot(category, title, filename):
    path = f"dashboard/data/{category}/{category}.csv"
    df = pd.read_csv(path, sep=';').sort_values(by="1D_return")
    plt.barh(df["name"], df["1D_return"])
    plt.title(title)
    plt.grid(True, axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(f"dashboard/plots/{filename}")
    plt.close()

# Grid of bar plots (4 subplots)
fig, axs = plt.subplots(2, 2, figsize=(11, 7))

categories = [
    ("indices", "Indices"),
    ("commodities", "Commodities"),
    ("fixed_income", "Fixed Income"),
    ("crypto", "Crypto"),
]

for ax, (cat, title) in zip(axs.flatten(), categories):
    filename = "major_indices.csv" if cat == "indices" else f"{cat}.csv"
    df = pd.read_csv(f"dashboard/data/{cat}/{filename}", sep=";")
    df = df.sort_values(by="1D_return")
    ax.barh(df["name"], df["1D_return"])
    ax.set_title(title)
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig("dashboard/plots/grid_returns.pdf")
plt.close()
print("✅ Saved grid plot to dashboard/plots/grid_returns.pdf")

# Sparkline price trends
def fetch_and_plot(ticker_dict, title, filename):
    tickers = list(ticker_dict.values())
    prices = yf.download(tickers, period="7d", interval="1d")["Close"]
    if isinstance(prices, pd.Series):  # Single ticker
        prices = prices.to_frame()

    plt.figure(figsize=(10, 4))
    for col in prices.columns:
        plt.plot(prices[col], label=col)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(f"dashboard/plots/{filename}")
    plt.close()
    print(f"✅ Saved sparkline: {filename}")

# Reuse the same tickers as in build_data_v2
index_tickers = {
    "OSEBX": "^OSEAX", "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "DOW JONES": "^DJI"
}
fetch_and_plot(index_tickers, "Sparkline: Major Indices", "sparkline_indices.pdf")

crypto_tickers = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"
}
fetch_and_plot(crypto_tickers, "Sparkline: Crypto", "sparkline_crypto.pdf")
