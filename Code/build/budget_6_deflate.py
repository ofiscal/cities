if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ser


if True: # folders
  source = os.path.join ( c.outdata, "budget_5_add_regalias",
                          "recip-" + str(c.subsample) )
  dest   = os.path.join ( c.outdata, "budget_6_deflate",
                          "recip-" + str(c.subsample) )
  if not os.path.exists ( dest ):
    os.makedirs         ( dest )

if True: # The inflation data.
  deflator = pd.read_csv (
    os.path.join ( c.outdata,
                   "inflation.csv" ) )
  deflator["deflator"] = ( # This statement has two purposes:
    # (1) Normalize it to be in terms of 2018 pesos.
    # (2) Invert it, so that below I can multiply a series by it,
    #     which is faster than dividing the series by it.
    1 / ( deflator["deflator"] /
          float ( deflator
                  [ deflator["year"] == 2018 ]
                  ["deflator"]
                  . iloc[0] ) ) )

for s in ser.series:
  df0 : pd.DataFrame = ( # The original, not to be mutated.
    pd.read_csv ( os.path.join ( source,
                                 s.name + ".csv" ) ) )
  df1 : pd.DataFrame = (
    df0 . copy () # A copy, to be mutated and saved.
    . merge ( deflator, on = "year" ) )

  for c in s.money_cols:
    df1[c] = df1[c] * df1["deflator"]
    if True: # A loose test:
             # Verifies that the ratio total money from 2018 to 2013
             # has fallen by between 1.2 and 1.3.
             # (The peso devalued by a factor of very close to 1.25
             # over that time. The exact value depends a bit
             # on which inflation series (from 2023 or from 2019) is used.)
      ratio_pre_deflation  = ( ( df0 [ df0["year"] == 2018 ] [c] . sum() ) /
                               ( df0 [ df0["year"] == 2013 ] [c] . sum() ) )
      ratio_post_deflation = ( ( df1 [ df1["year"] == 2018 ] [c] . sum() ) /
                               ( df1 [ df1["year"] == 2013 ] [c] . sum() ) )
      assert ratio_pre_deflation > ratio_post_deflation * 1.2
      assert ratio_pre_deflation < ratio_post_deflation * 1.3
      assert ( # Also, it should be that the 2013 peso data is bigger
               # in the new data frame than in the old one.
        ( df0 [ df0["year"] == 2013 ] [c] . sum() ) <
        ( df1 [ df1["year"] == 2013 ] [c] . sum() ) )

  df1 = df1.drop( columns = ["deflator"] )
  df1.to_csv (
    os.path.join ( dest,
                   s.name + ".csv" ),
    index = False )
