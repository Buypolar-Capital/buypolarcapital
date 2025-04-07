import yfinance as yf
import pandas as pd
import os

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "data")
summary_dir = os.path.join(data_dir, "summary")
os.makedirs(summary_dir, exist_ok=True)

def save_returns(ticker_dict, label, subfolder):
    tickers = list(ticker_dict.values())
    df = yf.download(tickers, period="7d", auto_adjust=True)["Close"]
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    returns = ((latest - prev) / prev * 100).round(2)
    df_out = pd.DataFrame({
        "name": list(ticker_dict.keys()),
        "ticker": list(ticker_dict.values()),
        "1D_return": returns.values
    })
    os.makedirs(os.path.join(data_dir, subfolder), exist_ok=True)
    df_out.to_csv(os.path.join(data_dir, subfolder, f"{label}.csv"), index=False, sep=";")

# --- Indices ---
index_tickers = {
    "OSEBX": "OSEBX.OL",  # Oslo Børs Benchmark Index ETF (or choose a better proxy)
    "S&P 500": "^GSPC",
    "NASDAQ": "QQQ",       # Use QQQ ETF instead of ^IXIC
    "DOW JONES": "DIA",    # Use DIA ETF instead of ^DJI
    "MSCI World": "URTH",
    "Emerging Mkts": "EEM",
    "CSI 300": "ASHR",
    "Bitcoin": "BTC-USD"
}

save_returns(index_tickers, "major_indices", "indices")

# --- Commodities ---
commodity_tickers = {
    "Brent Oil": "BZ=F",
    "Gold": "GC=F",
    "Copper": "HG=F",
    "Natural Gas": "NG=F"
}
save_returns(commodity_tickers, "commodities", "commodities")

# --- Fixed Income (ETF proxies) ---
fi_tickers = {
    "US 10Y": "IEF",
    "US 2Y": "SHY",
    "German 10Y": "BWX",
    "Norwegian Bonds": "GOVT"
}
save_returns(fi_tickers, "fixed_income", "fixed_income")

# --- Crypto ---
crypto_tickers = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD"
}
save_returns(crypto_tickers, "crypto", "crypto")

# --- Summary Output ---
summary_df = pd.DataFrame([{
    "date": pd.Timestamp.today().date(),
    "num_indices": len(index_tickers),
    "num_commodities": len(commodity_tickers),
    "num_fixed_income": len(fi_tickers),
    "num_crypto": len(crypto_tickers),
    "commentary": "Markets tracked across all major asset classes. Customize with LLMs later."
}])
summary_df.to_csv(os.path.join(summary_dir, "summary.csv"), index=False, sep=";")

print("✅ All market data downloaded and saved.")
