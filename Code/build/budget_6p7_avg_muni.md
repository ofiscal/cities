This file a tricky test at the end of Code/build/budget_6p7_avg_muni.py.

The test is to verify that the number of rows in each %-valued series is equal to the sum of the number of rows in the corresponding peso-valued series and the number of averages that should have been computed:
```
    assert len(pct_series) == nAverages + len(non_pct_series)
```

The number of averages that should have been computed is defined this way:
```
    nAverages = len(
      non_pct_series
      [ non_pct_series["muni code"] != 0 ] .
        # The logic behind needing to include the preceding line
        # is complicated; see budget_6p7_avg_muni.md
      groupby( ["dept code","year","item categ"] ) .
      apply( lambda _: () ) )
```

Why do we need to first restrict that set to rows in which the muni code is not equal to zero?

The answer is that there are two `(dept code, year, item categ)` triples for which we have dept-level data but no muni-level data:
```
>>> pct_series[
...   ( (pct_series["dept code"] == 99 ) &
...     (pct_series["year"] == 2016 ) &
...     (pct_series["item categ"] == "Servicio de la deuda" ) ) |
...   ( (pct_series["dept code"] == 88 ) &
...     (pct_series["year"] == 2015 ) &
...     (pct_series["item categ"] == "Agropecuario" ) ) ]
       dept code  muni code  year            item categ    item oblig
86772         88        0.0  2015          Agropecuario  3.728199e+09
88552         99        0.0  2016  Servicio de la deuda  1.099429e+08
```

(Dept 88 = San Andrés, and dept 99 = Vichada.)

Therefore there was no average computed for those two `(dept,year,categ)` triples.

We can verify that those are the only two `(dept,year,categ)` triples for which no muni was computed by doing the following:
```
avs = ( pct_series # triples for which an average was computed
        [ pct_series["muni code"] == -2 ]
        [["dept code","year","item categ"]] .
        drop_duplicates() )
all = ( pct_series # all triples
        [["dept code","year","item categ"]] .
        drop_duplicates() )
( pd.concat( [avs,all,all] ) . # the set of triples in avs and not in all
  drop_duplicates(keep=False) )
  # empty -- good
( pd.concat( [all,avs,avs] ) . # the set of triples in all and not in avs
  drop_duplicates(keep=False) )
  # Gives this:
  #        dept code  year            item categ
  # 86772         88  2015          Agropecuario
  # 88552         99  2016  Servicio de la deuda
```
