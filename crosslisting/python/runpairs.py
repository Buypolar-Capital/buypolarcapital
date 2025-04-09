import os
from fetch import fetch_and_save_data
from plotprice import plot_price_data

PAIRS = [
    {"name": "schibsted_vs_aapl", "eu_ticker": "SCHA.OL", "us_ticker": "AAPL", "eu_label": "Schibsted (SCHA.OL)", "us_label": "Apple (AAPL)"},
    {"name": "sap_vs_sap", "eu_ticker": "SAP.DE", "us_ticker": "SAP", "eu_label": "SAP (Germany)", "us_label": "SAP (US)"},
    {"name": "astrazeneca_vs_azn", "eu_ticker": "AZN.L", "us_ticker": "AZN", "eu_label": "AstraZeneca (LSE)", "us_label": "AstraZeneca (NYSE)"},
    {"name": "siemens_vs_siegy", "eu_ticker": "SIE.DE", "us_ticker": "SIEGY", "eu_label": "Siemens (Germany)", "us_label": "Siemens (US ADR)"},
    {"name": "nestle_vs_nsgry", "eu_ticker": "NESN.SW", "us_ticker": "NSRGY", "eu_label": "Nestlé (SIX)", "us_label": "Nestlé (ADR)"},
    {"name": "novartis_vs_nvs", "eu_ticker": "NOVN.SW", "us_ticker": "NVS", "eu_label": "Novartis (SIX)", "us_label": "Novartis (NYSE)"},
    {"name": "unilever_vs_ul", "eu_ticker": "ULVR.L", "us_ticker": "UL", "eu_label": "Unilever (LSE)", "us_label": "Unilever (NYSE)"},
]

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

for pair in PAIRS:
    print(f"\n🚀 Running: {pair['name']}")
    csv_path = fetch_and_save_data(pair)
    if csv_path is not None:
        output_path = os.path.join(PLOTS_DIR, f"{pair['name']}_price_data.pdf")
        try:
            plot_price_data(
                pair['name'],
                pair['eu_label'],
                pair['us_label'],
                data_path=csv_path,
                output_path=output_path
            )
        except Exception as e:
            print(f"❌ Failed plotting {pair['name']}: {e}")
