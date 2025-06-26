import streamlit as st
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NBIM Dashboard", layout="wide")
st.image("assets/logo.png", width=150)

# === Load data ===
df_eq = pd.read_csv("data/nbim_top10_equities.csv", index_col=0, parse_dates=True)
df_bonds = pd.read_csv("data/nbim_top10_bonds.csv", index_col=0, parse_dates=True)
df_realestate = pd.read_excel("data/nbim_top10_realestate.xlsx", index_col=0, parse_dates=True, decimal=",")
df_renewable = pd.read_excel("data/nbim_top10_renewable.xlsx", index_col=0, parse_dates=True, decimal=",")

# === Build dynamic portfolio value timeseries ===
portfolio = df_eq.add(df_bonds, fill_value=0).add(df_realestate, fill_value=0).add(df_renewable, fill_value=0)
start_date = pd.Timestamp("2025-04-23")
end_date = portfolio.index[-1]

start_value = portfolio.loc[start_date].sum()
end_value = portfolio.loc[end_date].sum()

# === Animate ticker ===
steps = 50
duration = 5
increment = (end_value - start_value) / steps
placeholder = st.empty()

for i in range(steps + 1):
    current_value = start_value + i * increment
    placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 80px;'>{int(current_value):,} NOK</h1>",
        unsafe_allow_html=True
    )
    time.sleep(duration / steps)

if st.button("Refresh"):
    st.write("")

# === Metadata values (dynamically computed) ===
latest_eq = df_eq.iloc[-1].dropna()
latest_bonds = df_bonds.iloc[-1].dropna()
latest_realestate = df_realestate.iloc[-1].dropna()
latest_renewable = df_renewable.iloc[-1].dropna()

equity_value = latest_eq.sum()
bond_value = latest_bonds.sum()
real_estate_value = latest_realestate.sum()
renewable_value = latest_renewable.sum()

equity_companies = len(latest_eq)
bond_issuers = len(latest_bonds)
real_estate_properties = len(latest_realestate)
renewable_projects = len(latest_renewable)

# Optional: replace with dynamic detection if desired
equity_countries = 10
bond_countries = 8
real_estate_countries = 5
renewable_countries = 3

# === Total portfolio value
total_value = equity_value + bond_value + real_estate_value + renewable_value

# === Category percentages
equity_pct = 100 * equity_value / total_value
bond_pct = 100 * bond_value / total_value
real_estate_pct = 100 * real_estate_value / total_value
renewable_pct = 100 * renewable_value / total_value

# === Dashboard content ===
st.header("All investments")
st.markdown(f"<h1 style='font-size:64px;color:#001538;'>{int(total_value):,} NOK</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([.25, .25, 1])

def card(link, title, value, note):
    st.markdown(f"<h5 style='margin-bottom: 0.2rem; bold; '>{title}</h5>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 20px; color: #001538; font-weight: bold; margin: 0;'>{value:,.0f} NOK</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #001538; font-size: 13px; margin-top: 0;'>{note}</p>", unsafe_allow_html=True)
    if st.button("Open", key=title):
        st.switch_page(f"pages/{link}")

with col1:
    card("1 Equities.py", "Equities", int(equity_value), f"{equity_countries} countries, {equity_companies} companies, {equity_pct:.1f}%")
    card("2 Fixed income.py", "Fixed income", int(bond_value), f"{bond_countries} countries, {bond_issuers} bonds, {bond_pct:.1f}%")
with col2:
    card("3 Real estate.py", "Real estate", int(real_estate_value), f"{real_estate_countries} countries, {real_estate_properties} properties, {real_estate_pct:.1f}%")
    card("4 Renewable energy infrastructure.py", "Renewable", int(renewable_value), f"{renewable_countries} countries, {renewable_projects} projects, {renewable_pct:.1f}%")
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
    fig.update_layout(coloraxis_showscale=False, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)






# === Historic investments chart ===
st.markdown("---")
st.header("Historic investments")

# 1. Build and clean stacked DataFrame
stacked_df = pd.DataFrame({
    "Equities": df_eq.sum(axis=1),
    "Fixed income": df_bonds.sum(axis=1),
    "Real estate": df_realestate.sum(axis=1),
    "Renewable": df_renewable.sum(axis=1)
}).dropna()

# 2. Take last 10 days and format index for categorical x-axis
stacked_df = stacked_df.tail(10).copy()
stacked_df["Date"] = stacked_df.index.strftime("%b %d")  # e.g. "Jun 25"
stacked_df["Total market value"] = stacked_df[["Equities", "Fixed income", "Real estate", "Renewable"]].sum(axis=1)

# 3. Define stacking order and color palette
stack_order = ["Equities", "Fixed income", "Real estate", "Renewable"]
color_map = {
    "Equities": "#001538",
    "Fixed income": "#bfc3c9",
    "Real estate": "#0026ff",
    "Renewable": "#d65218"
}

# 4. Plot stacked bar chart
fig_bar = px.bar(
    stacked_df,
    x="Date",
    y=stack_order,
    labels={"value": "Value (NOK)", "variable": "Asset class"},
    color_discrete_map=color_map,
    height=500
)

# 5. Add total market value as a line plot
fig_line = px.line(
    stacked_df,
    x="Date",
    y="Total market value"
)
for trace in fig_line.data:
    trace.name = "Total value"
    trace.line.color = "black"
    trace.line.width = 2
    fig_bar.add_trace(trace)

# 6. Update layout for compact look
fig_bar.update_layout(
    barmode="stack",
    legend_title="",
    xaxis_title="Date",
    yaxis_title="Value (NOK)",
    xaxis_type="category",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=500
)

st.plotly_chart(fig_bar, use_container_width=True)

# === Footer ===
st.markdown("---")
st.caption("Egil Furnes 2025")