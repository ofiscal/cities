# To determine whether the (muni,year,concepto)-aggregated data makes sense.

import os
import numpy as np
import pandas as pd

import Code.common as c
import Code.util as u
import Code.build.sisfut_metadata as sm


source       = "output/conceptos_3_muni_year_categ_top/recip-"     + str(c.subsample)
dest         = "output/conceptos_4_muni_year_categ/recip-"         + str(c.subsample)
dest_summary = "output/conceptos_4_muni_year_categ_summary/recip-" + str(c.subsample)
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
for (s, item_variety) in [
    ("ingresos"       ,"recaudo"),
    ("inversion"      ,"oblig"),
    ("funcionamiento" ,"oblig") ]:
  df_myi_summaries[s] = (
    dfs[s] .
    groupby( by = ["muni code","year","item categ"] ) .
    apply( lambda df2r :
           summarize_muni_yr_categ( "item " + item_variety, df2r) ) .
    reset_index() .
    drop( columns = ["level_3"] ) )
  df_myi_summaries[s] . to_csv( dest + "/" + s + ".csv",
    index = False )
  df_summaries[s] = ( u.myDescribe( df_myi_summaries[s] ) .
                      transpose() )
  df_summaries[s] . to_csv( dest_summary + "/" + s + ".csv" )

