# What this does

This project generates, for each of the 1100 Colombian municipalities,
a .pdf document describing how its revenue and spending have evolved in recent years,
and how they compare to the department average.

# Where to find the output

208 of the resulting reports can be found [here](https://github.com/ofiscal/cities-output).
The reason there are only 208 there is that the project was an experiment --
we intentionally treated a subsample of Colombia's population,
to determine the treatment's effects on voter behavior.
(There were two other treatments as well --
one in which the reports were made available to the local media,
and one in which they were provided to the staff of political candidates.)

# Dependencies

## Data dependencies

These reports are built from [data provided by SISFUT](https://sisfut.dnp.gov.co/app/reportes/categoria).
Smaller data sets (e.g. the inflation series) are included in this repository.

## Software dependencies

There is [a handy Docker container](https://hub.docker.com/r/ofiscal/tax.co)
that can be used to run the code.

The set of programs this repository depends on has not been documented.
Whatever they are, the Docker container provides them.
At the least it includes Python 3, Anaconda and LaTeX.
