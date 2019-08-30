### Variables
SHELL := bash

subsample?=100
  # default value; can be overridden from the command line,
  # as in "make all subsample=10"
  # possibilities: 1, 10, 100 and 1000
ss=$(strip $(subsample))
  # removes trailing space
myPython=PYTHONPATH='.' python3

.PHONY: all									\
  keys										\
  budget_1									\
  budget_1p5 									\
  budget_2_subsample								\
  budget_2_subsamples								\
  subsample									\
  budget_3_muni_year_item							\
  budget_4_scaled								\
  pics

all: keys									\
  budget_1									\
  budget_1p5									\
  budget_2_subsample								\
  budget_2_subsamples								\
  budget_3_muni_year_item							\
  budget_4_scaled								\
  output/inflation.csv								\
  output/regalias.csv								\
  pics

keys =										\
  output/keys/budget.csv							\
  output/keys/geo.csv

budget_1 =									\
  output/budget_1/funcionamiento.csv						\
  output/budget_1/ingresos.csv							\
  output/budget_1/inversion.csv

budget_1p5 =									\
  output/budget_1p5/funcionamiento.csv						\
  output/budget_1p5/ingresos.csv						\
  output/budget_1p5/inversion.csv

budget_2_subsample =								\
  output/budget_2_subsample/recip-$(ss)/funcionamiento.csv			\
  output/budget_2_subsample/recip-$(ss)/ingresos.csv				\
  output/budget_2_subsample/recip-$(ss)/inversion.csv

budget_2_subsamples =								\
  output/budget_2_subsample/recip-10/funcionamiento.csv				\
  output/budget_2_subsample/recip-10/ingresos.csv				\
  output/budget_2_subsample/recip-10/inversion.csv				\
  output/budget_2_subsample/recip-100/funcionamiento.csv			\
  output/budget_2_subsample/recip-100/ingresos.csv				\
  output/budget_2_subsample/recip-100/inversion.csv				\
  output/budget_2_subsample/recip-1000/funcionamiento.csv			\
  output/budget_2_subsample/recip-1000/ingresos.csv				\
  output/budget_2_subsample/recip-1000/inversion.csv

budget_3_muni_year_item =							\
  output/budget_3_muni_year_item/recip-$(ss)/funcionamiento.csv			\
  output/budget_3_muni_year_item/recip-$(ss)/ingresos.csv			\
  output/budget_3_muni_year_item/recip-$(ss)/inversion.csv

#sanity_child_sum_is_parent =							\
#  output/sanity_child_sum_is_parent/recip-$(ss)/funcionamiento.csv		\
#  output/sanity_child_sum_is_parent/recip-$(ss)/ingresos.csv			\
#  output/sanity_child_sum_is_parent/recip-$(ss)/inversion.csv			\
#  output/sanity_child_sum_is_parent_summary/recip-$(ss)/funcionamiento.csv	\
#  output/sanity_child_sum_is_parent_summary/recip-$(ss)/ingresos.csv		\
#  output/sanity_child_sum_is_parent_summary/recip-$(ss)/inversion.csv

explore_order_of_mag_x_yrs =							\
  output/explore/order_of_mag_x_yrs/recip-$(ss)/report.csv

budget_4_scaled =								\
  output/budget_4_scaled/recip-$(ss)/funcionamiento.csv				\
  output/budget_4_scaled/recip-$(ss)/ingresos.csv				\
  output/budget_4_scaled/recip-$(ss)/inversion.csv

pics = output/reports/done.txt


#### Recipes

keys: $(keys)
$(keys):					\
  Code/build/keys.py				\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/keys.py

budget_1: $(budget_1)
$(budget_1):					\
  Code/build/budget_1.py			\
  Code/build/budget_1_defs.py			\
  Code/build/budget_1_tests.py			\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/budget_1.py

budget_1p5: $(budget_1p5)
$(budget_1p5):					\
  $(budget_1)					\
  Code/build/budget_1p5.py			\
  Code/build/budget_1p5_defs.py			\
  Code/build/budget_1p5_tests.py		\
  Code/build/aggregation_regexes.py		\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/budget_1p5.py

budget_2_subsamples: $(budget_2_subsamples)
$(budget_2_subsamples):				\
  $(budget_1p5)					\
  Code/build/budget_2_subsample.py		\
  Code/build/budget_2_subsample_defs.py		\
  Code/build/budget_1_tests.py			\
  Code/build/aggregation_regexes.py		\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/budget_2_subsample.py

budget_3_muni_year_item: $(budget_3_muni_year_item)
$(budget_3_muni_year_item):			\
  $(budget_2_subsample)				\
  Code/build/budget_3_muni_year_item.py		\
  Code/build/budget_3_muni_year_item_defs.py	\
  Code/common.py				\
  Code/params/cl.py				\
  Code/params/fixed.py				\
  Code/util.py					\
  Code/build/aggregation_regexes.py		\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/budget_3_muni_year_item.py $(ss)

# TODO ? resurrect. This broke when we switched item code specs.
# In the new method we never create top, child and categ columns;
# instead we just keep rows with item codes equal to one of the top categories.
#sanity_child_sum_is_parent: $(sanity_child_sum_is_parent)
#$(sanity_child_sum_is_parent):			\
#  $(budget_3_muni_year_item)			\
#  Code/build/sanity_child_sum_is_parent.py	\
#  Code/common.py				\
#  Code/util.py					\
#  Code/build/sisfut_metadata.py
#	$(myPython) Code/build/sanity_child_sum_is_parent.py $(ss)

explore_order_of_mag_x_yrs: $(explore_order_of_mag_x_yrs)
$(explore_order_of_mag_x_yrs):			\
  $(budget_3_muni_year_item)			\
  Code/explore/order_of_mag_x_yrs.py		\
  Code/common.py				\
  Code/util.py					\
  Code/build/sisfut_metadata.py
	$(myPython) Code/explore/order_of_mag_x_yrs.py $(ss)

budget_4_scaled: $(budget_4_scaled)
$(budget_4_scaled):				\
  $(budget_3_muni_year_item)			\
  Code/build/budget_4_scaled.py			\
  Code/explore/order_of_mag_x_yrs_defs.py	\
  Code/common.py				\
  Code/util.py					\
  Code/build/sisfut_metadata.py
	$(myPython) Code/build/budget_4_scaled.py $(ss)

budget_5_deflate_and_regalias: $(budget_5_deflate_and_regalias)
$(budget_5_deflate_and_regalias):		\
  $(budget_4_scaled)				\
  output/regalias.csv				\
  output/inflation.csv				\
  Code/build/budget_5_deflate_and_regalias.py	\
  Code/common.py				\
  Code/series_metadata.py
	$(myPython) Code/build/budget_5_deflate_and_regalias.py $(ss)

output/inflation.csv:				\
  data/inflation.csv				\
  Code/build/inflation.py
	$(myPython) Code/build/inflation.py

output/regalias.csv:				\
  data/regalias.csv				\
  Code/build/regalias.py
	$(myPython) Code/build/regalias.py

pics: $(pics)
$(pics):					\
  $(budget_4_scaled)				\
  Code/main.py
	date
	$(myPython) Code/main.py $(ss)
	date
