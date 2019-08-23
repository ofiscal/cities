# Comparing 100 times the percentage change* in peso-valued columns,
# to determine whether it's true, as appears from eyeballing some samples,
# that figures from 2017 and after are a thousand times greater than those from before.
#
# *that is, 0 indicates no change, 1 indicates the value doubled, 2 indicates it tripled,
# -1 indicates it went to 0, inf indicates it was zero and now is positive, etc.

import os
import pandas as pd

import Code.common as c
import Code.util as util
import Code.build.sisfut_metadata as sm


source = "output/conceptos_3_muni_year_categ_top/recip-" + str(c.subsample)
dest   = "output/explore/order_of_mag_x_yrs/recip-"      + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in sm.series:
  dfs[s] = pd.read_csv( source + "/" + s + ".csv" )

def add_pct_change(
    column : str,
    df : pd.DataFrame ) -> pd.DataFrame:
  """ PITFALL: Mutates its input.
      PITFALL: Not really percent change -- rather, 100 times that."""
  df["pc"] = df[column].pct_change()
  return df

dfs_by_muni_item = {}
for (s, pesos_column) in [
    ("ingresos"       ,"item recaudo"),
    ("inversion"      ,"item oblig"),
    ("funcionamiento" ,"item oblig") ]:
  df = dfs[s]
  df = df[ df["item top"] ]
  dfs_by_muni_item[s] = (
    df .
    groupby( by = ["muni code", "item categ"] ) .
    apply( lambda df: add_pct_change( pesos_column, df) ) .
    reset_index() )

report = pd.DataFrame()
for s in sm.series:
  dfmi = dfs_by_muni_item[s]
  summary_2017 = util.myDescribe( dfmi[ dfmi["year"] == 2017 ][["pc"]] )
  summary_2017["2017"] = True
  summary_2017["data"] = s
  summary_others = util.myDescribe( dfmi[ dfmi["year"] != 2017 ][["pc"]] )
  summary_others["2017"] = False
  summary_others["data"] = s
  report = report.append( [summary_2017, summary_others] )

( report .
  transpose() .
  to_csv( dest + "/report.csv" ) )
