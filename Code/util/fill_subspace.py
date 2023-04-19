""" If your data is missing some years, or some places,
or whatever, this will create observations for those missing spots,
with whatever you were hoping to observe set to 0.
"""

if True:
  from typing import List,Set,Dict
  import pandas as pd


def powerset(
    axis_names : List[str], # columns definiing the subspace
    df0 : pd.DataFrame ):
  """Given all the values of the columns in axis_names,
creates a set of rows with every possible combination."""
  axes = []
  for c in axis_names:
    df = pd.DataFrame( df0[c].drop_duplicates() )
    df["const"] = 0
    axes.append(df)
  acc = axes[0]
  for ax in axes[1:]:
    acc = acc.merge( ax, how="outer", on="const" )
  return acc . drop( columns = "const" )

powerset( # demo; no time to formalize
  ["a","b"],
  pd.DataFrame( [[1,2,3],[4,5,6],[7,8,9]],
                columns = ["a","b","c"] ) )

def fill_space(
    axis_names : List[str], # columns definiing the subspace
    zero_if_missing : List[str], # more columns
    df0 : pd.DataFrame ):
  space = powerset( axis_names, df0 )
  for c in zero_if_missing:
    space[c] = 0
  return (
    pd . concat( [df0, space], axis = "rows" ) .
    groupby( axis_names ) .
    agg( sum ) .
    reset_index() )

fill_space( # the spot (a,b)=(2,3) should appear,
            # with v=0
  ['a','b'],
  ['v'],
  pd.DataFrame( { 'a' : [1,1,2],
                  'b' : [3,4,4],
                  'v' : [1,2,3] } ) )
