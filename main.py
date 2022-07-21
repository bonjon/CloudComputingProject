import subprocess
import sys
import requests


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


import streamlit as st
import pandas as pd
import plotly.express as px

install('streamlit')

API_KEY = "PKG95PV0R6DI0C2G522P"
API_SECRET = "knWqSpYCGrkQopBig8K4dIWYNASADqzcjgalRx8O"
BASE_URL = "https://data.alpaca.markets/"
parameters = {"start": "2021-10-01T0:00:00Z",
              "timeframe": "1Day", "symbols": "AAPL,TSLA,AMZN,META,NFLX", "adjustment": "raw"}
headers = {"Apca-Api-Key-Id": API_KEY, "Apca-Api-Secret-Key": API_SECRET}
response = requests.get(url=BASE_URL + "v2/stocks/bars?", headers=headers, params=parameters)
st.title('Data Analytics')
option = st.selectbox('Select the Company Stock that you want to see', ('Apple', 'Tesla', 'Amazon', 'Meta', 'Netflix'))
st.write('You selected:', option)
if option == 'Apple':
    df = pd.DataFrame.from_dict(response.json()['bars']['AAPL'])
    fig = px.line(df, x='t', y='c', title='Apple Stock')
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
elif option == 'Tesla':
    df = pd.DataFrame.from_dict(response.json()['bars']['TSLA'])
    fig = px.line(df, x='t', y='c', title='Tesla Stock')
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
elif option == 'Amazon':
    df = pd.DataFrame.from_dict(response.json()['bars']['AMZN'])
    fig = px.line(df, x='t', y='c', title='Amazon Stock')
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
elif option == 'Meta':
    df = pd.DataFrame.from_dict(response.json()['bars']['META'])
    fig = px.line(df, x='t', y='c', title='META Stock')
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
elif option == 'Netflix':
    df = pd.DataFrame.from_dict(response.json()['bars']['NFLX'])
    fig = px.line(df, x='t', y='c', title='Netflix Stock')
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
