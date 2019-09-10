for s in ser.series:
  print( s.name )
  df = raw[s.name]
  df[ df["muni"] == "BOGOTÁ, D.C." ]["muni code"].unique()

  for i in sorted( df["muni"].astype(str).unique() ):
    print(i)
  print( (raw[s.name]["muni code"].unique() == 11001).any() )


for s in ser.series:
  print( s.name )
  spots = (
    raw[s.name]
    [["muni code","dept code"]] .
    groupby( ["muni code","dept code"] ) .
    agg(sum) .
    reset_index() )
  # print( spots )
  print( spots["muni code"] == 11001 ) # 11001 = Bogota

for s in ser.series:
  df = raw[s.name]
  print( s.name )
  print( df["muni"].unique() )
  print( df["dept"].unique() )

