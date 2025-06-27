import streamlit as st
import pandas as pd
import plotly.express as px
import os

# === Settings ===
st.set_page_config(layout="wide")
st.image(os.path.join(os.path.dirname(__file__), "../assets/logo.png"), width=150)
st.title("Renewable Energy Infrastructure")

# === Load data ===
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "nbim_top10_renewable.xlsx")
df_renewable = pd.read_excel(data_path, index_col=0, parse_dates=True, decimal=",")
latest = df_renewable.iloc[-1].dropna()
total_renewable_value = latest.sum()
renewable_projects = len(latest)
renewable_countries = 3  # Adjust if dynamic metadata available

# === Estimate total portfolio value to calculate share
total_portfolio_value = st.session_state.get("total_value", total_renewable_value / 0.001)
renewable_pct = 100 * total_renewable_value / total_portfolio_value

# === Header ===
st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem;'>
    <div>
        <h2 style='margin-bottom: 0.2rem;'>Renewable energy infrastructure</h2>
        <p style='margin: 0; font-weight: bold; font-size: 18px; color: #001538;'>{int(total_renewable_value):,} NOK</p>
        <p style='margin: 0; color: gray;'>{renewable_countries} countries, {renewable_projects} projects, {renewable_pct:.1f}% of total</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === Map view ===
country_map = {
    "Germany": 1, "Spain": 1, "Netherlands": 1, "United Kingdom": 1
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

# === Top projects (metadata) ===
st.markdown("### Top projects")
st.markdown("<hr style='margin-top: -1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

project_meta = {
    "Copenhagen Infrastructure V": {
        "Partner": "Copenhagen Infrastructure Partners", "Sector": "Multi-sector fund", "Country": "International", "Ownership (%)": 9.00
    },
    "He Dreiht, Germany": {
        "Partner": "EnBW, Allianz Capital Partners, AIP", "Sector": "Wind", "Country": "Germany", "Ownership (%)": 16.63
    },
    "Peñarrubia, Spain": {
        "Partner": "Iberdrola", "Sector": "Solar", "Country": "Spain", "Ownership (%)": 49.00
    }
}
# Build DataFrame
table_data = []
for project, meta in project_meta.items():
    table_data.append({
        "Project": project,
        "Partner": meta["Partner"],
        "Ownership (%)": meta["Ownership (%)"],
        "Sector": meta["Sector"],
        "Country": meta["Country"]
    })
df_table = pd.DataFrame(table_data)

# === Search bar ===
search_query = st.text_input("Search project or partner", value="", placeholder="🔍 e.g. Iberdrola")
if search_query:
    df_table = df_table[df_table["Project"].str.lower().str.contains(search_query.lower()) |
                        df_table["Partner"].str.lower().str.contains(search_query.lower())]

# === Show top 2 first ===
show_all = st.session_state.get("show_all_renewable", False)
df_display = df_table if show_all else df_table.head(2)

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
        .format({'Ownership (%)': '{:.2f}%'})
)

# === Show more toggle
if len(df_table) > 2:
    if not show_all and st.button("Show 1 more +", key="more_renewable"):
        st.session_state["show_all_renewable"] = True
    elif show_all and st.button("Show less –", key="less_renewable"):
        st.session_state["show_all_renewable"] = False

# === Historic development ===
st.markdown("### Historic development")

# Prepare total series
historic_df = pd.DataFrame({
    "Renewable": df_renewable.sum(axis=1)
}).dropna().tail(10)
historic_df["Date"] = historic_df.index.strftime("%b %d")

# Dynamic y-axis
ymin = historic_df["Renewable"].min() * 0.95
ymax = historic_df["Renewable"].max() * 1.05

# Bar chart (total only)
fig_bar = px.bar(
    historic_df,
    x="Date",
    y="Renewable",
    color_discrete_sequence=["#001538"],
    labels={"Renewable": "Value (NOK)", "Date": "Date"},
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
