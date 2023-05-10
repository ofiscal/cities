# SOLVED, I think:
# Add "intereses" and "amortizaciones"
# from `Operación Efectiva de Caja 2000-2021`
# to get that year's debt payments.

from typing import List, Dict, GenericAlias
import os.path as path
import pandas as pd
import numpy as np


#####
##### Define paths
#####

year : GenericAlias = int
in19 = "data/2019/sisfut/csv"
in23 = "data/2023/sisfut/csv"
out19 = "output/2019"


#####
##### In inputs, compare column names and dtypes
#####

# The "view as of" (vao) years 19 and 23.
# This will be a dictionary, the keys of which are 2-digit years,
# and the values of which are pandas data frames.
vao19 : Dict [year, pd.DataFrame] = {}
vao23 : Dict [year, pd.DataFrame] = {}

for y in range(13,22):
  vao23[y] = pd.read_csv (
    path.join ( in23, "20" + str(y) + "_deuda.csv" ) )
  if y <= 18:
    vao19[y] = pd.read_csv (
      path.join ( in19, "20" + str(y) + "_deuda.csv" ) )

# As of 2019, each data frame had the same columns amd dtypes
for df in vao19.values():
  print(df.columns
        .equals(
          vao19[13].columns ) )
  print(df.dtypes
        .equals(
          vao19[13].dtypes ) )

# As of 2023, each data frame had the same columns
for df in vao23.values():
  print(df.columns
        .equals(
          vao23[13].columns ) )

# and they *mostly* had the same dtypes:
pd.options.display.min_rows = 500
for df in vao23.values():
  print(df.dtypes
        .equals(
          vao23[13].dtypes ) )

# The exception is at year 16, and it's no big deal --
# it just uses ints where the others use floats.
mismatches = pd.DataFrame()
for c in vao23[13].columns:
  if (vao23[13][c].dtype) != (vao23[16][c].dtype):
    mismatches = pd.concat (
      [ mismatches,
        pd.Series ( { "column" : c,
                      "2013 type" : vao23[13][c].dtype,
                      "2016 type" : vao23[16][c].dtype } ) ],
      axis = "columns" )
mismatches.transpose()

# The sets of columns aren't the same in the two views
# (i.e. the view from 2019 and the view from 2023).
( vao19[13].columns
  . equals(
    vao23[13].columns ) )


#####
##### Determine what I need from them
#####

# This raw data seems less interesting ...
# prod19_0 = pd.read_csv(
#   path.join ( out19,
#               "budget_0_collect",
#               "deuda.csv" ) )

# ... than this cleaned data.
prod19_1 = pd.read_csv(
  path.join ( out19,
              "budget_1",
              "deuda.csv" ) )

# Seems simple enough.
prod19_1.dtypes

# According to the definition of categs_to_code
# in Code/build/classify_budget_codes.py,
# we are only interested in rows for which the "item code" is "T".


#####
##### Determine what to keep in them
#####

# Here are the columns I end up with.

prod19_1.dtypes
# name           object
# dept code       int64
# muni code     float64
# item code      object
# item oblig    float64
# year            int64

# "year" is fixed in each data set.
# The others will correspond to (hopefully exactly one)
# column in the input data.

vao23[13].columns

# "Nombre Entidad" in the new data is clearly what I eventually call "name".
# "dept code" and "muni code"
# are "Cód. DANE Departamento" and "Cód. DANE Municipio".

# That leaves "item code" and "item oblig".
# Nothing in the new data looks like that.


#####
##### Daniel explains I'm using the wrong 2023 data
#####

# What I need now is instead
# "Operación Efectiva de Caja 2000-2021",
# also downloadable from SISFUT (see `data/2023/sisfut/README.md`).
# Relevant columns in it are likely to include:
#   Intereses de la deuda pública
#   Regalías (not deuda but good for this project)
#   Déficit o Superávit Total
#   FINANCIAMIENTO
#   Crédito Externo neto
#   Desembolsos
#   Amortizaciones
#   Crédito Interno neto
#   Desembolsos
#   Amortizaciones
#   Recursos del Balance, Variación de Depósitos y Otros

# SOLVED! Daniel says debt payments = intereses + amortizaciones.
