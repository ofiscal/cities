#### #### #### ####
#### #### #### #### Variables
#### #### #### ####

SHELL := bash

subsample?=100
  # default value; can be overridden from the command line,
  # as in "make all subsample=10"
  # possibilities: 1, 10, 100 and 1000
ss=$(strip $(subsample))
  # removes trailing space
myPython=PYTHONPATH='.' python3

.PHONY: all			\
  keys				\
  budget_1			\
  budget_1p5 			\
  budget_2_subsample		\
  budget_2_subsamples		\
  subsample			\
  budget_3_dept_muni_year_item	\
  budget_4_scaled		\
  budget_5_add_regalias		\
  budget_6_deflate		\
  budget_7_verbose		\
  budget_8_pivots		\
  sample_tables 		\
  pics

all: keys			\
  budget_1			\
  budget_1p5			\
  budget_2_subsample		\
  budget_2_subsamples		\
  budget_3_dept_muni_year_item	\
  budget_4_scaled		\
  budget_5_add_regalias		\
  budget_6_deflate		\
  budget_7_verbose		\
  budget_8_pivots		\
  output/inflation.csv		\
  sample_tables 		\
  output/regalias.csv           \
  pics

keys =				\
  output/keys/budget.csv	\
  output/keys/geo.csv

budget_1 =				\
  output/budget_1/funcionamiento.csv	\
  output/budget_1/ingresos.csv		\
  output/budget_1/inversion.csv		\
  output/budget_1/deuda.csv

budget_1p5 =							\
  output/budget_1p5/ingresos.csv				\
  output/budget_1p5/gastos.csv

budget_2_subsample =						\
  output/budget_2_subsample/recip-$(ss)/ingresos.csv		\
  output/budget_2_subsample/recip-$(ss)/gastos.csv

budget_2_subsamples =						\
  output/budget_2_subsample/recip-10/ingresos.csv		\
  output/budget_2_subsample/recip-10/gastos.csv			\
  output/budget_2_subsample/recip-100/ingresos.csv		\
  output/budget_2_subsample/recip-100/gastos.csv		\
  output/budget_2_subsample/recip-1000/ingresos.csv		\
  output/budget_2_subsample/recip-1000/gastos.csv

budget_3_dept_muni_year_item =					\
  output/budget_3_dept_muni_year_item/recip-$(ss)/ingresos.csv	\
  output/budget_3_dept_muni_year_item/recip-$(ss)/gastos.csv

#sanity_child_sum_is_parent =							\
#  output/sanity_child_sum_is_parent/recip-$(ss)/funcionamiento.csv		\
#  output/sanity_child_sum_is_parent/recip-$(ss)/ingresos.csv			\
#  output/sanity_child_sum_is_parent/recip-$(ss)/inversion.csv			\
#  output/sanity_child_sum_is_parent_summary/recip-$(ss)/funcionamiento.csv	\
#  output/sanity_child_sum_is_parent_summary/recip-$(ss)/ingresos.csv		\
#  output/sanity_child_sum_is_parent_summary/recip-$(ss)/inversion.csv

explore_order_of_mag_x_yrs =					\
  output/explore/order_of_mag_x_yrs/recip-$(ss)/report.csv

budget_4_scaled =						\
  output/budget_4_scaled/recip-$(ss)/ingresos.csv		\
  output/budget_4_scaled/recip-$(ss)/gastos.csv

budget_5_add_regalias =					\
  output/budget_5_add_regalias/recip-$(ss)/ingresos.csv	\
  output/budget_5_add_regalias/recip-$(ss)/gastos.csv

budget_6_deflate =					\
  output/budget_6_deflate/recip-$(ss)/ingresos.csv	\
  output/budget_6_deflate/recip-$(ss)/gastos.csv

budget_7_verbose =					\
  output/budget_7_verbose/recip-$(ss)/ingresos.csv	\
  output/budget_7_verbose/recip-$(ss)/gastos.csv

# Listing one place (Honda, in Tolima)
# is sufficient to trigger the recipe.
# Listing every place would be tedious.
budget_8_pivots =					\
  output/pivots/recip-$(ss)/TOLIMA/HONDA/ingresos.csv	\
  output/pivots/recip-$(ss)/TOLIMA/HONDA/gastos.csv

sample_tables =					\
  output/sample_tables/recip-$(ss)/ingresos.csv	\
  output/sample_tables/recip-$(ss)/gastos.csv

pics = output/reports/done.txt


#### #### #### ####
#### #### #### #### Recipes
#### #### #### ####

keys: $(keys)
$(keys):			\
  Code/build/make_keys.py	\
  Code/metadata/raw_series.py
	$(myPython) Code/build/make_keys.py

# PITFALL: Don't include Code/metadata/terms.py;
# it's safe to omit and causes unnecessary re-running,
# not affordable at these early slow stages.
budget_1: $(budget_1)
$(budget_1):					\
  Code/build/budget_1.py			\
  Code/build/budget_1_defs.py			\
  Code/build/budget_1_tests.py			\
  Code/metadata/raw_series.py
	$(myPython) Code/build/budget_1.py

# PITFALL: Don't include Code/metadata/terms.py;
# it's safe to omit and causes unnecessary re-running,
# not affordable at these early slow stages.
budget_1p5: $(budget_1p5)
$(budget_1p5):					\
  $(budget_1)					\
  Code/build/budget_1p5.py			\
  Code/build/budget_1p5_tests.py		\
  Code/build/classify_budget_codes.py		\
  Code/metadata/terms.py                        \
  Code/metadata/raw_series.py
	$(myPython) Code/build/budget_1p5.py

# PITFALL: Don't include Code/metadata/terms.py;
# it's safe to omit and causes unnecessary re-running,
# not affordable at these early slow stages.
budget_2_subsamples: $(budget_2_subsamples)
$(budget_2_subsamples):				\
  $(budget_1p5)					\
  Code/build/budget_2_subsample.py		\
  Code/build/budget_2_subsample_defs.py		\
  Code/build/budget_1_tests.py			\
  Code/metadata/raw_series.py
	$(myPython) Code/build/budget_2_subsample.py

# PITFALL: Don't include Code/metadata/terms.py;
# it's safe to omit and causes unnecessary re-running,
# not affordable at these early slow stages.
budget_3_dept_muni_year_item: $(budget_3_dept_muni_year_item)
$(budget_3_dept_muni_year_item):		\
  $(budget_2_subsample)				\
  Code/build/budget_3_dept_muni_year_item.py	\
  Code/common.py				\
  Code/util/misc.py				\
  Code/metadata/two_series.py
	$(myPython) Code/build/budget_3_dept_muni_year_item.py $(ss)

# TODO ? resurrect. This broke when we switched item code specs.
# In the new method we never create top, child and categ columns;
# instead we just keep rows with item codes equal to one of the top categories.
#sanity_child_sum_is_parent: $(sanity_child_sum_is_parent)
#$(sanity_child_sum_is_parent):			\
#  $(budget_3_dept_muni_year_item)		\
#  Code/build/sanity_child_sum_is_parent.py	\
#  Code/common.py				\
#  Code/util/misc.py				\
#  Code/metadata/raw_series.py
#	$(myPython) Code/build/sanity_child_sum_is_parent.py $(ss)

explore_order_of_mag_x_yrs: $(explore_order_of_mag_x_yrs)
$(explore_order_of_mag_x_yrs):			\
  $(budget_3_dept_muni_year_item)		\
  Code/explore/order_of_mag_x_yrs.py		\
  Code/common.py				\
  Code/util/misc.py				\
  Code/metadata/terms.py                        \
  Code/metadata/raw_series.py
	$(myPython) Code/explore/order_of_mag_x_yrs.py $(ss)

budget_4_scaled: $(budget_4_scaled)
$(budget_4_scaled):				\
  $(budget_3_dept_muni_year_item)		\
  Code/build/budget_4_scaled.py			\
  Code/explore/order_of_mag_x_yrs_defs.py	\
  Code/common.py				\
  Code/util/misc.py				\
  Code/metadata/terms.py                        \
  Code/metadata/raw_series.py
	$(myPython) Code/build/budget_4_scaled.py $(ss)

budget_5_add_regalias: $(budget_5_add_regalias)
$(budget_5_add_regalias):		\
  $(budget_4_scaled)			\
  output/regalias.csv			\
  Code/build/budget_5_add_regalias.py	\
  Code/common.py			\
  Code/metadata/terms.py                \
  Code/metadata/two_series.py
	$(myPython) Code/build/budget_5_add_regalias.py $(ss)

budget_6_deflate: $(budget_6_deflate)
$(budget_6_deflate):			\
  $(budget_5_add_regalias)		\
  output/inflation.csv			\
  Code/build/budget_6_deflate.py	\
  Code/common.py			\
  Code/metadata/terms.py                \
  Code/metadata/two_series.py
	$(myPython) Code/build/budget_6_deflate.py $(ss)

budget_7_verbose: $(budget_7_verbose)
$(budget_7_verbose):			\
  $(budget_6_deflate)			\
  Code/build/budget_7_verbose.py	\
  Code/build/use_keys.py		\
  Code/common.py			\
  Code/util/misc.py			\
  Code/metadata/terms.py                \
  Code/metadata/two_series.py
	$(myPython) Code/build/budget_7_verbose.py $(ss)

budget_8_pivots: $(budget_8_pivots)
$(budget_8_pivots):				\
  $(budget_7_verbose)				\
  Code/build/budget_8_pivots.py			\
  Code/common.py				\
  Code/util/aggregate_all_but_biggest.py	\
  Code/metadata/two_series.py
	$(myPython) Code/build/budget_8_pivots.py $(ss)

sample_tables: $(sample_tables)
$(sample_tables):				\
  $(budget_7_verbose)				\
  Code/common.py				\
  Code/draw/sample_tables.py			\
  Code/util/aggregate_all_but_biggest.py	\
  Code/metadata/terms.py			\
  Code/metadata/two_series.py
	$(myPython) Code/draw/sample_tables.py $(ss)

output/inflation.csv:				\
  data/inflation.csv				\
  Code/build/inflation.py
	$(myPython) Code/build/inflation.py

output/regalias.csv:			\
  data/regalias/muni.csv		\
  data/regalias/dept.csv		\
  Code/build/regalias.py		\
  Code/build/use_keys.py
	$(myPython) Code/build/regalias.py

pics: $(pics)
$(pics):			\
  $(budget_4_scaled)		\
  Code/build/use_keys.py	\
  Code/main.py
	date
	$(myPython) Code/main.py $(ss)
	date
