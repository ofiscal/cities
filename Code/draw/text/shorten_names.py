if True:
  from typing import Dict
  import pandas as pd
  import Code.common as c

dept_data = pd.read_csv( "data/regions/depts-brief.csv" )
muni_data = ( pd.read_csv( "data/regions/munis-brief.csv" ) .
          drop_duplicates() )

def update_dict( d : Dict["k","v"],
                 key : "k",
                 value : "v" ):
  d[key] = value

depts, munis = {},{}

for (data,dct) in [ (dept_data, depts),
                    (muni_data, munis) ]:
  data.apply(
    lambda row:
    update_dict( dct,
                 row["long"],
                 row["short"] ),
    axis = "columns" )

