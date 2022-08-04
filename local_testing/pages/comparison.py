from pkgutil import get_data
import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.plotting import scatter_matrix
from configuration import *
from utils import get_df

st.title("Data Analytics")

dataframes = []
for sim in SYMBOLS.keys():
    df = get_df(sim)
    if df is not None:
        df["s"] = SYMBOLS[sim]
        dataframes.append(df)

df = pd.concat(dataframes)

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

data = pd.pivot_table(df, values="c", index=["t"], columns=["s"]).reset_index()

st.plotly_chart(px.scatter_matrix(data.drop(columns=["t"])))
