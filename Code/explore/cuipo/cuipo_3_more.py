import pandas as pd
from   typing import List, Dict, Set
#
from   Code.explore.cuipo.lib import my_describe
import Code.build.use_keys as uk
import Code.explore.cuipo.load as load


################
# Load some data
################

g   = load   . read_gastos_pre_cuipo     ()
i   = load   . read_ingresos_pre_cuipo   ()
g22 = load   . read_gastos_cuipo_22      ()
i22 = load   . read_ingresos_cuipo_22    ()
gr  = load   . read_cuipo_geo_restrictor ()
geo = uk.geo . copy                      ()

cuipo = { "gastos"   : g22,
          "ingresos" : i22}

# pristine (not to modify) versions, for comparison
g22p = load . read_gastos_cuipo_22      ()
i22p = load . read_ingresos_cuipo_22    ()


########################
# Process the CUIPO data
########################

for i in cuipo.keys():
  cuipo[i] : pd.DataFrame = (
    cuipo[i]
    [ cuipo[i]["2_COD_CHIP"]
      . isin ( gr["Id_Entidad"] ) ]
    . copy () ) # This silly-looking copy-self instruction dodges a
                # "value ... set on a copy of a slice" error.
  cuipo[i] ["ent-str"] = (
    cuipo[i]["2_COD_CHIP"]
    . astype (str)
    . str.zfill (9) ) # left-pad with zeroes
  for (colname, sMin, sMax) in [ ("muni", -5, None),
                                 ("dept", -5, -3 ) ]:
    cuipo[i] [colname] = ( cuipo[i] ["ent-str"]
                           . apply ( lambda s : s[ sMin : sMax ] )
                           . astype ( int ) )

## PENDING


# Maybe also "*ambito*" (case-insensitive) and
# "34_Conceptos_Cuipo_Agregacion".
gastos :
2_COD_CHIP
3_ENTIDAD
4_COD_CONCEPTO
5_CONCEPTO
30_OBLIGACIONES

ingresos :
2_COD_CHIP
3_Entidad
4_COD_CONCEPTO
5_CONCEPTO
27_TOTAL_RECAUDO # TODO : Ask Daniel: Correct?
# Other choices are:
#   23_RECAUDO_VIGENCIA_ACTUAL_SIN_SITUACION_DE_FONDOS   float64
#   24_RECAUDO_VIGENCIA_ACTUAL_CON_SITUACION_DE_FONDOS   float64
#   25_RECAUDO_VIGENCIA_ANTERIOR_SIN_SITUACION_DE_FONDOS float64
#   26_RECAUDO_VIGENCIA_ANTERIOR_CON_SITUACION_DE_FONDOS float64
#   28_VALOR_DESTINACION_ESPECIFICA                      float64
