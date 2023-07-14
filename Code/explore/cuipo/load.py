# PURPOSE: Define some data sets used in much of `Code/cuipo/explore/`.
#
# PITFALL: Highly side-effectful (reads from disk). Takes a while.
#
# USAGE: It seems more natural to import all definitions individually,
# rather than qualifying them behind the module name, as in
#   from   Code.explore.cuipo.load import build_3, g, i, g22, i22, jc, geo

from   os import path
import pandas as pd
#
import Code.build.use_keys as uk


build_3 = "output/2023/budget_3_dept_muni_year_item/recip-1"

g = pd.read_csv (
  path.join ( build_3, "gastos.csv" ) )

i = pd.read_csv (
  path.join ( build_3, "ingresos.csv" ) )

g22 = pd.read_csv (
  path.join ( "data/cuipo/2022",
              "Ejecucion_GastosDic2022.csv" ) )

i22 = pd.read_csv (
  path.join ( "data/cuipo/2022",
              "Ejecucion_IngresosDic2022.csv" ) )

jc = (
  pd.read_csv (
    path.join ( "data/cuipo",
                "dept-and-muni-CHIPs.csv" ) )
  . drop ( columns = ["E-Mail"] ) )

geo = uk.geo . copy()
