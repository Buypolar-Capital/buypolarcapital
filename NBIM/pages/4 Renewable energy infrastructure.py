import streamlit as st

st.set_page_config(layout="wide")
st.title("⚡ Renewable Energy Infrastructure")

st.markdown("NBIM has begun investing in select renewable energy infrastructure projects across Europe and North America.")

# Hardcoded projects
projects = [
    {
        "name": "Borssele 1 & 2 Offshore Wind Farm",
        "location": "Netherlands",
        "type": "Offshore Wind",
        "value": "14,200,000,000 NOK",
        "icon": "🌊🌀"
    },
    {
        "name": "Ocotillo Solar Facility",
        "location": "California, USA",
        "type": "Solar PV",
        "value": "6,800,000,000 NOK",
        "icon": "☀️🔋"
    },
    {
        "name": "Nysäter Wind Park",
        "location": "Sweden",
        "type": "Onshore Wind",
        "value": "4,500,000,000 NOK",
        "icon": "🌬️🌲"
    }
]

# Display in 3 columns
cols = st.columns(3)
for col, project in zip(cols, projects):
    with col:
        st.markdown(f"### {project['icon']} {project['name']}")
        st.markdown(f"**Location:** {project['location']}")
        st.markdown(f"**Type:** {project['type']}")
        st.metric(label="Investment Value", value=project["value"])
