import streamlit as st
import pandas as pd
import plotly.express as px

# === Settings ===
st.set_page_config(layout="wide")
st.image("assets/logo.png", width=150)
st.title("Real estate")

# === Load data ===
df_realestate = pd.read_excel("data/nbim_top10_realestate.xlsx", index_col=0, parse_dates=True, decimal=",")
latest = df_realestate.iloc[-1].dropna()
total_real_estate_value = latest.sum()
real_estate_properties = len(latest)
real_estate_countries = 5  # Adjust if desired

# === Estimate total portfolio value to calculate %
total_portfolio_value = st.session_state.get("total_value", total_real_estate_value / 0.018)
real_estate_pct = 100 * total_real_estate_value / total_portfolio_value

# === Header ===
st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem;'>
    <div>
        <h2 style='margin-bottom: 0.2rem;'>Real estate</h2>
        <p style='margin: 0; font-weight: bold; font-size: 18px; color: #001538;'>{int(total_real_estate_value):,} NOK</p>
        <p style='margin: 0; color: gray;'>{real_estate_countries} countries, {real_estate_properties} properties, 0.0% of total</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === Map view ===
country_map = {
    "France": 1, "Germany": 1, "United States": 1, "United Kingdom": 1, "Switzerland": 1
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

# === Top properties (static metadata) ===
st.markdown("### Top properties")
st.markdown("<hr style='margin-top: -1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

property_meta = {
    "Victor Hugo, 28-32 Avenue Victor Hugo, 75016, Paris, France": {"Partner": "AXA", "Sector": "Office", "Country": "France", "Ownership (%)": 50.00},
    "Kranzler Eck Berlin, Kurfürstendamm 19-24, 10719, Berlin, Germany": {"Partner": "AXA", "Sector": "Office", "Country": "Germany", "Ownership (%)": 50.00},
    "50-60 Binney Street, 02142, Cambridge, United States": {"Partner": "Alexandria & MetLife", "Sector": "Office", "Country": "United States", "Ownership (%)": 41.00},
    "73-89 Oxford Street & 1 Dean Street, W1D 3RB, London, United Kingdom": {"Partner": "Boston Properties", "Sector": "Office", "Country": "United Kingdom", "Ownership (%)": 45.00},
    "Bahnhofstrasse 1, 8001, Zurich, Switzerland": {"Partner": "AXA", "Sector": "Office", "Country": "Switzerland", "Ownership (%)": 45.00}
}

# Build DataFrame
table_data = []
for prop, meta in property_meta.items():
    table_data.append({
        "Property": prop,
        "Partner": meta["Partner"],
        "Ownership (%)": meta["Ownership (%)"],
        "Sector": meta["Sector"],
        "Country": meta["Country"]
    })
df_table = pd.DataFrame(table_data)

# === Search bar ===
search_query = st.text_input("Search property or partner", value="", placeholder="🔍 e.g. AXA or Paris")
if search_query:
    df_table = df_table[df_table["Property"].str.lower().str.contains(search_query.lower()) |
                        df_table["Partner"].str.lower().str.contains(search_query.lower())]

# === Show top 3 first ===
show_all = st.session_state.get("show_all_realestate", False)
df_display = df_table if show_all else df_table.head(3)

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
if len(df_table) > 3:
    if not show_all and st.button("Show 2 more +", key="more_realestate"):
        st.session_state["show_all_realestate"] = True
    elif show_all and st.button("Show less –", key="less_realestate"):
        st.session_state["show_all_realestate"] = False

# === Historic development ===
st.markdown("### Historic development")

# Prepare totals
historic_df = pd.DataFrame({
    "Real estate": df_realestate.sum(axis=1)
}).dropna().tail(10)
historic_df["Date"] = historic_df.index.strftime("%b %d")

# Dynamic y-axis range
ymin = historic_df["Real estate"].min() * 0.95
ymax = historic_df["Real estate"].max() * 1.05

# Bar chart of total real estate
fig_bar = px.bar(
    historic_df,
    x="Date",
    y="Real estate",
    color_discrete_sequence=["#001538"],
    labels={"Real estate": "Value (NOK)", "Date": "Date"},
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
