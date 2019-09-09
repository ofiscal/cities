"""
PITFALL
This only corrects the peso-valued columns we are interested in --
namely "item recaudo" and "item oblig".

What this does: This multiplies pre-2016 values by 1000,
because (as you might guess) in the raw data,
pre-2017 peso values are about 1000 times smaller than those post-2016.
"""

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.build.sisfut_metadata as sm
  import Code.explore.order_of_mag_x_yrs_defs as lib


if True:
  source = "output/budget_3_dept_muni_year_item/recip-" + str(c.subsample)
  dest   = "output/budget_4_scaled/recip-"         + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

def correct_peso_column( column : str,
                         df : pd.DataFrame ) -> pd.DataFrame:
  """ PITFALL: Mutates its input. """
  df.loc[ df["year"] < 2017
          , column] *= 1000
  return df

dfs, dfs_by_muni_item = ({},{})
for (file,pesos_col) in [
    ("ingresos" ,"item recaudo"),
    ("gastos"   ,"item oblig") ]:
  if True: # clean the data
    df = pd.read_csv( source + "/" + file + ".csv",
                      encoding = "utf-16" )
    df = correct_peso_column( pesos_col, df )
    dfs[file] = df
  if True: # add percent change across years within place-item
    df_by_muni_item = (
      df[["year",     "muni code", "dept code", "item categ",pesos_col]] .
      groupby( by = [ "muni code", "dept code", "item categ"] ) .
      apply( lambda df: lib.add_pct_change( pesos_col, df) ) .
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
    dfs_by_muni_item[file] = df_by_muni_item
  df.to_csv( dest + "/" + file + ".csv" ,
             encoding="utf-16",
             index = False )
