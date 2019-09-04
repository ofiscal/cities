x = ( pd.DataFrame( { "year"      : [1,1,1,1,2,2,2,2],
                      "item code" : [0,1,2,3,0,1,2,3],
                      "value"     : [0,1,2,3,
                                     10,11,12,13] } ) .
     sort_values( ["year","value"],
                   ascending = False ) )

( x .
  groupby( "year" ) .
  apply( lambda df:
         ( df .
           head(2) .
           drop( columns = ["year"] ) # year is restored when index is reset
          ) ) .
  reset_index() .
  drop( columns = "level_1" ) )

( x .
  groupby( "year" ) .
  apply( lambda df:
         ( df .
           iloc[2:] .
           drop( columns = ["year"] ) # year is restored when index is reset
          ) ) .
  reset_index() .
  drop( columns = "level_1" ) .
  groupby( "year" ) .
  agg( sum ) .
  drop( columns = "item code" ) .
  reset_index() )
