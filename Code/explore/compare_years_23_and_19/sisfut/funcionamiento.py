# PURPOSE: Compare the columns named in
# the `column_subsets` dictionary defined in Code/metadata/raw_series.py
# across all years in both views.

from typing import List, Dict, GenericAlias
import pandas as pd
import numpy as np
#
import Code.explore.compare_years_23_and_19.sisfut.lib as lib
import Code.metadata.terms as t
import Code.build.classify_budget_codes as codes


(vao19,vao23) = lib.load_views_from_2019_and_2023 ( "funcionamiento" )


################
# Nombre Entidad

# 2021 is again useless for this data set --
# only 193 Entidades as of 2023 05 23.
# The other years have roughly enough Entidades.

for year, df in ( vao19.items() ):
  print ( year, ": ", len ( df["Nombre Entidad"].unique() ) )

for year, df in ( vao23.items() ):
  print ( year, ": ", len ( df["Nombre Entidad"].unique() ) )

# Ignoring that one, the shortest series is vao23[19].
# The others have most of the Entidades that it does.
names19 = set ( vao23[19] ["Nombre Entidad"].unique() )
for year in range(13,21):
  names = set ( vao23[year] ["Nombre Entidad"].unique() )
  print("")
  print("year: ", year)
  x = list(names19 - names)
  x.sort() # stupid impure function
  print("In 2019 and not this year.",x)
  y = list(names - names19)
  y.sort() # stupid impure function
  print("In this year and not 2019.", y)


########################
# Cód. DANE Departamento

# They all have the same department codes.
codes13 = set ( vao23[13]["Cód. DANE Departamento"].unique() )
for year in range(13,22):
  codes = set ( vao23[year]["Cód. DANE Departamento"].unique() )
  print("")
  print("year: ", year)
  print( "In 2013 and not this year.",
         pd.Series(list(codes13 - codes)) . sort_values() )
  print( "In this year and not 2013.",
         pd.Series(list(codes - codes13)) . sort_values() )


#####################
# Cód. DANE Municipio

# Again 2021 has pitifully few (162 as of 2023 05 23)
# and of the rest 2014 has the least.
for year in vao23.keys():
  print ( year, len ( vao23 [year] ["Cód. DANE Municipio"]
                      . unique() ) )

# Again, they're all more or less the same, but with a handful
# of municipalities not in 2019, and vice-versa.
codes19 = set ( vao23[19] ["Cód. DANE Municipio"] . unique() )
for year in vao23.keys():
  codes = set ( vao23[year]["Cód. DANE Municipio"].unique() )
  print("")
  print("year: ", year)
  print( "In 2019 and not this year.",
         pd.Series(list(codes19 - codes)) . sort_values() )
  print( "In this year and not 2019.",
         pd.Series(list(codes - codes19)) . sort_values() )


#################
# Código Concepto

vao23 [13] ["Código Concepto"]

# Every year there is a different number of codes.
for year in vao23.keys():
  print ( year, len ( vao23 [year] ["Código Concepto"]
                      . unique() ) )

# PITFALL: For each year, at least one of the codes we need is absent.
# (The worst, perhaps predictably, is 2021, which is missing 7 of them.)
funcionamiento_codes_we_use = set()
for v in codes.categs_to_codes[t.funcionamiento].values():
  funcionamiento_codes_we_use = { *funcionamiento_codes_we_use, *v }
for year in vao23.keys():
  print("")
  print(year)
  print( "Missing from this year: ",
         ( funcionamiento_codes_we_use -
           set ( vao23 [year] ["Código Concepto"] . unique() ) ) )


#################
# Obligaciones

vao23 [13] ["Obligaciones"]

for year in vao23.keys(): # They are all floats.
  print ( vao23 [year] ["Obligaciones"] . dtype )

restricted_views_23 = {}
for year in vao23.keys():
  df = vao23 [year]
  restricted_views_23[year] = \
    df [ df ["Código Concepto"]
         . isin ( funcionamiento_codes_we_use ) ]

# PITFALL: Expenses through 2016 are in thousands of pesos.
# After that, they are in pesos.
# (There's already code in build/ to correct for this.)
# PITFALL: Figures for 2021 are around 5 times bigger than the previous year.
# I suspect that's because bigger places are more likely to be
# among those that managed to report already for 2021.
descriptions = pd.DataFrame()
for year in restricted_views_23.keys():
  df = restricted_views_23 [year]
  s = df ["Obligaciones"] . describe()
  s.name = year
  descriptions = pd.concat ( [ descriptions, s ],
                             axis = 1 )
descriptions . transpose()
