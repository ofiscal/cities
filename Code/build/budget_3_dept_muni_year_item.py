# What this does: aggregate spending observations
#   within (muni,year,item code) triples,
#   using the broad item categories defined in classify_budget_codes.py
#   It also replaces missing muni values with -1,
#   because rows with a missing group variable disappear
#   upon using pandas.DataFrame.groupby().
#
# Why aggregate: For most of the data, a given (muni, year, item)
#   triple identifies exactly one row -- but sometimes it does not,
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
  dfs0, dfs1, dfs2 = {}, {}, {} # input, midput, output
  spacetime = ["muni code","dept code","year"]


######
###### Build
######

# dfs0: read data
for s in ["ingresos","gastos"]:
  dfs0[s] = pd.read_csv( source + "/" + s + ".csv",
                        encoding = "utf-16" )

# dfs1: fill NaN values in muni with -1,
# create "item categ" and drop "item code",
# aggregate within spacetime-categ cells
for s in ["ingresos","gastos"]:
  dfs1[s] = dfs0[s].copy()
  df = dfs1[s]
  if True: # manip indiv columns
    df["muni code"] = ( df["muni code"] .
                        fillna(-1) )
    df["item categ"] = (
      df["item code"] .
      astype(str) .
      apply( lambda c: codes.codes_to_categs[c] ) )
    df = df.drop( columns = ["item code"] )
  df = util.to_front( # aggregate within item categories
    spacetime + ["item categ"],
    ( df .
      groupby( by = spacetime + ["item categ"] ) .
      agg( sum ) .
      reset_index() ) )

# dfs2: For ingresos only, for each spacetime slice,
# subtract the "recaudo" value in the row where categ = "transfers"
# from the "recaudo" value in the row where categ = "propios".
if True:
  def tax_categ_subtract (
      subtract : "x",      # the categ value of rows to subtract
      subtract_from : "x", # the categ value of rows to subtract from
      categ : str, # the name of an "x"-valued column
      value : str, # the name of a peso-valued column
      df0 : pd.DataFrame # a single muni-dept-year cell
      ) -> pd.DataFrame:
    df = df0.copy()
    subtract_vec = (df[ df[categ] == subtract ]
                    [value] )
    if len(subtract_vec) < 1: return df
    assert len(subtract_vec) == 1
    if True: # debugging
      print( "\nOld df:\n", df )
      print( "subtract from: ",
             df.loc[ df[categ] == subtract_from, value ] )
      print( "subtract: ", subtract_vec )
      print( "result: ", (
        df.loc[ df[categ] == subtract_from,
                value ] -
        float( subtract_vec ) ) )
    df.loc[ df[categ] == subtract_from,
            value ] = (
      df.loc[ df[categ] == subtract_from,
              value ] -
      float( subtract_vec ) )
    print( "New df:\n", df )
    return df
  if True: # test it on fake data
    x = pd.DataFrame( { "cat" : [ "1", "2", "3"],
                        "val" : [ 11,  12,  13 ] } )
    assert ( tax_categ_subtract( "1", "2", "cat", "val", x ) .
             # subtract val at row where cat=1 from val at row where cat=2
             equals(
               pd.DataFrame( { "cat" : ["1",  "2", "3"],
                               "val" : [ 11.0, 1.0, 13.0 ] } ) ) )
    assert ( tax_categ_subtract( "0", "2", "cat", "val", x ) .
             # here the subtract code ("0") is not present
             equals( x ) )

if True: # test it on one spacetime slice of the real data
  s = "ingresos"
  spot = dfs1[s][spacetime].iloc[0]
  df1 = dfs1[s][ (dfs1[s][spacetime] == spot).transpose().all() ]
  df2 = tax_categ_subtract(
    subtract = "Por transferencias de la Nación",
    subtract_from = "Por recursos propios",
    categ = "item categ",
    value = "item recaudo",
    df0 = df1 )
  assert ( (df1["item recaudo"] > df2["item recaudo"]) .
           any() )
  assert (         df1.drop(columns = ["item recaudo"] ) .
           equals( df2.drop(columns = ["item recaudo"] ) ) )
  # del( s, spot, df1, df2 )

if True:
  dfs2 ["gastos"] = dfs1["gastos"] # pointer equality is fine for gastos;
    # this section is only supposed to change the ingresos data
  spots = ( dfs1["ingresos"][spacetime] .
            groupby(spacetime) .
            agg( 'first' ) .
            reset_index() )
  acc = pd.DataFrame()
  ing = dfs1["ingresos"]
  for spot in spots.index:
    df = ing[ (ing[spacetime] == spots.iloc[spot]).all( axis="columns") ]
    acc = acc.append( 
      tax_categ_subtract(
        subtract = "Por transferencias de la Nación",
        subtract_from = "Por recursos propios",
        categ = "item categ",
        value = "item recaudo",
        df0 = df ) )

acc = acc . sort_values(spacetime) . reset_index(drop=True)
ing = ing . sort_values(spacetime) . reset_index(drop=True)
assert (acc["item recaudo"] < ing["item recaudo"]).any()
(acc == ing).all()

if True: # do it to all the (applicable) real data
  dfs2 ["gastos"] = dfs1["gastos"] # pointer equality is fine here
  dfs2 ["ingresos"] = (
    dfs1 ["ingresos"] . copy() .
    groupby( spacetime ) .
    apply( lambda df :
           tax_categ_subtract(
             subtract = "Por transferencias de la Nación",
             subtract_from = "Por recursos propios",
             categ = "item categ",
             value = "item recaudo",
             df0 = df ) ) .
    reset_index( drop=True ) )


######
###### Test, output
######

for s in ["ingresos","gastos"]:
  df.to_csv( dest + "/" + s + ".csv" ,
             encoding="utf-16",
             index = False )
