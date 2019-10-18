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

total_pop = treated["population"].sum()

treated["pop fraction"] = (
  treated["population"] / total_pop )

budget = 6e6 / (8*1.19) # The money to spend before VAT over 8 days
treated["budget"] = (
  ( treated["pop fraction"] * budget ) .
  apply( lambda n: round(n,2) ) )

treated["muni short"] = (
  treated["muni"] . apply( lambda s: shorten_names.munis[s] ) )
treated["dept short"] = (
  treated["dept"] . apply( lambda s: shorten_names.depts[s] ) )

treated["url"] = (
  treated . apply(
    lambda row : 
    ( "http://luiscarlosreyes.com/wp-content/uploads/2019/10/"
      + row["dept short"] + "__" + row["muni short"]
      + "_" + str(row["muni code"]) + ".pdf" ),
    axis = "columns" ) .
  replace( " ", "-" ) )


treated_1 = treated[ treated["group"]==1 ]
treated_2 = treated[ treated["group"]==2 ]

( pd.concat( [ treated_1 . iloc[0:35],
               treated_2 . iloc[0:34] ],
             axis = "rows" )
  [["muni code","muni","dept","group","url"]].
  to_excel( "manuela.xlsx" ) )

( pd.concat( [ treated_1 . iloc[35:70],
               treated_2 . iloc[34:69] ],
             axis = "rows" )
  [["muni code","muni","dept","group","url"]].
  to_excel( "juan.xlsx" ) )

( pd.concat( [ treated_1 . iloc[70:],
               treated_2 . iloc[69:] ],
             axis = "rows" )
  [["muni code","muni","dept","group","url"]].
  to_excel( "jeff.xlsx" ) )

