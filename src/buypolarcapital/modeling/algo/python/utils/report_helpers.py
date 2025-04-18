import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import skew, kurtosis


def create_model_comparison_report(results_list, save_path="reports/model_comparison.pdf"):
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    import pandas as pd
    import os

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    rows = []
    for item in results_list:
        row = {"Ticker": item["ticker"], "Strategy": item["strategy"]}
        row.update(item["metrics"])  # Unpack metrics dict
        rows.append(row)

    df = pd.DataFrame(rows)

    with PdfPages(save_path) as pdf:
        # Page 1: Table of metrics
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis("off")
        table = ax.table(cellText=df.values, colLabels=df.columns, loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 2)
        plt.title("Model Comparison Report", fontsize=14)
        pdf.savefig()
        plt.close()

        # Page 2+: Bar plots for each metric
        metric_mapping = {
            "avg_slip": "Average Slippage",
            "sharpe": "Sharpe Ratio",
            "hit_ratio": "VWAP Win %"
        }

        for col_key, display_name in metric_mapping.items():
            if col_key not in df.columns:
                print(f"⚠️ Skipping plot for missing metric: {col_key}")
                continue
            pivot = df.pivot(index="Ticker", columns="Strategy", values=col_key)
            pivot.plot(kind="bar", figsize=(10, 6), title=display_name)
            plt.ylabel(display_name)
            plt.xticks(rotation=45)
            plt.tight_layout()
            pdf.savefig()
            plt.close()


    print(f"\n✅ Saved model comparison report to {save_path}")
