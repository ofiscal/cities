if True:
  import os.path as path
  import pandas as pd
  from typing import Dict
  #
  import Code.common as c


def split_at_middlest_space( s : str ) -> int:
  n = len(s)
  indices = (
    map(
      lambda pair: pair[0],
      filter(
        lambda pair: pair[1],
        zip( range( 1, 1+n ),
             map( lambda c: c==" ",
                  s ) ) ) ) )
  indices_with_distance = list( map( lambda i: (i, abs(i-n/2)),
                                     indices ) )
  min_distance = min( list( map( lambda pair: pair[1],
                                 indices_with_distance.copy() ) ) )
  closest = ( list( filter( lambda pair: pair[1] == min_distance,
                            indices_with_distance ) )
              [0][0] )
  l = list(s)
  l[closest-1] = "\n"
  return "".join(l)

dept_data = (
  pd.read_csv (
    path.join ( c.indata,
                "regions",
                "depts-brief.csv" ) ) )
muni_data = (
  pd.read_csv (
    path.join ( c.indata,
                "regions",
                "munis-brief.csv" ) )
  . drop_duplicates() )

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
