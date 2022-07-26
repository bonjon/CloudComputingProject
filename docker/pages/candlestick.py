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
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)
option_candlestick = st.selectbox(
    "Select the graph type you want to see:",
    ["Candlestick", "OHLC"],
)

st.write("You selected:", option)

df = pd.DataFrame.from_dict(response.json()["bars"][SYMBOLS[option]])

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["t"], open=df["o"], high=df["h"], low=df["l"], close=df["c"]
        )
    ]
    if option_candlestick == "Candlestick"
    else go.Ohlc(x=df["t"], open=df["o"], high=df["h"], low=df["l"], close=df["c"])
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list(
            [
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ),
)
# update
fig.update_layout(template='plotly_dark',
                  xaxis_rangeselector_font_color='white',
                  xaxis_rangeselector_activecolor='#626efb',
                  xaxis_rangeselector_bgcolor='#262730',
                 )
st.plotly_chart(fig)
