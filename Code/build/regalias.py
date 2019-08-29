import pandas as pd


folder = "data/regalias"

wide = pd.read_csv( folder + "/raw.csv",
                    encoding = "utf-16" )

wide = wide.rename( columns = {
  "periodo 2019-2020" : "2019-2020",
  "periodo 2017-2018" : "2017-2018",
  "periodo 2016-2015" : "2015-2016",
  "periodo 2013-2014" : "2013-2014" } )

if False: # verify that muni codes correspond to (muni,dept) the same way
  # in the regalias data as in our main body of SISFUT data. (They do.)
  geo = (
    pd.read_csv( "output/keys/geo.csv" ) .
    rename( columns =
            { "Cód. DANE Municipio" : "muni code",
              "Nombre DANE Municipio" : "muni",
              "Nombre DANE Departamento" : "dept" } ) )

  for df in [wide,geo]:
    for c in ["muni","dept"]:
      df[c] = df[c].apply( str.lower )
  
  test_match = (
    wide . merge( geo,
                  on = "muni code" )
    [["muni code","muni_x","muni_y","dept_x","dept_y"]]
  )
  
  test_match = test_match[
    ( test_match["muni_x"] != test_match["muni_y"] ) |
    ( test_match["dept_x"] != test_match["dept_y"] ) ]
  
  # There are a few mismatches. Eyeballing the data in OpenOffice,
  # one sees that they are due entirely to minor spelling differences,
  # e.g. "don matías" v. "donmatías"
  test_match.to_csv(
    "output/explore/regalias_muni_codes.csv",
    encoding="utf-16",
    index = False )
