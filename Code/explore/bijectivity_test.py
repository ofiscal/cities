# Determine whether the columns in each duplicative pair
# (defined in Code.sisfut_about) indeed correspond 1-to-1.
# They mostly are.
# Anomalies are written to output/non_bijective/.

from itertools import chain
import pandas as pd
import Code.metadata.four_series as sm


######
###### Build dup_columns, from which all other data in this file is built.
######

dup_columns = pd.DataFrame()
for series in sm.series:
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv(
      ( sm.source_folder + "original_csv/"
        + str(year) + "_" + series + ".csv" )
      , usecols = set.intersection(
          set( sm.column_subsets[series] )
        , sm.duplicative_columns_set ) )
    shuttle["year"] = year
    dup_columns = dup_columns.append( shuttle )


######
###### Test whether apparently-duplicate column pairs are in fact isomorphic.
######

# "duplicate pairs": each frame below has 2 columns
dps, dps_unique_pairs, dps_counts = ({},{},{})
for p in sm.duplicative_columns:
  dps[p] = dup_columns[[ p[0], p[1] ]].copy()
  dps[p]["dummy"] = 0
    # only used so that |rows| > 0 after .agg() step
  dps_unique_pairs[p] = dps[p].groupby(list(p)).agg(max)
    # here "max" could as well be any other function
  dps_unique_pairs[p]["count"] = 1
  dps_unique_pairs[p] = dps_unique_pairs[p].drop(columns="dummy")
  for i in [0,1]:
    dps_counts[p[i]] = (
      dps_unique_pairs[p]
      . groupby( p[i] )
      . agg(sum) )

problems = {}
for p in sm.duplicative_columns:
  for i in (0,1):
    if dps_counts[p[i]]["count"].max() > 1:
      print( p, i )
      x = ( dps_counts[p[i]]
            . reset_index() )
      y = ( dps_unique_pairs[p]
            . reset_index()
            . drop( columns = "count" ) )
      x0 = x[ x["count"] > 1 ]
      problems[p[i]] = y.merge(x0, on=p[i])
      problems[p[i]].to_csv( "output/non_bijective/" +
                             p[i] + ".csv"
                           , index = False )


######
###### Test whether department resolves the municipal code-name ambiguity.
###### (It does.)
######

# Hopefully, even though (muni name) can resolve to multiple (muni code)s,
# (muni name, dept name) will resolve to exactly one (muni code).
# (For dept, name and code are isomorphic, as shown above.)
geos = [ "Cód. DANE Municipio"
       , "Nombre DANE Municipio"
       , "Nombre DANE Departamento" ]
       # PITFALL: geo_names depends on this order
geo_code = geos[0]
geo_names = geos[1:]

# "duplicate triples": each frame below has 3 columns.
# What's duplicative, I'm hoping, is that (muni code) <=> (muni name, muni dept).
dts, dts_unique_triples = ({},{})
dts = dup_columns[geos] . copy()
dts["dummy"] = 0
  # only used so that |rows| > 0 after .agg() step
dts_unique_triples = dts.groupby(geos).agg(max)
  # here "max" could as well be any other function
dts_unique_triples["count"] = 1
dts_unique_triples = ( dts_unique_triples
                     . drop( columns="dummy" ) )
for i in [geo_names, geo_code]: # verify bijectivity
  assert (
    ( dts_unique_triples
    . groupby( i )
    . agg(sum) )
    ["count"] . max() == 1 )
