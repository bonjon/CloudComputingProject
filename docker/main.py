import subprocess
import sys
import requests


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install("streamlit")

import streamlit as st
import pandas as pd
import plotly.express as px


API_KEY = "PKG95PV0R6DI0C2G522P"
API_SECRET = "knWqSpYCGrkQopBig8K4dIWYNASADqzcjgalRx8O"
BASE_URL = "https://data.alpaca.markets/"
parameters = {
    "start": "2021-10-01T0:00:00Z",
    "timeframe": "1Day",
    "symbols": "AAPL,TSLA,AMZN,META,NFLX",
    "adjustment": "raw",
}
headers = {"Apca-Api-Key-Id": API_KEY, "Apca-Api-Secret-Key": API_SECRET}
response = requests.get(
    url=BASE_URL + "v2/stocks/bars?", headers=headers, params=parameters
)
st.title("Data Analytics")

SYMBOLS = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Meta": "META",
    "Netflix": "NFLX",
}

option = st.selectbox(
    "Select the Company Stock that you want to see",
    (SYMBOLS.keys()),
)

st.write("You selected:", option)

df = pd.DataFrame.from_dict(response.json()["bars"][SYMBOLS[option]])
fig = px.line(df, x="t", y="c", title=str(option) + " Stock")
fig.update_xaxes(type="category")
st.plotly_chart(fig)
