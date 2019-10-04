# This demosntrates that:
# The raw data does include a few negative budget items,
# but they must be very disaggregated, because after stage 1p5,
# which keeps only the aggregate codes we need,
# the minimum rises to zero.

if True:
  import pandas as pd
  import numpy as np
  #
  import Code.metadata.raw_series as sis
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes


d1 = {}
for s in sis.series:
  d1[s] = pd.read_csv( "output/budget_1/" + s + ".csv" )

for (s,c) in [("ingresos","item recaudo"),
              ("inversion","item oblig"),
              ("funcionamiento","item oblig")]:
  print(s)
  d1[s][c].describe()

d1p5 = {}
for s in ["ingresos","gastos"]:
  d1p5[s] = pd.read_csv( "output/budget_1p5/" + s + ".csv" )

for (s,c) in [("ingresos","item recaudo"),
              ("gastos","item oblig")]:
  print(s)
  d1p5[s][c].describe()
