---------------

rename  's/xxx/yyy/' "*.py"
find . -type f \( -iname \*.py -o -iname \*.sh -o -iname \*.txt -o -iname \*.org -o -iname \*.md -o -iname \*Makefile\* \) -print0 | xargs -0
  # grep -i "\"pc\""
  # sed -i "s/xxx/yyy/g"

make all vintage=2019 subsample=100 > make.out 2> make.err
make all vintage=2019 subsample=1000
make all vintage=2019 subsample=100
make all vintage=2019 subsample=10
make all vintage=2019 subsample=1
