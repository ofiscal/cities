# PURPOSE:
# Switch from two series to four:
#   2: gastos, ingresos
#   4: gastos, gastos-pct, ingresos, ingresos-pct
# Convert peso values to percentages for the -pct files.
#   TRICKY: Must include munis which spent nothing on that item.
# Compute an "average municipality" for each department.
#   But only in the -pct files.

if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ser

if True: # folders
  source = "output/budget_6_deflate/recip-"        + str(c.subsample)
  dest   = "output/budget_6p5_dept_average/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input data
  dfs = {}
  for s in ser.series:
    dfs[s.name] = pd.read_csv(
      source + "/" + s.name + ".csv" )

for s in ser.series:
  df = dfs[s.name]
  assert False == "Something clever here."

