import pandas as pd
import Code.sisfut_about as sc

dfs = {}
for series in ["ingresos","inversion","funcionamiento"]:
  dfs[ series ] = pd.DataFrame()
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv( source_folder + "original_csv/"
                           + str(year) + "_" + series + ".csv"
                         , usecols = sc.column_subsets[series]
                         , nrows = 1000 # TODO : DROP THIS LINE eventually
    )
    dfs[ series ] = dfs[ series ].append( shuttle )
  dfs[ series ].to_csv( source_folder + "collated-subsets/"
                        + series + ".csv"
                      , index = False)
