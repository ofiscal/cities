# Definitions to know when manipulating the SISFUT data.
# Nothing defined here is a function -- it's all data,
# specifically folder locations and column names.

from itertools import chain
import Code.metadata.terms as t


series = [t.ingresos,
          t.inversion,
          t.funcionamiento,
          t.deuda]

columns_peso = {
  "ingresos" : [
      ("Total Ingresos"         , "item total")
    # , ("Presupuesto Definitivo" , "item def")
    # , ("Recaudo"                , "item recaudo")
    # , ("Presupuesto Inicial"    , "item init")
  ], "inversion" : [
      ("Obligaciones"           , "item oblig")
    # , ("Presupuesto Inicial"    , "item init")
    # , ("Presupuesto Definitivo" , "item def")
    # , ("Compromisos"            , "item comp")
    # , ("Pagos"                  , "item pagos")
  ], "funcionamiento" : [
      ("Obligaciones"           , "item oblig")
    # , ("Presupuesto Inicial"    , "item init")
    # , ("Presupuesto Definitivo" , "item def")
    # , ("Compromisos"            , "item comp")
    # , ("Pagos"                  , "item pagos")
  ], "deuda" : [
      ("Obligaciones"           , "item oblig")
    # , ("Presupuesto Inicial"    , "item init")
    # , ("Presupuesto Definitivo" , "item def")
    # , ("Compromisos"            , "item comp")
    # , ("Pagos"                  , "item pagos")
  ] }

column_subsets = { # Columns that we might actually use.
  "ingresos" : [
    # "Código FUT"
      ("Nombre Entidad"           , "name")
    , ("Cód. DANE Departamento"   , "dept code")
    , ("Nombre DANE Departamento" , "dept")
    , ("Cód. DANE Municipio"      , "muni code")
    , ("Nombre DANE Municipio"    , "muni")
    , ("Código Concepto"          , "item code")
    , ("Concepto"                 , "item")
    ] + columns_peso["ingresos"],
  "inversion" : [
    # "Código FUT"
      ("Nombre Entidad"           , "name")
    , ("Cód. DANE Departamento"   , "dept code")
    , ("Nombre DANE Departamento" , "dept")
    , ("Cód. DANE Municipio"      , "muni code")
    , ("Nombre DANE Municipio"    , "muni")
    , ("Código Concepto"          , "item code")
    , ("Concepto"                 , "item")
    # , "Código Fuentes De Financiación"
    # , "Fuentes de Financiación"
    ] + columns_peso["inversion"],
  "funcionamiento" : [
    # "Código FUT"
      ("Nombre Entidad"           , "name")
    , ("Cód. DANE Departamento"   , "dept code")
    , ("Nombre DANE Departamento" , "dept")
    , ("Cód. DANE Municipio"      , "muni code")
    , ("Nombre DANE Municipio"    , "muni")
    , ("Código Concepto"          , "item code")
    , ("Concepto"                 , "item")
    # , "Código Fuente Financiación"
    # , "Fuente Financiación"
    ] + columns_peso["funcionamiento"],
  "deuda" : [
    # "Código FUT"
      ("Nombre Entidad"           , "name")
    , ("Cód. DANE Departamento"   , "dept code")
    , ("Nombre DANE Departamento" , "dept")
    , ("Cód. DANE Municipio"      , "muni code")
    , ("Nombre DANE Municipio"    , "muni")
    , ("Código Concepto"          , "item code")
    , ("Concepto"                 , "item")
    # Código Tipo Deuda
    # Tipo Deuda
    # Código Tipo Operación
    # Tipo Operación
    # Código Fuente
    # Fuente
    ] + columns_peso["deuda"]
}

column_subsets_long, column_subsets_short = ({},{})
def fst(x): return x[0]
def snd(x): return x[1]
for s in series:
  column_subsets_long[s]  = list( map( fst, column_subsets[s] ) )
  column_subsets_short[s] = list( map( snd, column_subsets[s] ) )

duplicative_columns_long = [
#    ("Código FUT", "Nombre Entidad" )
    ("Cód. DANE Departamento", "Nombre DANE Departamento" )
  , ("Cód. DANE Municipio", "Nombre DANE Municipio" )
  , ("Código Concepto", "Concepto" )
#  , ("Código Fuente Financiación", "Fuente Financiación" )
#  , ("Código Fuentes De Financiación", "Fuentes de Financiación" )
  ]
duplicative_columns_long_set = set(
  # chain.from_iterable concatenates these 2-element lists
  chain.from_iterable( [ [ c[0], c[1] ]
                         for c in duplicative_columns_long ] ) )
omittable_columns_long = set( map( lambda x: x[1]
                            , duplicative_columns_long ) )

duplicative_columns_short = [
#    ("Código FUT", "Nombre Entidad" )
    ("dept code", "dept" )
  , ("muni code", "muni" )
  , ("item code", "item" )
#  , ("Código Fuente Financiación", "Fuente Financiación" )
#  , ("Código Fuentes De Financiación", "Fuentes de Financiación" )
  ]
duplicative_columns_short_set = set(
  # chain.from_iterable concatenates these 2-element lists
  chain.from_iterable( [ [ c[0], c[1] ]
                         for c in duplicative_columns_short ] ) )
omittable_columns_short = set(
  map( lambda x: x[1],
       duplicative_columns_short ) )

column_subsets_no_dups_short = {}
column_subsets_no_dups_long = {}
for s in series:
  column_subsets_no_dups_short[s] = [
    i for i in column_subsets_short[s]
    if not i in map( snd,
                     duplicative_columns_short ) ]
  column_subsets_no_dups_long[s] = [
    i for i in column_subsets_long[s]
    if not i in map( snd,
                     duplicative_columns_long ) ]
column_subsets_no_dups_short["gastos"] = (
  column_subsets_no_dups_short["inversion"] )
column_subsets_no_dups_long["gastos"] = (
  column_subsets_no_dups_long["inversion"] )
