# PURPOSE: Define some data sets used in much of `Code/cuipo/explore/`.
#
# USAGE: Boilerplate:
#
#   import Code.build.use_keys as uk
#   import Code.explore.cuipo.load as load
#
#   g   = load . read_gastos_pre_cuipo ()
#   i   = load . read_ingresos_pre_cuipo ()
#   g22 = load . read_gastos_cuipo_22 ()
#   i22 = load . read_ingresos_cuipo_22 ()
#   gr  = load . read_cuipo_geo_restrictor ()
#   geo = uk.geo . copy ()

from   os import path
import pandas as pd


build_3 = "output/2023/budget_3_dept_muni_year_item/recip-1"

def read_gastos_pre_cuipo () -> pd.DataFrame:
  return pd.read_csv (
    path.join ( build_3, "gastos.csv" ) )

def read_ingresos_pre_cuipo () -> pd.DataFrame:
  return pd.read_csv (
    path.join ( build_3, "ingresos.csv" ) )

def read_gastos_cuipo_22 () -> pd.DataFrame:
  return pd.read_csv (
    path.join ( "data/cuipo/2022",
                "Ejecucion_GastosDic2022.csv" ) )

def read_ingresos_cuipo_22 () -> pd.DataFrame:
  return pd.read_csv (
    path.join ( "data/cuipo/2022",
                "Ejecucion_IngresosDic2022.csv" ) )

def read_cuipo_geo_restrictor () -> pd.DataFrame:
  return (
    pd.read_csv (
      path.join ( "data/cuipo",
                  "dept-and-muni-CHIPs.csv" ) )
    . drop ( columns = ["E-Mail"] ) )
