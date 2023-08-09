The .csv files found here describe the correspondence between
"conceptos" (what I translated to "items")
and "códigos conceptos" (translated as "item codes")
in the SISFUT and CUIPO data.

PITFALL: In some cases,
the data translates a code into words in more than one way.
I don't know whether that's true of any of the codes we are interested in,
though.

For the SISFUT data,
these files include only the codes we are interested in,
and indicate how we aggregate those raw codes into the high-level categories
on which we want to report --
e.g. "building hospitals" (too much detail) is part of "salud" (just right),
"paying teachers" (too much detail) is part of "education" (just right),
etc.
PITFALL: Confusingly, the SISFUT concepto keys are built by
a file with a lot of "cuipo" in its path:
`Code/explore/cuipo/cuipo_4_concept_keys.py`

For the CUIPO data, we want to build the same aggregate categories,
and the purpose of these files is to allow us to construct them.
Therefore the CUIPO files found here include *all* income and spending codes,
whether we are interested in them or not.
