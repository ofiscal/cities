"""
PITFALL
This only corrects the peso-valued columns we are interested in --
namely "item recaudo" and "item oblig".

What this does: This multiplies pre-2016 values by 1000,
because (as you might guess) in the raw data,
pre-2017 peso values are about 1000 times smaller than those post-2016.

It's a long program because it then tests that the percentage change from one year to the next is well behaved, ensuring that no similar problems remain present.
"""

if True:
  from typing import List, Set, Dict
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ts
  import Code.metadata.four_series as sm
  import Code.explore.order_of_mag_x_yrs_defs as lib


if True:
  source = "output/budget_3_dept_muni_year_item/recip-" + str(c.subsample)
  dest   = "output/budget_4_scaled/recip-"         + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # function to multiply early years by 1000
  def correct_peso_columns( cols : List[str],
                            df : pd.DataFrame ) -> pd.DataFrame:
    """ PITFALL: Mutates its input. """
    for c in cols:
      df.loc[ df["year"] < 2017,
              c] *= 1000
    return df
  if True: # test it
    x = pd.DataFrame( {"a" : [0,1,2,3,4,5],
                       "b" : [0,1,2,3,4,5],
                       "c" : [0,1,2,3,4,5],
                       "year" : list( range( 2013, 2019 ) ) } )
    assert (
      correct_peso_columns( ["a","b"], x )
      .equals(
        pd.DataFrame( {
          "a" : [0,1000,2000,3000,4,5],
          "b" : [0,1000,2000,3000,4,5],
          "c" : [0,1,2,3,4,5],
          "year" : list( range( 2013, 2019 ) ) } ) ) )

dfs, dfs_by_muni_item = ({},{})
for s in ts.series:
  if True: # clean the data
    df = pd.read_csv( source + "/" + s.name + ".csv" )
    df = correct_peso_columns( s.peso_cols, df )
    dfs[s.name] = df
  if True: # add percent change across years within place-item
    df_by_muni_item = (
      df[["year",     "muni code", "dept code", "item categ"]
         + s.peso_cols ] .
      groupby( by = [ "muni code", "dept code", "item categ"] ) .
      apply( lambda df:
             lib.add_pct_change( s.peso_cols[0], df) ) .
      reset_index() )
    for year in list( range( 2013, 2019 ) ):
      median_change = (
        ( df_by_muni_item
          [df_by_muni_item["year"] == year ]
          ["pc"] ) .
        median() )
      assert ( (median_change <  2) &
               (median_change > -(2/3) ) )
        # These bounds might look pretty loose --
        # they say that in each (file,year) pair,
        # the median (across (municipality, budget item) pairs)
        # rose by no more than 200% (i.e. tripling), and fell by no more than two-thirds.
        # In fact they can't be made much tighter (and still have every subsample pass).
        # Fortunately, these bounds are far more than tight enough to assure
        # the order of magnitude problem is solved.
    dfs_by_muni_item[s.name] = df_by_muni_item
  df.to_csv( dest + "/" + s.name + ".csv",
             index = False )
