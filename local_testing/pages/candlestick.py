import streamlit as st
import plotly.graph_objects as go
from utils import *
from configuration import *

st.title("Data Analytics")

option = st.selectbox(
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)

option_candlestick = st.selectbox(
    "Select the graph type you want to see:",
    ["Candlestick", "OHLC"],
)

df = get_df(option)

# st.write("You selected:", option)

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
fig.update_layout(
    template="plotly_dark",
    xaxis_rangeselector_font_color="white",
    xaxis_rangeselector_activecolor="#626efb",
    xaxis_rangeselector_bgcolor="#262730",
)
st.plotly_chart(fig)
