# PURPOSE:
# Determine whether the CUIPO and SISFUT data are comparable,
# by comparing COP values after matching on city and item.
#
# RESULT:
# They don't correspond.
# We'll have to build new keys for CUIPO,
# and compare CUIPO aggregates to SISFUT aggregates,
# because the individual expenditure codes have changed.

import pandas as pd
from   typing import List, Dict, Set
#
from   Code.explore.cuipo.lib import my_describe
import Code.build.use_keys as uk
import Code.explore.cuipo.load as load


################
# Load some data
################

gr    = load   . read_cuipo_geo_restrictor ()
geo   = uk.geo . copy                      ()

if True: # Nearly-pristine* (not to modify) versions, for comparison.
  # (They are only modified in this "if" statement.)
  g   = load   . read_gastos_pre_cuipo     ()
  i   = load   . read_ingresos_pre_cuipo   ()
  g22 = load   . read_gastos_cuipo_22      ()
  i22 = load   . read_ingresos_cuipo_22    ()

  g = ( g
        . drop ( columns = ["item total"] )
        . rename ( columns = {"item oblig" : "item total"} ) )


########################
# Process the CUIPO data
########################

cuipo = { "gastos"    : g22.copy(),
          "ingresos"  : i22.copy() }

for (source, kind, colDict) in [
    ( g22, "gastos",
      { "2_COD_CHIP"       : "chip",
        "3_ENTIDAD"        : "entity",
        "4_COD_CONCEPTO"   : "item code",
        "5_CONCEPTO"       : "item",
        "30_OBLIGACIONES"  : "COP",
       } ),
    ( i22, "ingresos",
      { "2_COD_CHIP"       : "chip",
        "3_Entidad"        : "entity",
        "4_COD_CONCEPTO"   : "item code",
        "5_CONCEPTO"       : "item",
        "27_TOTAL_RECAUDO" : "COP",
       } ) ]:

  cuipo[kind] : pd.DataFrame = (
    cuipo[kind]
    [ cuipo[kind]["2_COD_CHIP"]
      . isin ( gr["Id_Entidad"] ) ]
    [ list ( colDict.keys() ) ]
    . rename ( columns = colDict )
    . copy () ) # This silly-looking copy-self instruction dodges a
                # "value ... set on a copy of a slice" error.

  cuipo[kind] ["ent-str"] = ( # Entity as string.
    cuipo[kind]["chip"]
    . astype (str)
    . str.zfill (9) ) # left-pad with zeroes

  for (colname, sMin, sMax) in [ ("muni code", -5, None),
                                 ("dept code", -5, -3 ) ]:
    cuipo[kind] [colname] = ( cuipo[kind] ["ent-str"]
                              . apply ( lambda s : s[ sMin : sMax ] )
                              . astype ( int ) )


#########################
# Process the SISFUT data
#########################

sisfut = { "gastos"   : g.copy(),
           "ingresos" : i.copy() }

for kind in sisfut.keys():
  sisfut  [kind] ["muni code"] = (
    sisfut[kind] ["muni code"] . astype ( int ) )
  sisfut[kind] = (
    sisfut[kind] . rename ( columns = {"item total" : "COP"} ) )


############################
# Merge CUIPO and older data
############################

m = {}

# Bad news. Not a single code matches.
for kind in sisfut.keys():
  m[kind] = (
    sisfut[kind]
    [sisfut[kind] ["year"] == 2020]
    . merge ( cuipo[kind],
              on = ["muni code","item code"] ) )
