import numpy  as np
import pandas as pd

import Code.build.sisfut_metadata as sm


def row_numbers_after_keeping_only_relevant_item_codes( dfs ):
  for (file,length) in [ ( "ingresos"      , 191767 ),
                         ( "inversion"     , 863226 ),
                         ( "funcionamiento", 261443 ) ]:
    assert len( dfs[file] ) == length

def column_names_after_agg( dfs ):
  for i in sm.series:
    assert ( list( dfs[i].columns ) ==
             ( sm.column_subsets_no_dups_short[i] +
               ["year"] ) )

def types_and_missings_for_data_after_adding_item_code_columns( dfs ):
  stats_ref, stats = ({},{})
  for s in ["ingresos"]:
    df = dfs[s]
    stats[s] = pd.DataFrame(
      { "dtype"   :     df.dtypes.astype( str ),
#        "min"     :     df.min(),# TODO : use, somehow
#        "max"     :     df.max(),# TODO : use, somehow
        "missing" : 1 - df.count() / len(df) } )
    stats_ref[s] = pd.concat(
      [ pd.read_csv( "Code/stats/raw/" + s + ".csv",
                     index_col = 0 ),
        pd.read_csv( "Code/stats/item_columns/" + s + ".csv",
                     index_col = 0 ) ] ,
      axis = "rows" )
    assert ( (  stats_ref[s]["dtype"]  )
             == (stats[s]["dtype"]  ) ) . all()
    assert ( (2*stats_ref[s]["missing"])
             >= (stats   [s]["missing"]) ) . all()

