# This adds regalias to the ingresos data.
# It just copies the gastos data unchanged to a new directory --
# CPU-inefficient, yes, but safer than doing something more confusing.

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.terms as t
  import Code.metadata.two_series as ser


if True: # bearings
  source = "output/budget_4_scaled/recip-"       + str(c.subsample)
  dest   = "output/budget_5_add_regalias/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input
  dfsi = {}
  for s in ser.series:
    dfsi[s.name] = pd.read_csv (
      os.path.join ( source,
                     s.name + ".csv" ) )
  regalias = pd.read_csv ( "output/regalias.csv" )

if True: # Adjust regalias.
  if c.subsample > 1: # Discard some regalias rows if needed.
    if True: # Find all the relevant (dept,muni) pairs.
      df = dfsi[s.name] # For extracting (dept, muni) pairs,
                        # any member of dfsi is equivalent.
      places = set(
        df[["dept code","muni code"]] .
        groupby( ["dept code","muni code"] ) .
        apply( lambda df: df.iloc[0] ) .
        reset_index( drop=True ) .
        apply( lambda row: ( row["dept code"],
                             row["muni code"] ),
               axis = "columns" ) )
    if True: # Discard irrelevant regalias observations.
      regalias["keeper"] = (
        regalias.apply( ( lambda row:
                          (row["dept code"], row["muni code"])
                          in places ),
                        axis = "columns" ) )
      regalias = regalias[ regalias["keeper"] ]
      regalias = regalias.drop( columns = "keeper" )
  if True: # Define money_cols.
    for c in ser.ingresos.money_cols:
      regalias[c] = regalias["regalias"]
    regalias = regalias.drop( columns = ["regalias"] )
  regalias["item categ"] = t.regalias

if True: # output
  dfso = {}
  dfso["gastos"] = dfsi["gastos"]
  dfso["ingresos"] = pd.concat(
    [ dfsi["ingresos"],
      regalias ],
    sort = True, # Sort columns by name so they align.
    axis = "rows" )
  for s in ser.series:
    dfso[s.name].to_csv(
      dest + "/" + s.name + ".csv",
      index = False )
