# Determining whether the new (2023) CUIPO data
# is comparable to the oild SISFUT data.


from   math import floor
from   os import path
import pandas as pd
from   typing import List, Dict, Set
#
import Code.build.use_keys as uk


def my_describe ( df : pd.DataFrame ) -> pd.DataFrame:
  return ( df . describe() . transpose ()
           [ ['count', 'mean', 'std', 'min', '50%', 'max'] ] )

################
# Input the data
################

build_3 = "output/2023/budget_3_dept_muni_year_item/recip-1"

g = pd.read_csv (
  path.join ( build_3, "gastos.csv" ) )

i = pd.read_csv (
  path.join ( build_3, "ingresos.csv" ) )

g22 = pd.read_excel (
  path.join ( "data/cuipo/",
              "Ejecucion_GastosDic2022.xlsx" ) )

i22 = pd.read_excel (
  path.join ( "data/cuipo/",
              "Ejecucion_IngresosDic2022.xlsx" ) )

geo = uk.geo . copy()


####################
# Examine "entities"
####################

entities = pd.Series ( g22
                       . loc[ g22["4_COD_CONCEPTO"] == "2" ]
                       ["3_ENTIDAD"] . unique() )
# They include businesses, not just depts and munis. That's problematic.

entities [ entities
           . str.match ("Departamento de.*") ]
# There are exactly 32 departments, which is correct.

entities [ entities
           . str.match ("Villavicencio") ]
# Disappointing: There's no prefix like "Municipio de"
# one could filter on to extract municipalities.

if True: # Good: There is a 1-1 correspondence
         # between entity and CHIP code. Proof:
  chip_entities = ( g22
                    . groupby ( ["2_COD_CHIP", "3_ENTIDAD"] )
                    . agg ( "first" )
                    . reset_index () )
  chip_entities["count"] = 1
  for group in ["2_COD_CHIP", "3_ENTIDAD"]:
    print ( chip_entities
            . groupby ( group )
            . agg ( sum )
            . describe() . transpose () )


##################################################
# Exclude businesses (we only want depts and muis)
##################################################

if True:
  # Via binary search, the code below lets one manually identify
  # the boundary between the last non-business
  # and the first business, assuming they are in fact ordered that way.
  (low,high) = (659240, 659252)

  print ( (low,high)                  )
  print ( g22.iloc[low]["3_ENTIDAD"]  )
  print ( g22.iloc[high]["3_ENTIDAD"] )
  half = floor((low+high)/2)
  print ( g22.iloc[half]["3_ENTIDAD"] )
  # Now set low=half or high=half depending on the last result.


# Inspecting the results of the following,
# businesses do appear to appear after depts and munis.

low_entities  = pd.Series ( g22 . iloc[:low]  ["3_ENTIDAD"] . unique() )
high_entities = pd.Series ( g22 . iloc[high:] ["3_ENTIDAD"] . unique() )

for i in low_entities: print ( i )
print ( low_entities . shape )

for i in high_entities: print ( i )
print ( high_entities . shape )


####################################################################
# CHIP implies dept and muni! (Not necessarily the reverse, though.)
#
# Daniel found that the dept and muni codes *are*
# embedded in the CHIP code; they are, resp. the first two of the last five,
# and the last five, digits of the CHIP code.
# (That's because the dept code is embedded in the muni code. too.)

chips = g22 [["2_COD_CHIP","3_ENTIDAD"]] . copy()
chips ["ent-str"] = ( # Entidad as string
  chips["2_COD_CHIP"]
  . astype (str)
  . apply (lambda s: s[-5:] ) )
chips ["dept code"] = ( chips ["ent-str"]
                        . apply ( lambda s: s[:2] )
                        . astype ( int ) )
chips ["muni code"] = ( chips ["ent-str"]
                        . astype ( int ) )

chips [ chips["muni code"] == 5001 ]


geo[ geo["dept code"] == 15 ]


# Next problem: Are there pairs of CHIP codes with the same last 5 digits?
# If so, how can we strip out the businesses?
