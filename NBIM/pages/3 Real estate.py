import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Real Estate")

# Load data (using hardcoded total value from image)
total_real_estate_value = 363_583_276_805  # Matching the image value
countries = 14
investments = 910
percentage = "1.8% of all investments"

# Display header info
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='margin: 0;'>Real estate</h2>
            <p style='margin: 0;'>{total_real_estate_value:,} NOK</p>
            <p style='margin: 0;'>{countries} countries, {investments} investments, {percentage}</p>
        </div>
        <div>
            <select style='padding: 5px;'>
                <option>Year (as at 31.12) 2024</option>
            </select>
            <select style='padding: 5px;'>
                <option>Investments in 3 regions, {countries} countries</option>
            </select>
            <select style='padding: 5px;'>
                <option>All</option>
            </select>
        </div>
    </div>
""", unsafe_allow_html=True)

# World map
country_map = {
    "France": 1, "Germany": 1, "United States": 1
}
df_map = pd.DataFrame({
    "Country": list(set(country_map.keys())),  # Unique countries
    "Invested": [1] * len(set(country_map.keys()))  # Same length as countries, all 1
})
fig_map = px.choropleth(df_map, locations="Country", locationmode="country names",
                        color="Invested", color_continuous_scale="Blues",
                        labels={"Invested": "Invested"}, title="",
                        height=300)
fig_map.update_layout(coloraxis_showscale=False, margin={"r": 0, "t": 30, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)

# Search and download section
st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
        <input type='text' placeholder='Search for company' style='padding: 5px; width: 200px;'>
    </div>
""", unsafe_allow_html=True)

# Table data (based on the image)
data = {
    "Partners": [
        "AXA", "AXA", "Alexandria Real Estate and MetLife", "Boston Properties", "AXA"
    ],
    "Properties": [
        "Victor Hugo, 28-32 Avenue Victor Hugo, 75016, Paris, France",
        "Kranzler Eck Berlin, Kurfürstendamm 19-24, 10719, Berlin, Germany",
        "50-60 Binney Street, 02142, Cambridge, United States",
        "73-89 Oxford Street & 1 Dean Street, W1D 3RB, London, United Kingdom",
        "Bahnhofstrasse 1, 8001, Zurich, Switzerland"
    ],
    "Ownership": [50.00, 50.00, 41.00, 45.00, 45.00],
    "Sectors": ["Office"] * 5,
    "Countries": ["France", "Germany", "United States", "United Kingdom", "Switzerland"]
}
df_all = pd.DataFrame(data)

# -------- Search and Filter --------
search_query = st.text_input("Search for company", "")
filtered_df = df_all[df_all["Properties"].str.contains(search_query, case=False, na=False) |
                     df_all["Partners"].str.contains(search_query, case=False, na=False)]

# -------- Show first 3, then rest --------
default_rows = 3
show_all = st.session_state.get("show_all", False)

if not show_all:
    df_display = filtered_df.head(default_rows)
else:
    df_display = filtered_df

# -------- Table display (NBIM-style tweaks) --------
st.markdown("""
    <style>
        .stDataFrame tbody td {
            font-size: 14px;
            padding: 6px 8px;
        }
        .stDataFrame thead tr th {
            background-color: #f2f2f2;
            font-weight: 600;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.dataframe(
    df_display.style.format({
        'Ownership': '{:.2f}%'
    }),
    use_container_width=True
)

# -------- Show more button --------
if len(filtered_df) > default_rows and not show_all:
    if st.button("Show 2 more +"):
        st.session_state.show_all = True