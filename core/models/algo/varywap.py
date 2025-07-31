
from data.vwap_dataset import VWAPExecutionDataset

dataset = VWAPExecutionDataset("AAPL", interval="1m", period="5d")
X, y = dataset[0]

print("Sample X:", X)
print("Sample y:", y)
