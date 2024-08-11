import streamlit as st
import pandas as pd
import numpy as np
import regex as re
from ftfy import fix_text
from io import BytesIO
import xlsxwriter
from pyxlsb import open_workbook as open_xlsb


@st.cache(allow_output_mutation=True)
def load_xlsx(*args, **kwargs):
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


def group_sum(*args, **kwargs):
    """
    group_sum groups DataFrame on column name

    Returns:
        DataFrame: grouped DataFrame
    """
    df = args[0].groupby(kwargs.get('on_column'), as_index=False)[
        [kwargs.get('sum_column', 'Total')]].sum()
    return df


def count_unique(*args, **kwargs):
    df = args[0].groupby(kwargs.get('on_column'), as_index=False)[
        kwargs.get('count_column', 'Total')]
    return df


def agg_df(*args, **kwargs):
    df = args[0].groupby(kwargs.get('on_column'), as_index=False).agg()


def infer_type(df):
    dfn = df.infer_objects()
    return dfn


def download_xlsx(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def build_tags(args):
    # shopify tags
    args.brands = args.brands.replace(', ', ',').split(',')
    args.brands = list(map(lambda i: i.replace(i, f'Brand_{i}'), args.brands))
    args.brands = ', '.join(args.brands)


def cleaner(x):
    to_remove = ['everest parts supplies ', 'everest parts brand ', 'everest brand ']
    vals = re.sub(r'|'.join(to_remove), '', x, flags=re.I)
    vals = vals.strip()
    if x.startswith('New '):
        vals = re.sub(r'^New ', '', x, flags=re.I)
        vals = vals.strip()
    x = vals
    return x


def skus(x, vals):
    matches = []
    for i in x:
        if vals.get(i) is not None:
            matches.append(vals[i])
    return matches
