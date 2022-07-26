import requests
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


def get_data():
    for sym, items in sorted(response.json()["bars"].items()):
        for item in items:
            item.update({"s": sym})
            yield item


df = pd.DataFrame.from_dict([elem for elem in get_data()])

fig = px.line(df, x="t", y="c", color="s", title="Comparing Stock")
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
fig.update_layout(
    template="plotly_dark",
    xaxis_rangeselector_font_color="white",
    xaxis_rangeselector_activecolor="#626efb",
    xaxis_rangeselector_bgcolor="#262730",
)

st.plotly_chart(fig)
