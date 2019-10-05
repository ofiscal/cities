These data were created from the results of conceptos_1.py,
by running the following code:

```
stats = {}
for s in sm.series:
  new_columns = ["item categ", "item top"]
  df = dfs[s][new_columns]
  stats[s] = pd.DataFrame(
    { "dtype"   :     df.dtypes,
      "min"     :     df.min(),
      "max"     :     df.max(),
      "missing" : 1 - df.count() / len(df) } )
  stats[s].to_csv( "Code/stats/item_columns/" + s + ".csv" )
```
