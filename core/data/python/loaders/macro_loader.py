import pandas as pd
from fredapi import Fred
from pytrends.request import TrendReq
from ..utils.config import FRED_API_KEY, DATA_PATH

fred = Fred(api_key=FRED_API_KEY)

def load_macro():
    series = {
        "CPI_US": "CPIAUCSL",
        "GDP_US": "GDP",
        "FEDFUNDS": "FEDFUNDS"
    }
    df = pd.DataFrame()
    for name, code in series.items():
        ts = fred.get_series(code)
        df[name] = ts
    df.index.name = "date"
    df.reset_index().to_parquet(DATA_PATH / "macro" / "fred.parquet", index=False)
    print("[✔] Saved FRED macro data")

def load_google_trends():
    pytrends = TrendReq()
    pytrends.build_payload(["inflation", "recession"], timeframe="today 5-y")
    df = pytrends.interest_over_time()
    df.reset_index().to_parquet(DATA_PATH / "macro" / "google_trends.parquet", index=False)
    print("[✔] Saved Google Trends data")