# The inflation series is indexed by a composite "year-month"
# string column. We only need the 12th month of each year after 2011.
#
# PITFALL: The inflation indices I downloaded in 2019
# are not, in levels, the same as those I downloaded in 2023.
# In fact, the percent changes aren't even the same either,
# but they're pretty close. I don't know which inflation series
# I was using in 2019. I've given the 2023 series the precise name
# "inflation-no-food-2023-03.csv", to avoid similar confusion in future.

from   os import path, makedirs
import pandas         as pd
#
import Code.common    as common
from   Code.params.cl_arg_universe import vintage_universe


##################################
# Define `deflator : pd.DataFrame`

if common.vintage == 2019:

  def is_last_month(s : str) -> bool:
    return s[-2:] == "12"

  def is_after_2011(s : str) -> bool:
    return int( s[:4] ) > 2011

  def year_month_to_year(s : str) -> int:
    return int( s[:4] )

  deflator = pd.read_csv (
    path.join ( common.indata,
                "inflation.csv" ),
    encoding = "utf-16" )
  deflator = ( deflator
               [ deflator["when"] .
                 apply( is_last_month ) ] )
  deflator = ( deflator
               [ deflator["when"] .
                 apply( is_after_2011 ) ]
               . copy() )
  deflator["year"] = ( deflator["when"] .
                       apply( year_month_to_year ) )

elif common.vintage == 2023:

  deflator = pd.read_csv (
    path.join ( common.indata,
                "inflation.csv" ) )
  deflator = deflator [ deflator["month"] == 12 ]

else: raise ValueError ( "vintage not in ", vintage_universe )


#########################################
# Write `deflator : pd.DataFrame` to disk

if not path.exists ( common.outdata ):
  makedirs ( common.outdata )
( deflator[["year","deflator"]] .
  to_csv ( path.join ( common.outdata,
                       "inflation.csv" ),
           encoding="utf-8",
           index = False ) )
