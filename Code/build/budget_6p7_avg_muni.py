# PURPOSE:
# In the -pct files, compute an "average municipality"
# for each district.

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  #
  import Code.common as c
  from Code.util.percentify import percentify_columns
  import Code.metadata.two_series as s2
  import Code.metadata.four_series as s4

if True: # folders
  source  = "output/budget_6p5_cull_and_percentify/recip-" + str(c.subsample)
  dest = "output/budget_6p7_avg_muni/recip-"               + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input data
  dfs = {}
  for s in s4.series:
    dfs[s.name] = pd.read_csv(
      source + "/" + s.name + ".csv" )

if True: # how to add a column that counts munis in each dept
  def add_munis_in_dept_col( df : pd.DataFrame ) -> pd.DataFrame:
    """ Adds a column indicating how many munis are in each dept. """
    new = df[~(df["muni code"]<0)][["dept code"]]
    new["munis"] = 1
    new = ( new . groupby(["dept code"]) .
            agg({"dept code" : "first",
                 "munis"     : sum}) .
            reset_index(drop=True) )
    return df.merge( new, how="left", on="dept code" )
  if True: # test it
    x = pd.DataFrame( { "dept code" : [1,11,11,22,22,22,22],
                        "muni code" : [1,2,3,4,5,6,-1],
                        "noise"     : [1,2,3,4,5,6,7] } )
    y = add_munis_in_dept_col(x)
    z = pd.DataFrame( { "dept code" : [1,11,11,22,22,22,22],
                        "muni code" : [1,2,3,4,5,6,-1],
                        "noise"     : [1,2,3,4,5,6,7],
                        "munis"     : [1,2,2,3,3,3,3] } )
    assert y.equals(z)

if True: # define how to compute the average muni in a dept
  assert False == "broken -- must be at the dept-year-categ level, not the dept-year level"
  def prepend_avg_muni( money_cols : [str],
                        df0 : pd.DataFrame
                      ) -> pd.DataFrame:
    """ Input:  All munis in a given department-year-item-categ slice.
        Output: The same, plus a new "average" muni. """
    df = ( df0.copy()
           [df0["muni code"] != -1] )
             # omit department-level data; use only munis
    if len(df) == 0: return df # This dept has no muni-level info
    avg = df.head(1)
    n = len(df)
    for col_name in money_cols:
      col = df[col_name]
      col = col[ ~ pd.isnull(col) ]
      m = len(col)
    avg["muni code"] = -2 # TODO ? Ugly.
    return pd.concat( [ pd.DataFrame([avg]),
                        df0],
                      axis="rows" )
  if True: # test it
    x = pd.DataFrame( [ [13, -1, 1, 2, 1],
                        [13,  1, 2, 2, 2],
                        [13,  2, 3, 6, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","moolah"] )
    y = pd.DataFrame( [ [13, -2, 2.5, 4, 2],
                        [13, -1, 1,   2, 1],
                        [13,  1, 2,   2, 2],
                        [13,  2, 3,   6, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","moolah"] )
    assert ( prepend_avg_muni( ["money","cash"], x) .
             reset_index(drop=True) .
             equals( y.astype('float') ) )

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
