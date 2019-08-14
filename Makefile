### Variables
SHELL := bash

subsample?=100
  # default value; can be overridden from the command line,
  # as in "make raw subsample=10"
  # possibilities: 1, 10, 100 and 1000
ss=$(strip $(subsample))
  # removes trailing space
myPython=PYTHONPATH='.' python3

.PHONY: all							\
  keys								\
  conceptos_1							\
  conceptos_2_subsample						\
  conceptos_2_subsamples					\
  subsample conceptos_3_agg

all: keys							\
  conceptos_1							\
  conceptos_2_subsample						\
  conceptos_2_subsamples					\
  conceptos_3_agg

keys =								\
  output/keys/concepto.csv					\
  output/keys/geo.csv

conceptos_1 =							\
  output/conceptos_1/funcionamiento.csv				\
  output/conceptos_1/ingresos.csv				\
  output/conceptos_1/inversion.csv

conceptos_2_subsample =						\
  output/conceptos_2_subsample/recip-$(ss)/funcionamiento.csv	\
  output/conceptos_2_subsample/recip-$(ss)/ingresos.csv		\
  output/conceptos_2_subsample/recip-$(ss)/inversion.csv

conceptos_2_subsamples =					\
  output/conceptos_2_subsample/recip-10/funcionamiento.csv	\
  output/conceptos_2_subsample/recip-10/ingresos.csv		\
  output/conceptos_2_subsample/recip-10/inversion.csv		\
  output/conceptos_2_subsample/recip-100/funcionamiento.csv	\
  output/conceptos_2_subsample/recip-100/ingresos.csv		\
  output/conceptos_2_subsample/recip-100/inversion.csv		\
  output/conceptos_2_subsample/recip-1000/funcionamiento.csv	\
  output/conceptos_2_subsample/recip-1000/ingresos.csv		\
  output/conceptos_2_subsample/recip-1000/inversion.csv

conceptos_3_agg =						\
  output/conceptos_3_agg/recip-$(ss)/funcionamiento.csv		\
  output/conceptos_3_agg/recip-$(ss)/ingresos.csv		\
  output/conceptos_3_agg/recip-$(ss)/inversion.csv


#### Recipes

keys: $(keys)
$(keys):							\
  Code/build/keys.py						\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/keys.py

conceptos_1: $(conceptos_1)
$(conceptos_1):							\
  Code/build/conceptos_1.py					\
  Code/build/conceptos_1_defs.py				\
  Code/build/conceptos_1_tests.py				\
  Code/build/aggregation_regexes.py				\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_1.py

conceptos_2_subsamples: $(conceptos_2_subsamples)
$(conceptos_2_subsamples):					\
  $(conceptos_1)						\
  Code/build/conceptos_2_subsample.py				\
  Code/build/aggregation_regexes.py				\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_2_subsample.py

conceptos_3_agg: $(conceptos_3_agg)
$(conceptos_3_agg):						\
  $(conceptos_2_subsample)					\
  Code/build/conceptos_3_agg.py					\
  Code/util.py							\
  Code/build/aggregation_regexes.py				\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_3_agg.py $(ss)
