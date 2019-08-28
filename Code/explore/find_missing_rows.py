"""
## How to verify 90 rows are missing.
Verify this by running "wc -l * | grep total".

The raw data (21 files) has 4199219 lines.
  4199219 - 21 = 4199198 rows.
The collected data (3 files) has 4199111 lines.
  4199111 - 3 = 4199108 rows.
There are thus 4199198 - 4199108 =
  90 rows missinng.
"""

import os

from Code.build.conceptos_1_defs import collect_raw
import Code.build.sisfut_metadata as sm


folder = {
  "orig" : "data/sisfut/original_csv",
  "bughunt" : "output/explore/missing_rows" }
folder["with_index"] = folder["bughunt"] + "/with_index"
folder["collected"] = folder["bughunt"] + "/collected"
for i in folder.keys():
  if not os.path.exists( folder[i] ):
    os.makedirs( folder[i] )


if True: # add a manual index to each file
  for filename in os.listdir( folder["orig"] ):
    with open( folder["orig"] + "/" + filename) as f:
        lines = f.readlines()
    with open( folder["with_index"] + "/" + filename, "w") as f:
      f.write(
        "manual index," + lines[0] )
      for i in range(1,len(lines)):
        f.write(
          str(i) + "," + lines[i] )

dfs = collect_raw( folder["with_index"],
                   extra_columns = {"manual index"} )

for s in sm.series:
  dfs[s].to_csv( folder["collected"] + "/" + s + ".csv",
                 index = False )

### FOUND THEM!

for s in ["inversion"]: # ingresos and funcionamiento are good
  df = dfs[s]
  df["diff"] = df["manual index"].diff()
  df["diff-lead"] = df["diff"].shift(-1)
  weird = df[ (df["diff"     ] != 1) |
      (df["diff-lead"] != 1) ][["year","manual index","diff","diff-lead","muni code","dept code","item code"]]


"""
##  How I know "ingresos" and "funcionamiento" are okay.
No python necessary; just count lines in files.
In total the raw files should have 7 more lines than the collected files,
because the raw ones have 7 headers, and the collected file just has 1.
It bears out:

ingresos:
  output/explore/missing_rows/with_index$ wc *ingreso* | grep total
    993941   7043387 151922753 total
  output/explore/missing_rows/with_index$ wc ../collected/ingresos.csv
    993935  1841460 81642432 ../collected/ingresos.csv

funcionamiento:
  output/explore/missing_rows/with_index$ wc *funcion* | grep total
    1454505  20550122 310136025 total
  output/explore/missing_rows/with_index$ wc ../collected/funcionamiento.csv
    1454499   2715778 123125951 ../collected/funcionamiento.csv


##  no last rows are missing
Compare some python (left) with some bash (right):
>>> ( df.groupby("year")
      ["manual index"].max() )
year                            wc -l *inver*
2012    225565                  225566 2012_inversion.csv
2013    242819                  242820 2013_inversion.csv
2014    243636                  243637 2014_inversion.csv
2015    252566                  252567 2015_inversion.csv
2016    247112                  247113 2016_inversion.csv
2017    268355                  268356 2017_inversion.csv
2018    270713                  270714 2018_inversion.csvx


##  no first rows are missinng
> len( df[ df["manual index"] == 1 ] )
7


##  TODO - therefore, every missing row can be identified by
take all rows where diff = 2
subtract 1 from their manual index
note the year
search for rows starting with those indices in the file for that yearx
"""
