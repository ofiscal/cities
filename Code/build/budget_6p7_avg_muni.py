# PURPOSE:
# In the -pct files, compute an "average municipality"
# for each district.

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  import pandas.api.types as ptypes
  #
  import Code.common as c
  import Code.metadata.terms as t
  from Code.util.percentify import percentify_columns
  import Code.build.use_keys as uk
  import Code.metadata.two_series as s2
  import Code.metadata.four_series as s4

if True: # folders
  source = "output/budget_6p5_cull_and_percentify/recip-" + str(c.subsample)
  dest   = "output/budget_6p7_avg_muni/recip-"            + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input data
  geo = ( uk.depts_and_munis
         [["dept code","muni code","munis"]] )
  dfs = {}
  for s in s4.series:
    dfs[s.name] = pd.read_csv(
      source + "/" + s.name + ".csv" )

if True: # define how to compute the average non-dept muni
         # in some (dept,year,item categ) cell
  def prepend_avg_muni( money_cols : List[str],
                        df0 : pd.DataFrame
                      ) -> pd.DataFrame:
    """
Input: A slice with constant (dept,year,item categ).
Output: The same, plus a new "average" muni.
        Average is only over munis; it omits the dept row.
PITFALL: Upstream, apply fillna(-1) to money columns.
"""
    df = ( df0.copy()
           [df0["muni code"] != -1] )
    assert len(df) > 0
      # Fails if dept has no muni-level info.
      # (Bogotá comes close: it has no "dept"-level info.)
    munis_in_dept = int(
        geo.loc[ ( geo       ["dept code"] ==
                   df.iloc[0]["dept code"] ),
                 "munis" ] .
        head(1) )
    avg = df.iloc[0] . copy()
    avg["muni code"] = -2 # TODO ? Ugly.
    avg[money_cols] = ( # The missing-rows-aware mean.
        df[money_cols] . sum() / munis_in_dept )
    return pd.concat( [ pd.DataFrame([avg]),
                        df0],
                      axis="rows" )
  if True: # test it
    # Department 99 has 4 municipalities.
    x = pd.DataFrame( [ [99, -1, 1, 2, 1],
                        [99,  1, 1, 65, 2],
                        [99,  2, 5, 15, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","pecan"] )
    y = pd.DataFrame( [ [99, -2, 1.5, 20, 2],
      # The previous row (the only new one) has
      # average money=(1+5) / 4,
      # average cash=(15+65) / 4,
      # and is otherwise just like the muni with code 1.
                        [99, -1, 1,    2, 1],
                        [99,  1, 1,   65, 2],
                        [99,  2, 5,   15, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","pecan"] )
    assert ( prepend_avg_muni( ["money","cash"], x) .
             reset_index(drop=True) .
             equals( y.astype('float') ) )

assert False = "RESUME HERE"

for s in s2.series:
  df = dfs[s.name + "-pct"]
  df = (
    df . groupby( ["dept code","year"] ) .
    apply( lambda df:
           prepend_avg_muni( s.money_cols, df ) ) )

# 1
#     reset_index( drop = True) )
# #     sort_values( spacetime ) )
#   dfs[s.name + "-pct"] = df
# 
# 1
#   if True: # dimensions check
#     assert len(df) == 1 + len(dfs[s.name])
#     assert df.columns == dfs[s.name].columns
# 
# for s in s4.series:
#   dfs[s.name].to_csv( dest + "/" + s.name + ".csv" )

