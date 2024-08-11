import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import association_rules, apriori


def analyze(*args, **kwargs):
    """
    analyze creates basket analysis with support and lift metrics
    Arguments:
    [
        args[0] = DataFrame,
        args[1] = Invoice or Order Id,
        args[2] = Barcode, or Comparible Basket Item
        args[3] = Quantity sold of each item within each order
    ]
    """

    def encodeUnits(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    def format_data(*args):
        df = (args[0].groupby([args[1], args[2]])[args[3]].sum(
        ).unstack().reset_index().fillna(0).set_index(args[1]))
        df_enc = df.parallel_applymap(encodeUnits)
        df_enc_plus = df_enc[(df_enc > 0).sum(axis=1) >= 2]
        return df_enc_plus

    def apply_apriori(df, **kwargs):
        """
        Applies Aprior and Association Rules

        Args:
            df (pd.DataFrame): Dataframe
            min_support: default 0.002, kwarg


        Returns:
            pd.DataFrame: DataFrame with antecedent and consequents
        """
        bk = apriori(df, min_support=kwargs.get('min_support', .002), use_colnames=True).sort_values(
            'support', ascending=False).reset_index(drop=True)
        assoc = association_rules(bk, metric='lift', min_threshold=1).sort_values(
            by='lift', ascending=False).reset_index(drop=True)
        assoc[['antecedents', 'consequents']] = assoc[[
            'antecedents', 'consequents']].applymap(lambda x: ', '.join(x))
        return assoc

    basket = format_data(*args)
    bk_df = apply_apriori(basket)
    return bk_df
