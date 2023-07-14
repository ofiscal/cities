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

#g22_2 = pd.read_csv (
#  path.join ( "data/cuipo/2022",
#              "Ejecucion_GastosDic2022.csv" ) )


### Convert gastos from xlsx to csv

i22 = pd.read_excel (
  path.join ( "data/cuipo/2022",
              "Ejecucion_IngresosDic2022.xlsx" ) )

i22.to_csv (
  path.join ( "data/cuipo/2022",
              "Ejecucion_IngresosDic2022.csv" ),
  index = False )

#i22_2 = pd.read_csv (
#  path.join ( "data/cuipo/2022",
#              "Ejecucion_IngresosDic2022.csv" ) )
