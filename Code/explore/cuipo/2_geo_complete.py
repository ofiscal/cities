# PURPOSE: Evaluate the completeness of the 2022 CUIPO data,
# starting with whether it has all munis and depts,
# and whether the Áreas Metropolitanas can safely be ignored.

import pandas as pd
from   typing import List, Dict, Set
#
from   Code.explore.cuipo.load import g, i, g22, i22, jc, geo
from   Code.explore.cuipo.lib import my_describe


###############################
# 18 municipalities are missing
###############################

jc_ids = jc["Id_Entidad"]
g22_ids = g22["2_COD_CHIP"]
i22_ids = i22["2_COD_CHIP"]

missing_ids = set(jc_ids) - { *set(g22_ids), *set(i22_ids) }

missing_names = ( jc [ jc["Id_Entidad"] . isin ( missing_ids ) ]
                  ["Entidad"] )

proto_regex = ".*(" + "|".join ( list( missing_names ) ) + ").*"

# I then edited that by hand, reducing some problematically long expressions
# and making tildes optional.
regex = '.*(Anor[ií]|Apartad[oó]|Bol[ií]var|Bugalagrande|California|Caramanta|Carur[uú]|Corrales|Cotorra|Fuente.*Oro|Galeras|Ituango|Uribe|Momil|Luc[í]a|Sopetr[aá]n|Ulloa|Urrao).*'

# I still find almost none of them in CUIPO,
# with the possible exception of Bolivar.
( g22 [ g22 ["3_ENTIDAD"]
        . str.match( regex,
                     case = False ) ]
  ["3_ENTIDAD"]
  . unique() )


##################################################################
# Some "Áreas Metropolitanas" are not present under any other name
##################################################################

# Find the strings containing "Área Metropolitana" of interest.
# (This finds a few that are not of interest, too --
# the ones that are all *start* with the substring "Área".)
( g22 ["3_ENTIDAD"]
  [ g22["3_ENTIDAD"]
    . str.match( ".*[AÁ]rea.*Metropolitana.*") ]
  . unique() )

# Substrings of interest from the above, reduced and tilde-sanitized:
regex = ".*(Bucaramanga|Aburr[aá]|Barranquilla|C[uú]cuta|Occidente|Valledupar).*"

# Some of those are not in JC's data:
( jc["Entidad"]
  [ jc["Entidad"]
    . str.match ( regex ) ] )

# Speficially:
missing = ["Valle de Aburrá",
           "Barranquilla",
           "Cúcuta",
           "Centro Occidente"]