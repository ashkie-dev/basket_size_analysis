# ! Old main
from mlxtend.frequent_patterns import apriori, association_rules
import regex as re
import pandas as pd
import numpy as np
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=False, verbose=1)


def analyze(*args, **kwargs):
    """
    analyze creates basket analysis with support and lift metrics
    Arguments:
    [
        args[0] = DataFrame,
        cols=[
        args[1] = Invoice or Order Id,
        args[2] = Barcode, or Comparible Basket Item
        args[3] = Quantity sold of each item within each order
    ]
    """

    def encodeUnits(x):
        """Hot encodes dataframe

        Args:
            x (int): _description_

        Returns:
            bool: encoded value
        """

        if x <= 0:
            return False
        if x >= 1:
            return True

    def format_data(*args):
        cols = args[0].columns.to_list()
        df = args[0].copy()

        df[cols[3]] = df[cols[3]].astype(float)

        df = (args[0].groupby([cols[0], cols[1]])[cols[3]].sum(
        ).unstack().reset_index().fillna(0).set_index(cols[0]))

        df_enc = df.parallel_applymap(encodeUnits)
        df_enc_plus = df_enc[(df_enc > 0).sum(axis=1) >= 2]

        return df_enc_plus

# --------------old format_data function--------------
    # def format_data(*args):
    #     df = (args[0].groupby([args[1], args[2]])[args[3]].sum(
    #     ).unstack().reset_index().fillna(0).set_index(args[1]))
    #     df_enc = df.parallel_applymap(encodeUnits)
    #     df_enc_plus = df_enc[(df_enc > 0).sum(axis=1) >= 2]
    #     return df_enc_plus

    def apply_apriori(df, **kwargs):
        """
        Applies Aprior and Association Rules

        Args:
            df (pd.DataFrame): Dataframe
            min_support: default 0.002, kwarg


        Returns:
            pd.DataFrame: DataFrame with antecedent and consequents
        """

        bk = apriori(df, min_support=kwargs.get('min_support', 0.002), use_colnames=True).sort_values(
            'support', ascending=False).reset_index(drop=True)

        assoc = association_rules(bk, metric='lift', min_threshold=1).sort_values(
            by='lift', ascending=False).reset_index(drop=True)
        assoc[['antecedents', 'consequents']] = assoc[[
            'antecedents', 'consequents']].applymap(lambda x: ', '.join(x))

        return assoc

    basket = format_data(*args)
    bk_df = apply_apriori(basket)

    return bk_df


def format_dtypes(*args, **kwargs):
    """Formats Dataframe data types

    Returns:
        pd.Dataframe: formatted dataframe for processing
    """

    col_names = ['Name', 'Lineitem sku', 'Lineitem name', 'Lineitem quantity']
    df_in = args[0].copy()
    df_out = df_in[col_names].copy()

    df_out['Name'] = df_out['Name'].astype(str)
    df_out['Lineitem quantity'] = df_out['Lineitem quantity'].astype(np.int32)
    return df_out
