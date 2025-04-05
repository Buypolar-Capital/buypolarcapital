import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

class VWAPExecutionDataset:
    def __init__(self, ticker="AAPL", days_back=30, interval="1m"):
        self.ticker = ticker
        self.interval = interval
        self.end = datetime.today().date() - timedelta(days=1)  # Yesterday
        self.start = self.end - timedelta(days=days_back - 1)   # 30 days back
        print(f"Dataset range: {self.start} to {self.end}")

        self.raw_df = self._load_data()
        self.daily_sessions = self._split_into_daily_sessions()

    def _load_data(self):
        print(f"Fetching {self.ticker} 1-minute data from {self.start} to {self.end} in chunks...")
        start = pd.to_datetime(self.start)
        end = pd.to_datetime(self.end)
        all_data = []

        chunk_size = pd.Timedelta(days=7)
        current = start

        while current < end:
            chunk_end = min(current + chunk_size, end)
            print(f" → {current.date()} to {chunk_end.date()}")

            try:
                df_chunk = yf.download(
                    self.ticker,
                    start=current.strftime("%Y-%m-%d"),
                    end=(chunk_end + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
                    interval=self.interval,
                    progress=False,
                    prepost=False
                )
                if not df_chunk.empty:
                    df_chunk = df_chunk.reset_index()
                    all_data.append(df_chunk)
            except Exception as e:
                print(f"  ❌ Failed for {current.date()} - {e}")

            current = chunk_end + pd.Timedelta(days=1)

        if not all_data:
            raise ValueError("No data downloaded.")

        df = pd.concat(all_data).dropna().reset_index(drop=True)
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        return df

    def _split_into_daily_sessions(self):
        df = self.raw_df.copy()
        df["Date"] = df["Datetime"].dt.date

        daily_sessions = []
        unique_days = sorted(df["Date"].unique())

        for i, day in enumerate(unique_days):
            day_df = df[df["Date"] == day].copy()
            if len(day_df) < 200:  # Skip incomplete days
                continue

            # Time-based features
            day_df["elapsed_minutes"] = ((day_df["Datetime"] - day_df["Datetime"].iloc[0]).dt.total_seconds() // 60).astype(int)
            day_df["minute_of_day"] = day_df["elapsed_minutes"]
            day_df["log_price"] = np.log(day_df["Close"])
            day_df["return"] = day_df["Close"].pct_change().fillna(0)
            day_df["volatility"] = day_df["return"].rolling(20).std().fillna(0)
            day_df["normalized_volume"] = day_df["Volume"] / day_df["Volume"].rolling(20).mean().fillna(1)

            # VWAP calculation
            day_df["cum_volume"] = day_df["Volume"].cumsum()
            day_df["cum_pv"] = (day_df["Close"] * day_df["Volume"]).cumsum()
            day_df["vwap"] = day_df["cum_pv"] / day_df["cum_volume"]

            # Execution direction
            execution_side = "buy" if i % 2 == 0 else "sell"
            day_df["side"] = execution_side

            # Features and targets
            features = day_df[[
                "log_price", "return", "volatility", "normalized_volume", "minute_of_day"
            ]].copy()

            session = {
                "date": day,
                "side": execution_side,
                "features": features.reset_index(drop=True),
                "price_series": day_df["Close"].reset_index(drop=True),
                "vwap": day_df["vwap"].iloc[-1],
                "volume": day_df["Volume"].reset_index(drop=True)
            }
            daily_sessions.append(session)

        return daily_sessions

    def get_train_test_split(self, train_days=24, test_days=5):
        train_start = pd.to_datetime(self.start)
        train_end = train_start + pd.Timedelta(days=train_days - 1)
        test_start = train_end + pd.Timedelta(days=1)
        test_end = pd.to_datetime(self.end)

        train = [s for s in self.daily_sessions if train_start <= pd.to_datetime(s["date"]) <= train_end]
        test = [s for s in self.daily_sessions if test_start <= pd.to_datetime(s["date"]) <= test_end]
        return train, test