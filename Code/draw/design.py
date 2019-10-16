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
sizeText_title = 60 * scale_font
sizeText_tickLabel = 10 * scale_font
sizeText_legend = 8 * scale_font
sizeText_chartPage = 16 * scale_font
sizeText_chartBody = 12 * scale_font
sizeText_zenPageTitle = 18 * scale_font
sizeText_zenPageBody = 15 * scale_font
sizeText_lastPageAbove = 8 * scale_font
sizeText_lastPageBelow = 6 * scale_font
sizeText_inBars = 6 * scale_font
sizeText_aboveBars = 8 * scale_font
sizeLineWidth = 0.5 * scale_font
sizeBarWidth = 0.3

# colors
background_color = "mediumaquamarine"
dark_blue = "#2f399b"
light_blue = "#8bc2c3"
teal = "#4196a2"
orange = "#d8841c"

def against(color): # for draw/design.py
  if color == dark_blue: return "white"
  if color == "white": return "black"
  raise ValueError( "Color to show against " + color + " is undefined." )


# fonts
font_thick = fm.FontProperties(
  fname = "design/Montserrat_Black.ttf" )
font_thin = fm.FontProperties(
  fname = "design/Montserrat_Medium.ttf" )

