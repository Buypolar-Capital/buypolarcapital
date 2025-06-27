import os
import pandas as pd

@st.cache_data
def load_fixed_income_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "nbim_top10_bonds.csv")
    return pd.read_csv(data_path, index_col="Date", parse_dates=True)

@st.cache_data
def load_equity_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "nbim_top10_equities.csv")
    return pd.read_csv(data_path, index_col=0, parse_dates=True)

@st.cache_data
def load_real_estate_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "nbim_top10_realestate.xlsx")
    return pd.read_excel(data_path, index_col=0, parse_dates=True, decimal=",")

@st.cache_data
def load_renewable_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "nbim_top10_renewable.xlsx")
    return pd.read_excel(data_path, index_col=0, parse_dates=True, decimal=",")
