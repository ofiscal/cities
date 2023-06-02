if True:
  import Code.build.classify_budget_codes as cla
  import Code.metadata.raw_series as s4
  import Code.metadata.terms as t


for s in s4.series:
  for i in sorted(cla.of_interest[s]):
    print(i)

with open("test.txt", "w") as myfile:
  for s in s4.series:
    myfile.write( "\nFile: " + str.upper(s) + "\n")
    d = cla.categs_to_codes[s]
    for k in d.keys():
      myfile.write("\t" + k + "\n")
      for s in sorted(d[k]):
        myfile.write("\t\t" + s + "\n")
