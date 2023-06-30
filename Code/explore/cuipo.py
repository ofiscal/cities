# Determining whether the new (2023) CUIPO data
# is comparable to the oild SISFUT data.

from   os import path
import pandas as pd
from   typing import List, Dict, Set
#
import Code.build.use_keys as uk


build_3 = "output/2023/budget_3_dept_muni_year_item/recip-1"

g = pd.read_csv (
  path.join ( build_3, "gastos.csv" ) )

i = pd.read_csv (
  path.join ( build_3, "ingresos.csv" ) )

eg22 = pd.read_excel (
  path.join ( "data/cuipo/",
              "Ejecucion_GastosDic2022.xlsx" ) )

ei22 = pd.read_excel (
  path.join ( "data/cuipo/",
              "Ejecucion_IngresosDic2022.xlsx" ) )

geo = uk.geo
geo [ geo["dept"] == "VICHADA" ]



def my_describe ( df : pd.DataFrame ) -> pd.DataFrame:
  return ( df . describe() . transpose ()
           [ ['count', 'mean', 'std', 'min', '50%', 'max'] ] )

33   34_Conceptos_Cuipo_Agregacion       bool
10   11_CONS_MGA_PROD                 float64
12   13_CONS_CPC                      float64
17   18_MGA_SECTOR                    float64
24   25_COD_POLITICA                  float64
26   27_COD_CHIP_TERCERO              float64
28   29_COMPROMISOS                   float64
 9   10_CONS_MGA_PROGR                float64
 0   1_Índice                           int64
 1   2_COD_CHIP                         int64
16   17_COD_AMBITO                      int64
29   30_OBLIGACIONES                    int64
30   31_PAGOS                           int64
32   33_Conceptos_Cuipo_Nivel           int64
 5   6_COD_VIGENCIA                     int64
 7   8_COD_SECCION                      int64
11   12_PRODUCTO_MGA                   object
13   14_CPC_PRODUCTO                   object
14   15_COD_DETALLE_SECTORIAL          object
15   16_DETALLE_SECTORIAL              object
18   19_SECTOR                         object
19   20_CONS_FUENTE                    object
20   21_FUENTE                         object
21   22_BPIN                           object
22   23_COD_SF                         object
23   24_SITUACION_FONDOS               object
 2   3_ENTIDAD                         object
25   26_POLITICA                       object
27   28_Terceros_CHIP.ENTIDAD          object
31   32_Conceptos_Cuipo_Padre          object
 3   4_COD_CONCEPTO                    object
 4   5_CONCEPTO                        object
 6   7_VIGENCIA                        object
 8   9_SECCION_PRESUPUESTAL            object

for i in [11,13,14,15,21]:
  print()
  print("IT'S: " + str(i) )
  print ( eg22.iloc [:,i] . unique() )

for i in [11,13,14,15,18,19,20,21,22,23,2,25,27,31,3,4,6,8]:
  print()
  print("IT'S: " + str(i) )
  print ( eg22.iloc [:,i] )
