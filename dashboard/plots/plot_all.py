import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_table(data_path, title, filename):
    df = pd.read_csv(data_path, sep=';').sort_values(by='1D_return')
    plt.figure(figsize=(8, 5))
    plt.barh(df["name"], df["1D_return"])
    plt.title(title)
    plt.grid(True, axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    os.makedirs("dashboard/plots", exist_ok=True)
    plt.savefig(f"dashboard/plots/{filename}")
    plt.close()

plot_table("dashboard/data/indices/major_indices.csv", "Major Indices – 1D Return", "indices_returns.pdf")
# (Add more plots here later if you want)

print("✅ All plots saved.")
