import streamlit as st
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NBIM Dashboard", layout="wide")

st.image("assets/logo.svg", width=150)

# Ticker at top
start_value = 19380050014233
end_value = 19754495025174
steps = 50
duration = 5

increment = (end_value - start_value) / steps
placeholder = st.empty()

for i in range(steps + 1):
    current_value = start_value + i * increment
    placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{int(current_value):,} NOK</h1>", unsafe_allow_html=True)
    time.sleep(duration / steps)

# st.success("✅ Simulert daglig verdi ferdig animert!")
if st.button("Value development"):
    st.write("Redirect to value development page (not implemented)")

# Combined layout with stacked buttons and map
st.header("All investments")

# Reading the value of the asset classes 
df_eq = pd.read_csv("data/nbim_top10_equities.csv", index_col=0)
df_bonds = pd.read_csv("data/nbim_top10_bonds.csv", index_col=0)
df_realestate = pd.read_excel("data/nbim_top10_realestate.xlsx", index_col=0, decimal=",")
df_renewable = pd.read_excel("data/nbim_top10_renewable.xlsx", index_col=0, decimal=",")
real_estate_value = df_realestate.iloc[-1].sum()
renewable_value = df_renewable.iloc[-1].sum()
total_value = df_eq.iloc[-1].sum() + df_bonds.iloc[-1].sum() + real_estate_value + renewable_value


# --------- DYNAMIC VALUE METADATA ---------
# Equities
equity_value = df_eq.iloc[-1].sum()
equity_companies = df_eq.shape[1]
equity_countries = 10

# Fixed Income
bond_value = df_bonds.iloc[-1].sum()
bond_issuers = df_bonds.shape[1]
bond_countries = 8

# Real Estate
real_estate_value = df_realestate.iloc[-1].sum()
real_estate_properties = df_realestate.shape[1]
real_estate_countries = 5  # Based on your sample

# Renewables
renewable_value = df_renewable.iloc[-1].sum()
renewable_projects = df_renewable.shape[1]
renewable_countries = 3  # Based on your data


st.subheader("Total market value")
st.markdown(f"<h1 style='font-size:48px;'>{int(total_value):,} NOK</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

def card(link, title, value, note):
    if st.button(title, key=title):
        st.switch_page(f"pages/{link}")
    st.metric(label="Value", value=f"{value:,.0f} NOK", delta=note)

with col1:
    card("1 Equities.py", "📈 Equities", int(equity_value), f"{equity_countries} countries, {equity_companies} companies")
    card("2 Fixed income.py", "💸 Fixed income", int(bond_value), f"{bond_countries} countries, {bond_issuers} bonds")
with col2:
    card("3 Real estate.py", "🏢 Real estate", real_estate_value, f"{real_estate_countries} countries, {real_estate_properties} properties")
    card("4 Renewable energy infrastructure.py", "🌱 Renewable energy infrastructure", renewable_value, f"{renewable_countries} countries, {renewable_projects} projects")
with col3:
    country_map = {
        ".HK": "China", ".KS": "South Korea", ".T": "Japan", ".PA": "France",
        ".SW": "Switzerland", ".AS": "Netherlands", ".DE": "Germany",
        ".TO": "Canada", "NVO": "Denmark", "AAPL": "United States",
        "TSM": "Taiwan", "BNDX": "Germany", "IGIL.L": "United Kingdom",
        "ZFL.TO": "Canada", "1345.T": "Japan", "AUSB": "Australia",
        "EZA": "South Africa", "ESGV": "Spain"
    }
    df_map = pd.DataFrame({"Country": list(set(country_map.values())), "Invested": 1})
    fig = px.choropleth(df_map, locations="Country", locationmode="country names",
                        color="Invested", color_continuous_scale="Blues",
                        labels={"Invested": "Invested"})
    fig.update_layout(coloraxis_showscale=False, margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data delvis simulert for demonstrasjonsformål © Egil 2025")