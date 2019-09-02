###### This has a funny name because I split budget_1.py into two parts.
###### (Read it as "budget 1 point 5.py".)
###### It restricts the data to the budget items of interest.

import os
import pandas as pd

import Code.build.budget_1p5_tests as tests
import Code.build.sisfut_metadata as sm
import Code.build.budget_codes as codes


source = "output/budget_1"
dest = "output/budget_1p5"
if not os.path.exists( dest ):
  os.makedirs( dest )

dfs = {}
for s in sm.series:
  dfs[s] = pd.read_csv( source + "/" + s + ".csv",
                        encoding = "utf-16" )

# compute aggregated item code (ic) columns
# dfs_ic = codes.aggregated_item_codes( dfs )

dfs_ic = {}
for (s,regex) in [ ("ingresos"      , codes.ingresos),
                   ("inversion"     , codes.two_subcodes),
                   ("funcionamiento", codes.funcionamiento) ]:
  dfs_ic[s] = codes.match_budget_codes(
    dfs[s], regex )
  if True: # These tests aren't very tight.
    assert ( len( dfs[s] ) > # Ensure the data shrank.
             len( dfs_ic[s] ) )
    if s == "funcionamiento":
      kept = dfs_ic[s]["item code"].unique()
      assert len(kept) == 1 # Ensure we only kept one code in "funcionamiento.csv"
      assert kept[0] == "1" # Ensure that it's the total ingresos code.

tests.column_names_after_agg( dfs_ic )

# TODO ? The following 2 tests broke once we switched budget item specs --
# specifically, because we now use codes.match_budget_codes()
# rather than codes.aggregated_item_codes().
# 
# tests.row_numbers_after_keeping_only_relevant_item_codes( dfs_ic )
# tests.types_and_missings_for_data_after_adding_item_code_columns( dfs_ic )

for s in sm.series:
  dfs_ic[s].to_csv( dest + "/" + s + ".csv",
                    encoding="utf-16",
                    index = False )

