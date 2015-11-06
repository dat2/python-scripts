"""

This is a simple script to generate a colors.html file in your directory. 
You can take any palette from https://jiffyclub.github.io/palettable/ and
get any number of (interpolated) colours.

"""
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def padded_hex(num, n=2):
  """
  Convert a number to a #xx hex string (zero padded to n digits)
  """
  return ("%x" % num).zfill(n)

def rgb_to_hex(col):
  """
  Convert a color list to a hex color string
  eg. [r,g,b] => #xxxxxx
  """
  return "#" + "".join(map(padded_hex, col))

def generate_colors(desired_palette, num_desired_colors):
  """
  Generate an array of color strings, interpolated from the desired_palette.
  desired_palette is from palettable

  Conceptually, this takes a list of colors, and lets you generate any length
  of colors from that array.
  """
  cmap = desired_palette.mpl_colormap
  mappable = ScalarMappable(norm=Normalize(vmin=0, vmax=1), cmap=cmap)

  cols = []
  for i in range(1,num_desired_colors+1):
    (r,g,b,a) = mappable.to_rgba((i - 1) / num_desired_colors)
    cols.append(rgb_to_hex(map(lambda x: int(x*255), [r,g,b])))

  return cols

# HTML stuff

def generate_class(ic):
  """
  Generate a .style-<i> class from the input tuple.

  eg.
  >>> generate_class((0,"#fcae42"))
  ".style-0 { background-color: #fcae42; }"
  """
  (i,c) = ic
  return ".style-" + str(i) + " { background-color: " + c + "; }"

def generate_div(i):
  """
  Generate a div with the style-<i> class.

  eg.
  >>> generate_div(0)
  "<div class="box style-0"></div>
  """
  return '<div class="box style-' + str(i) + '"></div>'

def generate_box_style():
  """
  Generate the style for each box to show.
  """
  return ".box { display: inline-block; width: 150px; height: 150px;}"

def generate_html(desired_palette, desired_colors):
  """
  Write a simple html string to 'colors.html' preformatted.
  """
  colors = generate_colors(desired_palette, desired_colors)

  classes = map(generate_class, enumerate(colors))
  divs = map(generate_div, range(0,desired_colors))

  html = '<!DOCTYPE html>\n<html lang="en">\n  <head>\n  <meta charset="UTF-8">\n  <title>Generated Colors</title>'
  html += "\n  <style>\n    " + generate_box_style() + "\n    ".join(classes) + "\n  </style>"
  html += "\n  </head>\n  <body>"
  html += "\n    <div>\n      " + "\n      ".join(divs) + "\n    </div>"
  html += "\n  </body>\n</html>"

  with open('colors.html', 'w') as f:
    print(html, file=f)


if __name__ == "__main__":
  # the desired palette, and colours from the palette
  from palettable.colorbrewer.diverging import Spectral_11
  desired_palette = Spectral_11
  desired_colors = 20

  generate_html(desired_palette, desired_colors)
