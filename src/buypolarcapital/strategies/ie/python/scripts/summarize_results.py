import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Paths
BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data" / "processed" / "features_2010_2022.csv"
MODEL_PATH = BASE_PATH / "models" / "xgboost_osebx_model.json"
FEATURES_PATH = BASE_PATH / "models" / "features.txt"
PLOT_PATH = BASE_PATH / "plots"
PLOT_PATH.mkdir(parents=True, exist_ok=True)

# Load data and model
df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
with open(FEATURES_PATH) as f:
    feature_names = [line.strip() for line in f.readlines()]
X = df[feature_names]
y = df["included"] if "included" in df.columns else pd.Series([0]*len(df))

model = XGBClassifier()
model.load_model(MODEL_PATH)

# Predict and evaluate
df["prediction"] = model.predict(X)
report_dict = classification_report(y, df["prediction"], output_dict=True, zero_division=0)
report_df = pd.DataFrame(report_dict).transpose()

# Safe backtest summary
try:
    df["log_return"] = (1 + df["return_60d"]).apply(lambda x: pd.NA if x <= 0 else pd.np.log(x))
    daily_perf = df[df["prediction"] == 1].groupby("Date")["log_return"].mean()
    daily_perf = daily_perf.dropna()
    cumulative = daily_perf.cumsum().apply(lambda x: pd.np.exp(x))

    start_date = daily_perf.index.min()
    end_date = daily_perf.index.max()

    summary_data = {
        "Start Date": start_date.strftime("%Y-%m-%d") if pd.notnull(start_date) else "N/A",
        "End Date": end_date.strftime("%Y-%m-%d") if pd.notnull(end_date) else "N/A",
        "Backtest Days": len(daily_perf),
        "Total Return": cumulative.iloc[-1] if len(cumulative) > 0 else "N/A",
        "Average Daily Return": daily_perf.mean() if len(daily_perf) > 0 else "N/A",
    }
except Exception as e:
    summary_data = {
        "Start Date": "N/A",
        "End Date": "N/A",
        "Backtest Days": 0,
        "Total Return": "N/A",
        "Average Daily Return": "N/A",
    }

# Plot summary to PDF
fig, axes = plt.subplots(2, 1, figsize=(8.5, 11))

# Table 1: Classification report
sns.heatmap(report_df.iloc[:-1, :-1], annot=True, fmt=".2f", cmap="Blues", ax=axes[0])
axes[0].set_title("Classification Report")

# Table 2: Strategy metrics
axes[1].axis("off")
table_data = [[k, str(v)] for k, v in summary_data.items()]
table = axes[1].table(cellText=table_data, colLabels=["Metric", "Value"], loc="center")
table.auto_set_font_size(False)
table.set_fontsize(10)
axes[1].set_title("Backtest Summary", fontweight="bold")

# Save to PDF
pdf_path = PLOT_PATH / "summary_model_and_backtest.pdf"
plt.tight_layout()
plt.savefig(pdf_path)
print(f"Summary PDF saved to: {pdf_path}")
