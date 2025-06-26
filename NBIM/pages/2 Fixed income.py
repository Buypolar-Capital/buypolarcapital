import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_fixed_income_data

st.set_page_config(layout="wide")
st.title("🏦 Fixed Income")

# Load data
df = load_fixed_income_data()
total_fixed_income_value = 5_253_095_232_980  # Matching the image value
countries = 49
investments = 1507
percentage = "26.6% of all investments"

# Display header info
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='margin: 0;'>Fixed income</h2>
            <p style='margin: 0;'>{total_fixed_income_value:,} NOK</p>
            <p style='margin: 0;'>{countries} countries, {investments} investments, {percentage}</p>
        </div>
        <div>
            <select style='padding: 5px;'>
                <option>Year (as at 31.12) 2024</option>
            </select>
            <select style='padding: 5px;'>
                <option>Investments in 6 regions, {countries} countries</option>
            </select>
            <select style='padding: 5px;'>
                <option>All</option>
            </select>
        </div>
    </div>
""", unsafe_allow_html=True)

# World map
country_map = {
    "Switzerland": 1, "Netherlands": 1, "United States": 1, "Italy": 1,
    "Hong Kong": 1, "Ireland": 1, "New Zealand": 1
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
        <div>
            <a href='#' style='margin-right: 10px; text-decoration: none;'>Download your selection (xls)</a>
            <a href='#' style='text-decoration: none;'>Download your selection (csv)</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Table data
data = {
    "Issuers": ["ABB Finance BV", "ABN AMRO Bank NV", "ABSC NIMS Trust", "ACEA SpA", "AGCO Corp",
                "AGCO International Holdings BV", "AHS Hospital Corp", "AIA Group Ltd", "AIB Group PLC",
                "AMCO - Asset Management Co SpA", "ANZ New Zealand Int'l Ltd"],
    "Value NOK": [993_276_580, 3_579_463_204, 9, 69_107_073, 255_496_097,
                  353_199_422, 143_162_318, 649_796_086, 2_158_518_920,
                  1_159_195_334, 1_060_977_438],
    "Sectors": ["Corporate Bonds", "Corporate Bonds/Securitized Bonds", "Securitized Bonds",
                "Government Related Bonds", "Corporate Bonds", "Corporate Bonds",
                "Corporate Bonds", "Corporate Bonds", "Corporate Bonds",
                "Government Related Bonds", "Corporate Bonds/Securitized Bonds"],
    "Incorporated in": ["Switzerland", "Netherlands", "United States", "Italy",
                        "United States", "United States", "United States",
                        "Hong Kong", "Ireland", "Italy", "New Zealand"]
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
    'Value NOK': '{:,.0f}'
}))

# Show more button
if st.button("Show 30 more +"):
    st.write("Additional data would be loaded here.")