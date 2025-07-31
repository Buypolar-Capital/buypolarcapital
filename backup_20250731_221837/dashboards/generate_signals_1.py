import pandas as pd
import os

# --- Setup ---
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, 'data')
signals_dir = os.path.join(data_dir, 'signals')
os.makedirs(signals_dir, exist_ok=True)

# --- Load index data ---
indices_path = os.path.join(data_dir, 'indices', 'major_indices.csv')
df = pd.read_csv(indices_path, sep=';')

# --- Generate simple signals ---
signals = []
for _, row in df.iterrows():
    val = float(row['1D_return'])
    signal = "BUY" if val > 1 else ("SELL" if val < -1 else "HOLD")
    signals.append({
        "name": row["name"],
        "signal": signal,
        "return": val
    })

# --- Save signals ---
signals_df = pd.DataFrame(signals)
signals_df.to_csv(os.path.join(signals_dir, "signals.csv"), index=False, sep=';')
print(f"✅ Signals written to {os.path.join(signals_dir, 'signals.csv')}")
