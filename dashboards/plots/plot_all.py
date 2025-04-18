import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("dashboard/plots", exist_ok=True)

def save_bar_plot(category, filename, title):
    csv_file = "major_indices.csv" if category == "indices" else f"{category}.csv"
    path = f"dashboard/data/{category}/{csv_file}"
    df = pd.read_csv(path, sep=";").sort_values(by="1D_return")

    plt.figure(figsize=(6, 4))
    plt.barh(df["name"], df["1D_return"])
    plt.title(title)
    plt.grid(True, axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    output_path = f"dashboard/plots/{filename}.png"
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Saved {category} → {output_path}")

save_bar_plot("indices", "indices_returns", "Major Indices")
save_bar_plot("commodities", "commodities_returns", "Commodities")
save_bar_plot("fixed_income", "fixed_income_returns", "Fixed Income")
save_bar_plot("crypto", "crypto_returns", "Crypto")
