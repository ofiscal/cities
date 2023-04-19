# PURPOSE:
#  (1) Aggregate spending observations within
#    (muni,year,item code) triples,
#    using the broad item categories from classify_budget_codes.py
#    Why: For most of the data, a given (muni, year, item)
#    triple identifies exactly one row -- but sometimes it does not,
#    because spending on an item can be divided by fuente and ejecutor,
#    as demonstrated in explore/duplicate_rows.py.
#  (2) Replace missing muni values with 0,
#    because rows with a missing group variable disappear
#    upon using pandas.DataFrame.groupby().
#  (3) Subtract ingresos category TI.A.2.6 (transferencias)
#    from TI.A (propios).
#    TODO: What is this for?
#    I understand that T1.A includes T1.A.2.6,
#    and that apparently we don't want it to.
#    But why not? What *are* those things, even?
#    And do they still (in 2023)
#    mean what they used to mean (in 2019)?

if True:
  from typing import List, Set, Dict
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.util.misc as util
  import Code.build.classify_budget_codes as codes
  import Code.metadata.terms as t
  import Code.metadata.two_series as s2


if True:
  budget_key = pd.read_csv( "output/keys/budget.csv" )
  source = "output/budget_2_subsample/recip-"           + str(c.subsample)
  dest   = "output/budget_3_dept_muni_year_item/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )
  dfs0, dfs1, dfs2 = {}, {}, {} # input, midput, output
  spacetime = ["muni code","dept code","year"]


######
###### Build
######

# dfs0: read data
for s in [t.ingresos,t.gastos]:
  dfs0[s] = pd.read_csv( source + "/" + s + ".csv" )

# dfs1: fill NaN values in muni with 0,
# create "item categ" and drop "item code",
# aggregate within spacetime-categ cells
for s in [t.ingresos,t.gastos]:
  df = dfs0[s].copy()
  if True: # manip indiv columns
    df["muni code"] = ( df["muni code"] .
                        fillna(0) )
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
      # TODO : What black magic did I have in mind when I wrote
      # that two of the following arguments have the type "x"?
      # It might relate to the type variables in the definition of
      #   `Code.build.classify_budget_codes.invert_many_to_one_dict`.
      subtract : "x",        # the categ value of rows to subtract
      subtract_from : "x",   # the categ value of rows to subtract from
      categ : str,           # the name of an "x"-valued column
      valueCols : List[str], # the name of a peso-valued column
      df0 : pd.DataFrame     # a single muni-dept-year cell
      ) -> pd.DataFrame:
    df = df0.copy()
    for value in valueCols:
      subtract_vec = (df[ df[categ] == subtract ]
                      [value] )
      if len(subtract_vec) < 1: pass
      else:
        assert len(subtract_vec) == 1
        df.loc[ df[categ] == subtract_from,
                value ] = (
          df.loc[ df[categ] == subtract_from,
                  value ] -
          float( subtract_vec ) )
    return df
  if True: # test it on fake data
    x = pd.DataFrame( { "cat" : [ "1", "2", "3"],
                        "val" : [ 11,  12,  13 ] } )
    assert ( tax_categ_subtract( "1", "2", "cat", ["val"], x ) .
             # Subtract val at row where cat=1 from val at row where cat=2.
             equals(
               pd.DataFrame( { "cat" : ["1",  "2", "3"],
                               "val" : [ 11.0, 1.0, 13.0 ] } ) ) )
    assert ( tax_categ_subtract( "0", "2", "cat", ["val"], x ) .
             # The subtract code ("0") is not present, so `x` is unchanged.
             equals( x ) )

if False: # TODO ? This approach, using .groupby(),
  # is more natural, and ought to give the same result as the next one,
  # in which I for-loop through all spots in spacetime and accumulate.
  # Instead it has no effect.
  dfs2 [t.gastos] = dfs1[t.gastos] # pointer equality is fine here
  dfs2 [t.ingresos] = (
    dfs1 [t.ingresos] . copy() .
    groupby( spacetime ) .
    apply( lambda df :
           tax_categ_subtract(
             subtract      = t.transfer,
             subtract_from = t.propios,
             categ = "item categ",
             value = "item recaudo",
             df0   = df ) ) .
    reset_index( drop=True ) )
  if True: # test that it worked
    before = dfs1[t.ingresos].sort_values(spacetime).reset_index(drop=True)
    after = dfs2[t.ingresos].sort_values(spacetime).reset_index(drop=True)
    assert ( not     before["item recaudo"] .
             equals( after ["item recaudo"] ) )
    pd.concat( [before["item recaudo"],
                after["item recaudo"]], axis = "columns" )

if True: # accumulate (in acc) a data frame like df but
         # having applied tax_categ_subtract() to each spacetime slice
  dfs2 [t.gastos] = dfs1[t.gastos] # pointer equality is fine for gastos;
    # this section is only supposed to change the ingresos data
  ing             = dfs1[t.ingresos]
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
        subtract      = t.transfer,
        subtract_from = t.propios,
        categ = "item categ",
        valueCols = s2.ingresos.money_cols,
        df0   = df ) )
  dfs2[t.ingresos] = acc

if True: # test (loosely) that it worked
  acc = acc . sort_values(spacetime) . reset_index(drop=True)
  ing = ing . sort_values(spacetime) . reset_index(drop=True)
  assert ( acc.drop( columns = s2.ingresos.money_cols ) .
           equals(
             ing.drop( columns = s2.ingresos.money_cols ) ) )
  for c in s2.ingresos.money_cols:
    assert (acc[c]  < ing[c]).any()
    assert (acc[c] <= ing[c]).all()


######
###### Test, output
######

for s in [t.ingresos,t.gastos]:
  dfs2[s].to_csv( dest + "/" + s + ".csv" ,
                  index = False )
