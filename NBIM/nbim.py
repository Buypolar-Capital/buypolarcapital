import streamlit as st
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NBIM Dashboard", layout="wide")

# -------------------------------
# Logo + Title
# -------------------------------
col1, col2 = st.columns([1, 8])
with col1:
    st.image("assets/logo.svg", width=500)
with col2:
    st.markdown("### Norges Bank Investment Management")
    st.caption("For future generations")

st.markdown("---")
st.title("🇳🇴 Oljefondets oversikt")
st.caption("Simulert sanntidsverdi og aktivaklasser — bygget med Streamlit")

# -------------------------------
# Simulert ticker (based on daily change)
# -------------------------------
start_value = 19300000000000  # From 2 days ago
end_value = 19368837985983    # From yesterday
steps = 50
duration = 5  # seconds

increment = (end_value - start_value) / steps
placeholder = st.empty()

for i in range(steps + 1):
    current_value = start_value + i * increment
    formatted = f"{int(current_value):,}".replace(",", " ")
    placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 60px;'>{formatted} NOK</h1>",
        unsafe_allow_html=True
    )
    time.sleep(duration / steps)

st.success("✅ Simulert daglig verdi ferdig animert!")

# -------------------------------
# Aktivaklasse-fordeling (mock)
# -------------------------------
st.subheader("📊 Fordeling etter aktivaklasse")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Aksjer", "12 000 mrd NOK", "62%")
col2.metric("Renter", "6 000 mrd NOK", "31%")
col3.metric("Eiendom", "1 000 mrd NOK", "5%")
col4.metric("Fornybar infrastruktur", "400 mrd NOK", "2%")

# Optional pie chart
show_pie = st.checkbox("Vis kakediagram")
if show_pie:
    df_pie = pd.DataFrame({
        "Kategori": ["Aksjer", "Renter", "Eiendom", "Fornybar"],
        "Verdi": [12000, 6000, 1000, 400]
    })
    fig = px.pie(df_pie, names="Kategori", values="Verdi", title="Fordeling av fondets verdi (mrd NOK)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -------------------------------
# ALL INVESTMENTS SECTION
# -------------------------------
st.header("All investments")

# Load local data
df_eq = pd.read_csv("data/nbim_top10_equities.csv", index_col=0)
df_bonds = pd.read_csv("data/nbim_top10_bonds.csv", index_col=0)

real_estate_value = 363_583_276_805
renewable_value = 25_347_713_861
total_value = df_eq.iloc[-1].sum() + df_bonds.iloc[-1].sum() + real_estate_value + renewable_value

st.subheader("💰 Total market value")
st.markdown(f"<h1 style='font-size:48px;'>{int(total_value):,} NOK</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
col3, col4 = st.columns([1, 1])

def card(link, title, value, note):
    if st.button(title, key=title):
        st.switch_page(f"pages/{link}")
    st.metric(label="Value", value=f"{value:,.0f} NOK", delta=note)

with col1:
    card("1 Equities.py", "📈 Equities", int(df_eq.iloc[-1].sum()), "63 countries, 8659 companies")
with col2:
    card("2 Fixed income.py", "💸 Fixed income", int(df_bonds.iloc[-1].sum()), "49 countries, 1507 bonds")
with col3:
    card("3 Real estate.py", "🏢 Real estate", real_estate_value, "14 countries, 910 properties")
with col4:
    card("4 Renewable energy infrastructure.py", "🌱 Renewable energy infrastructure", renewable_value, "4 countries, 7 projects")

# -------------------------------
# 🌍 Map of invested countries
# -------------------------------
st.subheader("🌍 Countries with investments")

country_map = {
    ".HK": "China", ".KS": "South Korea", ".T": "Japan", ".PA": "France",
    ".SW": "Switzerland", ".AS": "Netherlands", ".DE": "Germany",
    ".TO": "Canada", "NVO": "Denmark", "AAPL": "United States",
    "TSM": "Taiwan", "BNDX": "Germany", "IGIL.L": "United Kingdom",
    "ZFL.TO": "Canada", "1345.T": "Japan", "AUSB": "Australia",
    "EZA": "South Africa", "ESGV": "Spain"
}
seen_countries = set(country_map.values())
df_map = pd.DataFrame({"Country": list(seen_countries), "Invested": 1})
fig = px.choropleth(df_map, locations="Country", locationmode="country names",
                    color="Invested", color_continuous_scale="Blues",
                    labels={"Invested": "Invested"},
                    title="Countries with Investments")
fig.update_layout(coloraxis_showscale=False, margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data delvis simulert for demonstrasjonsformål © Egil 2025")
