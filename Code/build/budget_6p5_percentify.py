# PURPOSE:
# Switch from two series to four:
#   Initial 2: gastos, ingresos
#   Final 4: gastos, gastos-pct, ingresos, ingresos-pct
#     In the -pct files, convert peso values to percentages.

if True:
  import os
  import pandas                                 as pd
  from   typing import List,Set,Dict
  #
  import Code.build.budget_6p5_percentify_defs  as lib
  import Code.common                            as c
  import Code.metadata.four_series              as s4
  import Code.metadata.two_series               as s2
  from   Code.util.percentify import percentify_columns


if True: # folders
  source = os.path.join ( c.outdata, "budget_6_deflate",
                          "recip-" + str(c.subsample) )
  dest   = os.path.join ( c.outdata, "budget_6p5_cull_and_percentify",
                          "recip-" + str(c.subsample) )
  if not os.path.exists ( dest ):
    os.makedirs (         dest )

spacetime = ["dept code","muni code","year"]

if True: # input data
  dfs = {}
  for s in s2.series:
    df = pd.read_csv (
      os.path.join ( source,
                     s.name + ".csv" ) )
    df = ( df # Reorder some columns, and in the case of the `gastos` data,
              # drop the "item total" columns.
           [spacetime + ["item categ"] + s.money_cols] )
    dfs[s.name] = df

for s in s2.series:
  # Add "ingresos-pct" and "gastos-pct" data sets to `dfs`,
  # in which the money columns have been percentified.
  df = dfs [s.name] . copy()
  df = ( df
         . groupby ( # TODO ? the `group_keys` option
                     # appears to have no effect (any longer?) here.
                     # Maybe it should be removed.
           spacetime,
           group_keys = False )
         . apply ( lambda df:
                   percentify_columns (
                     s.money_cols, df ) )
         . reset_index ( drop = True) )
  dfs[s.name + "-pct"] = df

for s in s2.series: # test the axes
  m = ( dfs [s.name] .          # money-valued
        sort_values ( spacetime ) .
        reset_index ( drop = True ) )
  p = ( dfs [s.name + "-pct"] . # "percentage of money"-valued
        sort_values ( spacetime ) .
        reset_index ( drop = True ) )
  assert m.columns.equals ( p.columns )     # same columns
  assert ( m [spacetime] . reset_index () . # same spacetime rows
           equals ( p [spacetime]
                    . reset_index () ) )

  # Verify that within each spacetime group,
  # sorting by the percentified or the non-percentified
  # money column has the same effect,
  # at least after reducing the gruop to a set of rows
  # over which all money (not percentage) values are unique.
  t = m.merge ( p,
                on = spacetime + ["item categ"] )
  t["index"] = t.index
  for c in s.money_cols:
    assert ( t . groupby ( spacetime )
             . apply ( lambda group :
                       lib.order_of_both_values_the_same (
                         unique_col = c + "_x",
                         other_col  = c + "_y",
                         df         = group ) )
             . all () )

for s in s4.series:
  dfs[s.name] . to_csv (
    os.path.join ( dest,
                   s.name + ".csv" ),
    index = False )
