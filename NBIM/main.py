import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.title("Norges Bank Investment Management")
st.write("hello world")
st.text_input("favourite model?")
x = st.text_input("favourite movie?")
st.write(f"your favourite movie is: {x}")

is_clicked = st.button("Click Me")
st.write('## This is a H2 Title!')







