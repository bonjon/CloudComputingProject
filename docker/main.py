import subprocess
import sys
import requests


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install("streamlit")
install("plotly")
install("streamlit-aggrid")

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
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)

st.write("You selected:", option)

df = pd.DataFrame.from_dict(response.json()["bars"][SYMBOLS[option]])
fig = px.line(df, x="t", y="c", title=str(option) + " Stock")
# fig.update_xaxes(type="category")
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
# to hide the weeends and holidays
""" fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
        dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
    ]
) """
st.plotly_chart(fig)

max_closing_price = df["c"].max()
st.metric(f"Highest Close price for {option}: ", round(max_closing_price, 4))

max_date = df[df["c"] == max_closing_price]["t"].values[0]
st.metric(f"Highest Close Price for {option} was observed on: ", max_date)

min_closing_price = df["c"].min()
st.metric(f"Lowest Close price for {option}: ", round(min_closing_price, 4))

min_date = df[df["c"] == min_closing_price]["t"].values[0]
st.metric(f"Lowest Close Price for {option} was observed on: ", min_date)
