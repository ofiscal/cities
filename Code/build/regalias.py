if True:
  from   os import path, makedirs
  import pandas               as pd
  import pathlib
  #
  import Code.build.use_keys  as uk
  import Code.common          as common
  from   Code.params.cl_arg_universe import vintage_universe
  import Code.util.misc       as util


# We currently have no regalias data for the view from 2023,
# so this just creates symlinks to the last stage.
if common.vintage == 2023:
  for p in [ pathlib.Path ( q )
             for q in
             [ path.join ( common.indata,  "regalias", "muni.csv" ),
               path.join ( common.indata,  "regalias", "dept.csv" ),
               path.join ( common.outdata, "regalias.csv" ) ] ]:
    if not path.exists ( p.parent ):
      makedirs(          p.parent )
    p.touch ()

elif common.vintage == 2019:
  if not path.exists ( common.outdata ):
    makedirs ( common.outdata )

  if True: # ingest
    wide_muni = (
      pd.read_csv (
        path.join (
          common.indata,
          "regalias",
          "muni.csv" ) ) .
      rename ( columns = {
        "cod_dane"          : "muni code",
        "periodo 2019-2020" : "2019-2020",
        "periodo 2017-2018" : "2017-2018",
        "periodo 2016-2015" : "2015-2016",
        "periodo 2013-2014" : "2013-2014" } ) )
    wide_dept = (
      pd.read_csv (
        path.join ( common.indata,
                    "regalias",
                    "dept.csv" ) ) .
      rename( columns = {
        "cod_dane"          : "5 digit dane code",
        "departamento"      : "dept",
        "periodo 2019-2020" : "2019-2020",
        "PERIODO 2018-2017" : "2017-2018",
        "periodo 2015-2016" : "2015-2016",
        "periodo 2014-2013" : "2013-2014" } ) )
    wide_dept["muni code"] = 0

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
    # in the regalias data as in our main body of SISFUT data.
    # TODO ? They did in 2019. I have not repeated the exercise in 2023.
    # Spelling differences can throw it off, so it needs human oversight.
    for df in [wide_muni, uk.geo]: # lowercase words are easier to compare
      for c in ["muni", "dept"]:
        df[c] = df[c].apply ( str.lower )
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
    test_match.to_csv (
      path.join ( common.outdata, "explore",
                  "regalias_muni_codes.csv" ),
      index = False )

  if True: # reduce to the data we need
    year_pairs = [ "2017-2018",
                   "2015-2016",
                   "2013-2014" ]
    wide_muni = wide_muni[["dept code","muni code"] + year_pairs]
    wide_dept = wide_dept[["dept code","muni code"] + year_pairs]
    wide = pd.concat( [wide_muni, wide_dept ],
                      sort = True ) # Sort columns to conform the two frames.
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
      long = pd.concat( [long, df] )
      df["year"] = startYear + 1
      long = pd.concat( [long, df] )
    long.to_csv ( path.join ( common.outdata,
                              "regalias.csv" ),
                  index = False )

else:
  raise ValueError ( "vintage not in ", vintage_universe )
