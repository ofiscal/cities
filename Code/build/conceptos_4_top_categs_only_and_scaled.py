""" PITFALL
This only corrects the peso-valued columns we are interested in --
namely "item recaudo" and "item oblig".

Two purposes:

(1): Problem: Peso values pre-2017 are about 1000 times smaller than those post-2016.
Solution: This multiplies pre-2016 values by 1000,

(2): Keep only top categories, not the sum of their immediate children.
(The latter are an alternate way of coming to the same figure.
They are almost equivalent, but not exactly --
see sanity_child_sum_is_parent.py.) """

import os
import pandas as pd

import Code.common as c
import Code.build.sisfut_metadata as sm
import Code.explore.order_of_mag_x_yrs as lib


source = "output/conceptos_3_muni_year_categ_top/recip-"        + str(c.subsample)
dest   = "output/conceptos_4_top_categs_only_and_scaled/recip-" + str(c.subsample)
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
    ("ingresos"       ,"item recaudo"),
    ("inversion"      ,"item oblig"),
    ("funcionamiento" ,"item oblig") ]:
  if True: # clean the data
    df = pd.read_csv( source + "/" + file + ".csv" )
    df = df[ df["item top"] ]
    assert (df["item top"] == True).all()
    df = df.drop( columns = ["item top"] )
    df = correct_peso_column( pesos_col, df )
    dfs[file] = df
  if True: # verify the data
    df_by_muni_item = (
      df[["year","muni code","item categ",pesos_col]] .
      groupby( by = ["muni code", "item categ"] ) .
      apply( lambda df: lib.add_pct_change( pesos_col, df) ) .
      reset_index() )
    for year in list( range( 2013, 2019 ) ):
      median_change = (
        df_by_muni_item
        [df_by_muni_item["year"] == year ]
        ["pc"] .
        median() )
      # print( str(year), file, median_change )
      assert ( (median_change <  1) &
               (median_change > -0.5) )
        # These bounds might look pretty loose --
        # they say the median (across (municipality, budget item) pairs)
        # did no more than double or no less than halve in each (file,year) pair.
        # In fact they can't be made much tighter (and still have every subsample pass).
        # Fortunately, they're far more than tight enough to assure that
        # the order of magnitude problem is solved.
    dfs_by_muni_item[file] = df_by_muni_item
  df.to_csv( dest + "/" + file + ".csv" ,
             index = False )

