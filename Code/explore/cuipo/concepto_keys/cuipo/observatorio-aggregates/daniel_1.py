import pandas as pd

# Remove the "big categories" column (ingreso or gasto),
# and reorders columns and rows.

i = pd.read_excel ( "daniel/orig-xlsx/ingresos.xlsx" )
i = ( i [[ "observatorio name",
           "item code",
           "item",
          ]]
      . sort_values ( [ "observatorio name",
                        "item code"] ) )
i.to_csv ( "daniel/ingresos.csv",
           index = False )

g = pd.read_excel ( "daniel/orig-xlsx/gastos.xlsx" )
g = ( g [[ "observatorio name",
           "item code",
           "item",
          ]]
      . sort_values ( [ "observatorio name",
                        "item code" ] ) )
g.to_csv ( "daniel/gastos.csv",
           index = False )
