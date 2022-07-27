import streamlit as st
from utils import *
from configuration import *

bucket = get_bucket()

st.title("Data Analytics")

option = st.selectbox(
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)

df = get_df(bucket, option)

# st.write("You selected:", option)
st.dataframe(df)
