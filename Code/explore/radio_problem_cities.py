# In the radio script we state how much a place spent on edu, health and
# infrastructure. This code demonstrates that some places only reported
# those for the last two years. For them, the mean we would report with
# the current process is therefore biased upward by a factor of 1/3.

import Code.metadata.terms as t

gas = pd.read_csv(
  "output/budget_7_verbose/recip-1/" + s.name + ".csv")

geo = ( # geo indices of interest
  gas .
  copy()
  [space] .
  drop_duplicates() )

gas = (
  gas[
    ( gas["item categ"] .
      isin( [t.edu, t.infra, t.salud] ) ) &
    ( gas["year"] > 2015 ) ] .
  copy() )
gas["years"] = 1
gr = (
  gas . groupby(
    ["dept code", "muni code", "item categ"] ) .
  agg( sum ) .
  reset_index() )
bad_mcs = pd.DataFrame(
  { "muni code" : gr[ gr["years"] < 3 ]["muni code"].unique() } )

bad_mcs["muni"] = (
  bad_mcs["muni code"] .
  apply( lambda cell:
         str( geo.loc[ geo["muni code"] == cell,
                       "muni" ] .
              iloc[0] ) ) )

