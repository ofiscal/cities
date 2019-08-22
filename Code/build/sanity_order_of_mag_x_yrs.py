import os
import pandas as pd

import Code.common as c
import Code.build.sisfut_metadata as sm


source = "output/conceptos_3_muni_year_categ_top/recip-" + str(c.subsample)
dest   = "output/sanity_order_of_mag_x_yrs/recip-"       + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in sm.series:
  dfs[s] = pd.read_csv( source + "/" + s + ".csv" )

def add_pct_change(
    column : str,
    df : pd.DataFrame ) -> pd.DataFrame:
  """ PITFALL: Mutates its input. """
  df["pc"] = df[column].pct_change()
  return df

for s in ["ingresos"]:
  for muni in [5091]:
    df = dfs[s]
    df_muni = df[ (df["muni code"] == muni) &
                  df["item top"] ]
    df_muni_items = (
      df_muni .
      groupby( by = ["muni code", "item categ"] ) .
      apply( lambda df: add_pct_change( "item recaudo", df) ) .
      reset_index() )
    df_muni_items[["muni code","year","item categ","item recaudo","pc"]]
