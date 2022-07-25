import subprocess
import sys
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["t"], open=df["o"], high=df["h"], low=df["l"], close=df["c"]
        )
    ]
)
fig.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig)
