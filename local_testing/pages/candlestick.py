import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import *
from configuration import *
import numpy as np

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

df["ema_1"] = df["c"].ewm(span=ema_1, adjust=False).mean()
df["ema_2"] = df["c"].ewm(span=ema_2, adjust=False).mean()
df["macd"] = df["ema_1"] - df["ema_2"]
df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
df["macd_area"] = df["macd"] - df["macd_signal"]
df["tp"] = (df["h"] + df["l"] + df["c"]) / 3
df["tp_sma"] = df["tp"].rolling(20).mean()
df["tp_std"] = df["tp"].rolling(20).std(ddof=0)
df["RSI"] = RSI(df["c"])  # .fillna(0)

# st.write("You selected:", option)
fig = make_subplots(
    vertical_spacing=0,
    rows=4,
    cols=1,
    row_heights=[0.8, 0.2, 0.2, 0.15],
    shared_xaxes=True,
)
fig.add_trace(
    go.Candlestick(
        x=df["t"],
        open=df["o"],
        high=df["h"],
        low=df["l"],
        close=df["c"],
        name="Candlestick",
    )
    if option_candlestick == "Candlestick"
    else go.Ohlc(
        x=df["t"],
        open=df["o"],
        high=df["h"],
        low=df["l"],
        close=df["c"],
        name="OHLC",
    )
)
fig.add_trace(
    go.Scatter(
        x=df["t"],
        y=df["ema_1"],
        opacity=0.8,
        name="EMA 1",
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df["t"],
        y=df["ema_2"],
        opacity=0.8,
        name="EMA 2",
    ),
    row=1,
    col=1,
)
# Upper Bound
fig.add_trace(
    go.Scatter(
        x=df["t"],
        y=df["tp_sma"] + (df["tp_std"] * 2.0),
        line_color="gray",
        # line = {'dash': 'dash'},
        name="Upper band",
        opacity=0.2,
    ),
    row=1,
    col=1,
)
# Lower Bound
fig.add_trace(
    go.Scatter(
        x=df["t"],
        y=df["tp_sma"] - (df["tp_std"] * 2),
        line_color="gray",
        fill="tonexty",
        name="Lower band",
        opacity=0.2,
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df["t"],
        y=df["macd"],
        name="MACD",
    ),
    row=2,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df["t"],
        y=df["macd_signal"],
        name="MACD signal",
    ),
    row=2,
    col=1,
)
mask = df["macd_area"] >= 0.0
fig.add_trace(
    go.Scatter(
        x=df["t"][mask],
        y=df["macd_area"][mask],
        line=dict(color="rgba(0,255,0,0.4)"),
        fill="tozeroy",
        fillcolor="rgba(0,255,0,0.4)",
    ),
    row=2,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df["t"][~mask],
        y=df["macd_area"][~mask],
        line=dict(color="rgba(255,0,0,0.4)"),
        fill="tozeroy",
        fillcolor="rgba(255,0,0,0.4)",
    ),
    row=2,
    col=1,
)

fig.add_trace(
    go.Scatter(x=df["t"], y=df["RSI"], name="RSI"),
    row=3,
    col=1,
)
# Add overbought/oversold
fig.add_hline(
    y=30,
    row=3,
    col=1,
    line_color="#336699",
    line_width=2,
    line_dash="dash",
)
fig.add_hline(
    y=70,
    row=3,
    col=1,
    line_color="#336699",
    line_width=2,
    line_dash="dash",
)

fig.add_trace(
    go.Bar(
        x=df["t"],
        y=df["v"],
        marker_color="yellow",
        name="Volume",
    ),
    row=4,
    col=1,
)

fig.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list(
            [
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
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
    rangeslider_visible=False,
    showline=True,
    linewidth=1,
    linecolor="black",
    mirror=False,
    row=3,
    col=1,
)
fig.update_xaxes(
    rangeslider_visible=True,
    showline=True,
    linewidth=1,
    linecolor="black",
    mirror=False,
    row=4,
    col=1,
)
# to hide the weeends and holidays
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),  # hide weekends
        dict(values=["2022-12-25", "2022-01-01"]),  # hide Christmas and New Year's
    ]
)

fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="MACD", showgrid=False, row=2, col=1)
fig.update_yaxes(title_text="RSI", row=3, col=1)
fig.update_yaxes(title_text="Volume", row=4, col=1)
# update
fig.update_layout(
    template="plotly_dark",
    xaxis_rangeselector_font_color="white",
    xaxis_rangeselector_activecolor="#626efb",
    xaxis_rangeselector_bgcolor="#262730",
    showlegend=False,
)

st.plotly_chart(fig)


def stochastic(df, k, d):
    df = df.copy()
    low_min = df["l"].rolling(window=k).min()
    high_max = df["h"].rolling(window=k).max()
    df["stoch_k"] = 100 * (df["c"] - low_min) / (high_max - low_min)
    df["stoch_d"] = df["stoch_k"].rolling(window=d).mean()
    return df


stochs = stochastic(df, k=14, d=3)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df["t"], y=stochs.stoch_k, name="K stochastic"))
fig1.add_trace(go.Scatter(x=df["t"], y=stochs.stoch_d, name="D stochastic"))
fig1.add_hline(
    y=20,
    line_color="#336699",
    line_width=2,
    line_dash="dash",
)
fig1.add_hline(
    y=80,
    line_color="#336699",
    line_width=2,
    line_dash="dash",
)

st.plotly_chart(fig1)
