if True:
  import pandas as pd
  import Code.build.use_keys as uk
  import Code.draw.text.shorten_names as shorten_names

if True: # initial data
  treated = pd.read_excel( "data/regions/fb-treated.xlsx" )
  geo = uk.geo
  geo["muni code"] = (
    geo["muni code"] . astype( int ) )
  population = (
    pd.read_excel(
      "data/regions/population_2018.xlsx" )
    [["muni code","population"]] )

treated = (
  treated . drop( columns = ["muni","dept"] ) .
  merge( population,
         how = "inner",
         on = "muni code" ) .
  merge( geo, how = "inner", on = "muni code" ) )

( treated . # for the README file in the cities-output repo
  apply(
    ( lambda row:
      "[" + row["dept"] + " -- " + row["muni"] +
      # "](https://raw.githubusercontent.com/ofiscal/cities-output/master/reportes/" +
     "](http://luiscarlosreyes.com/wp-content/uploads/2019/10/" +
     str(row["muni code"]) + ".pdf)\n"
     ),
    axis = "columns" ) .
  to_csv( "for-readme.txt",
         index = False) )

total_pop = treated["population"].sum()

treated["pop fraction"] = (
  treated["population"] / total_pop )

budget = 6e6 / (8*1.19) # The money to spend before VAT over 8 days
treated["budget"] = (
  ( treated["pop fraction"] * budget ) .
  apply( lambda n: round(n,2) ) )

treated["muni short"] = (
  treated["muni"] . apply( lambda s: shorten_names.munis[s] ) )
treated["muni no space"] = (
  treated["muni short"] . apply( lambda s:
                                 s.replace(" ","") ) )
treated["dept short"] = (
  treated["dept"] . apply( lambda s: shorten_names.depts[s] ) )

treated["url"] = (
  treated . apply(
    lambda row :
    # "https://raw.githubusercontent.com/ofiscal/cities-output/master/reportes/" +
    "http://luiscarlosreyes.com/wp-content/uploads/2019/10/" +
    str(row["muni code"]) + ".pdf",
    axis = "columns" ) )

treated["title"] = "Finanzas municipales"
treated["description"] = (
  "¿En qué se gasta la plata el gobierno de #" +
  treated["muni no space"] + "?" )

cols_to_keep = ["muni code","muni","dept","group",
                "url","title","description"]

treated_1 = treated[ treated["group"]==1 ]
treated_2 = treated[ treated["group"]==2 ]

( pd.concat( [ treated_1 . iloc[0:35],
               treated_2 . iloc[0:34] ],
             axis = "rows" )
  [cols_to_keep] .
  to_excel( "manuela.xlsx" ) )

( pd.concat( [ treated_1 . iloc[35:70],
               treated_2 . iloc[34:69] ],
             axis = "rows" )
  [cols_to_keep] .
  to_excel( "juan.xlsx" ) )

( pd.concat( [ treated_1 . iloc[70:],
               treated_2 . iloc[69:] ],
             axis = "rows" )
  [cols_to_keep] .
  to_excel( "jeff.xlsx" ) )

