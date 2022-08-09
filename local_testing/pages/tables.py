import streamlit as st
from utils import *
from configuration import *

st.title("Raw Data Analytics")

option = st.selectbox(
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)

df = get_df(option)

# st.write("You selected:", option)
st.dataframe(df)
