import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import requests

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

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        #    update_mode=GridUpdateMode.MODEL_CHANGED,
        #    allow_unsafe_jscode=True,
    )

    return selection

st.write("You selected:", option)
df = pd.DataFrame.from_dict(response.json()["bars"][SYMBOLS[option]])

selection = aggrid_interactive_table(df=df)
