import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

tickers = {
    "indices": {
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^DJI": "Dow Jones",
        "^FTSE": "FTSE 100",
    },
    "commodities": {
        "GC=F": "Gold",
        "CL=F": "Crude Oil",
        "SI=F": "Silver",
    },
    "crypto": {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "SOL-USD": "Solana",
    },
    "fixed_income": {
        "^TNX": "10Y US Yield",
        "^IRX": "3M US Yield",
    }
}

end_date = datetime.today()
start_date = end_date - timedelta(days=40)  # includes weekends

def save_clean_csv(df_all, asset_class):
    asset_dir = os.path.join(data_dir, asset_class)
    os.makedirs(asset_dir, exist_ok=True)
    df_all.to_csv(os.path.join(asset_dir, f"{asset_class}.csv"), sep=';', index=False)
    print(f"✅ Saved {asset_class} to {asset_class}.csv")

for asset_class, group in tickers.items():
    print(f"🔄 Downloading {asset_class}...")
    df_all = pd.DataFrame()
    for ticker, name in group.items():
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)[['Close']].reset_index()
            df = df.rename(columns={'Close': 'price'})
            df['ticker'] = name
            df['date'] = pd.to_datetime(df['Date']).dt.date
            df = df[['date', 'price', 'ticker']]
            df_all = pd.concat([df_all, df])
        except Exception as e:
            print(f"[⚠] Failed to download {ticker}: {e}")

    save_clean_csv(df_all, asset_class)
