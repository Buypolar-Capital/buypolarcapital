import yfinance as yf
import pandas as pd
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# ===========================
# EQUITIES (Top 10, 1 per country)
# ===========================
equity_csv = "data/nbim_top10_equities.csv"
if os.path.exists(equity_csv):
    print(f"✅ Equities data already exists — skipping download.")
else:
    print("🔄 Downloading equities...")

    tickers = {
        "AAPL": "Apple Inc (USA)",
        "TSM": "Taiwan Semiconductor (Taiwan)",
        "SAP.DE": "SAP SE (Germany)",
        "ASML.AS": "ASML Holding (Netherlands)",
        "NVO": "Novo Nordisk (Denmark)",
        "0700.HK": "Tencent Holdings (China)",
        "NESN.SW": "Nestlé SA (Switzerland)",
        "MC.PA": "LVMH (France)",
        "7203.T": "Toyota (Japan)",
        "005930.KS": "Samsung Electronics (South Korea)"
    }

    df_all = pd.DataFrame()

    for ticker, name in tickers.items():
        try:
            data = yf.download(ticker, period="1y", interval="1wk", progress=False)
            if data.empty or "Close" not in data:
                print(f"⚠️ No data for {name} ({ticker}) — skipping.")
                continue

            df_all[name] = data["Close"]
            print(f"✅ Retrieved: {name} ({ticker})")

        except Exception as e:
            print(f"❌ Error for {ticker}: {e}")

    df_all.index.name = "Date"
    df_all.to_csv(equity_csv)
    print(f"\n✅ Equities data saved to: {equity_csv}")

# ===========================
# FIXED INCOME PROXIES
# ===========================
bonds_csv = "data/nbim_top10_bonds.csv"
if os.path.exists(bonds_csv):
    print(f"\n✅ Fixed income data already exists — skipping download.")
else:
    print("\n🔄 Downloading fixed income proxies...")

    bond_tickers = {
        "TLT": "US Treasuries (Long-term)",
        "BNDX": "Global Bonds (ex-US)",
        "IEI": "Eurozone Bonds",
        "EMB": "Emerging Markets Bonds",
        "IGIL.L": "UK Gilts",
        "ZFL.TO": "Canada Bonds",
        "1345.T": "Japan Government Bonds",
        "AUSB": "Australia Government Bonds",
        "ESGV": "Eurozone Green Bonds (Spain/France/NL mix)",
        "EZA": "South Africa Government Bonds"
    }

    df_bonds = pd.DataFrame()

    for ticker, label in bond_tickers.items():
        try:
            data = yf.download(ticker, period="1y", interval="1wk", progress=False)
            if data.empty or "Close" not in data:
                print(f"⚠️ No bond data for {label} ({ticker}) — skipping.")
                continue

            df_bonds[label] = data["Close"]
            print(f"✅ Retrieved bond data for {label} ({ticker})")

        except Exception as e:
            print(f"❌ Error fetching {label} ({ticker}): {e}")

    df_bonds.index.name = "Date"
    df_bonds.to_csv(bonds_csv)
    print(f"\n✅ Fixed income data saved to: {bonds_csv}")
