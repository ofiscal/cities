# In the raw data, specifying (muni,dept,year,budget item)
# is not enough to narrow the choice down to one row.
# This is searching for additional fields that can be used
# to disambiguate the rows.

import Code.explore.duplicate_rows_defs as d

######
###### INGRESOS
######
# The ingresos does not need extra grouping columns,
# as demonstrated by the fact that the max value in this report is 1.
series = "ingresos"
df = d.fetch_series(series)
d.report(df,[])

######
###### FUNCIONAMIENTO
######
series = "funcionamiento"
df = d.fetch_series(series)
d.report(df,[]) # funcionamiento, however, needs more grouping columns
( # in fact, it needs more than one --
  # no matter which single extra grouping column we add,
  # the maximum number of rows in a group is still at least 7.
  # In fact the 99th percentile is at least 2; in 196449 rows, that's too many.
  d.report_1_extra_groupvar(
    df,
    d.non_group_fields[series] )
  [["i","max"] + d.percentiles_str] .
  sort_values(d.percentiles_str + ["max"] ) )
x = ( # But if we use "Código Unidad Ejecutora" *and* "Código Fuente Financiación",
  # the max group size is 1.
  d.report_2_extra_groupvars(
    df,
    d.non_group_fields[series] )
  [["i1","i2","max"] + d.percentiles_str] .
  sort_values(["max", "99%"]) ).transpose()
x.iloc[:,0] # This, the first column, is our solution.

######
###### INVERSION
######
# Tthe "inversion" data only has two extra columns that could plausibly
# be used to disambiguate rows.
series = "inversion"
df = d.fetch_series(series)
d.report(df,[])
( d.report_1_extra_groupvar(
    df,
    d.non_group_fields["inversion"] )
  [["i","max"] + d.percentiles_str] .
  sort_values(["max", "99%"]) .
  transpose() )
( d.report_2_extra_groupvars(
    df,
    d.non_group_fields["inversion"] )
  [["i1","i2","max"] + d.percentiles_str] .
  sort_values(["max", "99%"]) )

# One of those potential additional indices, "Código Fuentes De Financiación",
# is good for at least 99.999% disambiguation.
# Let's see what the remaining rows look like.
das = (
  df .
  groupby( d.group_fields +
           ["Código Fuentes De Financiación"] ) .
  agg( sum ) )
das[ das["one"] > 1 ].transpose()

# Great! There's only one weird municipality, number 25430 (Madrid, Cundinamarca)
# which reported 26 distinct rows with the same item code, "VAL" --
# a code which we don't use.
# So "Fuentes" is enough to completely disambiguate the rest.
