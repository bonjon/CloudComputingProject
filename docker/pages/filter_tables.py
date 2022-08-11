import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from utils import *
from configuration import *

bucket = get_bucket()

st.title("Tabular Data Analytics")

option = st.selectbox(
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)

df = get_df(bucket, option)

# st.write("You selected:", option)


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


selection = aggrid_interactive_table(df=df)
