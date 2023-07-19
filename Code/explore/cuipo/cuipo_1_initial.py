# PITFALL: Somewhat obsolete.
# This is the analysis I did before Juan Camilo had responded.
# His response supercedes much of it.

# PURPOSE: Determining whether the new (2023) CUIPO data
# is comparable to the oild SISFUT data.

# TODO: Much of this analysis is limited to the gastos data for 2022
# (`g22`), and should be duplicated for the ingresos data (`i22`).

from   math import floor
import pandas as pd
from   typing import List, Dict, Set
#
import Code.build.use_keys as uk
from   Code.explore.cuipo.lib import my_describe
import Code.explore.cuipo.load as load


g   = load . read_gastos_pre_cuipo ()
i   = load . read_ingresos_pre_cuipo ()
g22 = load . read_gastos_cuipo_22 ()
i22 = load . read_ingresos_cuipo_22 ()
geo = uk.geo . copy ()


########################
# Create CHIP substrings
########################

g22 ["ent-str"] = ( # Entidad as string
  g22["2_COD_CHIP"]
  . astype (str)
  . str.zfill (9) ) # left-pad with zeroes

for (name,rangeLow,rangeHigh) in [
    (":2"   ,None,2), # First 2 digits.
                      # Daniel thinks maybe 21=muni & 11=dept.
    (":-5"  ,None,-5), # All but the last 5 digits.
                       # I don't know what these are for.
    ("-5:"  ,-5,  None), # Last 5 digits. Looks like muni code.
    ("-5:-3",-5,  -3) ]: # First 2 of last 5 digits. Looks like dept code.
  g22[name] = (
    g22 ["ent-str"]
    . apply ( lambda s : s[rangeLow:rangeHigh] )
    . astype ( int ) )


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
         # between entity and CHIP code (at least in gastos).
         # Proof:
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

# Prefix 'm' is for 'maybe'.
mPlaceNames = pd.Series ( gLow["3_ENTIDAD"].unique() )

# Prefix 'm' is for 'maybe'.
mBizNames = pd.Series ( gHigh["3_ENTIDAD"].unique() )

# This matches few municipalities or departments,
# and most entities that are not.
regex = ".*(I.P.S|E.S.P|S.A.S|CPGA|C.P.G.M.A.E.|Fondo|Empresa|Lotería|Instituto|Terminal|Deporte| de Bomberos|Alianza|Tribunal|Consejo|Sistema|Asociación|Alumbrado|E.P.S.|E.S.E|E.I.C.E|S.A|Escuela|Fábrica|Fundación|Salud|Servicio|Caja de |[Cc]omercio|[Cc][aá]mara|Universidad|Universitaria|U.A.E|Administra|C.P.G.A|Corporaci[oó]n|Hospital|Casa.*Cultura|Aeropuerto|Inmobiliario|Diagnóstico|Industria|Transporte|Tecnológic|Politécnico|Licorera|Tránsito|Liquidaciones|Sociedad|Patrimonio|Agencia|IPS|Colegio).*"

# In the data where I would hope nothing matches the regex,
# three things do -- but they are all in fact municipalities.
mPlaceNames [ mPlaceNames
              . str.match ( regex ) ]
  # These three matches are all in fact places, not businesses.

mBizNames = ( mBizNames [ ~ mBizNames
                          . str.match ( regex ) ]
              . sort_values() )
for i in mBizNames: print(i)


# CHIP implies dept and muni! (Not necessarily the reverse, though.)
#
# Daniel found that the dept and muni codes *are*
# embedded in the CHIP code; they are, resp. the first two of the last five,
# and the last five, digits of the CHIP code.
# (That's because the dept code is embedded in the muni code. too.)


####################################################################
# Trying to separate businesses from munis and depts via CHIP codes.
####################################################################

chips = g22 [["1_Índice","2_COD_CHIP","3_ENTIDAD",
              ':2', ':-5', '-5:', '-5:-3']] . copy()

cLowUnique  = chips [:gSep] . drop_duplicates() # Excludes the `gSep`th row.
cHighUnique = chips [gSep:] . drop_duplicates()

for c in  [":2",":-5","-5:","-5:-3"]:
  ulow  = set ( cLowUnique [c] . unique() )
  uhigh = set ( cHighUnique[c] . unique() )
  print ()
  print (c)
  print ( ulow . intersection ( uhigh ) )

# FAILURE ? For each part of the CHIP code --
# the dept, the muni (which includes the dept), and the prefix --
# there are values of that part which appear both
# before and after the split. That is, there's no obvious way to use
# (only) CHIP codes to remove the businesses from the depts and munis.
#
# HOWEVER, the only overlap in the prefix (the first 4 digits)
# is in code 9232.

# Bad -- a mix of munis and other entities.
chips [ chips [":-5"] == 9232 ]

# Bad -- these (apparent) munis have CHIPs that do not start with 11 or 21.
for i in ( cLowUnique
           [ ~ cLowUnique [":2"]
             . isin ( [11,21] ) ]
           ["3_ENTIDAD"]
           . unique() ):
  print(i)

# Good -- `cHighUnique` has nothing whose CHIP starts with 11 or 21.
print ( cHighUnique [ cHighUnique[":2"] == 11 ] )
print ( cHighUnique [ cHighUnique[":2"] == 21 ] )

# To make these two variables appear in the results of `describe()`,
# turn them into numbers.
g22["34_Conceptos_Cuipo_Agregacion"] = (
  g22["34_Conceptos_Cuipo_Agregacion"] . astype ( int ) )

( g22 [ "7_VIGENCIA" ], vigencia_codes ) = pd.factorize (
  g22 [ "7_VIGENCIA" ] )

# A firehose of information. Too much; sertting aside.
print ( my_describe ( s [   chips [":2"] == 11 ] )              )
print ( my_describe ( s [   chips [":2"] == 21 ] )              )
print ( my_describe ( s [ ~ chips [":2"] . isin ( [11,21] ) ] ) )

# Consider the "ambito" code.
s = g22 [ "17_COD_AMBITO" ]
in11   = set ( s [   chips [":2"] == 11 ]              . unique() )
in21   = set ( s [   chips [":2"] == 21 ]              . unique() )
others = set ( s [ ~ chips [":2"] . isin ( [11,21] ) ] . unique() )

# For CHIP codes starting with 11 or 21, there are respectively 2 "ambito"s:
print (in11)
print (in21)

# One of those codes, 439,
# applies also to entities with a CHIP not starting with 11 or 21:
set.union ( in11, in21 ) . intersection ( others )

# 1083 things have ambito 439. They look like municipalities.
g22_ambito_439 = pd.Series ( g22 [ g22 [ "17_COD_AMBITO" ] == 439 ]
                             ["3_ENTIDAD"]
                             . unique() )
for e in g22_ambito_439:
  print(e)
print( len( g22_ambito_439 ) )

# BAD : Entities (cities?) with ambito 439 and CHIP[:2] not in [11,21]?
g22_ambito_439_ugly_first_2 = (
  g22 [ (   g22 [ "17_COD_AMBITO" ] ==       439     )   &
        ( ~ g22 [ ":2" ]            . isin ( [11,21] ) ) ]
  [["2_COD_CHIP","3_ENTIDAD","17_COD_AMBITO"]]
  . drop_duplicates () )
print ( g22_ambito_439_ugly_first_2 )

# GOOD ? Nothing in mBizNames has one of the ambito codes we hope identify
# munis and depts.
( g22 [ ( g22 ["3_ENTIDAD"]     . isin ( mBizNames )                ) &
        ( g22 ["17_COD_AMBITO"] . isin ( set.union ( in11, in21 ) ) ) ]
  [["2_COD_CHIP","3_ENTIDAD","17_COD_AMBITO"]] )

# BAD ? That includes even the "Area Metropolitana"s.
( g22 [ g22 ["3_ENTIDAD"] . str.match ( "Área Metropolitana.*" ) ]
  [["2_COD_CHIP","3_ENTIDAD","17_COD_AMBITO"]]
  . drop_duplicates () )

# Those "Área Metropolitana"s all have Ambito 442.
# What else has that Ambito?
( g22 [ g22 ["17_COD_AMBITO"] == 442 ]
  [["2_COD_CHIP","3_ENTIDAD"]]
  . drop_duplicates () )


#########################################
# Extracting a key for the "ambito" codes
#########################################

# g22 offers no guide, but i22 does -- it includes both
# "6_COD_AMBITO" (int) and "7_AMBITO" (str).
g22["17_COD_AMBITO"].describe()  # ranges from 438 to 454
i22["6_COD_AMBITO"].describe()   # ranges from 438 to 454
pd.factorize ( i22["7_AMBITO"] ) # ranges from 438 to 454

# Result:
# 438 Administración Central - Municipios
# 439 Administración Central - Bogotá D.C
# 440 Administración Central - San Andrés y Providencia
# 441 Administración Central - Departamentos
# 442 Estapúblicos, Asociaciones y Federaciones Territoriales
# 443 Fondos sin personería jurídica denominados especiales o cuenta
# 444 Empresas Territoriales no financieras sujetas al Decreto 115 de 1996
# 445 Empresas Nacionales no financieras sujetas al Decreto 115 de 1996
# 446 Empresas Nacionales no financieras no sujetas al Decreto 115 de 1996
# 447 Empresas Territoriales Financieras
# 448 Empresas Nacionales Financieras
# 449 Fiducias públicas - encargos fiduciarios - Convenios
# 450 Entes Autónomos Constitucionales  (No PGN)
# 451 Particulares o entidades que manejan fondos de la Nación
# 452 Empresas Territoriales no financieras no sujetas al Decreto 115 de 1996
