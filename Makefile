#### #### #### ####
#### #### #### #### USAGE
#### #### #### ####
#
# See README.md.

#### #### #### ####
#### #### #### #### Variables
#### #### #### ####

SHELL := bash

# PITFALL: Trailing space after definitions such as these will break them,
# and is easy to introduce accidentally by appending a comment to the line.
# PITFALL: Not every program uses all or even any of these variables,
# but anything that imports `Code.common` needs them to be defined.
vintage=2019
  # Default value.
  # Possibilities: 2019, 2023.
subsample?=100
  # Default value.
  # Possibilities: 1, 10, 100 and 1000
  # Can be overridden from the command line,
  # as in "make all subsample=10".

myPython=PYTHONPATH='.' python3
myArgs=--subsample=$(subsample) --vintage=$(vintage)

.PHONY: all                      \
  budget_0_collect               \
  budget_1                       \
  budget_1p5                     \
  budget_2_subsample             \
  budget_3_dept_muni_year_item   \
  budget_4_scaled                \
  budget_5_add_regalias          \
  budget_6_deflate               \
  budget_6p5_cull_and_percentify \
  budget_6p7_avg_muni            \
  budget_7_verbose               \
  budget_8_pivots                \
  budget_9_static_compare        \
  facebook_ads                   \
  inflation                      \
  keys                           \
  radio                          \
  regalias                       \
  reports                        \
  sample_tables                  \
  show_params                    \
  subsample

# `show_params` should be listed first,
# so that it always runs. (It depends on nothing.)
all:                             \
  budget_0_collect		 \
  budget_1			 \
  budget_1p5			 \
  budget_2_subsample		 \
  budget_3_dept_muni_year_item	 \
  budget_4_scaled		 \
  budget_5_add_regalias		 \
  budget_6_deflate		 \
  budget_6p5_cull_and_percentify \
  budget_6p7_avg_muni		 \
  budget_7_verbose		 \
  budget_8_pivots		 \
  budget_9_static_compare	 \
  facebook_ads			 \
  keys                           \
  inflation                      \
  regalias                       \
  radio                          \
  reports			 \
  show_params
  # sample_tables # Unneeded, except to understand more complex programs.

inflation = output/$(vintage)/inflation.csv
regalias =  output/$(vintage)/regalias.csv

keys =                                                  \
  output/$(vintage)/keys/budget.csv                     \
  output/$(vintage)/keys/geo.csv

budget_0_collect =                                      \
  output/$(vintage)/budget_0_collect/funcionamiento.csv	\
  output/$(vintage)/budget_0_collect/ingresos.csv	\
  output/$(vintage)/budget_0_collect/inversion.csv
ifeq ($(vintage),2019)
  budget_0_collect += \
    output/$(vintage)/budget_0_collect/deuda.csv
endif

budget_1 =                                              \
  output/$(vintage)/budget_1/funcionamiento.csv         \
  output/$(vintage)/budget_1/ingresos.csv		\
  output/$(vintage)/budget_1/inversion.csv
ifeq ($(vintage),2019)
  budget_1 += \
    output/$(vintage)/budget_1/deuda.csv
endif

budget_1p5 =                                            \
  output/$(vintage)/budget_1p5/ingresos.csv             \
  output/$(vintage)/budget_1p5/gastos.csv

budget_2_subsample =                                                             \
  output/$(vintage)/budget_2_subsample/recip-10/ingresos.csv                     \
  output/$(vintage)/budget_2_subsample/recip-10/gastos.csv                       \
  output/$(vintage)/budget_2_subsample/recip-100/ingresos.csv                    \
  output/$(vintage)/budget_2_subsample/recip-100/gastos.csv                      \
  output/$(vintage)/budget_2_subsample/recip-1000/ingresos.csv                   \
  output/$(vintage)/budget_2_subsample/recip-1000/gastos.csv

budget_3_dept_muni_year_item =                                                   \
  output/$(vintage)/budget_3_dept_muni_year_item/recip-$(subsample)/ingresos.csv \
  output/$(vintage)/budget_3_dept_muni_year_item/recip-$(subsample)/gastos.csv

#sanity_child_sum_is_parent =                                                                 \
#  output/$(vintage)/sanity_child_sum_is_parent/recip-$(subsample)/funcionamiento.csv         \
#  output/$(vintage)/sanity_child_sum_is_parent/recip-$(subsample)/ingresos.csv               \
#  output/$(vintage)/sanity_child_sum_is_parent/recip-$(subsample)/inversion.csv	      \
#  output/$(vintage)/sanity_child_sum_is_parent_summary/recip-$(subsample)/funcionamiento.csv \
#  output/$(vintage)/sanity_child_sum_is_parent_summary/recip-$(subsample)/ingresos.csv       \
#  output/$(vintage)/sanity_child_sum_is_parent_summary/recip-$(subsample)/inversion.csv

explore_order_of_mag_x_yrs =                                              \
  output/$(vintage)/explore/order_of_mag_x_yrs/recip-$(subsample)/report.csv

budget_4_scaled =                                                         \
  output/$(vintage)/budget_4_scaled/recip-$(subsample)/ingresos.csv       \
  output/$(vintage)/budget_4_scaled/recip-$(subsample)/gastos.csv

budget_5_add_regalias =                                                   \
  output/$(vintage)/budget_5_add_regalias/recip-$(subsample)/ingresos.csv \
  output/$(vintage)/budget_5_add_regalias/recip-$(subsample)/gastos.csv

budget_6_deflate =                                                                 \
  output/$(vintage)/budget_6_deflate/recip-$(subsample)/ingresos.csv               \
  output/$(vintage)/budget_6_deflate/recip-$(subsample)/gastos.csv

budget_6p5_cull_and_percentify =                                                   \
  output/$(vintage)/budget_6p5_cull_and_percentify/recip-$(subsample)/ingresos.csv \
  output/$(vintage)/budget_6p5_cull_and_percentify/recip-$(subsample)/gastos.csv

budget_6p7_avg_muni =                                                              \
  output/$(vintage)/budget_6p7_avg_muni/recip-$(subsample)/ingresos.csv            \
  output/$(vintage)/budget_6p7_avg_muni/recip-$(subsample)/gastos.csv

budget_7_verbose =                                                                 \
  output/$(vintage)/budget_7_verbose/recip-$(subsample)/ingresos.csv               \
  output/$(vintage)/budget_7_verbose/recip-$(subsample)/gastos.csv

# Listing one place (Honda, in Tolima)
# is sufficient to trigger the recipe.
# Listing every place would be tedious.
budget_8_pivots =                                                 \
  output/$(vintage)/pivots/recip-$(subsample)/timestamp-for-pivot-tables

budget_9_static_compare =                                         \
  output/$(vintage)/pivots/recip-$(subsample)/timestamp-for-static-compare

sample_tables =                                                   \
  output/$(vintage)/sample_tables/recip-$(subsample)/ingresos.csv \
  output/$(vintage)/sample_tables/recip-$(subsample)/gastos.csv

reports = output/$(vintage)/reports/recip-$(subsample)/timestamp-for-reports
facebook_ads = output/$(vintage)/facebook_ads/recip-$(subsample)/timestamp-for-facebook-ads
radio = output/$(vintage)/radio/recip-$(subsample)/timestamp-for-radio


#### #### #### ####
#### #### #### #### Recipes
#### #### #### ####

show_params:
	echo "vintage: "   -$(vintage)-
	echo "subsample: " -$(subsample)-

keys: $(keys)
$(keys):                                           \
  Code/build/make_keys.py                          \
  Code/metadata/raw_series.py
	date
	$(myPython) Code/build/make_keys.py $(myArgs)
	date

budget_0_collect: $(budget_0_collect)
$(budget_0_collect):                               \
  Code/build/budget_0_collect.py                   \
  Code/metadata/raw_series.py
	date
	$(myPython) Code/build/budget_0_collect.py $(myArgs)
	date

# PITFALL: Don't include Code/metadata/terms.py;
# it's safe to omit and causes unnecessary re-running,
# not affordable at these early slow stages.
budget_1: $(budget_1)
$(budget_1):			\
  $(budget_0_collect)		\
  Code/build/budget_1.py	\
  Code/build/budget_1_tests.py	\
  Code/util/misc.py		\
  Code/metadata/raw_series.py
	date
	$(myPython) Code/build/budget_1.py $(myArgs)
	date

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
	date
	$(myPython) Code/build/budget_1p5.py $(myArgs)
	date

# PITFALL: Don't include Code/metadata/terms.py;
# it's safe to omit and causes unnecessary re-running,
# not affordable at these early slow stages.
budget_2_subsample: $(budget_2_subsample)
$(budget_2_subsample):				\
  $(budget_1p5)					\
  Code/build/budget_2_subsample.py		\
  Code/build/budget_2_subsample_defs.py		\
  Code/build/budget_1_tests.py			\
  Code/util/misc.py				\
  Code/metadata/raw_series.py
	date
	$(myPython) Code/build/budget_2_subsample.py $(myArgs)
	date

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
	date
	$(myPython) Code/build/budget_3_dept_muni_year_item.py $(myArgs)
	date

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
#	$(myPython) Code/build/sanity_child_sum_is_parent.py $(myArgs)

explore_order_of_mag_x_yrs: $(explore_order_of_mag_x_yrs)
$(explore_order_of_mag_x_yrs):	     \
  $(budget_3_dept_muni_year_item)    \
  Code/explore/order_of_mag_x_yrs.py \
  Code/common.py		     \
  Code/util/misc.py		     \
  Code/metadata/terms.py             \
  Code/metadata/raw_series.py
	date
	$(myPython) Code/explore/order_of_mag_x_yrs.py $(myArgs)
	date

budget_4_scaled: $(budget_4_scaled)
$(budget_4_scaled):			  \
  $(budget_3_dept_muni_year_item)	  \
  Code/build/budget_4_scaled.py		  \
  Code/explore/order_of_mag_x_yrs_defs.py \
  Code/common.py			  \
  Code/util/misc.py			  \
  Code/metadata/terms.py                  \
  Code/metadata/raw_series.py
	date
	$(myPython) Code/build/budget_4_scaled.py $(myArgs)
	date

budget_5_add_regalias: $(budget_5_add_regalias)
$(budget_5_add_regalias):             \
  $(budget_4_scaled)                  \
  $(regalias)                         \
  Code/build/budget_5_add_regalias.py \
  Code/common.py                      \
  Code/metadata/terms.py              \
  Code/metadata/two_series.py
	date
	$(myPython) Code/build/budget_5_add_regalias.py $(myArgs)
	date

budget_6_deflate: $(budget_6_deflate)
$(budget_6_deflate):             \
  $(budget_5_add_regalias)       \
  $(inflation)                   \
  Code/build/budget_6_deflate.py \
  Code/common.py                 \
  Code/metadata/terms.py         \
  Code/metadata/two_series.py
	date
	$(myPython) Code/build/budget_6_deflate.py $(myArgs)
	date

budget_6p5_cull_and_percentify: $(budget_6p5_cull_and_percentify)
$(budget_6p5_cull_and_percentify):    \
  $(budget_6_deflate)		      \
  Code/build/budget_6p5_percentify.py \
  Code/util/percentify.py	      \
  Code/common.py		      \
  Code/metadata/two_series.py	      \
  Code/metadata/four_series.py
	date
	$(myPython) Code/build/budget_6p5_percentify.py $(myArgs)
	date

budget_6p7_avg_muni: $(budget_6p7_avg_muni)
$(budget_6p7_avg_muni):		    \
  $(budget_6p5_cull_and_percentify) \
  Code/build/budget_6p7_avg_muni.py \
  Code/common.py		    \
  Code/util/misc.py		    \
  Code/build/use_keys.py	    \
  Code/metadata/four_series.py
	date
	$(myPython) Code/build/budget_6p7_avg_muni.py $(myArgs)
	date

budget_7_verbose: $(budget_7_verbose)
$(budget_7_verbose):		 \
  $(budget_6p7_avg_muni)	 \
  Code/build/budget_7_verbose.py \
  Code/build/use_keys.py	 \
  Code/common.py		 \
  Code/util/misc.py		 \
  Code/metadata/terms.py         \
  Code/metadata/two_series.py
	date
	$(myPython) Code/build/budget_7_verbose.py $(myArgs)
	date

budget_8_pivots: $(budget_8_pivots)
$(budget_8_pivots):				\
  $(budget_7_verbose)				\
  Code/build/budget_8_pivots.py			\
  Code/common.py				\
  Code/util/aggregate_all_but_biggest/better.py	\
  Code/metadata/two_series.py
	date
	$(myPython) Code/build/budget_8_pivots.py $(myArgs)
	date

budget_9_static_compare: $(budget_9_static_compare)
$(budget_9_static_compare):		\
  $(budget_7_verbose)			\
  $(budget_8_pivots)			\
  Code/build/budget_9_static_compare.py	\
  Code/common.py			\
  Code/metadata/four_series.py
	date
	$(myPython) Code/build/budget_9_static_compare.py $(myArgs)
	date

# Unneeded, except to understand more complex programs.
sample_tables: $(sample_tables)
$(sample_tables):			       \
  $(budget_7_verbose)			       \
  Code/common.py			       \
  Code/draw/demo/sample_tables.py	       \
  Code/util/aggregate_all_but_biggest/gappy.py \
  Code/metadata/terms.py		       \
  Code/metadata/two_series.py
	date
	$(myPython) Code/draw/demo/sample_tables.py $(myArgs)
	date

inflation: $(inflation)
$(inflation):                   \
  data/$(vintage)/inflation.csv \
  Code/build/inflation.py
	date
	$(myPython) Code/build/inflation.py $(myArgs)
	date

regalias: $(regalias)
$(regalias):                        \
  data/$(vintage)/regalias/dept.csv \
  data/$(vintage)/regalias/muni.csv \
  Code/build/regalias.py            \
  Code/build/use_keys.py            \
  Code/util/misc.py
	date
	$(myPython) Code/build/regalias.py $(myArgs)
	date

reports: $(reports)
$(reports):			 \
  $(budget_8_pivots)		 \
  $(budget_9_static_compare)	 \
  Code/build/use_keys.py	 \
  Code/draw/chart/time_series.py \
  Code/draw/chart/pairs.py	 \
  Code/draw/text/newlines.py	 \
  Code/draw/pages.py		 \
  Code/draw/design.py		 \
  Code/draw/chart_content.py	 \
  Code/main/reports.py
	date
	$(myPython) Code/main/reports.py $(myArgs)
	date

facebook_ads: $(facebook_ads)
$(facebook_ads):		 \
  $(budget_8_pivots)		 \
  $(budget_9_static_compare)	 \
  Code/build/use_keys.py	 \
  Code/draw/chart/time_series.py \
  Code/draw/chart/pairs.py	 \
  Code/draw/text/newlines.py	 \
  Code/draw/pages.py		 \
  Code/draw/design.py		 \
  Code/draw/chart_content.py	 \
  Code/main/facebook_ads.py
	date
	$(myPython) Code/main/facebook_ads.py $(myArgs)
	date

radio: $(radio)
$(radio):		     \
  $(budget_8_pivots)	     \
  $(budget_9_static_compare) \
  Code/main/radio_scripts.py \
  Code/main/geo.py
	date
	$(myPython) Code/main/radio_scripts.py $(myArgs)
	date
