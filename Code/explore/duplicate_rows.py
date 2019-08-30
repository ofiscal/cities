import Code.explore.duplicate_rows_defs as d

# The ingresos does not need extra grouping columns,
# as demonstrated by the fact that the max value in this report is 1.
series = "ingresos"
df = d.data_2012(series)
d.report(df,[])

series = "funcionamiento"
df = d.data_2012(series)
d.report(df,[]) # funcionamiento, however, needs more grouping columns
( # in fact, it needs more than one --
  # no matter which single extra grouping column we add,
  # the maximum number of rows in a group is still at least 7.
  d.report_1_extra_groupvar(
    df,
    d.non_group_fields[series] )
  [["i","99%","max"]] .
  sort_values(["max", "99%"]) )
( # But if we use "Código Unidad Ejecutora" *and* "Código Fuente Financiación",
  # the max group size is 1.
  d.report_2_extra_groupvars(
    df,
    d.non_group_fields[series] )
  [["i1","i2","99%","max"]] .
  sort_values(["max", "99%"]) )

# But the "inversion" data is very weird --
# it only has two extra columns that could plausibly be used to disambiguate rows,
# and no matter which or how many of them we use, the data remains ambiguous.
series = "inversion"
df = d.data_2012(series)
d.report(df,[])
( d.report_1_extra_groupvar(
    df,
    d.non_group_fields["inversion"] )
  [["i","99%","max"]] .
  sort_values(["max", "99%"]) )
( d.report_2_extra_groupvars(
    df,
    d.non_group_fields["inversion"] )
  [["i1","i2","99%","max"]] .
  sort_values(["max", "99%"]) )
