# run_crosspair_modular.py
import os
from fetch_crosspair_modular import fetch_crosspair_data
from plot_crosspair_modular import plot_crosspair_leapfrog

PAIRS = [
    {
        "name": "schibsted_vs_aapl",
        "eu_ticker": "SCHA.OL",
        "us_ticker": "AAPL",
        "eu_label": "Schibsted (SCHA.OL)",
        "us_label": "Apple (AAPL)"
    },
    {
        "name": "sap_vs_sap",
        "eu_ticker": "SAP.DE",
        "us_ticker": "SAP",
        "eu_label": "SAP (Germany)",
        "us_label": "SAP (US)"
    },
    {
        "name": "astrazeneca_vs_azn",
        "eu_ticker": "AZN.L",
        "us_ticker": "AZN",
        "eu_label": "AstraZeneca (London)",
        "us_label": "AstraZeneca (NYSE)"
    },
    {
        "name": "siemens_vs_siegy",
        "eu_ticker": "SIE.DE",
        "us_ticker": "SIEGY",
        "eu_label": "Siemens (XETRA)",
        "us_label": "Siemens (OTC)"
    },
    {
        "name": "nestle_vs_nsgry",
        "eu_ticker": "NESN.SW",
        "us_ticker": "NSRGY",
        "eu_label": "Nestlé (SIX)",
        "us_label": "Nestlé (OTC)"
    }
]

for pair in PAIRS:
    print(f"\n🚀 Running: {pair['name']}")
    try:
        df = fetch_crosspair_data(
            name=pair["name"],
            eu_ticker=pair["eu_ticker"],
            us_ticker=pair["us_ticker"]
        )

        if df is not None:
            plot_crosspair_leapfrog(
                name=pair["name"],
                eu_label=pair["eu_label"],
                us_label=pair["us_label"]
            )
        else:
            print(f"⚠️ Skipping plot due to data fetch issue.")

    except Exception as e:
        print(f"❌ Failed {pair['name']}: {e}")
