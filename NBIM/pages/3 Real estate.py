import streamlit as st

st.set_page_config(layout="wide")
st.title("🏢 Real Estate Investments")

st.markdown("NBIM holds high-quality real estate assets across key global cities. Here's a snapshot of selected properties:")

# Hardcoded assets
assets = [
    {
        "city": "London",
        "country": "UK",
        "value": "85,000,000,000 NOK",
        "type": "Office complex in Mayfair",
        "image": "assets/real_estate_london.jpg"
    },
    {
        "city": "Paris",
        "country": "France",
        "value": "72,000,000,000 NOK",
        "type": "Retail & office space near Champs-Élysées",
        "image": "assets/real_estate_paris.jpg"
    },
    {
        "city": "New York",
        "country": "USA",
        "value": "91,000,000,000 NOK",
        "type": "Premium commercial building near Central Park",
        "image": "assets/real_estate_nyc.jpg"
    }
]

# Display layout
cols = st.columns(3)

for col, asset in zip(cols, assets):
    with col:
        st.image(asset["image"], use_column_width=True, caption=f'{asset["city"]}, {asset["country"]}')
        st.subheader(asset["type"])
        st.metric(label="Value", value=asset["value"])
