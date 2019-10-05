# Late in the process we decided to add servicio de deuda as another gasto.

import pandas as pd

source = "data/sisfut/csv"
late = pd.read_csv( source + "/2018_deuda.csv" )
early = pd.read_csv( source + "/2012_deuda.csv" )

(late.columns == early.columns).all()

for i in late.columns: print(i)

spending_dict =  {
    "Presupuesto Inicial"    : "item init",
    "Presupuesto Definitivo" : "item def",
    "Compromisos"            : "item comp",
    "Obligaciones"           : "item oblig",
    "Pagos"                  : "item pagos" }

assert ( len(set.intersection( set( spending_dict.keys() ),
                               set(late.columns) ) )
         == len( spending_dict.keys() ) )

