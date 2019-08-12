### Variables
SHELL := bash

.PHONY: all keys conceptos_1 conceptos_2_agg

all: keys                                                     \
  conceptos_1                                                 \
  conceptos_1_5_subsample                                     \
  conceptos_2_agg

keys =                                                        \
  output/keys/concepto.csv                                    \
  output/keys/geo.csv

conceptos_1 =                                                 \
  output/conceptos_1/funcionamiento.csv                       \
  output/conceptos_1/ingresos.csv                             \
  output/conceptos_1/inversion.csv

conceptos_1_5_subsample =                                     \
  output/conceptos_1_5_subsample/recip-10/funcionamiento.csv  \
  output/conceptos_1_5_subsample/recip-10/ingresos.csv        \
  output/conceptos_1_5_subsample/recip-10/inversion.csv       \
  output/conceptos_1_5_subsample/recip-100/funcionamiento.csv \
  output/conceptos_1_5_subsample/recip-100/ingresos.csv       \
  output/conceptos_1_5_subsample/recip-100/inversion.csv      \
  output/conceptos_1_5_subsample/recip-1000/funcionamiento.csv\
  output/conceptos_1_5_subsample/recip-1000/ingresos.csv      \
  output/conceptos_1_5_subsample/recip-1000/inversion.csv

conceptos_2_agg =                                             \
  output/conceptos_2_agg/funcionamiento.csv                   \
  output/conceptos_2_agg/ingresos.csv                         \
  output/conceptos_2_agg/inversion.csv

myPython=PYTHONPATH='.' python3


#### Recipes

keys: $(keys)
$(keys):                               \
  Code/build/keys.py                    \
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/keys.py

conceptos_1: $(conceptos_1)
$(conceptos_1):                       \
  Code/build/conceptos_1.py             \
  Code/build/aggregation_regexes.py     \
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_1.py

conceptos_1_5_subsample: $(conceptos_1_5_subsample)
$(conceptos_1_5_subsample):          \
  $(conceptos_1)                        \
  Code/build/conceptos_1_5_subsample.py \
  Code/build/aggregation_regexes.py     \
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_1_5_subsample.py

conceptos_2_agg: $(conceptos_2_agg)
$(conceptos_2_agg):                   \
  $(conceptos_1_5_subsample)            \
  Code/build/conceptos_2_agg.py         \
  Code/util.py                          \
  Code/build/aggregation_regexes.py     \
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_2_agg.py
