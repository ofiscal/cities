# problem: ANTIOQUIA, MUTATÁ, 2014
# output/pivots/recip-1/ANTIOQUIA/MUTATÁ/ingresos-pct.csv
# It's missing "dinero soberante".

import pandas as pd
from Code.build.use_keys import geo

# The problem in my data
bad = pd.read_csv(
  "output/pivots/recip-1/ANTIOQUIA/MUTATÁ/ingresos-pct.csv" )
bad["item categ"] = bad["item categ"].apply( lambda s: s[:10] )
bad # see the missing value

# Finding that place
where = geo[ (geo["dept"]== "ANTIOQUIA") &
             (geo["muni"]== "MUTATÁ") ]
mc = where["muni code"].iloc[0]

# The problem is in the original data
orig = pd.read_csv(
  "data/sisfut/csv/2014_ingresos.csv",
  usecols = ["Cód. DANE Municipio","Código Concepto", "Concepto"] )
orig[ (orig["Cód. DANE Municipio"]==mc) &
      (orig["Código Concepto"]=="TI.B" ) ] # absent (bad)
orig[ (orig["Cód. DANE Municipio"]==mc) &
      (orig["Código Concepto"]=="TI.A" ) ] # present (good)

