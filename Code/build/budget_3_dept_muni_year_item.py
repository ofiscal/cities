# What this does: aggregate spending observations
#   within (muni,year,item code) triples,
#   using the broad item codes defined in budget_codes.py
#   It also replaces missing muni values with -1,
#   because rows with a missing group variable disappear
#   upon using pandas.DataFrame.groupby().
#
# Why: For most of the data, a given (muni, year, item) triple
#   identifies exactly one row, but sometimes not,
#   because that kind of spending is divided by fuente and ejecutor,
#   as demonstrated in explore/duplicate_rows.py.

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.util as util
  import Code.build.sisfut_metadata as sm
  import Code.build.budget_3_dept_muni_year_item_defs as defs

if True:
  budget_key = pd.read_csv( "output/keys/budget.csv",
                            encoding = "utf-16" )
  source = "output/budget_2_subsample/recip-"      + str(c.subsample)
  dest   = "output/budget_3_dept_muni_year_item/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )
  #
  group_fields = [
    "year",
    "muni code",
    "dept code",
    "item code" ]

dfs = {}
for s in ["ingresos","gastos"]:
  df = pd.read_csv( source + "/" + s + ".csv",
                    encoding = "utf-16" )
  df["muni code"] = (
    df["muni code"] .
    fillna(-1) )
  df = ( df .
         groupby( by = group_fields ) .
         agg( sum ) .
         reset_index() )
  df["item code"] = df["item code"] . astype(str)
  df = util.to_front(
      ["muni code","year","item code","dept code","item"]
    , ( df.merge( budget_key
                , left_on = "item code"
                , right_on = "Código Concepto" )
      . drop( columns = [ "Código Concepto" ] ) # redundant given item code
      . rename( columns = { "Concepto" : "item" } )
      . sort_values( ["muni code","year","item code"] ) ) )
  dfs[s] = df
  df.to_csv( dest + "/" + s + ".csv" ,
             encoding="utf-16",
             index = False )
