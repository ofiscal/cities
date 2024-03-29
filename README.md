# How to run this

## To build the whole project

From the project root, run
```
make vintage=2023 subsample=1000
```
`vintage` can be in [2019, 2023].
`subsample` can be in [1,10,100,1000]. It is actually the reciprocal of the subsample size -- so 1 gives you the full sample and takes the longest.

If you run `make` without specifying those arguments,
default values will be used,
as found in `./Makefile`.


## To build something else

Do similarly to the above, except specify the target:
```
make <target> vintage=2023 subsample=1000
```

For possible values that `<target>` could take in the above,
see the definition of `.PHONY` in `./Makefile`.


# What this does

## The original vision, which is pretty well documented

This project generates, for each of the 1100 Colombian municipalities,
a .pdf document describing
how its revenue and spending evolved in recent years,
and how they compare to the department average.

## Some other parts are less well documented.

We later decided to send audio clips to radio stations,
and publish Facebook ads describing our work.
The three treatments were assigned randomly to different municipalities.

# Where to find the output

208 of the resulting reports can be found [here](https://github.com/ofiscal/cities-output).
The reason there are only 208 there is that the project was an experiment --
we intentionally treated a subsample of Colombia's population,
to determine the treatment's effects on voter behavior --
and so we could not make the rest public.
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
(Anaconda is not strictly necessary,
but some of the things it provides are -- scipy, for instance.)
