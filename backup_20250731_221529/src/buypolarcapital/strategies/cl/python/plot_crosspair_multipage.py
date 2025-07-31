import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

def generate_plots():
    try:
        # Define paths
        BASE_DIR = os.path.dirname(__file__)
        DATA_PATH = os.path.join(BASE_DIR, "data", "crosspair_intraday.csv")
        PLOT_PATH = os.path.join(BASE_DIR, "plots", "crosspair_leapfrog_fullrange.pdf")

        # Create plots directory if it doesn't exist
        os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)

        # Load and prepare data
        df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
        if df.empty:
            raise ValueError("Loaded data is empty")
        
        # Debug: Print column names
        print("Debug: CSV column names:", df.columns.tolist())
        
        # Rename columns to expected 'eu' and 'us' regardless of input
        if len(df.columns) != 2:
            raise ValueError(f"Expected 2 columns, found {len(df.columns)}")
        df.columns = ["eu", "us"]  # Force rename to match expected names
        print("Debug: Renamed columns to:", df.columns.tolist())

        # Ensure UTC timezone
        df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index.tz_convert("UTC")

        # Normalize prices by day
        def normalize_day(x):
            x_clean = x.dropna()
            return x / x_clean.iloc[0] if not x_clean.empty else pd.Series(index=x.index, dtype=float)

        df["eu_norm"] = df.groupby(df.index.date)["eu"].transform(normalize_day)
        df["us_norm"] = df.groupby(df.index.date)["us"].transform(normalize_day)

        # Market hours (UTC)
        MARKET_HOURS = {
            "eu": {"start": "07:00", "end": "15:25", "label": "Schibsted (SCHA.OL)"},
            "us": {"start": "14:30", "end": "21:00", "label": "Apple (AAPL)"}
        }

        # Generate PDF
        with PdfPages(PLOT_PATH) as pdf:
            unique_dates = sorted(set(df.index.date))
            print(f"Generating plots for {len(unique_dates)} days...")
            
            for date in unique_dates:
                try:
                    day = df[df.index.date == date]
                    if day.empty or day["eu_norm"].isna().all() or day["us_norm"].isna().all():
                        print(f"Skipping {date}: No valid data")
                        continue

                    # Create full day range
                    full_range = pd.date_range(
                        start=f"{date} 00:00",
                        end=f"{date} 23:55",
                        freq="5min",
                        tz="UTC"
                    )
                    
                    # Filter market hours and reindex
                    eu = day.between_time(
                        MARKET_HOURS["eu"]["start"],
                        MARKET_HOURS["eu"]["end"]
                    )["eu_norm"].reindex(full_range, method="ffill")
                    us = day.between_time(
                        MARKET_HOURS["us"]["start"],
                        MARKET_HOURS["us"]["end"]
                    )["us_norm"].reindex(full_range, method="ffill")

                    # Plot
                    plt.figure(figsize=(15, 7))
                    plt.plot(eu.index, eu, 
                            label=MARKET_HOURS["eu"]["label"], 
                            linewidth=2, 
                            color="#2ecc71")
                    plt.plot(us.index, us, 
                            label=MARKET_HOURS["us"]["label"], 
                            linewidth=2, 
                            color="#e74c3c", 
                            alpha=0.8)

                    plt.title(f"Cross-Market Leapfrogging — {date}", 
                            fontsize=16, 
                            pad=15)
                    plt.xlabel("Time (UTC)", fontsize=12)
                    plt.ylabel("Normalized Price (Day Start = 1.0)", fontsize=12)
                    plt.ylim(0.95, 1.05)
                    plt.xticks(rotation=45, ha="right")
                    plt.grid(True, linestyle="--", alpha=0.4, which="both")
                    
                    # Add vertical spans for market hours
                    plt.axvspan(
                        pd.Timestamp(f"{date} {MARKET_HOURS['eu']['start']} UTC"),
                        pd.Timestamp(f"{date} {MARKET_HOURS['eu']['end']} UTC"),
                        color="green", alpha=0.1, label="EU Market Hours"
                    )
                    plt.axvspan(
                        pd.Timestamp(f"{date} {MARKET_HOURS['us']['start']} UTC"),
                        pd.Timestamp(f"{date} {MARKET_HOURS['us']['end']} UTC"),
                        color="red", alpha=0.1, label="US Market Hours"
                    )

                    plt.legend(loc="best", fontsize=10)
                    plt.tight_layout()
                    
                    pdf.savefig(dpi=150)
                    plt.close()
                    print(f"Plotted {date}")
                    
                except Exception as e:
                    print(f"Warning: Failed to plot {date}: {str(e)}")
                    continue

        print(f"✅ Saved full-range multi-day plot to: {PLOT_PATH}")

    except FileNotFoundError:
        print(f"Error: Could not find data file at {DATA_PATH}")
    except Exception as e:
        print(f"Error: Failed to generate plots: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_plots()