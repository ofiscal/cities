if True:
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.series_metadata as ser


if True: # geo data
  geo = (
    pd.read_csv( "output/keys/geo.csv",
                 encoding = "utf-16" ) .
    rename( columns =
            { "Cód. DANE Municipio" : "muni code",
              "Cód. DANE Departamento" : "dept code",
              "Nombre DANE Municipio" : "muni",
              "Nombre DANE Departamento" : "dept" } ) )
  depts = ( geo[["dept code","dept"]] .
            groupby( "dept code" ) .
            agg('first') .
            reset_index() )
  munis = geo[["muni code","muni"]]

if True: # merge geo data into main data
  source   = "output/budget_6_deflate/recip-1"
  dfs = {}
  for s in ser.series:
    sn = s.name
    df = pd.read_csv( source + "/" + sn + ".csv",
                      encoding = "utf-16" )
    df = df.merge( munis,
                   how = "left", # b/c in geo, muni code is never -1
                   on = ["muni code"] )
    df = df.merge( depts,
                   on = ["dept code"] )
    dfs[sn] = df

# RESUME HERE: Restricting to the slice of data I need.
# Left to do: For each (muni,dept,year), take the top 5 expenditures,
# and sum the rest into a sixth.
# See tables_demo.py for a start.
muni_sample = {}
for s in ser.series:
  acc = pd.DataFrame()
  for m in [ "BOGOTÁ, D.C.",
             "SANTA MARTA",
             "FILANDIA",
             "VALLE DEL GUAMUEZ" ]:
    acc = acc.append( df[ df["muni"] == m ] )
  muni_sample[s.name] = acc

group_vars = ["muni code","dept code","year","item code"]
( muni_sample[s.name] .
  sort_values( group_vars )
  [group_vars + [s.pesos_col]] )

if False: # some hand-run tests
  len(df)
  ( df[['muni code', "muni",'year', 'item code', 'dept code',"dept"]] .
    describe(include="all").transpose()
    [["count","mean","min","max"]] )
  np.nan in df["muni"].unique()
  np.nan in df["dept"].unique()
