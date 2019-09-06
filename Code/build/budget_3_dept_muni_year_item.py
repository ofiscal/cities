# What this does: aggregate spending observations
#   within (muni,year,item code) triples,
#   using the broad item categories defined in classify_budget_codes.py
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
  import Code.build.classify_budget_codes as codes
  import Code.build.sisfut_metadata as sm

if True:
  budget_key = pd.read_csv( "output/keys/budget.csv",
                            encoding = "utf-16" )
  source = "output/budget_2_subsample/recip-"      + str(c.subsample)
  dest   = "output/budget_3_dept_muni_year_item/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )
  dfs0, dfs1 = {}, {} # input and output
  group_vars = ["muni code","dept code","year","item categ"]


######
###### Build
######

for s in ["ingresos","gastos"]:
  dfs0[s] = pd.read_csv( source + "/" + s + ".csv",
                        encoding = "utf-16" )
  df = dfs0[s]
  if True: # manip indiv columns
    df["muni code"] = ( df["muni code"] .
                        fillna(-1) )
    df["item categ"] = (
      df["item code"] .
      astype(str) .
      apply( lambda c: codes.codes_to_categs[c] ) )
    df = df.drop( columns = ["item code"] )
  df = util.to_front( # aggregate within item categories
    group_vars,
    ( df .
      groupby( by = group_vars ) .
      agg( sum ) .
      reset_index() .
      sort_values( group_vars ) ) )
  dfs1[s] = df

if True: # for ingresos data, subtract transfers from recursos propios
  def tax_categ_fix (
      subtract : "x",      # the categ value of rows to subtract
      subtract_from : "x", # the categ value of rows to subtract from
      categ : str, # the name of an "x"-valued column
      value : str, # a peso-valued column
      df0 : pd.DataFrame
      ) -> pd.DataFrame:
    """ In a given (muni,dept,year) frame,
    the peso-valued column in the row for which categ =
    recursos propios is too big.
    From it we must subtract the value in the peso-valued column
    in the row where categ = transferencias.
    This function generalizes that problem. """
    df = df0.copy()
    subtract_vec = (df[ df[categ] == subtract ]
                    [value] )
    assert len(subtract_vec) == 1
    df.loc[ df[categ] == subtract_from,
            value ] = (
      df.loc[ df[categ] == subtract_from,
              value ] -
      float( subtract_vec ) )
    return df
  if True: # test it
    x = pd.DataFrame( { "cat" : ["1", "2", "3"],
                        "val" : [ 1,   2,   3 ] } )
    assert ( tax_categ_fix( "1", "2", "cat", "val", x ) .
             equals(
               pd.DataFrame( { "cat" : ["1", "2", "3"],
                               "val" : [ 1.0, 1.0, 3.0 ] } ) ) )
  assert "TODO: resume here" == False

######
###### Test, output
######

for s in ["ingresos","gastos"]:
  print( len(dfs0[s]), len(dfs1[s]) )

for s in ["ingresos","gastos"]:
  df.to_csv( dest + "/" + s + ".csv" ,
             encoding="utf-16",
             index = False )
