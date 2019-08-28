# The inflation series is indexed by a composite "year-month"
# string column. We only need the 12th month of each year after 2011.

import pandas as pd


def is_last_month(s : str) -> bool:
  return s[-2:] == "12"

def is_after_2011(s : str) -> bool:
  return int( s[:4] ) > 2011

def year_month_to_year(s : str) -> int:
  return int( s[:4] )

deflator = pd.read_csv("data/inflation/raw.csv",encoding="utf-16")
deflator = ( deflator
             [ deflator["when"] .
               apply( is_last_month ) ] )
deflator = ( deflator
             [ deflator["when"] .
               apply( is_after_2011 ) ] )
deflator["year"] = ( deflator["when"] .
                     apply( year_month_to_year ) )
( deflator[["year","deflator"]] .
  to_csv( "data/inflation/final.csv",
          index = False ) )
