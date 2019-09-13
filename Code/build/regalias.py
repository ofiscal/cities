import pandas as pd


wide = pd.read_csv( "data/regalias.csv",
                    encoding = "utf-16" )

wide = wide.rename( columns = {
  "periodo 2019-2020" : "2019-2020",
  "periodo 2017-2018" : "2017-2018",
  "periodo 2016-2015" : "2015-2016",
  "periodo 2013-2014" : "2013-2014" } )

geo = (
  pd.read_csv( "output/keys/geo.csv",
               encoding = "utf-8" ) .
  rename( columns =
          { "Cód. DANE Municipio" : "muni code",
            "Cód. DANE Departamento" : "dept code",
            "Nombre DANE Municipio" : "muni",
            "Nombre DANE Departamento" : "dept" } ) )

if False: # verify that muni codes correspond to (muni,dept) the same way
  # in the regalias data as in our main body of SISFUT data. (They do.)
  for df in [wide,geo]: # lowercase words are easier to compare
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
    encoding="utf-8",
    index = False )

wide = wide.merge( # add "dept code" to regalias
  geo[["muni code","dept code"]],
  on = ["muni code"] )

if True: # change from wide to long, adding a "yaer" column
  long = pd.DataFrame()
  for startYear in [ 2013,
                     2015,
                     2017 ]:
    yearPair = str(startYear) + "-" + str(startYear+1)
    df = wide[[ 'muni code', "dept code", yearPair ]]
    df = df.rename( columns = { yearPair : "regalias" } )
    df["regalias"] = df["regalias"] / 2
    df["year"] = startYear
    long = long.append(df)
    df["year"] = startYear + 1
    long = long.append(df)
  long.to_csv( "output/regalias.csv",
               encoding="utf-8",
               index = False )

