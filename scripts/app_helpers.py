import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO


@st.cache(allow_output_mutation=True)
def load_xlsx(*args, **kwargs):
    # <---------------Streamlit function--------------->
    """

    load_csv --> reads csv into Pandas DataFramr
    args: *args, **kwargs
    Returns:
        pd.DataFrame
    """

    df = pd.read_excel(args[0], **kwargs)

    return df


def load_csv(*args, **kwargs):
    """
    load_csv --> reads csv into Pandas DataFramr
    args: *args, **kwargs
    Returns:
        pd.DataFrame
    """
    df = pd.read_csv(args[0], **kwargs)

    return df


def download_xlsx(df):
    """
    Download XLSX from Streamlit to local

    Args:
        df (pd.DataFrame): Dataframe to be download
    """

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    df.to_excel(writer, index=False, sheet_name='Sheet1')

    writer.save()
    processed_data = output.getvalue()

    return processed_data
