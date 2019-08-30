from typing import Set
import re

import numpy as np
import pandas as pd

import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


def match_budget_codes( d : pd.DataFrame,
                        r : re.Pattern ):
  return d[ ( ~ pd.isnull( d["item code"] .
                           str.extract(r) ) )
            . values ] # "values" turns the "not null" series into an array.
                       # TODO ? I don't know why it's needed.

assert ( # test it
  match_budget_codes(
    pd.DataFrame( { "item code" : ["TI.A","monkey"] } ),
    re.compile("(TI)") ) .
  equals( pd.DataFrame( { "item code" : ["TI.A"] } ) ) )


def aggregated_item_codes( dfs ):
  """
Back when we had not decided whether to use top categories or the sum of
each top category's children (immediate descendents), this function was useful.
Now that we only use the top category, it's overkill.

An 'item' is a record of spending or income (taxes). This function builds some new columns, the aggregate item subcodes by which the data will downstream be aggregated. It does not aggregate rows. The 'dfs' argument should be a dictionary containing the three data sets, per collect_raw()."""
  for (series, regexes) in [
        ("inversion"      , ac.regexes_for_2_codes() )
      , ("funcionamiento" , ac.regexes_for_2_codes() )
      , ("ingresos"       , ac.regexes_for_ingresos() ) ]:
    df = dfs[series]
  
    # build some columns
    (category, top, child) = regexes
    df["item categ"]       = (
        df["item code"]
      . str.extract( category ) )
    df["item top"]   = ~ pd.isnull(
        df["item code"]
      . str.extract( top ) )
    df["item child"] = ~ pd.isnull(
        df["item code"]
      . str.extract( child ) )
  
    df = ( # keep only rows labeled with top categories
           # or the first generation below the top categories
      df[ (df["item top"])
        | (df["item child"]) ] )
  
    # Verify that codigo-top is the boolean negative of codigo-child.
    # (That's not true before we drop rows categorized deeper than top or child.)
    assert ( len ( df[ ( (df["item top"].astype(int)) +
                         (df["item child"]).astype(int) )
                       != 1 ] )
             == 0 )
    df = df.drop( columns = ["item child"] )
  
    dfs[series] = df
  return dfs
