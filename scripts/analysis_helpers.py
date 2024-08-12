import streamlit as st
import pandas as pd
import numpy as np
import regex as re
from ftfy import fix_text
from io import BytesIO
import xlsxwriter
from pyxlsb import open_workbook as open_xlsb


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
    """aggregates column on dataframe"""

    df = args[0].groupby(kwargs.get('on_column'), as_index=False).agg()

    return df


def infer_type(df):
    dfn = df.infer_objects()

    return dfn


def build_tags(args):
    # TODO finish function
    # <-----------------------IN PROGRESS----------------------->
    # shopify tags
    args.brands = args.brands.replace(', ', ',').split(',')
    args.brands = list(map(lambda i: i.replace(i, f'Brand_{i}'), args.brands))
    args.brands = ', '.join(args.brands)


def cleaner(x, *args):
    to_remove = list(args)
    vals = re.sub(r'|'.join(to_remove), '', x, flags=re.I)
    vals = vals.strip()
    if x.startswith('New '):
        vals = re.sub(r'^New ', '', x, flags=re.I)
        vals = vals.strip()
    x = vals

    return x


def sku_mapping(x, vals):
    matches = []
    for i in x:
        if vals.get(i) is not None:
            matches.append(vals[i])

    return matches
