from os import truncate
import streamlit as st
import plotly.express as px
#from utils import *
#from configuration import *
import logging
import requests
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

st.title("Data Analytics")
parameters = {"start": "2021-01-01T0:00:00Z", "symbols":"AAPL", "include_content": "true", "limit":"50", "sort": "ASC"}
headers = {"APCA-API-KEY-ID": "PKF2QMR530IM4SKCFZ68", "APCA-API-SECRET-KEY": "4BGfZRQbMFZ67U0x5M8bayTUgUcP1qpK6lfdq1Zd"}
response = requests.get("https://data.alpaca.markets/v1beta1/news?", params=parameters, headers=headers)
df = pd.DataFrame.from_dict(response.json()["news"])
fig = px.histogram(df, x="source")
st.plotly_chart(fig)