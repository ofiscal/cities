These are functions for generating pivot tables for each municipality,
with columns corresponding to years,
rows corresponding to budget items,
and cells giving peso or percentage figures.

First the program used the functions in `gappy.py`.
The result was pivot tables in which the top five spendinng items for each year were made explicit,
and the others were lumped into a column called "otros".
Therefore if a municipality spent on item I in years X and Y,
and I was in the top five in year X but not Y,
the table would not show the amount for I in year Y at all.
A reader might think the municipality had spent nothing on it that year.

We decided that was confusing.

`better.py` results in pivot tables where, as before, the set of rows is the set of items that are top five for some year, plus "otros". However, it includes no missing values -- so continuing the preceding example, even though I was not top 5 in year Y, since it was in year X, it will be shown for both years X and Y.


