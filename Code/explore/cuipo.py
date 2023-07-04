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
# Correct: There are exactly 32 departments.

entities [ entities
           . str.match ("Villavicencio") ]
# Disappointing: There's no prefix like "Municipio de"
# one could filter on to distinguish municipalities from businesses.

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

# Via binary search, the code below lets one manually identify
# the boundary between the last non-business
# and the first business, assuming they are in fact ordered that way.
# First, set df to g22 or i22.
df = i22
(low,high) = (0,len(df)-1)

# Evaluate this by hand repeatedly.
# After each evaluation,
# set low=half or high=half depending on the last result.
print ( (low,high)                 )
print ( df.iloc[low]["3_Entidad"]  )
print ( df.iloc[high]["3_Entidad"] )
half = floor((low+high)/2)
print ( df.iloc[half]["3_Entidad"] )

# Solution for g22:
# (low,high) = (659249, 659250)

# MAYBE solution for i22:
# (low,high) = (134597, 134598) --
# but then what about Área Metropolitana de Bucaramanga,
# at index 135000?
# Either that's not a municipality,
# or the data isn't partitioned like we hope
# (with munis and departments coming first,
# and other entities after them).


#######################################
# Unique names in the high and low data
#######################################

gSep  = 659250
gLow  = g22 [:gSep]
gHigh = g22 [gSep:]

for e in gLow["3_ENTIDAD"].unique(): print(e)

place = pd.Series ( gLow["3_ENTIDAD"].unique() )

biz = pd.Series ( gHigh["3_ENTIDAD"].unique() )

regex = ".*(I.P.S|E.S.P|S.A.S|Fondo|Empresa|Lotería|Instituto|Terminal|Deporte|Alianza|Tribunal|Consejo|Sistema|Asociación|Alumbrado|E.P.S.|E.S.E|E.I.C.E|S.A|IPS|Fundación|Salud|Servicio|[Cc]aja de *[Cc]omp|[Cc]omercio|[Cc][aá]mara|Universidad|Universitaria|U.A.E|Administra|C.P.G.A|Corporaci[oó]n|Hospital|Casa.*Cultura|Diagnóstico|Industria|Transporte|Sociedad|Patrimonio|Agencia|Colegio).*"

place [ place . str.match ( regex ) ]
  # These three matches are all places.

biz = biz [ ~ biz . str.match ( regex ) ] . sort_values()
for i in biz: print(i)


# CHIP implies dept and muni! (Not necessarily the reverse, though.)
#
# Daniel found that the dept and muni codes *are*
# embedded in the CHIP code; they are, resp. the first two of the last five,
# and the last five, digits of the CHIP code.
# (That's because the dept code is embedded in the muni code. too.)


####################################################################
# Trying to separate businesses from munis and depts via CHIP codes.
####################################################################

chips = g22 [["2_COD_CHIP","3_ENTIDAD"]] . copy()
chips ["ent-str"] = ( # Entidad as string
  chips["2_COD_CHIP"]
  . astype (str)
  . str.zfill (9) )             # left-pad with zeroes
chips ["prefix"] = (            # I don't know what these are for.
  chips ["ent-str"]
  . apply (lambda s: s[:-5] )   # all but last 5 digits
  . astype ( int ) )
chips ["muni code"] = (
  chips ["ent-str"]
  . apply (lambda s: s[-5:] )   # last 5 digits
  . astype ( int ) )
chips ["dept code"] = (
  chips ["ent-str"]
  . apply (lambda s: s[-5:-3] ) # first 2 of last 5 digits
  . astype ( int ) )

clow  = chips [:high] # Note: This does not include the `high`th row.
chigh = chips [high:]

for c in  ["prefix", "muni code", "dept code"]:
  ulow  = set ( clow [c] . unique() )
  uhigh = set ( chigh[c] . unique() )
  print ()
  print (c)
  print ( ulow .intersection ( uhigh ) )

# FAILURE. For each part of the CHIP code -- the dept, the muni,
# and the prefix -- there are values of that part which appear both
# before and after the split. That is, there's no obvious way
# to use CHIP codes to remove the businesses from the depts and munis.
