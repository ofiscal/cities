# aggregate budget
#   within muni-year,
#   by broad (usually 2 prefixes, otherwise 3) budget category

import os
import pandas as pd

import Code.common as c
import Code.util as util
import Code.build.sisfut_metadata as sm
import Code.build.budget_3_muni_year_item_defs as defs


budget_key = pd.read_csv( "output/keys/budget.csv",
                          encoding = "utf-16" )
source       = "output/budget_2_subsample/recip-"       + str(c.subsample)
dest         = "output/budget_3_muni_year_item/recip-" + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

group_fields = [
  "year",
  "muni code",
  "dept code",
  "item code" ]

######
###### TODO : mystery
######
## Why does the grouping change the length of the data set?
#
#dfs_raw = {}
#for s in sm.series:
#   dfs_raw[s] = (
#     pd.read_csv( source + "/" + s + ".csv",
#                  encoding = "utf-16" ) .
#     sort_values( group_fields ) )
#
#dfs = {}
#for s in sm.series:
#  dfs[s] = ( dfs_raw[s] .
#             groupby( by = group_fields ) .
#             agg( sum ) .
#             reset_index() )
#
#dfs_raw[s].sort_values( group_fields )[group_fields]
#dfs[s].sort_values( group_fields )[group_fields]

dfs = {}
for s in sm.series:
  df = (
      pd.read_csv( source + "/" + s + ".csv",
                   encoding = "utf-16" )
    . groupby( by = group_fields )
    . agg( sum )
    . reset_index() )
  assert defs.group_is_redundant(
    "dept code", group_fields, df )
    # Given that we already aggregate on muni code,
    # aggregating on dept code is redundant,
    # but offers an easy way to keep the column without summing it.
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
