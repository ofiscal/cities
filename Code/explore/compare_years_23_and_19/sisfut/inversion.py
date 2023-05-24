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


(vao19,vao23) = lib.load_views_from_2019_and_2023 ( "inversion" )


################
# Nombre Entidad

# 2021 is again useless for this data set --
# only 193 Entidades as of 2023 05 23.
# The other years have roughly enough Entidades.

for year, df in ( vao19.items() ):
  print ( year, ": ", len ( df["Nombre Entidad"].unique() ) )

for year, df in ( vao23.items() ):
  print ( year, ": ", len ( df["Nombre Entidad"].unique() ) )

# Ignoring that one, the shortest series is vao23[14].
# The others have most of the Entidades that it does.
names14 = set ( vao23[14] ["Nombre Entidad"].unique() )
for year in range(13,21):
  names = set ( vao23[year] ["Nombre Entidad"].unique() )
  print("")
  print("year: ", year)
  x = list(names14 - names)
  x.sort() # stupid impure function
  print("In 2014 and not this year.",x)
  y = list(names - names14)
  y.sort() # stupid impure function
  print("In this year and not 2014.", y)


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

# Again 2021 has pitifully few (162 as of 2023 05 23)
# and of the rest 2014 has the least.
for year in vao23.keys():
  print ( year, len ( vao23 [year] ["Cód. DANE Municipio"]
                      . unique() ) )

# Again, they're all more or less the same, but with a handful
# of municipalities not in 2014, and vice-versa.
codes14 = set ( vao23[14] ["Cód. DANE Municipio"] . unique() )
for year in vao23.keys():
  codes = set ( vao23[year]["Cód. DANE Municipio"].unique() )
  print("")
  print("year: ", year)
  print( "In 2014 and not this year.",
         pd.Series(list(codes14 - codes)) . sort_values() )
  print( "In this year and not 2014.",
         pd.Series(list(codes - codes14)) . sort_values() )


#################
# Código Concepto

vao23 [13] ["Código Concepto"]

# Every year there is a different number of codes.
for year in vao23.keys():
  print ( year, len ( vao23 [year] ["Código Concepto"]
                      . unique() ) )

# Fortunately, each year has all the codes we use.
inversion_codes_we_use = set()
for v in codes.categs_to_codes[t.inversion].values():
  inversion_codes_we_use = { *inversion_codes_we_use, *v }
for year in vao23.keys():
  print("")
  print(year)
  print("Missing from this year: ",
        inversion_codes_we_use -
        set ( vao23 [year] ["Código Concepto"] . unique() ) )
