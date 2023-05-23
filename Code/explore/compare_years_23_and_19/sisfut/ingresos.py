# PURPOSE: Compare the columns named in
# the `column_subsets` dictionary defined in Code/metadata/raw_series.py
# across all years in both views.
#
# RESULT: The set of municipalities tracked in 2021 is terribly small --
# less than 200. For the other years, most of them are present.
# All the spending codes we need are present.

from typing import List, Dict, GenericAlias
import pandas as pd
import numpy as np
#
import Code.explore.compare_years_23_and_19.sisfut.lib as lib


(vao19,vao23) = lib.load_views_from_2019_and_2023 ( "ingresos" )

df = vao19[13]


################
# Nombre Entidad

for k,v in {1:2}.items(): print( k, ": ", v )

for year, df in ( vao19.items() ):
  print ( year, ": ", len ( df["Nombre Entidad"].unique() ) )

for year, df in ( vao23.items() ):
  print ( year, ": ", len ( df["Nombre Entidad"].unique() ) )

# Year 2021 in vao23 is way too short.
vao23[21] ["Nombre Entidad"].unique()

# Ignoring that one, the shortest series is vao23[19].
# Lets see if the others all have those names.
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
# They're all more or less the same but with a handful
# of municipalities not in 2019, and vice-versa.
# None of those differences appears to be due to simple misspelling.


########################
# Cód. DANE Departamento

# They all have the same codes.
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

# Again 2021 has pitifully few, and of the rest 2019 has the least.
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

# Every year there is a different number of codes.
vao23 [13] ["Código Concepto"]
for year in vao23.keys():
  print ( year, len ( vao23 [year] ["Código Concepto"]
                      . unique() ) )

# Fortunately, each year has the few codes we need.
codes_we_need = { "TI.A", "TI.A.2.6", "TI.B" }
  # These codes come from Code/build/classify_budget_codes.py
for year in vao23.keys():
  print("")
  print(year)
  print("Missing from this year: ",
        codes_we_need -
        set ( vao23 [year] ["Código Concepto"] . unique() ) )

# If for some reason I need to see all the codes in a year,
# the shortest ones first, this does that.
for year in vao23.keys():
  s = pd.DataFrame (
    { "code" :
      vao23 [year] ["Código Concepto"].unique() } )
  s["len"] = s["code"] . apply( len )
  print(s.sort_values("len")[0:5])
