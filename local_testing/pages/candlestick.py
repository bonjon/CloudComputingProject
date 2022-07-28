import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

ema_1 = st.slider(
    "Days of calculation for the 1st exponential moving average",
    min_value=1,
    max_value=200,
    value=12,
    format="%d",
    key="first_moving",
)
ema_2 = st.slider(
    "Days of calculation for the 2nd exponential moving average",
    min_value=1,
    max_value=200,
    value=26,
    format="%d",
    key="second_moving",
)
# st.write("You selected:", option)

df = get_df(option)

df["ema_1"] = df["c"].ewm(span=ema_1).mean()
df["ema_2"] = df["c"].ewm(span=ema_2).mean()
df["macd"] = df["ema_1"] - df["ema_2"]

# st.write("You selected:", option)
fig = make_subplots(
    vertical_spacing=0, rows=3, cols=1, row_heights=[0.7, 0.15, 0.15], shared_xaxes=True
)
fig.add_trace(
    go.Candlestick(x=df["t"], open=df["o"], high=df["h"], low=df["l"], close=df["c"])
    if option_candlestick == "Candlestick"
    else go.Ohlc(x=df["t"], open=df["o"], high=df["h"], low=df["l"], close=df["c"])
)
fig.add_trace(go.Scatter(x=df["t"], y=df["ema_1"]), row=1, col=1)
fig.add_trace(go.Scatter(x=df["t"], y=df["ema_2"]), row=1, col=1)
fig.add_trace(go.Bar(x=df["t"], y=df["macd"]), row=2, col=1)
fig.add_trace(go.Bar(x=df["t"], y=df["v"]), row=3, col=1)

fig.update_xaxes(
    rangeslider_visible=False,
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
    showline=True,
    linewidth=1,
    linecolor="black",
    mirror=False,
    row=1,
    col=1,
)
fig.update_xaxes(
    rangeslider_visible=False,
    showline=True,
    linewidth=1,
    linecolor="black",
    mirror=False,
    row=2,
    col=1,
)
fig.update_xaxes(
    rangeslider_visible=True,
    showline=True,
    linewidth=1,
    linecolor="black",
    mirror=False,
    row=3,
    col=1,
)
# update
fig.update_layout(
    template="plotly_dark",
    xaxis_rangeselector_font_color="white",
    xaxis_rangeselector_activecolor="#626efb",
    xaxis_rangeselector_bgcolor="#262730",
)
st.plotly_chart(fig)
