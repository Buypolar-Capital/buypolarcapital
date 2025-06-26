import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_equity_data

st.set_page_config(layout="wide")
st.title("📈 Equities")

# Load data
df = load_equity_data()
total_equity_value = 14_112_924_028_100  # Matching the image value
countries = 63
investments = 8659
percentage = "71.4% of all investments"

# Display header info
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='margin: 0;'>Equities</h2>
            <p style='margin: 0;'>{total_equity_value:,} NOK</p>
            <p style='margin: 0;'>{countries} countries, {investments} investments, {percentage}</p>
        </div>
        <div>
            <select style='padding: 5px;'>
                <option>Year (as at 31.12) 2024</option>
            </select>
            <select style='padding: 5px;'>
                <option>Investments in 7 regions, {countries} countries</option>
            </select>
            <select style='padding: 5px;'>
                <option>All</option>
            </select>
        </div>
    </div>
""", unsafe_allow_html=True)

# World map
country_map = {
    "United States": 1, "Taiwan": 1, "Germany": 1, "Netherlands": 1, "Denmark": 1,
    "China": 1, "Switzerland": 1, "France": 1, "Japan": 1, "South Korea": 1
}
df_map = pd.DataFrame({"Country": list(country_map.keys()), "Invested": list(country_map.values())})
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
        <div>
            <a href='#' style='margin-right: 10px; text-decoration: none;'>Download your selection (xls)</a>
            <a href='#' style='text-decoration: none;'>Download your selection (csv)</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Table data
data = {
    "Companies": ["Apple Inc", "Microsoft Corp", "NVIDIA Corp", "Alphabet Inc", "Amazon.com Inc",
                  "Meta Platforms Inc", "Broadcom Inc", "Taiwan Semiconductor Manufacturing Co Ltd",
                  "Tesla Inc", "Berkshire Hathaway Inc", "Eli Lilly & Co"],
    "Value NOK": [5_242_795_616, 4_96_984_325_033, 4_88_069_750_932, 3_32_448_846_184,
                  3_06_413_500_828, 2_24_313_687_214, 1_89_807_727_430, 1_74_541_226_808,
                  1_61_402_245_046, 1_07_027_642_241, 94_036_231_136],
    "Sectors": ["Technology", "Technology", "Technology", "Technology", "Consumer Discretionary",
                "Technology", "Technology", "Technology", "Consumer Discretionary", "Financials",
                "Health Care"],
    "Ownership": [1.22, 1.40, 1.31, 1.26, 1.17, 1.34, 1.54, 1.80, 1.10, 0.49, 1.13],
    "Country": ["United States", "United States", "United States", "United States", "United States",
                "United States", "United States", "Taiwan", "United States", "United States", "United States"]
}
df_table = pd.DataFrame(data)

# Display table
st.dataframe(df_table.style.set_properties(**{
    'text-align': 'left',
    'font-size': '14px',
    'border': '1px solid #ddd',
    'padding': '8px'
}).set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('text-align', 'left'), ('padding', '8px')]},
    {'selector': 'td', 'props': [('padding', '8px')]}
]).format({
    'Value NOK': '{:,.0f}',
    'Ownership': '{:.2f}%'
}))

# Show more button
if st.button("Show 30 more +"):
    st.write("Additional data would be loaded here.")