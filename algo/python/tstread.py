import pandas as pd
df = pd.read_parquet("data/raw/minute/AAPL.parquet")
print(df.head())

import pandas as pd
df = pd.read_parquet("data/raw/minute/TSLA.parquet")
print(df.head())

import pandas as pd
df = pd.read_parquet("data/simulated/exec_dataset.parquet")
print(df.head())
print(df.shape)
print(df.isna().sum())