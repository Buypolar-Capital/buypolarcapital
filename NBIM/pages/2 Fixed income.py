import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_fixed_income_data
import os 

# === Settings ===
st.set_page_config(layout="wide")
st.image(os.path.join(os.path.dirname(__file__), "../assets/logo.png"), width=150)
st.title("Fixed income")

# === Load data ===
df_bonds = load_fixed_income_data()
latest = df_bonds.iloc[-1].dropna()
total_bond_value = latest.sum()
bond_issuers = len(latest)
bond_countries = 10  # Optional: make dynamic if country metadata is available

# === Estimate total portfolio to calculate share
total_portfolio_value = total_bond_value / 0.266
bond_pct = 100 * total_bond_value / total_portfolio_value

# === Header ===
st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem;'>
    <div>
        <h2 style='margin-bottom: 0.2rem;'>Fixed income</h2>
        <p style='margin: 0; font-weight: bold; font-size: 18px; color: #001538;'>{int(total_bond_value):,} NOK</p>
        <p style='margin: 0; color: gray;'>{bond_countries} countries, {bond_issuers} issuers, 3.5% of total</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === Map view ===
country_map = {
    "Switzerland": 1, "Netherlands": 1, "United States": 1, "Italy": 1,
    "Hong Kong": 1, "Ireland": 1, "New Zealand": 1, "France": 1, "Germany": 1, "Australia": 1
}
df_map = pd.DataFrame({"Country": list(country_map.keys()), "Invested": list(country_map.values())})
fig_map = px.choropleth(
    df_map,
    locations="Country",
    locationmode="country names",
    color="Invested",
    color_continuous_scale="Blues",
    height=400
)
fig_map.update_layout(coloraxis_showscale=False, margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)

# === Top issuers (dynamic + search + show more) ===
st.markdown("### Top issuers")
st.markdown("<hr style='margin-top: -1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

# Example issuer metadata (static)
issuer_meta = {
    "Japan Government Bonds": {"Sector": "Government Bonds", "Country": "Japan"},
    "UK Gilts": {"Sector": "Government Bonds", "Country": "United Kingdom"},
    "Eurozone Bonds": {"Sector": "Government Bonds", "Country": "Eurozone"},
    "Emerging Markets Bonds": {"Sector": "Government Bonds", "Country": "Emerging Markets"},
    "US Treasuries (Long-term)": {"Sector": "Government Bonds", "Country": "United States"},
    "Global Bonds (ex-US)": {"Sector": "Government Bonds", "Country": "Global ex-US"},
    "Canada Bonds": {"Sector": "Government Bonds", "Country": "Canada"}
}


# Build table dynamically
latest_row = df_bonds.iloc[-1].dropna().sort_values(ascending=False)
table_data = []
for issuer, value in latest_row.items():
    meta = issuer_meta.get(issuer, {})
    table_data.append({
        "Issuer": issuer,
        "Value (NOK)": value,
        "Sector": meta.get("Sector", "Unknown"),
        "Country": meta.get("Country", "Unknown")
    })
df_table = pd.DataFrame(table_data)

# === Search + filter
search_query = st.text_input("Search issuer", value="", placeholder="🔍 e.g. ABB")
if search_query:
    df_table = df_table[df_table["Issuer"].str.lower().str.contains(search_query.lower())]

# === Show top 5 first ===
show_all = st.session_state.get("show_all_bonds", False)
df_display = df_table if show_all else df_table.head(5)

# === Display table ===
st.dataframe(
    df_display.style
        .hide(axis="index")
        .set_properties(**{
            "text-align": "left",
            "font-size": "14px",
            "border": "1px solid #eee",
            "padding": "8px",
            "background-color": "white"
        })
        .set_table_styles([{
            'selector': 'th', 'props': [
                ('background-color', '#001538'),
                ('color', 'white'),
                ('text-align', 'left'),
                ('padding', '8px')
            ]
        }])
        .format({'Value (NOK)': '{:,.2f}'})
)

# === Show more toggle
if not show_all and st.button("Show 5 more +", key="more_bonds"):
    st.session_state["show_all_bonds"] = True
elif show_all and st.button("Show less –", key="less_bonds"):
    st.session_state["show_all_bonds"] = False

# === Historic development ===
st.markdown("### Historic development")

# Prepare time series
historic_df = pd.DataFrame({
    "Fixed income": df_bonds.sum(axis=1)
}).dropna().tail(10)
historic_df["Date"] = historic_df.index.strftime("%b %d")

# Compute y-axis range with padding
ymin = historic_df["Fixed income"].min() * 0.95
ymax = historic_df["Fixed income"].max() * 1.05

# Create bar chart
fig_bar = px.bar(
    historic_df,
    x="Date",
    y="Fixed income",
    color_discrete_sequence=["#001538"],
    labels={"Fixed income": "Value (NOK)", "Date": "Date"},
    height=400
)

fig_bar.update_layout(
    yaxis_range=[ymin, ymax],
    xaxis_title="Date",
    yaxis_title="Value (NOK)",
    xaxis_type="category",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False
)

st.plotly_chart(fig_bar, use_container_width=True)


# === Footer ===
st.markdown("---")
st.caption("Egil Furnes 2025")
