import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from app_helpers import *
from analyze import analyze, format_dtypes

# page confg
st.set_page_config(page_title='Market Basket Analysis', layout='wide')
# TODO add image to static
# image = Image.open('static/{file}.jpg')
# st.image(image, width=150)
# page title
st.title('Market Basket Analysis')

if 'min_support' not in st.session_state:
    st.session_state.min_support = 0.000

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()


def run_process(*args):
    with st.spinner('Please wait while we do maths...'):
        st.session_state.df = analyze(args[0], args[1])
    return st.session_state.df


file_import = st.file_uploader(label='Import File')
# if file_import is not None:
imp_file = st.button('Import File')
if imp_file:
    df_in = load_xlsx(file_import)
    df_in = format_dtypes(df_in)
    st.dataframe(df_in)
    if st.button('Run Calculation...', on_click=run_process, args=(df_in, df_in.columns)):
        st.dataframe(st.session_state.df)

    # with st.spinner('Please wait while we do maths...'):
        # run_apriori = analyze(df_in, df_in.columns)
    # st.success('Finished some big brain type shit.')
