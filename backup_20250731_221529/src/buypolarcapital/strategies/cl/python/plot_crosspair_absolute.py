import builtins
str = builtins.str
assert str is builtins.str, "You've overwritten the built-in 'str' function!"
import builtins
str = builtins.str
assert callable(str)


import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_crosspair_absolute(name, eu_label, us_label, data_path, output_path):
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index.tz_convert("UTC")

    MARKET_HOURS = {
        "eu": {"start": "07:00", "end": "15:25"},
        "us": {"start": "14:30", "end": "21:00"}
    }

    with PdfPages(output_path) as pdf:
        for date in sorted(set(df.index.date)):
            day = df[df.index.date == date]
            if day.empty:
                continue

            date_str = str(date)
            time_range = pd.date_range(start=f"{date} 00:00", end=f"{date} 23:55", freq="5min", tz="UTC")

            eu_abs = day.between_time(MARKET_HOURS["eu"]["start"], MARKET_HOURS["eu"]["end"])["eu"].reindex(time_range, method="ffill")
            us_abs = day.between_time(MARKET_HOURS["us"]["start"], MARKET_HOURS["us"]["end"])["us"].reindex(time_range, method="ffill")

            eu_open = pd.Timestamp(f"{date} {MARKET_HOURS['eu']['start']}", tz="UTC")
            eu_close = pd.Timestamp(f"{date} {MARKET_HOURS['eu']['end']}", tz="UTC")
            us_open = pd.Timestamp(f"{date} {MARKET_HOURS['us']['start']}", tz="UTC")
            us_close = pd.Timestamp(f"{date} {MARKET_HOURS['us']['end']}", tz="UTC")

            fig, ax = plt.subplots(figsize=(12, 4))

            ax.plot(eu_abs.index, eu_abs, label=eu_label, linewidth=1.5)
            ax.plot(us_abs.index, us_abs, label=us_label, linewidth=1.5, alpha=0.8)
            ax.set_title(f"Absolute Prices — {date_str}")
            ax.set_ylabel("Price")
            ax.legend()
            ax.axvspan(eu_open, eu_close, color="gray", alpha=0.1)
            ax.axvspan(us_open, us_close, color="blue", alpha=0.05)
            ax.set_xlabel("Time (UTC)")

            fig.autofmt_xdate()
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()
            print(f"✅ Plotted {name} — {date}")

    print(f"✅ Saved PDF to {output_path}")
