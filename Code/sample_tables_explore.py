# This code is designed to be run interactively in a REPL,
# after running sample_tables.py, to diagnose the latter.

for s in ser.series:
  print( s.name )
  spots = (
    items_grouped # goes wrong for items_grouped, but okay before that
    [s.name]
    [["muni code","dept code","dept"]] .
    groupby( ["muni code","dept code"] ) .
    agg("first") .
    reset_index() )
  print( spots[ ( spots["muni code"] == -1 ) &
                ( spots["dept"].isin( [ "ANTIOQUIA",
                                        "CESAR",
                                        "CHOCÓ",
                                        "ARAUCA" ] ) ) ] )
