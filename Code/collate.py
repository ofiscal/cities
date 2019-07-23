import numpy as np
import pandas as pd

column_subsets = {
  "ingresos" : [
      "Código FUT"
    , "Nombre Entidad"
    , "Cód. DANE Departamento"
    , "Nombre DANE Departamento"
    , "Cód. DANE Municipio"
    , "Nombre DANE Municipio"
    , "Código Concepto"
    , "Concepto"
    , "Presupuesto Inicial"
    , "Presupuesto Definitivo"
    , "Recaudo"
    , "Total Ingresos" ]
  , "inversion" : [
      "Código FUT"
    , "Nombre Entidad"
    , "Cód. DANE Departamento"
    , "Nombre DANE Departamento"
    , "Cód. DANE Municipio"
    , "Nombre DANE Municipio"
    , "Código Concepto"
    , "Concepto"
    , "Código Fuentes De Financiación"
    , "Fuentes de Financiación"
    , "Presupuesto Inicial"
    , "Presupuesto Definitivo"
    , "Compromisos"
    , "Obligaciones"
    , "Pagos" ]
  , "funcionamiento" : [
      "Código FUT"
    , "Nombre Entidad"
    , "Cód. DANE Departamento"
    , "Nombre DANE Departamento"
    , "Cód. DANE Municipio"
    , "Nombre DANE Municipio"
    , "Código Concepto"
    , "Concepto"
    , "Código Fuente Financiación"
    , "Fuente Financiación"
    , "Presupuesto Inicial"
    , "Presupuesto Definitivo"
    , "Compromisos"
    , "Obligaciones"
    , "Pagos" ]
}

source_folder = "data/sisfut/"
dfs = {}
for series in ["ingresos","inversion","funcionamiento"]:
  dfs[ series ] = pd.DataFrame()
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv( source_folder + "original_csv/"
                           + str(year) + "_" + series + ".csv"
                         , usecols = column_subsets[series]
                         , nrows = 100 # TODO : DROP THIS LINE eventually
    )
    dfs[ series ] = dfs[ series ].append( shuttle )
  dfs[ series ].to_csv( source_folder + "collated-subsets/"
                        + series + ".csv"
                      , index = False)
