import os
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

os.makedirs("dashboard/plots", exist_ok=True)

# --- Individual Bar Plots (used in grid and separately) ---
def plot_category_grid(category, title):
    filename = "major_indices.csv" if category == "indices" else f"{category}.csv"
    path = f"dashboard/data/{category}/{filename}"
    df = pd.read_csv(path, sep=';').sort_values(by="1D_return")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(df["name"], df["1D_return"])
    ax.set_title(title)
    ax.grid(True, axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    output_path = f"dashboard/plots/{category}_grid.png"
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Saved {category} plot to {output_path}")

# --- Overview Grid of All ---
fig, axs = plt.subplots(2, 2, figsize=(11, 7))
categories = [
    ("indices", "Indices"),
    ("commodities", "Commodities"),
    ("fixed_income", "Fixed Income"),
    ("crypto", "Crypto"),
]

for ax, (cat, title) in zip(axs.flatten(), categories):
    filename = "major_indices.csv" if cat == "indices" else f"{cat}.csv"
    df = pd.read_csv(f"dashboard/data/{cat}/{filename}", sep=";").sort_values(by="1D_return")
    ax.barh(df["name"], df["1D_return"])
    ax.set_title(title)
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig("dashboard/plots/grid_returns.png")
plt.close()
print("✅ Saved overview grid to dashboard/plots/grid_returns.png")

# --- Sparklines ---
def fetch_and_plot(ticker_dict, title, filename):
    tickers = list(ticker_dict.values())
    prices = yf.download(tickers, period="7d", interval="1d")["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    plt.figure(figsize=(10, 4))
    for col in prices.columns:
        plt.plot(prices[col], label=col)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend(fontsize=7)
    plt.tight_layout()
    out_path = f"dashboard/plots/{filename.replace('.pdf', '.png')}"
    plt.savefig(out_path)
    plt.close()
    print(f"✅ Saved sparkline: {out_path}")

# Tickers for sparklines
index_tickers = {
    "OSEBX": "^OSEAX", "S\\&P 500": "^GSPC", "NASDAQ": "^IXIC", "DOW JONES": "^DJI"
}
fetch_and_plot(index_tickers, "Sparkline: Major Indices", "sparkline_indices.pdf")

crypto_tickers = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"
}
fetch_and_plot(crypto_tickers, "Sparkline: Crypto", "sparkline_crypto.pdf")
