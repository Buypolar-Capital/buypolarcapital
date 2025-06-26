import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_fixed_income_data

# === Settings ===
st.set_page_config(layout="wide")
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
        <p style='margin: 0; color: gray;'>{bond_countries} countries, {bond_issuers} issuers, {bond_pct:.1f}% of total</p>
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
    "ABB Finance BV": {"Sector": "Corporate Bonds", "Country": "Switzerland"},
    "ABN AMRO Bank NV": {"Sector": "Corporate/Securitized", "Country": "Netherlands"},
    "AGCO Corp": {"Sector": "Corporate Bonds", "Country": "United States"},
    "AIA Group Ltd": {"Sector": "Corporate Bonds", "Country": "Hong Kong"},
    "AIB Group PLC": {"Sector": "Corporate Bonds", "Country": "Ireland"}
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

# === Historic development chart ===
st.markdown("### Historic development")

historic_df = pd.DataFrame({
    "Fixed income": df_bonds.sum(axis=1)
}).dropna().tail(10)
historic_df["Date"] = historic_df.index.strftime("%b %d")
historic_df["Total"] = historic_df["Fixed income"]

fig_bar = px.bar(
    historic_df,
    x="Date",
    y="Fixed income",
    color_discrete_sequence=["#001538"],
    labels={"Fixed income": "Value (NOK)", "Date": "Date"},
    height=400
)

fig_line = px.line(
    historic_df,
    x="Date",
    y="Total"
)
for trace in fig_line.data:
    trace.name = "Total"
    trace.line.color = "#d65218"
    trace.line.width = 2
    fig_bar.add_trace(trace)

fig_bar.update_layout(
    barmode="stack",
    legend_title="",
    xaxis_title="Date",
    yaxis_title="Value (NOK)",
    xaxis_type="category",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_bar, use_container_width=True)

# === Footer ===
st.markdown("---")
st.caption("Egil Furnes 2025")
