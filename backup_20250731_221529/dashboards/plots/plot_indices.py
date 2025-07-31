import pandas as pd
import matplotlib.pyplot as plt
import os

data = pd.read_csv("dashboard/data/indices/major_indices.csv", sep=';')
data.sort_values(by='1D_return', inplace=True)

plt.figure(figsize=(8, 5))
plt.barh(data["name"], data["1D_return"])
plt.title("Major Indices – 1D Return (%)")
plt.tight_layout()

os.makedirs("dashboard/plots", exist_ok=True)
plt.savefig("dashboard/plots/indices_returns.pdf")
print("✅ Plot saved to dashboard/plots/indices_returns.pdf")
