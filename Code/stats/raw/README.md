These were created from the raw data,
right after running "conceptos_1_defs.collect_raw()",
using the following code:

```
stats = {}
for s in sm.series:
  df = dfs[s]
  stats[s] = pd.DataFrame(
    { "dtype"   :     df.dtypes,
      "min"     :     df.min(),
      "max"     :     df.max(),
      "missing" : 1 - df.count() / len(df) } )
  stats[s].to_csv( "Code/stats/raw/" + s + ".csv" )
```
