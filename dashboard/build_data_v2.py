import os
import yfinance as yf
import pandas as pd

# --- Setup paths ---
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "data")

categories = {
    "indices": ['SPY', 'QQQ', 'DIA', 'VTI', 'EFA'],  # Replacing ^GSPC etc with ETF proxies
    "commodities": ['GLD', 'SLV', 'USO', 'DBA', 'UNG'],
    "crypto": ['BTC-USD', 'ETH-USD', 'SOL-USD', 'DOGE-USD', 'XRP-USD'],
    "fixed_income": ['TLT', 'IEF', 'BND', 'SHY', 'LQD']
}

os.makedirs(data_dir, exist_ok=True)

# --- Helpers ---
def download_and_clean(tickers):
    df = yf.download(tickers, period="7d", interval="1d", auto_adjust=False, progress=False)
    results = []

    for ticker in tickers:
        try:
            closes = df['Close'][ticker] if isinstance(df.columns, pd.MultiIndex) else df['Close']
            closes = closes.dropna()
            if len(closes) < 2:
                print(f"[⚠] Skipping {ticker} — not enough valid data.")
                continue
            today_val = closes.iloc[-1]
            yesterday_val = closes.iloc[-2]
            change_pct = (today_val / yesterday_val - 1) * 100

            results.append({
                "name": ticker,
                "1D_return": f"{change_pct:.2f}%"
            })

        except Exception as e:
            print(f"[⚠] Skipping {ticker} — {e}")
            continue

    return pd.DataFrame(results)


def download_history(tickers):
    df = yf.download(tickers, period="30d", interval="1d", auto_adjust=True, progress=False)
    try:
        if isinstance(df.columns, pd.MultiIndex):
            df = df['Close']
    except Exception:
        pass
    df = df.reset_index().melt(id_vars='Date', var_name='ticker', value_name='price')
    df = df.dropna()
    df = df.rename(columns={"Date": "date"})
    return df


# --- Main Loop: Save 1D return & history ---
for group, tickers in categories.items():
    print(f"🔄 Downloading {group}...")
    try:
        daily_df = download_and_clean(tickers)
        if not daily_df.empty:
            group_path = os.path.join(data_dir, group)
            os.makedirs(group_path, exist_ok=True)
            daily_path = os.path.join(group_path, f"{group}.csv")
            daily_df.to_csv(daily_path, index=False, sep=';')
            print(f"✅ Saved {group} to {os.path.basename(daily_path)}")
        else:
            print(f"[❌] No valid data found for {group} — skipping file.")
    except Exception as e:
        print(f"[‼️] Unexpected error for {group}: {e}")

    print(f"📈 Saving 30-day history for {group}...")
    try:
        hist_df = download_history(tickers)
        if not hist_df.empty:
            history_path = os.path.join(data_dir, group, f"{group}_history.csv")
            hist_df.to_csv(history_path, index=False)
            print(f"✅ Saved historical {group}")
        else:
            print(f"[⚠] No historical data for {group}")
    except Exception as e:
        print(f"[⚠] Could not download history for {group}: {e}")
