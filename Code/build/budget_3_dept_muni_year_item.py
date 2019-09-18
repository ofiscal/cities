# What this does:
#  (1) Aggregate spending observations within
#    (muni,year,item code) triples,
#    using the broad item categories from classify_budget_codes.py
#    Why: For most of the data, a given (muni, year, item)
#    triple identifies exactly one row -- but sometimes it does not,
#    because spending on an item can be divided by fuente and ejecutor,
#    as demonstrated in explore/duplicate_rows.py.
#  (2) Replace missing muni values with -1,
#    because rows with a missing group variable disappear
#    upon using pandas.DataFrame.groupby().
#  (3) Subtract ingresos category TI.A.2.6 (transferencias)
#    from TI.A (propios).

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.util as util
  import Code.build.classify_budget_codes as codes
  import Code.metadata.four_series as sm


if True:
  budget_key = pd.read_csv( "output/keys/budget.csv",
                            encoding = "utf-8" )
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
                        encoding = "utf-8" )

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
  dfs1[s] = df

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
    if False: # debugging
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
    if False: # debugging
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

if False: # TODO ? This approach, using .groupby(),
  # is more natural, and ought to give the same result as the next one,
  # in which I for-loop through all spots in spacetime and accumulate.
  # Instead it has no effect.
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
  if True: # test that it worked
    before = dfs1["ingresos"].sort_values(spacetime).reset_index(drop=True)
    after = dfs2["ingresos"].sort_values(spacetime).reset_index(drop=True)
    assert ( not     before["item recaudo"] .
             equals( after ["item recaudo"] ) )
    pd.concat( [before["item recaudo"],
                after["item recaudo"]], axis = "columns" )

if True:
  dfs2 ["gastos"] = dfs1["gastos"] # pointer equality is fine for gastos;
    # this section is only supposed to change the ingresos data
  ing             = dfs1["ingresos"]
  spots = ( ing[spacetime] .
            groupby(spacetime) .
            agg( 'first' ) .
            reset_index() )
  acc = pd.DataFrame()
  for spot in spots.index:
    df = ing[ (ing[spacetime] == spots.iloc[spot]) .
              all( axis="columns") ]
    acc = acc.append( 
      tax_categ_subtract(
        subtract = "Por transferencias de la Nación",
        subtract_from = "Por recursos propios",
        categ = "item categ",
        value = "item recaudo",
        df0 = df ) )
  dfs2["ingresos"] = acc

if True: # test (loosely) that it worked
  acc = acc . sort_values(spacetime) . reset_index(drop=True)
  ing = ing . sort_values(spacetime) . reset_index(drop=True)
  assert (acc["item recaudo"] < ing["item recaudo"]).any()
  assert (acc["item recaudo"] <= ing["item recaudo"]).all()
  assert (         acc.drop(columns=["item recaudo"]) .
           equals( ing.drop(columns=["item recaudo"]) ) )


######
###### Test, output
######

for s in ["ingresos","gastos"]:
  dfs2[s].to_csv( dest + "/" + s + ".csv" ,
                  encoding="utf-8",
                  index = False )
