# Definitions to know when manipulating the SISFUT data.
# Nothing defined here is a function -- it's all data
# (specifically folder locations and column names).

from itertools import chain

series = ["ingresos","inversion","funcionamiento"]

source_folder = "data/sisfut/"
column_subsets = {
  "ingresos" : [
#      "Código FUT"
      "Nombre Entidad"
    , "Cód. DANE Departamento"
    , "Nombre DANE Departamento"
    , "Cód. DANE Municipio"
    , "Nombre DANE Municipio"
    , "Código Concepto"
    , "Concepto"
    , "Presupuesto Inicial"
    , "Presupuesto Definitivo"
    , "Recaudo"
    , "Total Ingresos"
  ] ,
  "inversion" : [
#     "Código FUT"
      "Nombre Entidad"
    , "Cód. DANE Departamento"
    , "Nombre DANE Departamento"
    , "Cód. DANE Municipio"
    , "Nombre DANE Municipio"
    , "Código Concepto"
    , "Concepto"
#    , "Código Fuentes De Financiación"
#    , "Fuentes de Financiación"
    , "Presupuesto Inicial"
    , "Presupuesto Definitivo"
    , "Compromisos"
    , "Obligaciones"
    , "Pagos"
  ] ,
  "funcionamiento" : [
#      "Código FUT"
      "Nombre Entidad"
    , "Cód. DANE Departamento"
    , "Nombre DANE Departamento"
    , "Cód. DANE Municipio"
    , "Nombre DANE Municipio"
    , "Código Concepto"
    , "Concepto"
#    , "Código Fuente Financiación"
#    , "Fuente Financiación"
    , "Presupuesto Inicial"
    , "Presupuesto Definitivo"
    , "Compromisos"
    , "Obligaciones"
    , "Pagos"
] }

duplicative_columns = [
#    ("Código FUT", "Nombre Entidad" )
    ("Cód. DANE Departamento", "Nombre DANE Departamento" )
  , ("Cód. DANE Municipio", "Nombre DANE Municipio" )
  , ("Código Concepto", "Concepto" )
#  , ("Código Fuente Financiación", "Fuente Financiación" )
#  , ("Código Fuentes De Financiación", "Fuentes de Financiación" )
  ]
duplicative_columns_set = set(
  # chain.from_iterable concatenates these 2-element lists
  chain.from_iterable( [ [ c[0], c[1] ]
                         for c in duplicative_columns ] ) )
omittable_columns = set( map( lambda x: x[1]
                            , duplicative_columns ) )
