if True:
  import pandas as pd
  import Code.util.misc as util
  import Code.build.use_keys as uk

if True: # ingest
  wide_muni = (
    pd.read_csv( "data/regalias/muni.csv" ) .
    rename( columns = {
      "cod_dane"          : "muni code",
      "periodo 2019-2020" : "2019-2020",
      "periodo 2017-2018" : "2017-2018",
      "periodo 2016-2015" : "2015-2016",
      "periodo 2013-2014" : "2013-2014" } ) )
  wide_dept = (
    pd.read_csv( "data/regalias/dept.csv" ) .
    rename( columns = {
      "cod_dane"          : "5 digit dane code",
      "departamento"      : "dept",
      "periodo 2019-2020" : "2019-2020",
      "PERIODO 2018-2017" : "2017-2018",
      "periodo 2015-2016" : "2015-2016",
      "periodo 2014-2013" : "2013-2014" } ) )
  wide_dept["muni code"] = -1

wide_muni = wide_muni.merge( # add "dept code" to regalias
  uk.geo[["muni code","dept code"]],
  on = ["muni code"] )

if True: # fix a "dept code" column for the dept data
         # (it was 1000 times too big)
  wide_dept["dept code"] = (
    wide_dept["5 digit dane code"] .
    astype(str) .
    apply( lambda s: s[:-3] ) .
    astype(int) )
  if False: # a manual test: it should be better than what we get
            # from matching on name
    wide_dept["dept"] = (
      wide_dept["dept"] . str.strip() . str.upper() )
    test = pd.merge( wide_dept, uk.depts,
                     how = "left", on = "dept" )
    print( test[["dept","dept code_x","dept code_y"]] )

if False: # verify that muni codes correspond to (muni,dept) the same way
  # in the regalias data as in our main body of SISFUT data. (They do.)
  for df in [wide_muni,uk.geo]: # lowercase words are easier to compare
    for c in ["muni","dept"]:
      df[c] = df[c].apply( str.lower )
  test_match = (
    wide_muni . merge( uk.geo,
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
    index = False )

if True: # reduce to the data we need
  year_pairs = [ "2017-2018",
                 "2015-2016",
                 "2013-2014" ]
  wide_muni = wide_muni[["dept code","muni code"] + year_pairs]
  wide_dept = wide_dept[["dept code","muni code"] + year_pairs]
  wide = wide_muni.append( wide_dept,
                           sort = True ) # sort columns to align
  wide = util.un_latin_decimal_columns(
    year_pairs, wide )

if True: # change from wide to long, adding a "yaer" column
  long = pd.DataFrame()
  for startYear in [ 2013,
                     2015,
                     2017 ]:
    yearPair = str(startYear) + "-" + str(startYear+1)
    df = ( wide[[ 'muni code', "dept code", yearPair ]] .
           rename( columns = { yearPair : "regalias" } ) )
    df["regalias"] = df["regalias"] / 2
    df["year"] = startYear
    long = long.append(df)
    df["year"] = startYear + 1
    long = long.append(df)
  long.to_csv( "output/regalias.csv",
               index = False )

