# This adds regalias to the ingresos data.
# It just copies the gastos data unchanged to a new directory --
# CPU-inefficient, yes, but safer than doing something more confusing.

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ser

if True: # bearings
  source = "output/budget_4_scaled/recip-"       + str(c.subsample)
  dest   = "output/budget_5_add_regalias/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input
  dfsi = {}
  for s in ser.series:
    dfsi[s.name] = pd.read_csv( source + "/" + s.name + ".csv" )
  regalias = (
    pd.read_csv( "output/regalias.csv" ) .
    rename( columns = { "regalias" :
                        ser.series_dict["ingresos"].pesos_col } ) )
  regalias      ["item categ"] = "regalias"

if True: # output
  dfso = {}
  dfso["gastos"] = dfsi["gastos"]
  dfso["ingresos"] = pd.concat(
    [ dfsi["ingresos"],
      regalias ],
    sort = True, # sort columns by name so they align
    axis = "rows" )
  for s in ser.series:
    dfso[s.name].to_csv(
      dest + "/" + s.name + ".csv",
      index = False )

