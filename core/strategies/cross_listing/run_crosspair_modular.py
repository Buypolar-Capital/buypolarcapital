# run_crosspair_modular.py
import os
from fetch_crosspair_modular import fetch_crosspair_data
from plot_crosspair_modular import plot_crosspair_leapfrog

PAIRS = [
    {"name": "schibsted_vs_aapl", "eu_ticker": "SCHA.OL", "us_ticker": "AAPL", "eu_label": "Schibsted", "us_label": "Apple"},
    {"name": "sap_vs_sap", "eu_ticker": "SAP.DE", "us_ticker": "SAP", "eu_label": "SAP (DE)", "us_label": "SAP (NYSE)"},
    {"name": "astrazeneca_vs_azn", "eu_ticker": "AZN.L", "us_ticker": "AZN", "eu_label": "AstraZeneca (LSE)", "us_label": "AstraZeneca (NASDAQ)"},
    {"name": "siemens_vs_siegy", "eu_ticker": "SIE.DE", "us_ticker": "SIEGY", "eu_label": "Siemens (XETRA)", "us_label": "Siemens (OTC)"},
    {"name": "nestle_vs_nsgry", "eu_ticker": "NESN.SW", "us_ticker": "NSRGY", "eu_label": "Nestlé (SWX)", "us_label": "Nestlé (ADR)"},
    {"name": "novartis_vs_nvs", "eu_ticker": "NOVN.SW", "us_ticker": "NVS", "eu_label": "Novartis (SWX)", "us_label": "Novartis (NYSE)"},
    {"name": "unilever_vs_ul", "eu_ticker": "ULVR.L", "us_ticker": "UL", "eu_label": "Unilever (LSE)", "us_label": "Unilever (NYSE)"}
]


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

for pair in PAIRS:
    print(f"\n🚀 Running: {pair['name']}")

    try:
        data_path = os.path.join(DATA_DIR, f"{pair['name']}_intraday.csv")
        output_path = os.path.join(PLOTS_DIR, f"{pair['name']}_leapfrog.pdf")

        df = fetch_crosspair_data(pair["name"], pair["eu_ticker"], pair["us_ticker"], data_path)

        if df is not None:
            plot_crosspair_leapfrog(
                name=pair["name"],
                data_path=data_path,
                output_path=output_path,
                eu_label=pair["eu_label"],
                us_label=pair["us_label"]
            )
        else:
            print(f"⚠️ Skipping {pair['name']} due to download error.")

    except Exception as e:
        print(f"❌ Failed {pair['name']}: {e}")