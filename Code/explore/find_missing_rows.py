import os

from Code.build.conceptos_1_defs import collect_raw
import Code.build.sisfut_metadata as sm


folder = {
  "orig" : "data/sisfut/original_csv",
  "bughunt" : "output/explore/missing_rows" }
folder["with_index"] = folder["bughunt"] + "/with_index"
folder["collected"] = folder["bughunt"] + "/collected"

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
  df[ (df["diff"     ] != 1) |
      (df["diff-lead"] != 1) ][["year","manual index","diff","diff-lead"]]
