The DNP data is pretty good. Everything that's supposed to be a number is a number, and the column names are consistent across spreadsheets. I am pleased. In this email, though, I'm going to focus on the bad news. (It might bad no problem at all, but I'll need your judgement to determine that.)

The data you asked me to select has a lot of columns that looked roughly isomorphic. For instance, "Código FUT" and "Nombre Entidad" seemed to contain the same information -- if you knew the code, it looked like you could determine the name, and vice versa.

I spent some time checking that intuition, and found the following. Four pairs of columns are indeed isomorphic:

Código FUT <-> Nombre Entidad
  Every Codigo is found paired with
  one and only one Nombre, and vice-versa.
Cód. DANE Departamento <-> Nombre DANE Departamento
  Also isomorphic (good).
Código Fuente Financiación <-> Fuente Financiación
  Also isomorphic (good).
Código Fuentes De Financiación <-> Fuentes de Financiación
  Also isomorphic (good).

However, the two remaining pairs are not as well-behaved.

Cód. DANE Municipio <-> Nombre DANE Municipio
  Good: no codigos maps to multiple nombres.
  Bad: Some nombres map to multiple codigos.

The attached spreadsheet entitled "Nombre DANE Municipio.csv" captures exactly which names map to more than one code. It starts like this:

Cód. DANE Municipio | Nombre DANE Municipio | count
5055.0              | ARGELIA               | 3
19050.0             | ARGELIA               | 3
76054.0             | ARGELIA               | 3
5059.0              | ARMENIA               | 2
63001.0             | ARMENIA               | 2

Given that that's true, which should we key on -- the code or the name? Are the codes more precise, indicating sub-regions that are called the same thing?

Código Concepto <-> Concepto
  This pair is not injective in either direction.
  That is, many concepts map to more than one code,
  and exactly one code ("VAL") maps to three different concepts.

The spreadsheet called "Código Concepto" enumerates "all" the codes (there's only one) that map to multiple concepts. That code is written "VAL", and it maps to three separate concepts. It is an unusual code -- most of the codes contain a lot of periods, for example, "TI.B.7.1". My guess is that "VAL" is some kind of error code, but I wonder if you could confirm that?

The reverse multiplicity is worse. Some Concepts are associated with many separate codes. The worst offender is the "DE FUNCIONARIOS" concept, which is associated with fifteen separate codes:

1.1.1.7.1
1.1.4.1.1.1.1
1.1.4.1.1.2.1
1.1.4.1.1.3.1
1.1.4.1.1.4.1
1.1.4.2.1.1.1
1.1.4.2.1.2.1
1.1.4.2.1.3.1
1.1.4.2.1.4.1
1.1.4.3.1.1
1.1.4.3.2.1
1.1.4.3.3.1
1.1.4.3.4.1
1.1.4.3.5.1
1.2.2.8.1

Note that most of those start with 1.1.4, but not all, and in fact one of them doesn't even start with 1.2.
