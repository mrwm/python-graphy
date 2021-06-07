#!/usr/bin/env python3

# line_graph.py
# Author: William Chung
# Last Updated: 
# Purpose: Creates line or bar graph(s) with the given data points
# Program Uses: ./line_graph.py
# Notes: 
#       - Requires svgwrite python module
#       - The resulting graph located a bit off the viewbox, so scroll up a bit
#
import svgwrite

# Size of the x increment. If no unit is givem (eg in, cm, mm, pt, px), then the
# default unit will be used: px
rect_width = 80   # This is basically the size of x

# How far apart each graph will be vertically
v_offset = 0

st_width = "1pt"  # Stroke width
dot_radius = "2.5pt"

# Each list needs to be named as "height_list_<number>"
# and <number> needs to start at 0
#
# Unused entrys needs to be deleted or else it will also be drawn
# Don't forget to delete the last comma as well!
height_dictionary = {
  "height_list_0" : [ 43, 71, 79, 79, 79],
  "height_list_1" : [ 60, 80, 100, 100, 100],
  "height_list_2" : [ 52, 78, 84, 84, 86],
  "height_list_3" : [ 50, 72, 78, 81, 82],
  "height_list_4" : [ 100, 100, 100, 100, 100],
  "height_list_5" : [ 43, 78, 82, 84, 84],
  "height_list_6" : [ 83, 93, 95, 95, 95]
}

color_dictionary = {
  # We can use words, rgb values, hex codes, etc for color
  # dont forget about the comma at the end (except for the last one)
  #
  # Also, no need to delete unused colors, since it will just be skipped
  "color_0" : "#811412",
  "color_1" : "yellow",
  "color_2" : "cyan",
  "color_3" : "green",
  "color_4" : "#ccc",
  "color_5" : "#048080",
  "color_6" : "orange"
}

# don't forget about the filename below!
dwg = svgwrite.Drawing('6.3-c.svg', profile='full')

# Do you want to show the rectangle?
show_rect = False

# Do you want to show the line graphs?
show_line = True

################################################################################
v_offset_origin = v_offset

if show_rect:
  # For making the bar graphs
  for group_index in range(0, len(height_dictionary)):
    x_index = 0
    for list_index in range(0, len(height_dictionary["height_list_"+str(group_index)])):
      # draw the boxes
      r_size = height_dictionary["height_list_"+str(group_index)][list_index]
      dwg.add(dwg.rect((x_index, -r_size + v_offset), (rect_width, r_size),
        fill=color_dictionary["color_"+str(group_index)])
      )
      x_index += rect_width
    v_offset += v_offset

if show_line:
  # For connecting the dots together
  v_offset = v_offset_origin
  for group_index in range(0, len(height_dictionary)):
    line_points = "M"
    x_index = 0
    l_max = len(height_dictionary["height_list_"+str(group_index)])
    for list_index in range(0, l_max):
      # draw the boxes
      r_size = height_dictionary["height_list_"+str(group_index)][list_index]
      if list_index < l_max-1:
        line_points = line_points + str(x_index) + "," + str(-r_size + v_offset) + ", "
      else:
        line_points = line_points + str(x_index) + "," + str(-r_size + v_offset)
      x_index += rect_width

    # draw a cubic-bezier-curve path
    dwg.add(dwg.path( d=line_points,
      stroke=color_dictionary["color_"+str(group_index)],
      fill="none",
      stroke_width=st_width)
    )
    v_offset += v_offset

  # For making the dots at the corner of each rectangle
  v_offset = v_offset_origin
  for group_index in range(0, len(height_dictionary)):
    x_index = 0
    for list_index in range(0, len(height_dictionary["height_list_"+str(group_index)])):
      # draw the boxes
      r_size = height_dictionary["height_list_"+str(group_index)][list_index]
      dwg.add(dwg.circle(center=(x_index, -r_size + v_offset),
        r=dot_radius,
        fill=color_dictionary["color_"+str(group_index)])
      )
      x_index += rect_width
    v_offset += v_offset

# output our svg image as raw xml
#print(dwg.tostring())

# write svg file to disk
dwg.save()
