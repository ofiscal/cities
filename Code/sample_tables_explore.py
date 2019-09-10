for s in ser.series:
  print( s.name )
  spots = (
    raw[s.name]
    [["muni code","dept code"]] .
    groupby( ["muni code","dept code"] ) .
    agg(sum) .
    reset_index() )
  print( spots )
  print( spots["muni code"] == 1101 ) # 1101 = Bogota

for s in ser.series:
  df = raw[s.name]
  print( s.name )
  print( df["muni"].unique() )
  print( df["dept"].unique() )

