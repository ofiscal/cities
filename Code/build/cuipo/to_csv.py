# CUIPO provides data in .xlsx format.
# This converts that data to .csv format.

from   os import path
import pandas as pd


### Convert gastos from xlsx to csv

g22 = pd.read_excel (
  path.join ( "data/cuipo/2022",
              "Ejecucion_GastosDic2022.xlsx" ) )

g22.to_csv (
  path.join ( "data/cuipo/2022",
              "Ejecucion_GastosDic2022.csv" ),
  index = False )


### Convert gastos from xlsx to csv

i22 = pd.read_excel (
  path.join ( "data/cuipo/2022",
              "Ejecucion_IngresosDic2022.xlsx" ) )

i22.to_csv (
  path.join ( "data/cuipo/2022",
              "Ejecucion_IngresosDic2022.csv" ),
  index = False )

if False: # For interactive testing
  # Almost everything is equal, i.e. unchanged by the formatting.
  # The one field that is an exception, "22_BPIN" in "gastos",
  # is irrelevant to this analysis. (It's a type casting glitch,
  # not a data corruption one.)
  res = {}
  for excel, slang_name, filename in [
      (g22, "gastos",   "Ejecucion_GastosDic2022"),
      (i22, "ingresos", "Ejecucion_IngresosDic2022") ]:
    csv = pd.read_csv (
      path.join ( "data/cuipo/2022",
                  filename + ".csv" ) )
    res[slang_name] = pd.Series (
      { c : ( excel[c]
              . equals ( csv[c] ) )
        for c in set ( list(excel.columns) +
                       list(csv.columns) ) } )
