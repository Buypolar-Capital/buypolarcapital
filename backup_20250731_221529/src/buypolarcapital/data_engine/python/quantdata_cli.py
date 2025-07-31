import argparse
from data_engine.loaders.equities_loader import load_equities
from data_engine.loaders.macro_loader import load_macro, load_google_trends

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("load", choices=["equities", "macro", "all"])
    args = parser.parse_args()

    if args.load == "equities":
        load_equities(["AAPL", "MSFT", "SPY"])
    elif args.load == "macro":
        load_macro()
        load_google_trends()
    elif args.load == "all":
        load_equities(["AAPL", "MSFT", "SPY"])
        load_macro()
        load_google_trends()

if __name__ == "__main__":
    main()