import os
import shutil
from fetch_crosspair_data import download_stock_data
from plot_crosspair_multipage import generate_plots

# Define crosslisted pairs
PAIRS = [
    {
        "name": "schibsted_vs_aapl",
        "eu_ticker": "SCHA.OL",
        "us_ticker": "AAPL"
    },
    {
        "name": "sap_vs_sap",
        "eu_ticker": "SAP.DE",
        "us_ticker": "SAP"
    },
    {
        "name": "astrazeneca_vs_azn",
        "eu_ticker": "AZN.L",
        "us_ticker": "AZN"
    },
    {
        "name": "siemens_vs_siegy",
        "eu_ticker": "SIE.DE",
        "us_ticker": "SIEGY"
    },
    {
        "name": "nestle_vs_nsgry",
        "eu_ticker": "NESN.SW",
        "us_ticker": "NSRGY"
    }
]

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

# Run for each pair
for pair in PAIRS:
    print(f"\n🚀 Starting pair: {pair['name']}")
    
    # Update tickers and name in fetch script dynamically
    fetch_script_path = os.path.join(BASE_DIR, "fetch_crosspair_data.py")
    with open(fetch_script_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace(
        '"SCHA.OL"', f'"{pair["eu_ticker"]}"'
    ).replace(
        '"AAPL"', f'"{pair["us_ticker"]}"'
    ).replace(
        '"schibsted_vs_aapl"', f'"{pair["name"]}"'
    )

    with open(fetch_script_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Fetch and plot
    df = download_stock_data()
    if df is not None:
        generate_plots()

        # Move and rename output files
        output_plot = os.path.join(PLOTS_DIR, "crosspair_leapfrog_fullrange.pdf")
        renamed_plot = os.path.join(PLOTS_DIR, f"{pair['name']}_leapfrog.pdf")

        if os.path.exists(output_plot):
            shutil.move(output_plot, renamed_plot)
            print(f"✅ Saved plot as {renamed_plot}")
        else:
            print("❌ Expected plot not found!")

    else:
        print(f"⚠️ Skipping plot for {pair['name']} due to download issues.")
