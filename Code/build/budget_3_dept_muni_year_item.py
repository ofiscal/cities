# PURPOSE:
#  (1) Aggregate spending observations by summing within
#    (place,year,item code) triples,
#    using the broad item categories from classify_budget_codes.py
#    Why: Although for most of the data, a given (place, year, item)
#    triple identifies exactly one row, sometimes it does not,
#    because spending on an item can be divided by fuente and ejecutor,
#    as demonstrated in explore/duplicate_rows.py.
#  (2) Replace missing muni values with 0,
#    because rows with a missing group variable disappear
#    upon using pandas.DataFrame.groupby().
#  (3) Subtract ingresos category TI.A.2.6 (transferencias)
#    from TI.A (propios).
#
#    TODO: What is (3) for?
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
  budget_key = pd.read_csv (
    os.path.join ( c.outdata,
                   "keys",
                   "budget.csv" ) )
  source = os.path.join ( c.outdata,
                          "budget_2_subsample",
                          "recip-" + str(c.subsample) )
  dest   = os.path.join ( c.outdata,
                          "budget_3_dept_muni_year_item",
                          "recip-" + str(c.subsample) )
  if not os.path.exists( dest ):
    os.makedirs(         dest )
  dfs0, dfs1, dfs2 = {}, {}, {} # input, midput, output
  spacetime = ["muni code","dept code","year"]


######
###### Build
######

# dfs0: read data
for s in [t.ingresos,t.gastos]:
  dfs0[s] = pd.read_csv (
    os.path.join ( source,
                   s + ".csv" ) )

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
  df = util.to_front ( # aggregate within item categories
    spacetime + ["item categ"],
    ( df . # PITFALL: This causes no change in the number of ingresos rows,
           # but the number of gastos falls to around 1/10 of what it was.
           # This can be checked thus:
           #   [ [ (k, df.shape) for k,df in d.items() ]
           #     for d in [dfs0, dfs1] ]
      groupby ( by = spacetime + ["item categ"] ) .
      sum ( numeric_only = True ) .
      reset_index () ) )
  dfs1[s] = df

# dfs2: For ingresos only, for each spacetime slice,
# we must subtract the "recaudo" value in the row where categ = "transfers"
# from the "recaudo" value in the row where categ = "propios".
# The function `tax_categ_subtract` permits that.
if True:
  def tax_categ_subtract (
      # PITFALL: The "x" below is a particular type of string:
      # it must be one of the values appearing in
      # the column named `categ` (the third argument).
      subtract      : "x",         # the categ value of rows to subtract
      subtract_from : "x",         # the categ value of rows to subtract from
      new_name      : "x",         # What to call subtract_from
                                   # after subtracting from it
      categ         : str,         # the name of an "x"-valued column
      valueCols     : List[str],   # the name of a peso-valued column
      df0           : pd.DataFrame # a single muni-dept-year cell
      ) -> pd.DataFrame:
    df = df0.copy()
    for value in valueCols:
      subtract_vec = ( df[ df[categ] == subtract ]
                       [value] )
      if len(subtract_vec) < 1: pass
      else: # There should be at most 1 row where categ = subtract.
        assert len(subtract_vec) == 1
        subtract_float = float ( subtract_vec.iloc [0] )
        df.loc[ df[categ] == subtract_from,
                value ] = ( # the subtraction
                  df.loc [ df[categ] == subtract_from,
                           value ]
                  - subtract_float )
        df.loc[ df[categ] == subtract_from,
                categ ] = new_name # the renaming
    return df

  if True: # test it on fake data
    x = pd.DataFrame( { "cat" : [ "1", "2", "3"],
                        "val" : [ 11,  12,  13 ] } )
    assert ( tax_categ_subtract( "1", "2", "2.1", "cat", ["val"], x ) .
             # Subtract val at row where cat=1 from val at row where cat=2.
             equals(
               pd.DataFrame( { "cat" : ["1",  "2.1", "3"],
                               "val" : [ 11, 1, 13 ] } ) ) )
    assert ( tax_categ_subtract( "0", "2", "2", "cat", ["val"], x ) .
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
             subtract_from = t.corrientes,
             new_name = t.propios,
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
    acc = pd.concat( [ acc,
                       tax_categ_subtract(
                         subtract      = t.transfer,
                         subtract_from = t.corrientes,
                         new_name      = t.propios,
                         categ = "item categ",
                         valueCols = s2.ingresos.money_cols,
                         df0   = df ) ] )
  dfs2[t.ingresos] = acc

if True: # Test (loosely) that it worked.
         # Recall that `acc` is defined after and using `ing`.
  accTest = acc . sort_values(spacetime) . reset_index(drop=True) . copy()
  ingTest = ing . sort_values(spacetime) . reset_index(drop=True) . copy()
  ingTest.loc [
    # Until this is done, the non-money columns of accTest and ingTest differ.
    ingTest["item categ" ] == t.corrientes,
    "item categ" ] = \
      t.propios
  assert ( # Their non-money columns are now equal.
    accTest.drop ( columns = s2.ingresos.money_cols ) .
    equals (
      ingTest.drop ( columns = s2.ingresos.money_cols ) ) )
  for c in s2.ingresos.money_cols:
    assert (accTest[c]  < ingTest[c]).any() # Some are smaller.
    assert (accTest[c] <= ingTest[c]).all() # None are bigger.


######
###### Test, output
######

for s in [t.ingresos, t.gastos]:
  dfs2 [s] . to_csv (
    os.path.join ( dest,
                   s + ".csv" ),
    index = False )
