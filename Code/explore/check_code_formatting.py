if True:
  import Code.build.classify_budget_codes as cla
  import Code.metadata.four_series as s4
  import Code.metadata.terms as t

for s in s4.series:
  for i in sorted(cla.of_interest[s]):
    print(i)
