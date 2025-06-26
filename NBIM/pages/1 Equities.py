import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_equity_data

# === Settings ===
st.set_page_config(layout="wide")
st.title("Equities")

# === Load data ===
df_eq = load_equity_data()
latest = df_eq.iloc[-1].dropna()
total_equity_value = latest.sum()
equity_companies = len(latest)
equity_countries = 10  # Update dynamically if possible

# === Estimate total investments to calculate %
total_portfolio_value = total_equity_value / 0.714
equity_pct = 100 * total_equity_value / total_portfolio_value

# === Header ===
st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem;'>
    <div>
        <h2 style='margin-bottom: 0.2rem;'>Equities</h2>
        <p style='margin: 0; font-weight: bold; font-size: 18px; color: #001538;'>{int(total_equity_value):,} NOK</p>
        <p style='margin: 0; color: gray;'>{equity_countries} countries, {equity_companies} companies, 96.5% of total</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === Map view (still static for now) ===
country_map = {
    "United States": 1, "Taiwan": 1, "Germany": 1, "Netherlands": 1, "Denmark": 1,
    "China": 1, "Switzerland": 1, "France": 1, "Japan": 1, "South Korea": 1
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

# === Top holdings (dynamic + search + show more) ===
st.markdown("### Top holdings")
st.markdown("<hr style='margin-top: -1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

# Hardcoded metadata for selected tickers
equity_meta = {
    "Apple Inc (USA)": {"Sector": "Technology", "Country": "United States"},
    "Taiwan Semiconductor (Taiwan)": {"Sector": "Technology", "Country": "Taiwan"},
    "SAP SE (Germany)": {"Sector": "Technology", "Country": "Germany"},
    "ASML Holding (Netherlands)": {"Sector": "Technology", "Country": "Netherlands"},
    "Novo Nordisk (Denmark)": {"Sector": "Health Care", "Country": "Denmark"},
    "Tencent Holdings (China)": {"Sector": "Communication Services", "Country": "China"},
    "Nestlé SA (Switzerland)": {"Sector": "Consumer Staples", "Country": "Switzerland"},
    "LVMH (France)": {"Sector": "Consumer Discretionary", "Country": "France"},
    "Toyota (Japan)": {"Sector": "Consumer Discretionary", "Country": "Japan"},
    "Samsung Electronics (South Korea)": {"Sector": "Technology", "Country": "South Korea"}
}

# Extract latest non-null prices from last row
latest_row = df_eq.iloc[-1].dropna()
latest_row_sorted = latest_row.sort_values(ascending=False)

# Build dataframe dynamically
table_data = []
for company, price in latest_row_sorted.items():
    meta = equity_meta.get(company, {})
    table_data.append({
        "Company": company,
        "Value (NOK)": price,
        "Sector": meta.get("Sector", "Unknown"),
        "Country": meta.get("Country", "Unknown")
    })

df_table = pd.DataFrame(table_data)

# === Search bar ===
search_query = st.text_input("Search company", value="", placeholder="🔍 e.g. Apple")
if search_query:
    df_table = df_table[df_table["Company"].str.lower().str.contains(search_query.lower())]

# === Show top 5 initially ===
show_all = st.session_state.get("show_all", False)
if not show_all:
    df_display = df_table.head(5)
else:
    df_display = df_table

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
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', '#001538'),
                ('color', 'white'),
                ('text-align', 'left'),
                ('padding', '8px')
            ]}
        ])
        .format({'Value (NOK)': '{:,.2f}'})
)

# === Show more toggle ===
if not show_all and st.button("Show 5 more +"):
    st.session_state["show_all"] = True
elif show_all and st.button("Show less –"):
    st.session_state["show_all"] = False


# === Historic development ===
st.markdown("### Historic development")

# Compute total equity values
historic_df = df_eq.copy().dropna().tail(10)
historic_df["Total"] = df_eq.sum(axis=1).dropna().tail(10)
historic_df["Date_str"] = historic_df.index.strftime("%b %d")

# Compute y-range
ymin = historic_df["Total"].min() * 0.95
ymax = historic_df["Total"].max() * 1.05

# Plot bar chart
fig = px.bar(
    historic_df,
    x="Date_str",
    y="Total",
    color_discrete_sequence=["#001538"],
    labels={"Total": "Value (NOK)", "Date_str": "Date"},
    height=400
)

fig.update_layout(
    yaxis_range=[ymin, ymax],
    xaxis_title="Date",
    yaxis_title="Value (NOK)",
    xaxis_type="category",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


# === Footer ===
st.markdown("---")
st.caption("Egil Furnes 2025")
