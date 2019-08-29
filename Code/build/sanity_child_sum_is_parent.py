# To determine whether, in the (muni,year,budget)-aggregated data,
# the figure associated with one of the "top" categories, i.e. a category we use,
# is equal to the sum of its immediate child categories. (It usually is.)

import os
import numpy as np
import pandas as pd

import Code.common as c
import Code.util as u
import Code.build.sisfut_metadata as sm


source       = "output/budget_3_muni_year_categ_top/recip-"    + str(c.subsample)
dest         = "output/sanity_child_sum_is_parent/recip-"         + str(c.subsample)
dest_summary = "output/sanity_child_sum_is_parent_summary/recip-" + str(c.subsample)
for d in [dest, dest_summary]:
  if not os.path.exists( d ):
    os.makedirs(         d )


# columns defining the unit of observation
columns_uob = ["muni code","year","item categ","item top"]

dfs = {}
for s in sm.series:
  dfs[s] = pd.read_csv( source + "/" + s + ".csv" )

def summarize_muni_yr_categ( col : str, df2r : pd.DataFrame ) -> pd.DataFrame:
  """Computes a one-row data frame with some statistics of interest,
regarding the column "col" in the data frame "df2r".
"df2r" should be a two-row data frame, defined by muni, year and budget item categ,
  in which "item top" takes the values 0 and 1.
"col" should be a budget column, for instance "item oblig"."""
  theMin = df2r[col].min()
  theMax = df2r[col].max()
  theRange = theMax - theMin
  theRatio = 0 if theRange == 0 else theRange / theMin
  return pd.DataFrame( { ( col + ", min"  ) : [theMin]
                       , ( col + ", max"  ) : [theMax]
                       , ( col + ", ratio") : [theRatio] } )

df_summaries, df_myi_summaries = ({},{})
for (s, pesos_column) in [
    ("ingresos"       ,"item recaudo"),
    ("inversion"      ,"item oblig"),
    ("funcionamiento" ,"item oblig") ]:
  df_myi_summaries[s] = (
    dfs[s] .
    groupby( by = ["muni code","year","item categ"] ) .
    apply( lambda df2r :
           summarize_muni_yr_categ( pesos_column, df2r) ) .
    reset_index() .
    drop( columns = ["level_3"] ) )
  df_myi_summaries[s] . to_csv( dest + "/" + s + ".csv",
    index = False )
  df_summaries[s] = ( u.myDescribe( df_myi_summaries[s] ) .
                      transpose() )
  df_summaries[s] . to_csv( dest_summary + "/" + s + ".csv" )

