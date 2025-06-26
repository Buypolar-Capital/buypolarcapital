import pandas as pd
import streamlit as st

@st.cache_data
def load_equity_data():
    return pd.read_csv("data/nbim_top10_equities.csv", index_col="Date", parse_dates=True)

@st.cache_data
def load_fixed_income_data():
    return pd.read_csv("data/nbim_top10_bonds.csv", index_col="Date", parse_dates=True)
