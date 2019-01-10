#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Search tools.
"""

from itertools import chain
import re
import numpy as np
from spacy import load


nlp = load("en_core_web_sm")


class DFSearch(object):
    def __init__(self, df):
        self.df = df


def lemmatized_df_search(x, y, fmt_string="df.columns[{}]"):
    search_res = {}
    tokens = list(chain(*x))
    colnames = list(chain(*[nlp(c) for c in y]))
    for i, xx in enumerate(colnames):
        for yy in tokens:
            if xx.lemma_ == yy.lemma_:
                search_res[yy.text] = fmt_string.format(i)
    return search_res


def search_args(entities, args):
    search_res = {}
    fmt = "args['{}'][{}]"
    ent_tokens = list(chain(*entities))
    for k, v in args.items():
        key = k.lstrip("?")
        argtokens = list(chain(*[re.findall(r"\w+", f) for f in v]))
        argtokens = list(chain(*[nlp(c) for c in argtokens]))
        for i, x in enumerate(argtokens):
            for y in ent_tokens:
                if x.lemma_ == y.lemma_:
                    search_res[y.text] = fmt.format(key, i)
    return search_res


def search_df(tokens, df):
    """Search a dataframe for tokens and return the coordinates."""
    search_res = {}
    txt_tokens = np.array([c.text for c in tokens])
    coltype = df.columns.dtype
    ixtype = df.index.dtype

    # search in columns
    column_ix = np.arange(df.shape[1])[df.columns.astype(str).isin(txt_tokens)]
    for ix in column_ix:
        token = df.columns[ix]
        ix = sanitize_indices(df.shape, ix, 1)
        search_res[token] = "df.columns[{}]".format(ix)

    # search in index
    index_ix = df.index.astype(str).isin(txt_tokens)
    for token in df.index[index_ix]:
        if token not in search_res:
            if ixtype == np.dtype("O"):
                indexer = "df.loc['{}']".format(token)
            else:
                indexer = "df.loc[{}]".format(token)
            search_res[token] = indexer

    # search in table
    for token in txt_tokens:
        if token not in search_res:
            mask = df.values.astype(str) == token
            try:
                column = df.columns[mask.sum(0).astype(bool)][0]
                # don't sanitize column
                index = df.index[mask.sum(1).astype(bool)][0]
                index = sanitize_indices(df.shape, index, 0)
            except IndexError:
                continue
            if coltype == np.dtype("O"):
                col_indexer = "'{}'".format(column)
            else:
                col_indexer = str(column)
            if ixtype == np.dtype("O"):
                ix_indexer = "'{}'".format(index)
            else:
                ix_indexer = str(index)
            search_res[token] = "df.loc[{}, {}]".format(ix_indexer, col_indexer)

    unfound = [token for token in tokens if token.text not in search_res]
    search_res.update(lemmatized_df_search(unfound, df.columns))
    return search_res
