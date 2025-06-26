import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("⚡ Renewable Energy Infrastructure")

# Load data (using hardcoded total value from image)
total_renewable_value = 25_347_713_861  # Matching the image value
countries = 4
investments = 7
percentage = "0.1% of all investments"

# Display header info
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='margin: 0;'>Renewable energy infrastructure</h2>
            <p style='margin: 0;'>{total_renewable_value:,} NOK</p>
            <p style='margin: 0;'>{countries} countries, {investments} investments, {percentage}</p>
        </div>
        <div>
            <select style='padding: 5px;'>
                <option>Year (as at 31.12) 2024</option>
            </select>
            <select style='padding: 5px;'>
                <option>Investments in Europe, {countries} countries</option>
            </select>
            <select style='padding: 5px;'>
                <option>All</option>
            </select>
        </div>
    </div>
""", unsafe_allow_html=True)

# World map
country_map = {
    "Germany": 1, "Spain": 1, "Netherlands": 1, "United Kingdom": 1
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

# Table data (based on the image)
data = {
    "Partners": ["Copenhagen Infrastructure Partners", "EnBW, Allianz Capital Partners and AIP Management",
                 "Iberdrola"],
    "Projects": ["Copenhagen Infrastructure V", "He Dreiht, Germany", "Peñarrubia, Spain"],
    "Ownership": [9.00, 16.63, 49.00],
    "Sectors": ["Multi-sector fund", "Wind", "Solar"],
    "Countries": ["International", "Germany", "Spain"]
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
    'Ownership': '{:.2f}%'
}))

# Show more button
if st.button("Show 30 more +"):
    st.write("Additional data would be loaded here.")

# Historic investments section
st.subheader("Historic investments infrastructure")
st.write("30")  # Placeholder for historic data count