# for Santander in 2014
# summed from the spreadsheet by hand, I get    2.890769e12
# But what I see after budget_5_add_regalias is 2.606003e12.
#
# The culprit seems to be that the number 285604743.385
# is being read by Python with a decimal point,
# and written by OpenOffice without one.
# But in the original data, the decimal point is there,
# so the code is okay.

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ser

regalias = (
    pd.read_csv( "output/regalias.csv",
                 encoding="utf-8" ) .
    rename( columns = { "regalias" :
                        ser.series_dict["ingresos"].pesos_col } ) )

regalias.to_csv( "output/regalias-utf-8.csv" )

if True: # sum muni-regalias to the dept level
  dept_regalias = (
    regalias . copy() .
    groupby( ["dept code","year"] ) .
    agg( sum ) .
    reset_index() )
  dept_regalias["muni code"] = -1

# dept code 68 is for Santander
d = dept_regalias[ (dept_regalias["dept code"] == 68) &
                   (dept_regalias["year"] == 2014) ]
r = regalias[ (regalias["dept code"] == 68) &
              (regalias["year"] == 2014) ]
r["item recaudo"].to_csv( "what the heck.csv" )
