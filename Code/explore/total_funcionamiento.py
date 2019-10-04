import numpy as np
import pandas as pd

import Code.common as c
import Code.util.misc as util
import Code.metadata.four_series as sm


######
###### The result:
###### (item code == 1) <=> (item == total gastos de funcionamiento)
######

# Here's a proof. (First run the if statement below to construct df.)

df[ df["item code"] == "1" ]["item"].unique()
df[ df["item"] == "total gastos de funcionamiento" ]["item code"].unique()


######
###### The initial exploration
######

if True: # This is like build.budget_1_defs.collect_raw
  df = pd.DataFrame()
  for year in range( 2012, 2019 ):
    shuttle = (
      pd.read_csv(
        "data/sisfut/csv/" + str(year) + "_funcionamiento.csv",
        usecols = set.union(
          {"Concepto"},
          set.difference(
            set( sm.column_subsets_long["funcionamiento"] ),
            sm.omittable_columns_long ) ) ) . # omit the omittable ones
      rename( columns = dict( sm.column_subsets["funcionamiento"] ) ) )
    shuttle["year"] = year
    df = df . append(shuttle)

df["item"] = df["item"].apply( str.lower )
df["item-says-total"] = ( df["item"] .
                          str.extract( re.compile( "(total)" ) ) )
df[ ~ pd.isnull( df["item-says-total"] ) ]["item"].unique()
df[ ~ pd.isnull( df["item-says-total"] ) ][["item code","item"]]
