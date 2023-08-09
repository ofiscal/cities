# PURPOSE:
# Build some of the .csv files found in these folders:
#   Code/explore/cuipo/concepto_keys/cuipo/all-conceptos/
#   Code/explore/cuipo/concepto_keys/sisfut/
# See the README files in this folder and below for more detail.

from   os import path
from   typing import Set, List, Dict
import pandas as pd
#
import Code.build.classify_budget_codes as cl
import Code.common as common
import Code.explore.cuipo.load as load
import Code.metadata.raw_series as raw
import Code.metadata.terms as t



##################################
# Build, save SISFUT concepto keys
##################################

if True: # load SISFUT data
  source = path.join ( common.outdata,
                       "budget_0_collect" )
  sisfut = {}
  for s in raw.series:
    sisfut[s] = pd.read_csv (
      path.join ( source,
                  s + ".csv" ) )

sisfut_key = ( pd.concat ( [ sisfut[kind] [["item", "item code"]]
                             for kind in sisfut.keys()],
                           axis = 0 )
               . drop_duplicates() )
sisfut_key = sisfut_key [
  ~ ( sisfut_key["item"] . isnull() ) ]

if False: # Show that some codes are described in more than one way.
  sisfut_key["1"] = 1
  sisfut_codes = ( sisfut_key
                   . groupby ( "item code" )
                   . agg ( "sum" ) )
  sisfut_codes [ sisfut_codes["1"] > 1 ] . describe()

def code_set_to_code_table (
    observatorio_name : str,
    codes : Set[str]
) -> pd.DataFrame:
  df = sisfut_key [ sisfut_key["item code"]
                    . isin ( codes ) ] . copy()
  df["observatorio name"] = observatorio_name
  return df . sort_values ( ["observatorio name", "item code"] )

code_set_to_code_table (
  "ambiental",
  cl.categs_to_codes [t.funcionamiento] [t.ambiental] )

for major_category in cl.categs_to_codes.keys ():
  ( pd.concat (
      [ code_set_to_code_table ( observatorio_name = k,
                                 codes = ( cl.categs_to_codes
                                           [major_category] [k] ) )
        for k in cl.categs_to_codes [major_category] . keys() ],
      axis = 0 )
    . to_csv (
      path.join ( "Code/explore/cuipo/concepto_keys/sisfut",
                  major_category + ".csv" ),
      index = False ) )


#####################################################
# Load, process CUIPO data; build CUIPO item-code key
#####################################################

gr  = load . read_cuipo_geo_restrictor ()
g22 = load . read_gastos_cuipo_22      ()
i22 = load . read_ingresos_cuipo_22    ()

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

for kind in cuipo.keys():
  ( cuipo[kind]
    [["item", "item code"]]
    . drop_duplicates ()
    . sort_values ( ["item code"] )
    . to_csv (
      path.join ( "Code/explore/cuipo/concepto_keys/cuipo",
                  kind + ".csv" ),
      index = False ) )
