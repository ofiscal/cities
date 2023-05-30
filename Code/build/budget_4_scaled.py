"""
PITFALL
This only corrects the peso-valued columns we are interested in --
namely "item recaudo" and "item oblig".

PURPOSE: (1) Multiply pre-2017 values by 1000,
because (as you might guess) in the raw data,
pre-2017 peso values are about 1000 times smaller than those post-2016.

(2_ After that,
test that the percentage change from one year to the next is well behaved,
to ensure that no similar problems remain present.
"""

if True:
  from typing import List, Set, Dict
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ts
  import Code.metadata.raw_series as sm
  import Code.explore.order_of_mag_x_yrs_defs as lib


if True:
  source = os.path.join ( c.outdata,
                          "budget_3_dept_muni_year_item",
                          "recip-" + str(c.subsample) )
  dest   = os.path.join ( c.outdata,
                          "budget_4_scaled",
                          "recip-" + str(c.subsample) )
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # function to multiply early years by 1000
  def correct_peso_columns( cols : List[str],
                            df : pd.DataFrame ) -> pd.DataFrame:
    """ PITFALL: Mutates its input. """
    for c in cols:
      df.loc[ df["year"] < 2017,
              c] *= 1000
    return df

  if True: # test it
    x = pd.DataFrame( {"a" : [0,1,2,3,4,5],
                       "b" : [0,1,2,3,4,5],
                       "c" : [0,1,2,3,4,5],
                       "year" : list( range( 2013, 2019 ) ) } )
    assert (
      correct_peso_columns( ["a","b"], x )
      .equals(
        pd.DataFrame( {
          "a" : [0,1000,2000,3000,4,5],
          "b" : [0,1000,2000,3000,4,5],
          "c" : [0,1,2,3,4,5],
          "year" : list ( range( 2013, 2019 ) ) } ) ) )

dfs, dfs_by_place_item = ({},{})
for s in ts.series:
  if True: # clean the data
    df = pd.read_csv (
      os.path.join ( source,
                     s.name + ".csv" ) )
    df = correct_peso_columns ( s.money_cols, df )
    dfs[s.name] = df

  if True:
    # PITFALL: This seems to assume (as happens to be true,
    # but it would be better to ensure it in this file)
    # that the data is sorted by year.
    df_by_place_item = (
      # add percent change across years within place-item
      df[["year",     "muni code", "dept code", "item categ"]
         + s.money_cols ] .
      groupby ( by = [ "muni code", "dept code", "item categ"],
                group_keys = False ) .
      apply( lambda df:
             lib.add_pct_change( s.money_cols[0], df) ) .
      reset_index() )

    # Test
    for year in list (
        range ( c.first_year + 1, # Skip the first year, because
                                  # median change that year is undefined.
                c.last_year + 1 ) ):
      median_change = (
        ( df_by_place_item
          [df_by_place_item["year"] == year ]
          ["pct change"] ) .
        median() )
      assert median_change < 2
      assert median_change > (-2/3)
        # These bounds might look pretty loose --
        # they say that in each (file,year) pair,
        # the median (across (municipality, budget item) pairs)
        # rose by no more than 300% (i.e. quadrupling), and fell by no more than two-thirds.
        # In fact they can't be made much tighter (and still have every subsample pass).
        # Fortunately, these bounds are far more than tight enough to assure
        # the order of magnitude problem is solved.
    dfs_by_place_item[s.name] = df_by_place_item
  df.to_csv (
    os.path.join ( dest,
                   s.name + ".csv" ),
    index = False )
