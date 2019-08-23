### Variables
SHELL := bash

subsample?=100
  # default value; can be overridden from the command line,
  # as in "make raw subsample=10"
  # possibilities: 1, 10, 100 and 1000
ss=$(strip $(subsample))
  # removes trailing space
myPython=PYTHONPATH='.' python3

.PHONY: all				\
  keys					\
  conceptos_1				\
  conceptos_2_subsample			\
  conceptos_2_subsamples		\
  subsample				\
  conceptos_3_muni_year_categ_top	\
  sanity_order_of_mag_x_yrs		\
  sanity_child_sum_is_parent		\
  pics

all: keys				\
  conceptos_1				\
  conceptos_2_subsample			\
  conceptos_2_subsamples		\
  conceptos_3_muni_year_categ_top	\
  sanity_child_sum_is_parent		\
  sanity_order_of_mag_x_yrs
  # pics

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

conceptos_3_muni_year_categ_top =					\
  output/conceptos_3_muni_year_categ_top/recip-$(ss)/funcionamiento.csv	\
  output/conceptos_3_muni_year_categ_top/recip-$(ss)/ingresos.csv	\
  output/conceptos_3_muni_year_categ_top/recip-$(ss)/inversion.csv

sanity_child_sum_is_parent =							\
  output/sanity_child_sum_is_parent/recip-$(ss)/funcionamiento.csv		\
  output/sanity_child_sum_is_parent/recip-$(ss)/ingresos.csv			\
  output/sanity_child_sum_is_parent/recip-$(ss)/inversion.csv			\
  output/sanity_child_sum_is_parent_summary/recip-$(ss)/funcionamiento.csv	\
  output/sanity_child_sum_is_parent_summary/recip-$(ss)/ingresos.csv		\
  output/sanity_child_sum_is_parent_summary/recip-$(ss)/inversion.csv

sanity_order_of_mag_x_yrs =	\
  output/sanity_order_of_mag_x_yrs/recip-$(ss)/report.csv

pics = output/a_page.pdf


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
  Code/build/conceptos_2_subsample_defs.py			\
  Code/build/conceptos_1_tests.py				\
  Code/build/aggregation_regexes.py				\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_2_subsample.py

conceptos_3_muni_year_categ_top: $(conceptos_3_muni_year_categ_top)
$(conceptos_3_muni_year_categ_top):			\
  $(conceptos_2_subsample)				\
  Code/build/conceptos_3_muni_year_categ_top.py		\
  Code/build/conceptos_3_muni_year_categ_top_defs.py	\
  Code/common.py					\
  Code/params/cl.py					\
  Code/params/fixed.py					\
  Code/util.py						\
  Code/build/aggregation_regexes.py			\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/conceptos_3_muni_year_categ_top.py $(ss)

sanity_child_sum_is_parent: $(sanity_child_sum_is_parent)
$(sanity_child_sum_is_parent):			\
  $(conceptos_3_muni_year_categ_top)		\
  Code/build/sanity_child_sum_is_parent.py	\
  Code/common.py				\
  Code/util.py					\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/sanity_child_sum_is_parent.py $(ss)

sanity_order_of_mag_x_yrs: $(sanity_order_of_mag_x_yrs)
$(sanity_order_of_mag_x_yrs):			\
  $(conceptos_3_muni_year_categ_top)		\
  Code/explore/order_of_mag_x_yrs.py	\
  Code/common.py				\
  Code/util.py					\
  Code/build/sisfut_metadata.py
	$(myPython) Code/explore/order_of_mag_x_yrs.py $(ss)

pics: $(pics)
$(pics): Code/main.py
	date
	$(myPython) Code/main.py $(ss)
	date

