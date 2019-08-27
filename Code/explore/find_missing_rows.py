import os

source = "data/sisfut/original_csv"
sink = "data/sisfut/bughunt"

for filename in os.listdir(source):
  with open(source + "/" + filename) as f:
      lines = f.readlines()
  with open(sink + "/" + filename, "w") as f:
    f.write(
      "manual index," + lines[0] )
    for i in range(1,len(lines)):
      f.write(
        str(i) + "," + lines[i] )

