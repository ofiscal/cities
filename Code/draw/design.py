import matplotlib.font_manager as fm

scale_font = 4
  # PITFALL: This is surprisingly important.
  # In order to import .png files (the logo) well,
  # we need to change the default figure size.
  #   The line that changes it looks like this:
  #     plt.rcParams.update({'figure.figsize': (38,24)})
  # If we change that again, it will distort all the fonts.
  # By always scaling fonts by the following parameter,
  # we won't have to adjust every font separately
  # after each change to the default figure size.
titleFontSize = 60 * scale_font
tickLabelSize = 7 * scale_font
legendFontSize = 7 * scale_font
chartPageTitleFontSize = 14 * scale_font
chartPageBodyTextSize = 8 * scale_font
zenPageTitleFontSize = 14 * scale_font
zenPageBodyFontSize = 10 * scale_font
lineWidth = 0.5 * scale_font
fontSizeInBars = 6 * scale_font
fontSizeAboveBars = 8 * scale_font

# colors
background_color = "mediumaquamarine"
dark_blue = "#2f399b"
orange = "#d8841c"

# fonts
font_thick = fm.FontProperties(
  fname = "design/Montserrat_Black.ttf" )
font_thin = fm.FontProperties(
  fname = "design/Montserrat_Light.ttf" )

